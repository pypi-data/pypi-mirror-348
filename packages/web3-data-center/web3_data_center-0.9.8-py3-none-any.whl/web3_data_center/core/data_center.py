from ..clients import BlockOpenSearchClient, FundingClient, Web3LabelClient, PGClient, Web3Client, XMonitorClient, EtherscanClient
from ..utils.cache import file_cache
from typing import List, Dict, Union, Tuple, Any, Optional, defaultdict

from web3 import Web3
from chain_index import get_chain_info, get_all_chain_tokens, protocols
import random
import logging
import time
import asyncio

from chain_index import constants

logger = logging.getLogger(__name__)

class AsyncClientProxy:
    def __init__(self, initialize_func):
        self._initialize_func = initialize_func
        self._client = None

    async def _get_client(self):
        """Initialize and return the actual client"""
        if self._client is None:
            self._client = await self._initialize_func()
        return self._client

    def __getattr__(self, name):
        """Returns a proxy for the method or property that will be accessed"""
        async def proxy_method(*args, **kwargs):
            client = await self._get_client()
            attr = getattr(client, name)
            if callable(attr):
                return await attr(*args, **kwargs)
            if args or kwargs:
                raise TypeError(f"'{name}' is not callable")
            return attr
        return proxy_method


class DataCenter:
    """Central data management and processing hub"""

    def __init__(self, config_path: str = "config.yml"):
        """Initialize DataCenter

        Args:
            config_path: Path to config file
        """
        self.config_path = config_path
        self._initialized = False
        self._clients = {}
        self.cache = {}
        
    async def __aenter__(self):
        """Async context manager entry"""
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    def __getattr__(self, name):
        """Lazily initialize and return client instances
        
        This method returns a proxy that handles both direct client access and method calls, e.g.:
        client = await dc.label_client
        or
        result = await dc.label_client.some_method()
        """
        if name not in self._clients:
            if name == 'label_client':
                self._clients[name] = AsyncClientProxy(self._initialize_label_client)
            elif name == 'pg_client':
                self._clients[name] = AsyncClientProxy(self._initialize_pg_client)
            elif name == 'web3_client':
                self._clients[name] = AsyncClientProxy(self._initialize_web3_client)
            elif name == 'blockos_client':
                self._clients[name] = AsyncClientProxy(self._initialize_blockos_client)
            elif name == 'x_monitor_client':
                self._clients[name] = AsyncClientProxy(self._initialize_x_monitor_client)
            elif name == 'etherscan_client':
                self._clients[name] = AsyncClientProxy(self._initialize_etherscan_client)
            elif name == 'funding_client':
                self._clients[name] = AsyncClientProxy(self._initialize_funding_client)
            else:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        
        return self._clients[name]

    async def _initialize_label_client(self):
        """Initialize Web3LabelClient asynchronously"""
        client = Web3LabelClient(config_path=self.config_path)
        await client.setup()
        return client

    async def _initialize_pg_client(self):
        """Initialize PGClient asynchronously"""
        client = PGClient(config_path=self.config_path, db_name="local")
        await client.setup()
        return client

    async def _initialize_web3_client(self):
        """Initialize Web3Client asynchronously"""
        client = Web3Client(config_path=self.config_path)
        await client.setup()
        return client

    async def _initialize_blockos_client(self):
        """Initialize BlockOpenSearchClient asynchronously"""
        client = BlockOpenSearchClient(config_path=self.config_path)
        await client.setup()
        return client

    async def _initialize_funding_client(self):
        """Initialize FundingClient asynchronously"""
        client = FundingClient(config_path=self.config_path)
        await client.setup()
        return client

    async def _initialize_x_monitor_client(self):
        """Initialize XMonitorClient asynchronously"""
        client = XMonitorClient(config_path=self.config_path)
        await client.setup()
        return client

    async def _initialize_etherscan_client(self):
        """Initialize EtherscanClient asynchronously"""
        client = EtherscanClient(config_path=self.config_path)
        await client.setup()
        return client

    async def is_contract_batch(self, addresses: List[str], chain: str = 'eth') -> List[Optional[bool]]:
        """Check if multiple addresses are contracts in parallel.
        
        Args:
            addresses: List of addresses to check
            chain: Chain identifier (default: 'eth')
            
        Returns:
            List of booleans (True for contract, False for non-contract, None for errors)
            in same order as input addresses
        """
        from web3 import Web3
        try:
            # Create coroutines for each address
            web3_client = await self.web3_client._get_client()
            tasks = []
            for address in addresses:
                try:
                    if address == '':
                        tasks.append(asyncio.sleep(0))  # Dummy task for empty address
                        continue
                    checksum_address = Web3.to_checksum_address(address)
                    task = web3_client.eth.get_code(checksum_address)
                    tasks.append(task)
                except Exception as e:
                    logger.error(f"Invalid address {address}: {str(e)}")
                    tasks.append(None)
            
            # Filter out None tasks and keep track of indices
            valid_tasks = []
            task_indices = []
            for i, task in enumerate(tasks):
                if task is not None:
                    valid_tasks.append(task)
                    task_indices.append(i)
            
            # Execute valid tasks
            if valid_tasks:
                results = await asyncio.gather(*valid_tasks, return_exceptions=True)
            else:
                results = []
            
            # Prepare final results list
            final_results = [None] * len(addresses)
            
            # Fill in results for valid tasks
            for idx, result in zip(task_indices, results):
                if isinstance(result, Exception):
                    logger.error(f"Error checking contract for {addresses[idx]}: {str(result)}")
                else:
                    final_results[idx] = result != b''
            
            return final_results
            
        except Exception as e:
            logger.error(f"Error in batch contract check: {str(e)}")
            return [None] * len(addresses)

    async def sample_transactions(
        self,
        single_block: Optional[Union[int, str]] = None,
        block_range: Optional[Tuple[int, int]] = None,
        sample_size: int = 100,
        to_addr_range: Optional[Tuple[str, str]] = None,
        value_range: Optional[Tuple[int, int]] = None,
        gas_range: Optional[Tuple[int, int]] = None,
        four_bytes_list: Optional[List[str]] = None,
        random_seed: Optional[int] = None,
        full_transactions: int = 0
    ) -> Union[List[str], List[Dict]]:
        """Sample transactions from specified blocks.
        
        Args:
            single_block: Single block to sample from
            block_range: Range of blocks to sample from (inclusive)
            sample_size: Number of transactions to sample
            to_address_range: Range of 'to' addresses to filter
            value_range: Range of transaction values to filter
            gas_range: Range of gas used to filter
            four_bytes_list: List of 4-byte function signatures to filter
            random_seed: Random seed for reproducibility
            full_transactions: Level of transaction detail to return:
                0: Only transaction hashes
                1: Transaction data without logs
                2: Full transaction data with logs
            
        Returns:
            List of transaction hashes if full_transactions=0,
            otherwise list of transaction dictionaries
        """
        if random_seed is not None:
            random.seed(random_seed)
            
        filtered_txs = []
        
        # If single block specified, use that
        if single_block is not None:
            filtered_txs.extend(
                await self._fetch_and_filter_block(
                    block_identifier=single_block,
                    to_addr_range=to_addr_range,
                    value_range=value_range,
                    gas_range=gas_range,
                    four_bytes_list=four_bytes_list,
                    full_transactions=full_transactions
                )
            )
            
        # Otherwise use block range
        elif block_range is not None:
            start_block, end_block = block_range
            
            # Calculate how many blocks we need to sample to get enough transactions
            # Assuming average of 200 transactions per block
            avg_txs_per_block = 200
            num_blocks_needed = max(1, sample_size // avg_txs_per_block * 2)  # Double for safety
            
            # Sample blocks within range
            block_numbers = range(start_block, end_block + 1)
            sampled_blocks = random.sample(block_numbers, min(num_blocks_needed, len(block_numbers)))
            
            # Fetch transactions from sampled blocks
            for blk_num in sampled_blocks:
                filtered_txs.extend(
                    await self._fetch_and_filter_block(
                        block_identifier=blk_num,
                        to_addr_range=to_addr_range,
                        value_range=value_range,
                        gas_range=gas_range,
                        four_bytes_list=four_bytes_list,
                        full_transactions=full_transactions
                    )
                )
                
                # If we have enough transactions, stop sampling blocks
                if len(filtered_txs) >= sample_size:
                    break
            
            # If we still don't have enough transactions, sample more blocks
            while len(filtered_txs) < sample_size:
                # Sample a new block
                remaining_blocks = set(block_numbers) - set(sampled_blocks)
                if not remaining_blocks:
                    break
                    
                new_block = random.choice(list(remaining_blocks))
                sampled_blocks.append(new_block)
                
                filtered_txs.extend(
                    await self._fetch_and_filter_block(
                        block_identifier=new_block,
                        to_addr_range=to_addr_range,
                        value_range=value_range,
                        gas_range=gas_range,
                        four_bytes_list=four_bytes_list,
                        full_transactions=full_transactions
                    )
                )
        
        # If we have more transactions than needed, randomly sample
        if len(filtered_txs) > sample_size:
            filtered_txs = random.sample(filtered_txs, sample_size)
        # If we have fewer transactions than needed, raise an error
        elif len(filtered_txs) < sample_size:
            raise ValueError(f"Could not find {sample_size} transactions matching criteria. Only found {len(filtered_txs)}")
            
        return filtered_txs

    async def _fetch_and_filter_block(
        self,
        block_identifier: Union[int, str],
        to_addr_range: Optional[Tuple[str, str]],
        value_range: Optional[Tuple[int, int]],
        gas_range: Optional[Tuple[int, int]],
        four_bytes_list: Optional[List[str]],
        full_transactions: int = 0
    ) -> Union[List[str], List[Dict]]:
        """
        Fetch and filter transactions from a block based on criteria.
        Returns either transaction hashes or transaction objects based on full_transactions parameter.

        Args:
            block_identifier: Block number or hash
            to_addr_range: Range of 'to' addresses to filter
            value_range: Range of transaction values to filter
            gas_range: Range of gas used to filter
            four_bytes_list: List of 4-byte function signatures to filter
            full_transactions: Level of transaction detail to return:
                0: Only transaction hashes
                1: Transaction data without logs
                2: Full transaction data with logs

        Returns:
            List of transaction hashes if full_transactions=0,
            otherwise list of transaction dictionaries
        """
        web3_client = await self.web3_client._get_client()
        block = await web3_client.eth.get_block(block_identifier, full_transactions=True)
        transactions = block.transactions

        result = []
        for tx in transactions:
            if self._match_filters(
                tx,
                to_addr_range=to_addr_range,
                value_range=value_range,
                gas_range=gas_range,
                four_bytes_list=four_bytes_list
            ):
                if full_transactions == 0:
                    # Return only transaction hash
                    result.append("0x"+tx.hash.hex())
                elif full_transactions == 1:
                    # Return transaction data without logs
                    tx_dict = dict(tx)
                    result.append(tx_dict)
                else:  # full_transactions == 2
                    # Return full transaction data with logs
                    tx_dict = dict(tx)
                    try:
                        tx_receipt = self.w3_client.get_transaction_receipt(tx.hash)
                        tx_dict['receipt'] = dict(tx_receipt)
                    except Exception as e:
                        logger.warning(f"Failed to get receipt for tx {tx.hash.hex()}: {str(e)}")
                    result.append(tx_dict)

        return result

    def _match_filters(
        self,
        tx: Dict,
        to_addr_range: Optional[Tuple[str, str]],
        value_range: Optional[Tuple[int, int]],
        gas_range: Optional[Tuple[int, int]],
        four_bytes_list: Optional[List[str]],
    ) -> bool:
        if to_addr_range and tx["to"] is not None:
            start_to, end_to = to_addr_range
            to_lower = tx["to"].lower()
            if not (start_to.lower() <= to_lower <= end_to.lower()):
                return False

        if value_range:
            min_val, max_val = value_range
            if not (min_val <= tx["value"] <= max_val):
                return False

        if gas_range:
            min_gas, max_gas = gas_range
            if not (min_gas <= tx["gas"] <= max_gas):
                return False

        if four_bytes_list:
            tx_input = tx.get("input", "0x")
            if len(tx_input) < 10:
                return False


            method_id = tx_input[0:10].lower()
            if method_id not in [m.lower() for m in four_bytes_list]:
                return False

        return True

    async def sample_addresses(
        self,
        sample_size: int = 100,
        only_contracts: int = 0,
        single_block: Optional[Union[int, str]] = None,
        block_range: Optional[Tuple[int, int]] = None,
        random_seed: Optional[int] = None,
        address_type: str = 'both',  # 'from', 'to', or 'both'
        max_attempts: int = 3  # Maximum number of sampling attempts
    ) -> List[str]:
        """Sample addresses from transactions, optionally filtering for contracts.
        
        Args:
            sample_size: Number of addresses to sample
            only_contracts: If True, only return contract addresses
            single_block: Single block to sample from
            block_range: Range of blocks to sample from (inclusive)
            random_seed: Random seed for reproducibility
            address_type: Type of addresses to sample ('from', 'to', or 'both')
            max_attempts: Maximum number of attempts to find enough addresses
            
        Returns:
            List of sampled addresses
        """
        if random_seed is not None:
            random.seed(random_seed)
        
        all_addresses = set()
        attempt = 0
        multiplier = 2  # Initial sampling multiplier
        
        while attempt < max_attempts:
            # Sample transactions with increasing multiplier
            current_sample_size = sample_size * multiplier * (attempt + 1)
            transactions = await self.sample_transactions(
                single_block=single_block,
                block_range=block_range,
                sample_size=current_sample_size,
                random_seed=random_seed,
                full_transactions=1
            )
            
            # Extract addresses based on type
            for tx in transactions:
                if address_type in ('from', 'both') and tx.get('from'):
                    all_addresses.add(tx['from'])
                if address_type in ('to', 'both') and tx.get('to'):
                    all_addresses.add(tx['to'])
            
            addresses = list(all_addresses)
            
            # If we need contracts, filter them, only_contract=-1 means no contract, 0 means mix, 1 means only contract
            if only_contracts != 0:
                is_contract_results = await self.is_contract_batch(addresses)
                # Filter out None values and treat them as non-contracts
                contract_addresses = [
                    addr for addr, is_contract in zip(addresses, is_contract_results)
                    if is_contract
                ]
                
                if only_contracts == 1:
                    addresses = contract_addresses
                else:
                    addresses = [addr for addr in addresses if addr not in contract_addresses]
            
            # If we have enough addresses, break
            if len(addresses) >= sample_size:
                break
                
            attempt += 1
            
        # If we still don't have enough addresses after all attempts, raise error
        if len(addresses) < sample_size:
            raise ValueError(
                f"Could not find {sample_size} {'contract ' if only_contracts else ''}"
                f"addresses after {max_attempts} attempts. Only found {len(addresses)}"
            )
        
        # Randomly sample the required number of addresses
        sampled_addresses = random.sample(addresses, sample_size)
        return sampled_addresses

    @file_cache(namespace="all_txs", ttl=3600*24)  # Cache for 24 hours
    async def fetch_all_txs_from(self, address: str) -> List[Dict[str, Any]]:
        """Fetch all transactions from a single address.
        
        Args:
            address: The address to fetch transactions from
            
        Returns:
            List of dictionaries representing the transactions
        """
        try:
            tx_hashes = await self.blockos_client.fetch_all_txhashes_from(address)
            return await self.blockos_client.search_transaction_batch(tx_hashes)
        except Exception as e:
            logger.error(f"Error fetching transactions for {address}: {e}")
            return []  # Return empty list instead of empty dict to maintain type consistency


    async def tx_entropy_of(self, address: str, tx_details: Dict[str, Any] = None) -> float:
        """Calculate the entropy of transactions based on multiple dimensions.
        
        Dimensions considered:
        - To address type (token/pair/normal contract/none)
        - Method ID
        - Gas price
        - Gas used
        - Value
        
        Returns:
            float: Entropy value representing transaction pattern complexity
        """
        import math
        
        if tx_details is None:
            tx_details = await self.fetch_all_txs_from(address)
        
        if not tx_details:
            return 0.0

        # Prepare address categorization
        counterparties = [tx['ToAddress'] for tx in tx_details.values()]
        is_contract_results = await self.is_contract_batch(counterparties)
        contract_counterparties = [
            addr for addr, is_contract in zip(counterparties, is_contract_results)
            if is_contract
        ]
        is_token_results = await self.is_token_contract_batch(contract_counterparties)
        token_counterparties = [
            addr for addr, is_token in zip(contract_counterparties, is_token_results)
            if is_token
        ]
        is_pair_results = await self.is_pair_contract_batch(contract_counterparties)
        pair_counterparties = [
            addr for addr, is_pair in zip(contract_counterparties, is_pair_results)
            if is_pair
        ]

        # Create address type mapping
        addr_type_map = {}
        for addr in counterparties:
            if addr in pair_counterparties:
                addr_type_map[addr] = 'pair'
            elif addr in token_counterparties:
                addr_type_map[addr] = 'token'
            elif addr in contract_counterparties:
                addr_type_map[addr] = 'normal'
            else:
                addr_type_map[addr] = 'eoa'
        # Prepare transaction feature vectors
        tx_features = []
        for tx in tx_details.values():
            to_addr = tx['ToAddress']
            feature = (
                addr_type_map[to_addr],  # Address type
                tx.get('CallFunction', '0x'),  # Method ID
                # tx.get('GasPrice', 0),  # Gas price
                round(math.log10(tx.get('GasUsed', 0)),2),  # Gas used
                1 if int(tx.get('Value', 0)) / 1e18 > 0 else 0  # Whether there's value transfer
            )
            tx_features.append(feature)

        # Calculate frequency of each unique feature combination
        feature_counts = {}
        total_txs = len(tx_features)
        for feature in tx_features:
            feature_counts[feature] = feature_counts.get(feature, 0) + 1

        # Calculate entropy
        entropy = 0.0
        for count in feature_counts.values():
            probability = count / total_txs
            entropy -= probability * math.log2(probability)

        return entropy

    async def is_token_contract_batch(self, addresses: List[str], chain: str = 'Ethereum') -> List[bool]:
        if not addresses:
            return []
        # query = """
        # SELECT address::text, EXISTS (
        #     SELECT 1 FROM token_info 
        #     WHERE address = ANY($1::text[]) AND chain = $2
        # ) AS is_token
        # FROM unnest($1::text[]) AS address
        # """
        query = """
            SELECT 
            a.address,
            EXISTS (
                SELECT 1
                FROM token_info t
                WHERE t.address = a.address
                AND t.chain   = $2
            ) AS is_token
            FROM unnest($1::text[]) AS a(address);
        """
        results = await self.pg_client.execute(query, (addresses, chain))
        return [result['is_token'] for result in results]

    async def is_pair_contract_batch(self, addresses: List[str], chain_id: int = 1) -> List[bool]:
        if not addresses:
            return []
        query = """
        SELECT address::text, EXISTS (
            SELECT 1 FROM pair_info 
            WHERE pair = ANY($1::text[]) AND chain_id = $2
        ) AS is_pair
        FROM unnest($1::text[]) AS address
        """
        results = await self.pg_client.execute(query, (addresses, chain_id))
        return [result['is_pair'] for result in results]


    async def is_automated_address(self, address: str, chain_id: int = 1) -> bool:
        """Check if an address is automated based on transaction patterns"""
        try:
            address = address.lower()
            first_interactions = await self.blockos_client.first_sent_transaction_batch([address])
            interactions_counts = await self.blockos_client.search_sent_transaction_count_batch([address])

            # Get current block number using web3 client
            web3_client = await self.web3_client._get_client()
            current_block = await web3_client.eth.block_number

            # print(first_interactions)
            # print(interactions_counts)
            # Frequency
            if not first_interactions.get(address) or 'first_tx_block' not in first_interactions[address]:
                return False
            # print("current block is", current_block, type(current_block))
            # print("first tx block is", first_interactions[address]['first_tx_block'], type(first_interactions[address]['first_tx_block']))
            days = (current_block - first_interactions[address]['first_tx_block']) / 300
            years = days / 365
            if years <= 0:
                return False
            avg_txs_per_year = interactions_counts[address]['totalTxCount'] / years
            # If more than 3000 transactions per year on average, consider it automated
            if avg_txs_per_year > 3000:
                print(f"High Yearly frequency: Address {address} is automated with {avg_txs_per_year} / year")
                return True

            tx_details = await self.fetch_all_txs_from(address)
            # choose latest 1000 txs, it's a dict 
            tx_details = {k: v for k, v in sorted(tx_details.items(), key=lambda item: item[1]['Timestamp'], reverse=True)[:300000]}
            
            # Check for transactions in the same block
            # Group transactions by block number
            txs_by_block = {}
            for tx_hash, tx in tx_details.items():
                block_num = int(tx['Block'])
                if block_num not in txs_by_block:
                    txs_by_block[block_num] = []
                txs_by_block[block_num].append(tx)
            
            # Check blocks with multiple transactions
            for block_num, txs in txs_by_block.items():
                if len(txs) > 1 and block_num > 15537393:
                    # 收集所有非0x095ea7b3的unique method IDs
                    unique_method_ids = set()
                    
                    for tx in txs:
                        if 'CallFunction' in tx:
                            method_id = tx['CallFunction']
                            # 排除0x095ea7b3 (approve方法)
                            # if method_id != '0x095ea7b3' and method_id != '0xa22cb465' and method_id != '0x':
                            unique_method_ids.add(method_id)
                    
                    # 只要有2个或以上不同的非approve method IDs，就认为是automated
                    if len(unique_method_ids) >= 2:
                        print(f"Multi Txs: {address} sent {len(txs)} txs in the same block {block_num} with {len(unique_method_ids)} different non-approve MethodIds: {unique_method_ids}")
                        return True
                    else:
                        print(f"Multi Txs: {address} sent txs in the same block {block_num}, but has only {len(unique_method_ids)} unique non-approve MethodIds (ignored)")
            # Check for high daily transaction count
            daily_tx_counts = defaultdict(int)
            for tx in tx_details.values():
                date = tx['Timestamp'][:10]  # Extract date part
                daily_tx_counts[date] += 1

            max_daily_txs = max(daily_tx_counts.values(), default=0)
            if max_daily_txs > 280:
                print(f"High Daily frequency: Address {address} has {max_daily_txs} / day")
                return True

            # Check trading bot usage
            automated_addresses = {
                '0x80a64c6D7f12C47B7c66c5B4E20E72bc1FCd5d9e',  # Maestro
                '0x3328f7f4a1d1c57c35df56bbf0c9dcafca309c49',  # Banana Old
                '0xdB5889E35e379Ef0498aaE126fc2CCE1fbD23216',  # Banana
                '0x58dF81bAbDF15276E761808E872a3838CbeCbcf9',  # Banana
                '0x3A10dC1A145dA500d5Fba38b9EC49C8ff11a981F',  # Sigma
                '0xe76014c179f19da26bb30a0f085ff0a466b92829',  # Sigma
                '0xED12310d5a37326E6506209C4838146950166760',  # Pepe
                '0x055c48651015cf5b21599a4ded8c402fdc718058',  # Pepe
                '0x26eab037f50706200739e07454754adf69187cc0',  # Pepe
                '0x3999d2c5207c06bbc5cf8a6bea52966cabb76d41',  # Unibot
                '0x07490d45a33d842ebb7ea8c22cc9f19326443c75',  # Unibot
                '0x126c9fbab3a2fca24edfd17322e71a5e36e91865',  # Unibot
                '0xe23cca7144c99de7b3af2bc76337daf8e210e604',  # Unibot
                '0x23943b4a865f4f1f39d9a737becf861ba862b535',  # Unibot
                '0xB86E490E72F050c424383d514362Dc61DaBB1Cc3',  # Shuriken
                '0x2c57f6dfe219be08d92ea55f985311abaece89a5',  # Readyswap
                '0xcf8b0f9422084695ef702bfce33976982ff3304b',  # Readyswap
                '0xb13c95E00312e301085d29ebB84c21fCA663dAae',  # Readyswap
                '0x2f17d3ceb71ad380441a90f8cb1882d91819e0f1',  # Readyswap
                '0x0000130d512ca69ca38add5b9ab2f9deff95c882',  # Magnum
                '0x0e233cfde879814937385e8748a8e899926402e0',  # Magnum
                '0xd3d1a9b5fD80398971cdc4f9772d4F89d89Fb09D',  # Magnum
                '0xb561a8a3ab70ba48b10c83432b72c6376bb8209e',  # Magnum
                '0xF268035F5F7Fa5BD43Eb8b84723D880Ec2748D81',  # Looter
                '0x95dd05950bc8CD5dEF7be0aDC600D0fadd15Bd86',  # Mizar
                '0x64375B06f5C626a52d3EA5fe496812a08958FB68',  # Moonbot
                '0x952e24a9f49a15cac92cf1f6d01b9536959948f4',  # Moonbot
                '0x43579754589644805ef2bb4696bfe6a5cf7aa809',  # Moonbot
                '0xE7e68e99205a186DAAf16981e8a1f8c72134b0d1DE', #XCeption
                '0x5061eFE73177315237bE75F51ECd29a9cAe73a27',  # Bitfoot
                '0x6a153cDf5cC58F47c17D6A6b0187C25c86d1acFD',  # Prophet
                '0x6a153cDf5cC58F47c17D6A6b0187C25c86d1acFD',  # Scarab
                '0xcef88d734db8b016b7e877482f110f41d6917126',  # Scarab
                '0xf8c23f311df5C467d085ba520626bf12e814388D',  # Scarab
                '0xd319758ac8737e4aac1e42b074bdaab8c4ecf426',  # Scarab
                '0x3cd3bf2bb1ea71c78f84395ff71e6882df1345a3',  # Scarab
                '0xe8515095a0faf405b7f5319fa47eb1713eac0c46',  # Scarab
                '0xa7d4d89ddfc9b963a296d3dca97863cb265f71fa',  # Scarab
                '0x039991ea3b787ceefe53eae4c733b2a2f0d06b7a',  # Scarab
                '0x5AF30459089C3CF02b79e71ea5Af6cf59E3F8E87',  # baZOOka
                '0x0bFAd705e2b71c88f0eD1cd49B58a4C05b23568D',  # Unodex
                '0xa90cff625aa1270074a05a9727a81861e64f4533',  # Unodex
                '0x45648b8c538b5a96a7e9f9bf57958163ecd19200',  # Unodex
                '0x502fafbb87b159ce38a867e9335e3aa649e5e841',  # Unodex
                '0x5bdf03d80c2cecee9b9154654d0fbaa2179d188d',  # Unodex
            }
            if any(tx['ToAddress'].lower() in automated_addresses for tx in tx_details.values()):
                print(f"Bot users: Address {address} uses at least one bot")
                return True
            
            address_entropy = await self.tx_entropy_of(address, tx_details)
            # if interactions_counts[address]['totalTxCount'] >= 30 and address_entropy <= 1:
            if address_entropy <= 2:
                print(f"Low entropy: Address {address} has low entropy {address_entropy}")
                return True
                
            # if address_entropy >= 5:
            #     print(f"High entropy: Address {address} has high entropy {address_entropy}")
            #     return False

            return False
        except Exception as e:
            print(f"Error checking address automation: {address} {str(e)}")
            return False

    

    async def calculate_all_pair_addresses(self, token_contract: str, chain: str = 'eth'):
        """
        Calculate all pair addresses for a token contract on a given chain.

        Args:
            token_contract (str): The contract address of the token.
            chain (str): The chain to calculate pair addresses for.
        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the pair addresses and their corresponding DEX types.
        """
            
        chain_obj = get_chain_info(chain)
        tokens = get_all_chain_tokens(chain_obj.chainId).get_all_tokens()
        pair_addresses = []
        for token_symbol, token_info in tokens.items():
            for dex_type in ['uniswap_v2', 'uniswap_v3']:
                pair_address = await self.calculate_pair_address(token_contract, token_info.contract, dex_type)   
                if await self.web3_client.get_code(pair_address) is not None:
                    pair_addresses.append({
                        'dex_type': dex_type,
                        'pair_address': pair_address
                    })
        return pair_addresses

    async def calculate_pair_address(self, tokenA, tokenB, dex_type='uniswap_v2', fee=None):
        """
        Calculate the pair address for a token pair on a given DEX.

        Args:
            tokenA (str): The contract address of the first token.
            tokenB (str): The contract address of the second token.
            dex_type (str): The type of DEX to use.
            fee (int): The fee for the pair.

        Returns:
            str: The pair address.
        """
        w3 = Web3()

        dex_settings = {
            'uniswap_v2': {
                'factory_address': '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f',
                'init_code_hash': '0x96e8ac4277198ff8b6f785478aa9a39f403cb768dd02cbee326c3e7da348845f'
            },
            'uniswap_v3': {
                'factory_address': '0x1F98431c8aD98523631AE4a59f267346ea31F984',
                'init_code_hash': '0xe34f199b19b2b4f47f68442619d555527d244f78a3297ea89325f843f87b8b54'
            },
            'sushiswap_v2': {
                'factory_address': '0xC0AeE478e3658e2610c5F7A4A2E1777c13d831ec7',
                'init_code_hash': '0x96e8ac42782006f8894161745b24916fe9339b629bc3e7ca895b7c575c1d9c77'
            }
        }

        dex = dex_settings.get(dex_type.lower())
        if not dex:
            raise ValueError("Unsupported DEX type")

        if tokenA > tokenB:
            tokenA, tokenB = tokenB, tokenA

        if dex_type.lower() == 'uniswap_v3' and fee is not None:
            salt = Web3.keccak(
                w3.codec.encode(['address', 'address', 'uint24'],
                            [Web3.toChecksumAddress(tokenA),
                            Web3.toChecksumAddress(tokenB),
                            fee])
            )
        else:
            salt = Web3.keccak(Web3.to_bytes(hexstr=tokenA) + Web3.to_bytes(hexstr=tokenB))

        pair_address = Web3.solidity_keccak(
            ['bytes', 'address', 'bytes32', 'bytes32'],
            [
                '0xff',
                dex['factory_address'],
                salt,
                dex['init_code_hash']
            ]
        )[-20:]

        return Web3.to_checksum_address(pair_address)


    async def get_root_funder(self, address: str, max_depth: int = 20) -> Optional[Dict[str, Any]]:
        """
        Get the root funder (the earliest funder with no further funding source) for a given address.
        This function will keep searching deeper until it finds an address with no funding source,
        or until it reaches max_depth.
        
        Args:
            address: The address to find the root funder for
            max_depth: Maximum depth to prevent infinite loops (default: 20)

        Returns:
            Optional[Dict[str, Any]]: Dictionary containing:
                - address: The root funder's address
                - tx_hash: The transaction hash that funded the previous address
                - depth: How many levels deep we found this funder
                - is_root: True if this is confirmed to be the root funder (no further funding found)
            Returns None if no funding information is found
        """
        try:
            current_address = address
            current_depth = 0
            last_tx_hash = None
            
            while current_depth < max_depth:
                # Try to get next funder
                result = await self.funding_client.simulate_view_first_fund(current_address)
                if not result:
                    if current_depth > 0:
                        return {
                            "address": current_address,
                            "tx_hash": last_tx_hash,
                            "depth": current_depth,
                            "is_root": True  # Confirmed root as no further funding found
                        }
                    return None

                result_data = result
                tx_hash = result_data.get('TxnHash')
                if not tx_hash:
                    if current_depth > 0:
                        return {
                            "address": current_address,
                            "tx_hash": last_tx_hash,
                            "depth": current_depth,
                            "is_root": True  # No transaction hash means no further funding
                        }
                    return None

                # Try to get funder from API response first
                next_funder = result_data.get('From')
                
                if not next_funder:
                    # Fallback to transaction lookup
                    try:
                        tx = await self.web3_client.get_transaction(tx_hash)
                        if not tx:
                            if current_depth > 0:
                                return {
                                    "address": current_address,
                                    "tx_hash": last_tx_hash,
                                    "depth": current_depth,
                                    "is_root": True  # No transaction means no further funding
                                }
                            return None
                        next_funder = tx['from']
                    except Exception as tx_error:
                        logger.error(f"Error getting transaction {tx_hash} in get_root_funder: {str(tx_error)}")
                        if current_depth > 0:
                            return {
                                "address": current_address,
                                "tx_hash": last_tx_hash,
                                "depth": current_depth,
                                "is_root": False  # Error means we're not sure if this is root
                            }
                        return None

                # Update for next iteration
                last_tx_hash = tx_hash
                current_address = next_funder
                current_depth += 1

            # If we reach max depth, return the last funder but indicate it might not be root
            return {
                "address": current_address,
                "tx_hash": last_tx_hash,
                "depth": current_depth,
                "is_root": False  # Reached max depth, might not be actual root
            }

        except Exception as e:
            logger.error(f"Error getting root funder for {address}: {str(e)}")
            return None
        
    async def get_root_funders(self, addresses: List[str], max_depth: int = 20) -> Dict[str, Optional[Dict[str, Any]]]:
        """
        Get the root funders (earliest funders with no further funding sources) for a list of addresses.
        
        Args:
            addresses: List of addresses to find the root funders for
            max_depth: Maximum depth to prevent infinite loops (default: 20)
            
        Returns:
            Dict[str, Optional[Dict[str, Any]]]: Dictionary mapping input addresses to their root funder info.
            Each root funder info contains:
                - address: The root funder's address
                - tx_hash: The transaction hash that funded the previous address
                - depth: How many levels deep we found this funder
                - is_root: True if this is confirmed to be the root funder
        """
        tasks = [self.get_root_funder(addr, max_depth) for addr in addresses]
        results = await asyncio.gather(*tasks)
        return dict(zip(addresses, results))
    
    @file_cache(namespace="token_metadata", ttl=3600*24)  # Cache for 24 hours
    async def get_token_metadata(self, token_address: str) -> Optional[Dict[str, Any]]:
        """Get token metadata from the database.
        
        Args:
            token_address: Token contract address
            
        Returns:
            Optional[Dict[str, Any]]: Token metadata if found, None otherwise
        """
        try:
            query = """
                SELECT symbol, decimals
                FROM token_info 
                WHERE address = $1
            """
            
            # logger.info(f"Getting token metadata for {token_address}")
            result = await self.pg_client.execute_query(query, (token_address.lower()))
            if result and len(result) > 0:
                return {
                    'symbol': result[0]['symbol'],
                    'decimals': result[0]['decimals']
                }
            return None
        except Exception as e:
            logger.error(f"Error getting token metadata: {str(e)}")
            return None

    async def get_token_transfer_txs(self, token_address: str) -> List[Dict[str, Any]]:
        """Get all transfer transactions for a token.
        
        Args:
            token_address: Token contract address

        Returns:
            List[Dict[str, Any]]: List of transfer transactions
        """
        try:
            query = """
                SELECT DISTINCT transaction_hash
                FROM token_transfers
                WHERE token_address = $1
            """
            result = await self.pg_client.execute_query(query, (token_address.lower()))
            return [row['transaction_hash'] for row in result]
        except Exception as e:
            logger.error(f"Error getting token transfers: {str(e)}")
            return []

    async def get_balance_changes_for_txs(self, tx_hashes: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Get balance changes for multiple transactions.
        
        Args:
            tx_hashes: List of transaction hashes to analyze
            
        Returns:
            Dict mapping transaction hash to its balance changes
        """
        if not tx_hashes:
            return {}

        def _ensure_address(addr: str, changes: Dict):
            """Ensure address exists in changes dict"""
            if addr.lower() not in changes:
                changes[addr.lower()] = {
                    'eth_change': 0,
                    'token_changes': {}
                }

        # Initialize the all_changes dictionary to store results
        all_changes = {}

        # Process transactions in batches of 100
        batch_size = 100
        
        for i in range(0, len(tx_hashes), batch_size):
            batch_hashes = tx_hashes[i:i + batch_size]
            # logger.info(f"Processing batch {i//batch_size + 1} of {(len(tx_hashes) + batch_size - 1)//batch_size}")
            
            try:
                # Use rate-limited search from OpenSearch client with required fields
                fields = ['Hash', 'Status', 'BalanceWrite', 'Logs']
                txs_data = await self.blockos_client.search_transaction_batch(batch_hashes, fields=fields)



                # Process each transaction in the batch
                for tx_hash, tx in txs_data.items():
                    tx_changes = {}
                    
                    # Skip failed transactions
                    if not tx.get("Status", False):
                        continue

                    # Process ETH balance changes from BalanceWrite
                    if "BalanceWrite" in tx:
                        for balance_write in tx["BalanceWrite"]:
                            address = balance_write["Address"].lower()
                            prev = int(balance_write["Prev"]) if balance_write["Prev"] != "0x" else 0
                            current = int(balance_write["Current"]) if balance_write["Current"] != "0x" else 0
                            
                            _ensure_address(address, tx_changes)
                            tx_changes[address]['eth_change'] = current - prev
                            # print(f"eth change in {tx_hash}, {address}, {current} - {prev}={current - prev}")

                    # Process token balance changes from logs
                    WETH_LOWER = constants.WrappedToken.ETHEREUM.lower()
                    if "Logs" in tx:
                        for log in tx["Logs"]:
                            # Skip non-Transfer events
                            if log["Topics"][0] == constants.TRANSFER_EVENT_TOPIC and len(log.get("Topics", [])) == 3:
                                # Get token contract and addresses
                                token_addr = log["Address"].lower()
                                from_addr = "0x" + log["Topics"][1][-40:].lower()
                                to_addr = "0x" + log["Topics"][2][-40:].lower()
                                
                                try:
                                    amount = int(log["Data"], 16)
                                except ValueError:
                                    logger.warning(f"Failed to parse token amount from log data: {log['Data']}")
                                    continue

                                # Get token metadata
                                token_data = await self.get_token_metadata(token_addr)
                                
                                # From address loses tokens
                                _ensure_address(from_addr, tx_changes)
                                if token_addr not in tx_changes[from_addr]['token_changes']:
                                    tx_changes[from_addr]['token_changes'][token_addr] = {
                                        'amount': 0,
                                        'symbol': token_data['symbol'] if token_data else '???',
                                        'decimals': token_data['decimals'] if token_data else 18
                                    }
                                tx_changes[from_addr]['token_changes'][token_addr]['amount'] -= amount
                                
                                # To address gains tokens
                                _ensure_address(to_addr, tx_changes)
                                if token_addr not in tx_changes[to_addr]['token_changes']:
                                    tx_changes[to_addr]['token_changes'][token_addr] = {
                                        'amount': 0,
                                        'symbol': token_data['symbol'] if token_data else '???',
                                        'decimals': token_data['decimals'] if token_data else 18
                                    }
                                tx_changes[to_addr]['token_changes'][token_addr]['amount'] += amount
                            elif log['Address'] == WETH_LOWER and len(log.get("Topics", [])) == 2:
                                if log['Topics'][0] == '0xe1fffcc4923d04b559f4d29a8bfc6cda04eb5b0d3c460751c2402c5c5cc9109c': #WETH Deposit
                                    dst = "0x" + log["Topics"][1][-40:].lower()
                                    amount = int(log["Data"], 16)
                                    _ensure_address(dst, tx_changes)
                                    if WETH_LOWER not in tx_changes[dst]['token_changes']:
                                        tx_changes[dst]['token_changes'][WETH_LOWER] = {
                                            'amount': 0,
                                            'symbol': 'WETH',
                                            'decimals': 18
                                        }
                                    tx_changes[dst]['token_changes'][WETH_LOWER]['amount'] += amount

                                    _ensure_address(WETH_LOWER, tx_changes)
                                    if WETH_LOWER not in tx_changes[WETH_LOWER]['token_changes']:
                                        tx_changes[WETH_LOWER]['token_changes'][WETH_LOWER] = {
                                            'amount': 0,
                                            'symbol': 'WETH',
                                            'decimals': 18
                                        }
                                    tx_changes[WETH_LOWER]['token_changes'][WETH_LOWER]['amount'] -= amount
                                    # tx_changes['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2']['token_changes']['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2']['amount'] -= amount

                                elif log['Topics'][0] == '0x7fcf532c15f0a6db0bd6d0e038bea71d30d808c7d98cb3bf7268a95bf5081b65': #WETH Withdraw
                                    src = "0x" + log["Topics"][1][-40:].lower()
                                    amount = int(log["Data"], 16)
                                    _ensure_address(src, tx_changes)
                                    if WETH_LOWER not in tx_changes[WETH_LOWER]['token_changes']:
                                        tx_changes[WETH_LOWER]['token_changes'][WETH_LOWER] = {
                                            'amount': 0,
                                            'symbol': 'WETH',
                                            'decimals': 18
                                        }
                                    tx_changes[src]['token_changes'][WETH_LOWER]['amount'] -= amount
                                    _ensure_address(WETH_LOWER, tx_changes)
                                    if WETH_LOWER not in tx_changes[WETH_LOWER]['token_changes']:
                                        tx_changes[WETH_LOWER]['token_changes'][WETH_LOWER] = {
                                            'amount': 0,
                                            'symbol': 'WETH',
                                            'decimals': 18
                                        }
                                    tx_changes[WETH_LOWER]['token_changes'][WETH_LOWER]['amount'] += amount
                            else:
                                continue

                    # Store changes for this transaction
                    all_changes[tx_hash] = tx_changes
            except Exception as e:
                logger.error(f"Error searching transactions batch {i}-{i+batch_size}: {str(e)}")
                continue

        return all_changes


    async def aggregate_balance_changes(self, tx_hashes: List[str]) -> Dict[str, Dict[str, Any]]:
        """Aggregate balance changes for every address across multiple transactions.
        
        Args:
            tx_hashes: List of transaction hashes to analyze
            
        Returns:
            Dict mapping addresses to their aggregated changes and related transactions:
            {
                "address": {
                    "eth_change": int,  # Total ETH change in wei
                    "token_changes": {
                        "token_address": {
                            "amount": int,  # Total token amount change
                            "symbol": str,  # Token symbol
                            "decimals": int # Token decimals
                        }
                    },
                    "transactions": [  # List of transactions affecting this address
                        {
                            "hash": str,  # Transaction hash
                            "eth_change": int,  # ETH change in this tx
                            "token_changes": {  # Token changes in this tx
                                "token_address": {
                                    "amount": int,
                                    "symbol": str
                                }
                            }
                        }
                    ]
                }
            }
        """
        # Get individual transaction changes
        tx_changes = await self.get_balance_changes_for_txs(tx_hashes)
        
        # Initialize aggregated changes
        aggregated = {}
        
        # Process each transaction
        for tx_hash, changes in tx_changes.items():
            # Process each address in the transaction
            for address, addr_changes in changes.items():
                # Initialize address in aggregated if not exists
                if address not in aggregated:
                    aggregated[address] = {
                        'eth_change': 0,
                        'token_changes': {},
                        'transactions': []
                    }
                
                # Add ETH changes
                aggregated[address]['eth_change'] += addr_changes['eth_change']
                
                # Add token changes
                for token_addr, token_data in addr_changes.get('token_changes', {}).items():
                    if token_addr not in aggregated[address]['token_changes']:
                        aggregated[address]['token_changes'][token_addr] = {
                            'amount': 0,
                            'symbol': token_data['symbol'],
                            'decimals': token_data['decimals']
                        }
                    aggregated[address]['token_changes'][token_addr]['amount'] += token_data['amount']
                
                # Add transaction to address history
                aggregated[address]['transactions'].append({
                    'hash': tx_hash,
                    'eth_change': addr_changes['eth_change'],
                    'token_changes': addr_changes.get('token_changes', {})
                })
        
        return aggregated


    async def get_profit_ranking(self, tx_hashes: List[str]) -> List[Dict[str, Any]]:
        """Calculate profit ranking for addresses involved in transactions.
        Only considers ETH, WETH, USDC, USDT, DAI and WBTC as profit sources.
        Ranks by positive profits only, but includes negative profits at the end.
        
        Token prices:
        - ETH/WETH: $3000
        - USDC/USDT/DAI: $1
        - WBTC: $100000
        
        Args:
            tx_hashes: List of transaction hashes to analyze
            
        Returns:
            List of dicts containing address and profit info, sorted by profit:
            [
                {
                    "address": str,
                    "total_profit_usd": float,
                    "profit_breakdown": {
                        "token_address": {
                            "symbol": str,
                            "amount": float,  # Token amount
                            "amount_usd": float  # USD value
                        }
                    },
                    "related_transactions": [  # List of transactions affecting this address
                        {
                            "hash": str,  # Transaction hash
                            "eth_change": float,  # ETH change in this tx
                            "token_changes": {  # Token changes in this tx
                                "token_address": {
                                    "amount": float,
                                    "symbol": str
                                }
                            }
                        }
                    ]
                }
            ]
        """
        # Token addresses and prices
        PROFIT_TOKENS = {
            "0x0000000000000000000000000000000000000000": {  # ETH
                "symbol": "ETH",
                "price": 3000,
                "decimals": 18
            },
            "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": {  # WETH
                "symbol": "WETH",
                "price": 3000,
                "decimals": 18
            },
            "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": {  # USDC
                "symbol": "USDC",
                "price": 1,
                "decimals": 6
            },
            "0xdac17f958d2ee523a2206206994597c13d831ec7": {  # USDT
                "symbol": "USDT",
                "price": 1,
                "decimals": 6
            },
            "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599": {  # WBTC
                "symbol": "WBTC",
                "price": 100000,
                "decimals": 8
            },
            "0x6b175474e89094c44da98b954eedeac495271d0f": {  # DAI
                "symbol": "DAI",
                "price": 1,
                "decimals": 18
            }
        }
        
        # Get aggregated changes
        aggregated = await self.aggregate_balance_changes(tx_hashes)
        
        # Calculate profits for each address
        profits = []
        losses = []  # Track losses separately
        for address, data in aggregated.items():
            profit_info = {
                "address": address,
                "total_profit_usd": 0,
                "profit_breakdown": {},
                "related_transactions": []
            }
            
            # Calculate ETH profit
            eth_change = data['eth_change'] / 1e18  # Convert wei to ETH
            if eth_change != 0:
                eth_profit_usd = eth_change * PROFIT_TOKENS["0x0000000000000000000000000000000000000000"]["price"]
                profit_info["profit_breakdown"]["0x0000000000000000000000000000000000000000"] = {
                    "symbol": "ETH",
                    "amount": eth_change,
                    "amount_usd": eth_profit_usd
                }
                profit_info["total_profit_usd"] += eth_profit_usd
            
            # Calculate token profits
            for token_addr, token_data in data.get('token_changes', {}).items():
                if token_addr in PROFIT_TOKENS:
                    token_info = PROFIT_TOKENS[token_addr]
                    amount = token_data['amount'] / (10 ** token_info['decimals'])
                    if amount != 0:
                        profit_usd = amount * token_info['price']
                        profit_info["profit_breakdown"][token_addr] = {
                            "symbol": token_info["symbol"],
                            "amount": amount,
                            "amount_usd": profit_usd
                        }
                        profit_info["total_profit_usd"] += profit_usd
            
            # Add related transactions with normalized values
            for tx in data.get('transactions', []):
                tx_info = {
                    "hash": tx['hash'],
                    "eth_change": tx['eth_change'] / 1e18,  # Convert wei to ETH
                    "token_changes": {}
                }
                
                # Normalize token amounts in transaction
                for token_addr, token_data in tx.get('token_changes', {}).items():
                    if token_addr in PROFIT_TOKENS:
                        token_info = PROFIT_TOKENS[token_addr]
                        amount = token_data['amount'] / (10 ** token_info['decimals'])
                        tx_info["token_changes"][token_addr] = {
                            "amount": amount,
                            "symbol": token_info["symbol"]
                        }
                
                profit_info["related_transactions"].append(tx_info)
            
            if profit_info["total_profit_usd"] > 0:  # Positive profit
                profits.append(profit_info)
            elif profit_info["total_profit_usd"] < 0:  # Negative profit (loss)
                losses.append(profit_info)
        
        # Sort profits by amount (descending) and losses by amount (ascending)
        profits.sort(key=lambda x: x["total_profit_usd"], reverse=True)
        losses.sort(key=lambda x: x["total_profit_usd"])
        
        # Return profits first, followed by losses
        return profits + losses



    @file_cache(namespace="funding_path", ttl=3600*168)  # Cache for 24 hours
    async def get_funding_path(self, address: str, max_depth: int = 20, stop_at_cex: bool = True) -> List[Dict[str, Any]]:
        """
        Get the complete funding path for an address up to the root funder or first CEX.
        
        Args:
            address: The address to get the funding path for
            max_depth: Maximum depth to search (default: 20)
            stop_at_cex: If True, stops at first CEX found (default: True)
            
        Returns:
            List[Dict[str, Any]]: List of funding steps, each containing:
                - address: The funder's address
                - tx_hash: The transaction hash
                - depth: The depth level of this funder
                - is_cex: Boolean indicating if the funder is a CEX/EXCHANGE
                - label: The address label (or "Default" if none)
                - name_tag: The name tag of the address (if any)
                - type: The type of the address (if any)
                - entity: The entity type of the address (if any)
        """
        path = []
        current_address = address
        depth = 0
        BATCH_SIZE = 10
        pending_funders = []
        pending_txs = []
        try:
            while depth < max_depth:
                # Get funding info for current address
                result = await self.funding_client.simulate_view_first_fund(current_address)
                # If no funding info found, we've reached the end
                # if not result or 'result' not in result or not result['result']:
                #     break
                if result is None:
                    break
                    
                result_data = result
                tx_hash = result_data.get('TxnHash')
                if not tx_hash:
                    break
                    
                # Get funder address
                next_funder = result_data.get('From')
                if not next_funder:
                    try:
                        tx = await self.web3_client.get_transaction(tx_hash)
                        if not tx:
                            logger.error(f"No transaction found for hash {tx_hash}")
                            break
                        next_funder = tx['from']
                    except Exception as e:
                        logger.error(f"Error getting transaction {tx_hash} in get_funding_path: {str(e)}")
                        break
                
                # Add to pending lists
                pending_funders.append(next_funder)
                pending_txs.append((tx_hash, depth + 1))
                
                # Process batch if we've reached BATCH_SIZE or at max depth
                if len(pending_funders) >= BATCH_SIZE or depth == max_depth - 1:
                    # Get labels for the batch
                    if self.label_client:
                        try:
                            label_results = await self.label_client.get_addresses_labels(pending_funders)
                            label_map = {
                                result['address'].lower(): result 
                                for result in label_results
                            }
                            
                            # Process each pending funder
                            for i, funder in enumerate(pending_funders):
                                funder_lower = funder.lower()
                                tx_hash, cur_depth = pending_txs[i]
                                label_info = label_map.get(funder_lower, {})
                                
                                # Check if it's a CEX
                                label_type = (label_info.get('type') or 'DEFAULT').upper()
                                name_tag = (label_info.get('name_tag') or '').upper()
                                is_cex = any(cex_term in label_type for cex_term in ['CEX', 'EXCHANGE'])
                                # Add to path
                                path.append({
                                    'address': funder,
                                    'tx_hash': tx_hash,
                                    'depth': cur_depth,
                                    'is_cex': is_cex,
                                    'label': label_info.get('label', 'Default'),
                                    'name_tag': name_tag,
                                    'type': label_type,
                                    'entity': label_info.get('entity')
                                })
                                
                                # If this is a CEX and we should stop, prune the path and return
                                if stop_at_cex and is_cex:
                                    return path[:path.index(path[-1]) + 1]
                            
                        except Exception as e:
                            logger.error(f"Error getting labels for funders batch: {str(e)}")
                            # Add funders without labels
                            for i, funder in enumerate(pending_funders):
                                tx_hash, cur_depth = pending_txs[i]
                                path.append({
                                    'address': funder,
                                    'tx_hash': tx_hash,
                                    'depth': cur_depth,
                                    'is_cex': False,
                                    'label': 'Default',
                                    'name_tag': '',
                                    'type': '',
                                    'entity': ''
                                })
                    
                    # Clear pending lists
                    pending_funders = []
                    pending_txs = []
                
                current_address = next_funder
                depth += 1
            
            # Process any remaining funders
            if pending_funders:
                if self.label_client:
                    try:
                        label_results = await self.label_client.get_addresses_labels(pending_funders)
                        label_map = {
                            result['address'].lower(): result 
                            for result in label_results
                        }
                        
                        for i, funder in enumerate(pending_funders):
                            funder_lower = funder.lower()
                            tx_hash, cur_depth = pending_txs[i]
                            label_info = label_map.get(funder_lower, {})
                            
                            label_type = (label_info.get('type') or 'DEFAULT').upper()
                            name_tag = (label_info.get('name_tag') or '').upper()
                            is_cex = any(cex_term in label_type for cex_term in ['CEX', 'EXCHANGE'])
                            entity = label_info.get('entity')
                            
                            path.append({
                                'address': funder,
                                'tx_hash': tx_hash,
                                'depth': cur_depth,
                                'is_cex': is_cex,
                                'label': label_info.get('label', 'Default'),
                                'name_tag': name_tag,
                                'type': label_type,
                                'entity': entity
                            })
                            
                            if stop_at_cex and is_cex:
                                return path[:path.index(path[-1]) + 1]
                            
                    except Exception as e:
                        logger.error(f"Error getting labels for remaining funders: {str(e)}")
                        for i, funder in enumerate(pending_funders):
                            tx_hash, cur_depth = pending_txs[i]
                            path.append({
                                'address': funder,
                                'tx_hash': tx_hash,
                                'depth': cur_depth,
                                'is_cex': False,
                                'label': 'Default',
                                'name_tag': '',
                                'type': '',
                                'entity': ''
                            })
            return path
            
        except Exception as e:
            logger.error(f"Error getting funding path: {str(e)}")
            return path


    async def check_funding_relationship(
        self, 
        address1: str, 
        address2: str, 
        max_depth: int = 20,
        stop_at_cex: bool = True,
        return_details: bool = False,
        exclude_cex_relationships: bool = False
    ) -> Optional[Union[Dict[str, Any], bool]]:
        """
        Check if two addresses have a funding relationship by finding common funders
        in their funding paths. A common funder can be:
        1. Same address in both paths
        2. Different addresses but belong to the same non-empty entity
        
        Args:
            address1: First address to check
            address2: Second address to check
            max_depth: Maximum depth to search in each path (default: 20)
            stop_at_cex: If True, stops traversing when a CEX/EXCHANGE is found (default: True)
            return_details: If True, returns full relationship details; if False, returns True/False (default: False)
            exclude_cex_relationships: If True, CEX/EXCHANGE entities won't be considered as valid relationships (default: False)
            
        Returns:
            Optional[Union[Dict[str, Any], bool]]: If return_details=True and a relationship is found, returns:
                - common_funder1: The funder's address in first path
                - common_funder2: The funder's address in second path (same as common_funder1 if same address)
                - depth1: Depth of funder in first address's path
                - depth2: Depth of funder in second address's path
                - tx_hash1: Transaction hash from funder to first path
                - tx_hash2: Transaction hash from funder to second path
                - common_type: Type of relationship (1: same entity, 2: same address with empty entity, 0: no relationship)
                - label: The funder's label
                - name_tag: The name tag of the funder
                - type: The type of the funder
                - entity: The entity of the funder (if any)
            If return_details=False and a relationship is found, returns True
            Otherwise returns None if no relationship was found
        """
        try:
            # Get funding paths for both addresses in parallel
            path1, path2 = await asyncio.gather(
                self.get_funding_path(address1, max_depth, stop_at_cex),
                self.get_funding_path(address2, max_depth, stop_at_cex)
            )
            
            # Create maps for faster lookup
            path1_map = {step['address']: step for step in path1}
            path2_map = {step['address']: step for step in path2}
            
            # Find relationships
            relationships = []
            
            # Case 1: Same address funders
            common_addresses = set(path1_map.keys()) & set(path2_map.keys())
            for addr in common_addresses:
                funder1 = path1_map[addr]
                funder2 = path2_map[addr]
                
                # Skip CEX/EXCHANGE entities if exclude_cex_relationships is True
                if exclude_cex_relationships:
                    # Check if address type contains CEX or EXCHANGE
                    funder_type = funder1.get('type', '').upper()
                    if 'CEX' in funder_type or 'EXCHANGE' in funder_type:
                        continue
                
                common_type = 1 if funder1.get('entity') and funder1['entity'] == funder2.get('entity') else 2
                relationships.append({
                    'common_funder1': addr,
                    'common_funder2': addr,
                    'funder1': funder1,
                    'funder2': funder2,
                    'combined_depth': funder1['depth'] + funder2['depth'],
                    'common_type': common_type
                })
            
            # Case 2: Different addresses with same non-empty entity
            entity_map1 = {}
            entity_map2 = {}
            
            for addr, data in path1_map.items():
                entity = data.get('entity')
                if entity:
                    if entity not in entity_map1:
                        entity_map1[entity] = []
                    entity_map1[entity].append((addr, data))
                    
            for addr, data in path2_map.items():
                entity = data.get('entity')
                if entity:
                    if entity not in entity_map2:
                        entity_map2[entity] = []
                    entity_map2[entity].append((addr, data))
            
            # Find addresses with same entity
            common_entities = set(entity_map1.keys()) & set(entity_map2.keys())
            for entity in common_entities:
                # Skip CEX/EXCHANGE entities if exclude_cex_relationships is True
                if exclude_cex_relationships:
                    # Check the first address in the entity to determine if it's a CEX/EXCHANGE
                    first_addr, first_data = entity_map1[entity][0]
                    entity_type = first_data.get('type', '').upper()
                    if 'CEX' in entity_type or 'EXCHANGE' in entity_type:
                        continue
                
                for addr1, funder1 in entity_map1[entity]:
                    for addr2, funder2 in entity_map2[entity]:
                        if addr1 != addr2:  # Skip if same address (already handled in Case 1)
                            relationships.append({
                                'common_funder1': addr1,
                                'common_funder2': addr2,
                                'funder1': funder1,
                                'funder2': funder2,
                                'combined_depth': funder1['depth'] + funder2['depth'],
                                'common_type': 1  # Same entity
                            })
            
            if not relationships:
                return None if return_details else False
                
            # Find the closest relationship (minimum combined depth)
            closest = min(relationships, key=lambda x: x['combined_depth'])
            
            if return_details:
                return {
                    'common_funder1': closest['common_funder1'],
                    'common_funder2': closest['common_funder2'],
                    'depth1': closest['funder1']['depth'],
                    'depth2': closest['funder2']['depth'],
                    'tx_hash1': closest['funder1']['tx_hash'],
                    'tx_hash2': closest['funder2']['tx_hash'],
                    'common_type': closest['common_type'],
                    'label': closest['funder1']['label'],
                    'name_tag': closest['funder1'].get('name_tag', ''),
                    'type': closest['funder1'].get('type', 'EOA'),
                    'entity': closest['funder1'].get('entity', '')
                }
            else:
                return True
            
        except Exception as e:
            logger.error(f"Error checking funding relationship: {str(e)}")
            return None if return_details else False

    async def check_funding_relationships_batch(
        self,
        target_addresses: List[str],
        check_addresses: List[str],
        max_depth: int = 20,
        stop_at_cex: bool = True,
        chunk_size: int = 4,
        return_details: bool = False,
        exclude_cex_relationships: bool = False
    ) -> Dict[str, Dict[str, Union[bool, Dict[str, Any]]]]:
        """
        Check funding relationships between multiple addresses in parallel.
        
        Args:
            target_addresses: List of addresses to check relationships with
            check_addresses: List of addresses to check against target_addresses
            max_depth: Maximum depth to search in each path (default: 20)
            stop_at_cex: If True, stops traversing when a CEX/EXCHANGE is found (default: True)
            chunk_size: Number of check_addresses to process in parallel (default: 4)
            return_details: If True, returns full relationship details; if False, returns True/False (default: False)
            exclude_cex_relationships: If True, CEX/EXCHANGE entities won't be considered as valid relationships (default: False)
            
        Returns:
            Dict[str, Dict[str, Union[bool, Dict[str, Any]]]]: Dictionary mapping each check_address to a dictionary of
            target_addresses and their relationship information (either boolean or detailed dict based on return_details)
        """
        try:
            # Initialize results dictionary
            results = {addr: {} for addr in check_addresses}
            
            # Process each check_address in parallel chunks
            for i in range(0, len(check_addresses), chunk_size):
                chunk = check_addresses[i:i+chunk_size]
                
                # Check each address in the chunk against all target_addresses
                async def check_single_address(check_addr):
                    addr_results = {}
                    
                    # First check if the check_address is in target_addresses
                    if check_addr in target_addresses:
                        if return_details:
                            # Create self-relationship details
                            return {check_addr: {
                                target: {
                                    'common_funder1': check_addr if target == check_addr else None,
                                    'common_funder2': check_addr if target == check_addr else None,
                                    'depth1': 0 if target == check_addr else None,
                                    'depth2': 0 if target == check_addr else None,
                                    'common_type': 2 if target == check_addr else None,  # Same address
                                } for target in target_addresses
                            }}
                        else:
                            return {check_addr: {target: (target == check_addr) for target in target_addresses}}
                    
                    # Helper function to check relationship with a single target address
                    async def check_with_target(target_addr):
                        result = await self.check_funding_relationship(
                            target_addr, 
                            check_addr, 
                            max_depth=max_depth, 
                            stop_at_cex=stop_at_cex,
                            return_details=return_details,
                            exclude_cex_relationships=exclude_cex_relationships
                        )
                        return target_addr, result
                    
                    # Run all relationship checks for this address in parallel
                    target_results = await asyncio.gather(*[
                        check_with_target(target_addr) for target_addr in target_addresses
                    ])
                    
                    # Collect results
                    for target_addr, relationship in target_results:
                        addr_results[target_addr] = relationship
                    
                    return {check_addr: addr_results}
                
                # Process all addresses in the current chunk in parallel
                chunk_results = await asyncio.gather(*[
                    check_single_address(addr) for addr in chunk
                ])
                
                # Update results dictionary
                for result_dict in chunk_results:
                    for check_addr, target_results in result_dict.items():
                        results[check_addr].update(target_results)
            
            return results
            
        except Exception as e:
            logger.error(f"Error in batch check funding relationships: {str(e)}")
            return {addr: {} for addr in check_addresses}

    async def find_product(self, dev_or_ca: str, volume_threshold: float = 0.95) -> List[str]:
        """Find product contracts deployed by a developer based on unique counterparties.

        Args:
            dev_or_ca (str): Developer's address or contract address
            volume_threshold (float): Include top contracts that account for this fraction of total unique counterparties (default: 0.8)

        Returns:
            List[str]: List of contract addresses sorted by number of unique counterparties
        """
        try:
            # Get all contracts deployed by the developer
            is_contract = await self.is_contract_batch([dev_or_ca])
            if is_contract[0]:
                res = await self.etherscan_client.get_deployment(dev_or_ca)
                dev = res['contractCreator']
            else:
                dev = dev_or_ca
            print(f"Developer: {dev}")
            deployed_contracts = await self.blockos_client.fetch_created_contracts(dev)
            if not deployed_contracts:
                return []

            # Get interaction counts for non token contract
            is_token = await self.is_token_contract_batch([contract['contract_address'] for contract in deployed_contracts])
            deployed_contracts = [contract for contract, is_token in zip(deployed_contracts, is_token) if not is_token]
            contract_counterparties = []
            for contract in deployed_contracts:
                try:
                    # Each call returns a NEW dictionary with a single contract's stats
                    interactions = await self.blockos_client.interactions_count_batch([contract['contract_address']])
                    
                    # Each response is a new dictionary with one entry
                    if isinstance(interactions, dict) and len(interactions) > 0:
                        # Get the first (and only) entry's stats
                        stats = list(interactions.values())[0]
                        if isinstance(stats, dict) and 'totalDCounterpartyCount' in stats:
                            count = stats['totalDCounterpartyCount']
                            if count > 0:
                                contract_counterparties.append((contract['contract_address'], int(count)))
                except Exception as e:
                    print(f"Error processing contract {contract['contract_address']}: {str(e)}")
                    continue

            if not contract_counterparties:
                return []

            # Sort contracts by number of unique counterparties in descending order
            contract_counterparties.sort(key=lambda x: x[1], reverse=True)

            # Calculate total unique counterparties across all contracts
            total = 0
            for _, count in contract_counterparties:
                total += int(count)
            total_counterparties = total
            threshold_count = int(total_counterparties * volume_threshold)

            # Include contracts until we reach the counterparty threshold
            product_addresses = []
            cumulative_count = 0
            
            for addr, count in contract_counterparties:
                product_addresses.append(addr)
                cumulative_count += count
                if cumulative_count >= threshold_count:
                    break

            return product_addresses

        except Exception as e:
            print(f"Error finding product by dev {dev}: {str(e)}")
            return []

    async def close(self) -> None:
        """Close all clients and clean up resources"""
        if hasattr(self, '_clients') and self._clients:
            try:
                # Close each client properly
                close_tasks = []
                for name, client_proxy in self._clients.items():
                    try:
                        # Only attempt to close if the client was actually initialized
                        if client_proxy._client is not None:
                            # Get the actual client instance
                            client = client_proxy._client
                            if hasattr(client, 'close') and callable(client.close):
                                # Add to our tasks list for concurrent execution
                                close_tasks.append(client.close())
                    except Exception as e:
                        logger.error(f"Error preparing to close {name}: {str(e)}")
                
                # Wait for all close operations to complete
                if close_tasks:
                    await asyncio.gather(*close_tasks, return_exceptions=True)
                
                # Clear clients dictionary
                self._clients.clear()
                self._initialized = False
                
            except Exception as e:
                logger.error(f"Error during client cleanup: {str(e)}")

    async def simulate_trade_token_in_block(self, token_address: str, block_number: int, to_address: str = '0xE8a91DA6CF1b9D65C74A02ec1F96eecB6DD241f3'):
        input_data_buy = protocols.Uniswap.swapExactETHForTokensSupportingFeeOnTransferTokens(
            amount_out_min=0,
            path=[constants.WrappedToken.ETHEREUM, token_address],
            to=to_address,
            deadline=int(time.time()) + 60 * 20  # 20 minutes from now
        )

        input_data_approve = protocols.ERC20.approve(
            spender=protocols.Uniswap.v2router,
            amount=10000000000000000
        )

        input_data_sell = protocols.Uniswap.swapExactTokensForETHSupportingFeeOnTransferTokens(
            amount_in=10000000000000000,
            amount_out_min=0,
            path=[token_address, constants.WrappedToken.ETHEREUM],
            to=to_address,
            deadline=int(time.time()) + 60 * 20  # 20 minutes from now
        )
        
        result = await self.funding_client.simulate_tx(
            block_number=block_number,
            block_index=0,
            from_address=to_address,  # Use the recipient address as sender
            to_address=protocols.Uniswap.v2router,
            gas_fee_cap=1074480206,  # Reasonable gas fee cap based on examples
            gas_tip_cap=1458880,     # Reasonable tip cap based on examples
            gas=200000,              # Higher gas limit for swap
            value="10000000000000000",  # 1 ETH in wei
            data=input_data,
            no_base_fee=False,
            skip_account_check=False,
            skip_balance_check=False,
            debug=False,
            preimage=True,
            tx_type=2  # EIP-1559 transaction
        )
        asyncio.gather(
            self.simulate_swap_in_block(token_address, block_number, to_address),
            self.simulate_swap_in_block(token_address, block_number, to_address),
            self.simulate_swap_in_block(token_address, block_number, to_address),
            self.simulate_swap_in_block(token_address, block_number, to_address),
            self.simulate_swap_in_block(token_address, block_number, to_address),
        )

    async def simulate_swap_in_block(self, token_address: str, block_number: int, to_address: str = '0xE8a91DA6CF1b9D65C74A02ec1F96eecB6DD241f3'):
        """Simulate a swap in transaction"""
        to_address = '0xE8a91DA6CF1b9D65C74A02ec1F96eecB6DD241f3'
        try:
            input_data = protocols.Uniswap.swapExactETHForTokens(
                amount_out_min=0,
                path=[constants.WrappedToken.ETHEREUM, token_address],
                to=to_address,
                deadline=int(time.time()) + 60 * 20  # 20 minutes from now
            )
            # Get the current balance of the address
            result = await self.funding_client.simulate_tx(
                block_number=block_number,
                block_index=0,
                from_address=to_address,  # Use the recipient address as sender
                to_address=protocols.Uniswap.v2router,
                gas_fee_cap=1074480206,  # Reasonable gas fee cap based on examples
                gas_tip_cap=1458880,     # Reasonable tip cap based on examples
                gas=200000,              # Higher gas limit for swap
                value="10000000000000000",  # 1 ETH in wei
                data=input_data,
                no_base_fee=False,
                skip_account_check=False,
                skip_balance_check=False,
                debug=False,
                preimage=True,
                tx_type=2  # EIP-1559 transaction
            )
            # print(result)
            if 'ErrorInfo' in result and result['ErrorInfo'] == '':
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"Error simulating swap in block: {str(e)}")
            return None

    # async def get_addresses_labels(self, addresses: List[str]) -> List[Dict[str, Any]]:
    #     """Get labels for a list of addresses"""
    #     try:
    #         label_client = await self.label_client
    #         return await label_client.get_addresses_labels(addresses)
    #     except Exception as e:
    #         logger.error(f"Error getting address labels: {str(e)}")
    #         return []

    # async def get_addresses_by_label(self, label: str, chain_id: int = 1) -> List[Dict[str, Any]]:
    #     """Find addresses by label"""
    #     try:
    #         label_client = await self.label_client
    #         return await label_client.get_addresses_by_label(label, chain_id)
    #     except Exception as e:
    #         logger.error(f"Error getting addresses by label: {str(e)}")
    #         return []
            
    # async def get_addresses_by_type(self, type_category: str, chain_id: int = 1) -> List[Dict[str, Any]]:
    #     """Find addresses by type"""
    #     try:
    #         label_client = await self.label_client
    #         return await label_client.get_addresses_by_type(type_category, chain_id)
    #     except Exception as e:
    #         logger.error(f"Error getting addresses by type: {str(e)}")
    #         return []

    async def build_addr_nodes(self, addresses: List[str], attributes: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Build address nodes with their properties.
        
        Args:
            addresses: List of addresses to build nodes for
            attributes: Optional list of attributes to return. If None, returns all attributes.
                       Available attributes:
                        - address: the hex address of the account
                        - isContract: whether the account is a contract
                        - totalTxCount: total valid transaction count, includes all transactions as long as 'from' or 'to' is the address
                        - totalDCounterpartyCount: the total number of distinct counterparties 
                            (for contract, it's the total number of distinct users interacting with the contract,
                            for account, it's the total number of distinct contracts the account has interacted with)
                        - totalMethodCount: the total number of methods triggered in all valid transactions
                        - firstTx: the first transaction hash
                            (for contract, it's the creation transaction hash,
                            for account, it's the funding transaction hash)
                        - firstTxBlock: block number of the first transaction
                        - currentBalance: current native token balance
                        # - totalAcTxCount: the total number of transactions interacting with account
                        # - totalCaInteracted: the toal number of contracts interacted
                        # - totalAcInteracted: the total number of accounts interacted
        
        Returns:
            List of dictionaries containing requested node data
        """
        start_time = time.perf_counter()
        timing_stats = {}

        # Get contract status for all addresses
        addresses = [addr.lower() for addr in addresses]
        timing_stats['address_prep'] = time.perf_counter() - start_time
        last_time = time.perf_counter()

        # If attributes not specified, return all
        if attributes is None:
            attributes = ["address", "isContract", "totalTxCount", "firstTx", "totalDCounterpartyCount", "totalMethodCount", "firstTxBlock", "currentBalance"]
        
        # Always include address in results
        if "address" not in attributes:
            attributes.append("address")

        # Initialize data fetching flags
        need_contract_status = "isContract" in attributes
        need_tx_count = "totalTxCount" in attributes
        need_method_count = "totalMethodCount" in attributes
        need_counterparty_count = "totalDCounterpartyCount" in attributes
        need_first_tx = any(attr in attributes for attr in ["firstTx", "firstTxBlock"])
        need_balance = "currentBalance" in attributes
        
        need_any_tx_data = need_tx_count or need_method_count or need_counterparty_count
        need_any_queries = need_any_tx_data or need_first_tx
        
        timing_stats['init_flags'] = time.perf_counter() - last_time
        last_time = time.perf_counter()
        
        # Get contract status if needed
        is_contract_map = {}
        if need_contract_status:
            is_contract_list = await self.is_contract_batch(addresses)
            # Filter out None values and treat them as non-contracts
            is_contract_map = {addr: bool(status) for addr, status in zip(addresses, is_contract_list)}
        timing_stats['contract_status'] = time.perf_counter() - last_time
        last_time = time.perf_counter()
        
        # Split addresses into contract and non-contract lists if any queries needed
        contract_addrs = []
        non_contract_addrs = []
        if need_any_queries:
            if need_contract_status:
                for addr in addresses:
                    if is_contract_map.get(addr, False):
                        contract_addrs.append(addr)
                    else:
                        non_contract_addrs.append(addr)
            else:
                # Even if contract status not needed, still split based on actual status
                # to maintain consistent batch counting
                for addr in addresses:
                    if is_contract_map.get(addr, False):
                        contract_addrs.append(addr)
                    else:
                        non_contract_addrs.append(addr)
        timing_stats['addr_split'] = time.perf_counter() - last_time
        last_time = time.perf_counter()
        
        # Initialize results dictionaries
        tx_counts = {}
        first_txs = {}
        method_counts = {}
        counterparty_counts = {}
        
        async def fetch_contract_data(addrs):
            if not addrs:
                return {}, {}
            fetch_start = time.perf_counter()
            tasks = []
            if need_any_tx_data:
                tasks.append(self.blockos_client.interactions_count_batch(addrs, "eth_block"))
            if need_first_tx:
                tasks.append(self.blockos_client.first_interaction_batch(addrs, "eth_block"))
            
            if not tasks:
                return {}, {}
            
            # Execute tasks
            results = await asyncio.gather(*tasks)
            counts = results[0] if need_any_tx_data else {}
            first_tx_data = results[-1] if need_first_tx else {}
            timing_stats['contract_fetch'] = time.perf_counter() - fetch_start
            return counts, first_tx_data

        async def fetch_non_contract_data(addrs):
            if not addrs:
                return {}, {}
            fetch_start = time.perf_counter()
            tasks = []
            if need_any_tx_data:
                tasks.append(self.blockos_client.search_sent_transaction_count_batch(addrs, "eth_block"))
            if need_first_tx:
                tasks.append(self.blockos_client.first_sent_transaction_batch(addrs, "eth_block"))
            
            if not tasks:
                return {}, {}
            
            # Execute tasks
            results = await asyncio.gather(*tasks)
            counts = results[0] if need_any_tx_data else {}
            first_tx_data = results[-1] if need_first_tx else {}
            timing_stats['non_contract_fetch'] = time.perf_counter() - fetch_start
            return counts, first_tx_data

        # Execute parallel queries for contract and non-contract addresses
        if need_any_queries:
            parallel_start = time.perf_counter()
            contract_results, non_contract_results = await asyncio.gather(
                fetch_contract_data(contract_addrs),
                fetch_non_contract_data(non_contract_addrs)
            )
            timing_stats['parallel_queries'] = time.perf_counter() - parallel_start
            process_start = time.perf_counter()
            
            # Process contract results
            contract_counts, contract_first_txs = contract_results
            for addr in contract_addrs:
                addr_data = contract_counts.get(addr, {})
                tx_counts[addr] = addr_data.get('totalTxCount', -1)
                method_counts[addr] = addr_data.get('totalMethodCount', -1)
                counterparty_counts[addr] = addr_data.get('totalDCounterpartyCount', -1)
                first_tx_data = contract_first_txs.get(addr, {})
                first_txs[addr] = {
                    'hash': first_tx_data.get('first_tx'),
                    'block': first_tx_data.get('first_tx_block')
                }
        
            # Process non-contract results
            non_contract_counts, non_contract_first_txs = non_contract_results
            for addr in non_contract_addrs:
                addr_data = non_contract_counts.get(addr, {})
                tx_counts[addr] = addr_data.get('totalTxCount', -1)
                method_counts[addr] = addr_data.get('totalMethodCount', -1)
                counterparty_counts[addr] = addr_data.get('totalDCounterpartyCount', -1)
                first_tx_data = non_contract_first_txs.get(addr, {})
                first_txs[addr] = {
                    'hash': first_tx_data.get('first_tx'),
                    'block': first_tx_data.get('first_tx_block')
                }
        
        # Get current balances if needed
        current_balances = {}
        if need_balance:
            balance_start = time.perf_counter()
            balances_result = await self.web3_client.get_balances(addresses)
            for addr, balance in zip(addresses, balances_result):
                current_balances[addr] = balance/1e18
            timing_stats['balance_fetch'] = time.perf_counter() - balance_start

        # Build final  list with requested attributes
        build_start = time.perf_counter()
        nodes = []
        for addr in addresses:
            node = {}
            addr = addr.lower()
            
            if "address" in attributes:
                node["address"] = addr
                
            if "isContract" in attributes:
                node["isContract"] = is_contract_map.get(addr, False)
            
            if "totalTxCount" in attributes:
                node["totalTxCount"] = tx_counts.get(addr, 0)
                
            if "totalMethodCount" in attributes:
                node["totalMethodCount"] = method_counts.get(addr, 0)
                
            if "totalDCounterpartyCount" in attributes:
                node["totalDCounterpartyCount"] = counterparty_counts.get(addr, 0)
                
            if "firstTx" in attributes and "firstTx" in attributes:
                node["firstTx"] = first_txs.get(addr, {}).get('hash')
                
            if "firstTxBlock" in attributes:
                node["firstTxBlock"] = first_txs.get(addr, {}).get('block')
        
            if "currentBalance" in attributes:
                node["currentBalance"] = current_balances.get(addr, 0)
            
            nodes.append(node)
        
        # timing_stats['build_nodes'] = time.perf_counter() - build_start
        # timing_stats['total_time'] = time.perf_counter() - start_time
        
        # logger.info("="*20 + " build_addr_nodes Performance Report " + "="*20)
        # logger.info(f"Processed {len(addresses)} addresses in {timing_stats['total_time']:.2f}s")
        # logger.info(f"Average processing speed: {len(addresses)/timing_stats['total_time']:.2f} addresses/sec")
        # logger.info("\nTiming breakdown:")
        # for stage, time_taken in timing_stats.items():
        #     if stage != 'total_time':
        #         percentage = time_taken/timing_stats['total_time']*100
                # logger.info(f"  {stage:<20}: {time_taken:>6.2f}s ({percentage:>5.1f}%)")
        # logger.info("="*70)
        
        # Add batch information
        # contract_count = len([addr for addr in addresses if is_contract_map.get(addr, False)])
        # non_contract_count = len(addresses) - contract_count
        # logger.info("\nBatch Information:")
        # logger.info(f"  Total Addresses: {len(addresses)}")
        # logger.info(f"  Contract Addresses: {contract_count}")
        # logger.info(f"  Non-Contract Addresses: {non_contract_count}")
        # logger.info(f"  Contract Batches: {len(contract_addrs) // self.opensearch_client._batch_size + (1 if len(contract_addrs) % self.opensearch_client._batch_size else 0)}")
        # logger.info(f"  Non-Contract Batches: {len(non_contract_addrs) // self.opensearch_client._batch_size + (1 if len(non_contract_addrs) % self.opensearch_client._batch_size else 0)}")
        
        return nodes

    async def build_tx_nodes(self, tx_hashes: List[str], attributes: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Build transaction nodes with their properties.
        
        Args:
            tx_hashes: List of transaction hashes to build nodes for
        
        Returns:
            List of dictionaries containing node data:
            - txHash: the transaction hash
            - blockNumber: the block number of the transaction
            - from: the sender of the transaction
            - to: the recipient of the transaction
            - value: the value in ETH
            - gasPrice: the gas price of the transaction
            - gasUsed: the gas used by the transaction
            - balanceChanges: optional dictionary of address balance changes
        """
        # Get transaction data from OpenSearch
        fields = ['Hash', 'FromAddress', 'ToAddress', 'Value', 'Status', 'GasPrice', 'GasUsed', 'BalanceWrite']
        txs_data = await self.blockos_client.search_transaction_batch(tx_hashes, "eth_block", fields=fields)
        
        if not txs_data:
            logger.error("No transaction data found")
            return []
        
        nodes = []
        
        # Build nodes with specified attributes
        if attributes is None:
            attributes = ['txHash', 'blockNumber', 'from', 'to', 'value', 'gasPrice', 'gasUsed', 'status']

        for tx_hash, tx in txs_data.items():
            # Calculate value in ETH (convert from Wei)
            value_wei = int(tx.get('Value', '0'), 16) if isinstance(tx.get('Value'), str) and tx.get('Value', '0').startswith('0x') else int(tx.get('Value', '0'))
            value_eth = value_wei / 10**18
            
            # Build node data
            node = {}
            for attr in attributes:
                if attr == 'txHash':
                    node[attr] = tx_hash
                elif attr == 'blockNumber':
                    node[attr] = int(tx.get('Block', 0))
                elif attr == 'from':
                    node[attr] = tx.get('FromAddress')
                elif attr == 'to':
                    node[attr] = tx.get('ToAddress')
                elif attr == 'value':
                    node[attr] = value_eth
                elif attr == 'gasPrice':
                    node[attr] = tx.get('GasPrice')
                elif attr == 'gasUsed':
                    node[attr] = tx.get('GasUsed')
                elif attr == 'status':
                    node[attr] = tx.get('Status', False)
                elif attr == 'balanceChanges':
                    balance_changes = {}
                    # Add balance changes if available
                    if 'BalanceWrite' in tx:
                        balance_changes = {}
                        for change in tx['BalanceWrite']:
                            addr = change['Address'].lower()
                            prev = int(change['Prev']) / 10**18
                            curr = int(change['Current']) / 10**18
                            balance_changes[addr] = {
                                'prev': prev,
                                'current': curr,
                                'diff': curr - prev
                            }
                        node['balanceChanges'] = balance_changes
            nodes.append(node)
        return nodes

    async def build_value_flow_map_by_txs_separately(self, tx_hashes: List[str]) -> Dict[str, Any]:
        """
        Build addr nodes, transaction nodes with their value flow relations.
        
        Args:
            tx_hashes: List of transaction hashes to build nodes for
        
        Returns:
            Dictionary containing:
            - addr_nodes: List of address nodes with properties (format matches build_addr_nodes)
            - tx_nodes: List of transaction nodes with properties (format matches build_tx_nodes)
            - relations: List of value flow relationships between transactions and addresses with fields:
                - txHash: the transaction hash
                - blockNumber: the block number of the transaction
                - from: source (address if outflow, transaction if inflow)
                - to: destination (transaction if outflow, address if inflow)
                - valueUSD: the absolute value of the transfer in USD
                - valueBreakdown: breakdown of value transfers by token
        """
        result = {
            'addr_nodes': [],
            'tx_nodes': [],
            'relations': []
        }
        
        # Build transaction nodes first to get block numbers
        if tx_hashes:
            result['tx_nodes'] = await self.build_tx_nodes(tx_hashes)

        # Create block number lookup
        tx_block_numbers = {node['txHash']: node['blockNumber'] for node in result['tx_nodes']}

        # Get profit ranking for all addresses involved
        profit_info = await self.get_profit_ranking(tx_hashes)

        # Extract unique addresses from profit info
        involved_addresses = set()
        for item in profit_info:
            involved_addresses.add(item['address'])
            
            # Process each transaction to create relations
            for tx in item['related_transactions']:
                total_value_usd = 0
                
                # Calculate total USD value from profit breakdown
                eth_change = tx['eth_change']
                if eth_change != 0:
                    eth_info = item['profit_breakdown'].get('0x0000000000000000000000000000000000000000')
                    if eth_info:
                        total_value_usd += eth_info['amount_usd']  # Keep sign for direction
                
                # Add token values
                for token_addr, token_info in tx['token_changes'].items():
                    if token_addr in item['profit_breakdown']:
                        token_profit = item['profit_breakdown'][token_addr]
                        total_value_usd += token_profit['amount_usd']  # Keep sign for direction
                
                if total_value_usd != 0:  # Create relation if there's any value flow
                    # eth_change/token_change positive: value flows FROM tx TO address
                    # eth_change/token_change negative: value flows FROM address TO tx
                    relation = {
                        'txHash': tx['hash'],
                        'blockNumber': tx_block_numbers.get(tx['hash']),
                        'from': tx['hash'] if eth_change > 0 else item['address'],  # tx->addr if positive change
                        'to': item['address'] if eth_change > 0 else tx['hash'],    # addr->tx if negative change
                        'valueUSD': abs(total_value_usd),
                        'valueBreakdown': item['profit_breakdown']
                    }
                    result['relations'].append(relation)

        # Build address nodes
        if involved_addresses:
            result['addr_nodes'] = await self.build_addr_nodes(list(involved_addresses), attributes=['address', 'isContract', 'totalTxCount', 'totalMethodCount', 'totalDCounterpartyCount', 'firstTx', 'firstTxBlock', 'currentBalance'])

        return result