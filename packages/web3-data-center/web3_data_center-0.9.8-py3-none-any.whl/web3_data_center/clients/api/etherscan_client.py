from .endpoint_config import EndpointConfig
from typing import Dict, Any, Optional, List
from ..mixins import AuthMixin, RateLimitMixin
from ..mixins.auth import AuthType
from .base_api_client import BaseAPIClient
from .endpoint_config import EndpointConfig
from typing import Dict, Any, Optional, List
from ..mixins import AuthMixin, RateLimitMixin
from ..mixins.auth import AuthType
from .base_api_client import BaseAPIClient


class EtherscanClient(BaseAPIClient, AuthMixin, RateLimitMixin):
    """Etherscan API client"""
    
    # API endpoint configurations
    ENDPOINTS = {
        'contract_creation': EndpointConfig(
            path="/api",
            batch_size=5,
            rate_limit=3.0,
            cost_weight=2.0
        ),
        'account_balance': EndpointConfig(
            path="/api",
            batch_size=20,
            rate_limit=5.0
        ),
        'account_txlist': EndpointConfig(
            path="/api",
            batch_size=100,
            rate_limit=5.0
        ),
        'account_tokentx': EndpointConfig(
            path="/api",
            batch_size=100,
            rate_limit=5.0
        ),
        'account_nfttx': EndpointConfig(
            path="/api",
            batch_size=100,
            rate_limit=5.0
        ),
        'account_internal_txs': EndpointConfig(
            path="/api",
            batch_size=100,
            rate_limit=5.0
        )
    }
    
    def __init__(self, config_path: str = "config.yml", use_proxy: bool = True):
        """Initialize Etherscan client"""
        super().__init__("etherscan", config_path, use_proxy)
        
        # Setup authentication and rate limits
        self.setup_auth(AuthType.API_KEY)
        self.setup_rate_limits(self.ENDPOINTS)
        
    @RateLimitMixin.rate_limited('contract_creation')
    async def get_deployment(self, address: str) -> Optional[Dict[str, Any]]:
        """Get contract deployment information"""
        params = {
            "module": "contract",
            "action": "getcontractcreation",
            "contractaddresses": address
        }
        
        params, headers = await self.authenticate_request(
            "GET", "/api", params, {}
        )
        
        result = await self._make_request("/api", params=params, headers=headers)
        return result.get('result', [{}])[0] if result else None

    async def get_deployments(self, addresses: List[str]) -> List[Dict[str, Any]]:
        """Get contract deployments in batches"""
        config = self.ENDPOINTS['contract_creation']
        results = []
        
        for i in range(0, len(addresses), config.batch_size):
            batch = addresses[i:i + config.batch_size]
            params = {
                "module": "contract",
                "action": "getcontractcreation",
                "contractaddresses": ','.join(batch)
            }
            
            params, headers = await self.authenticate_request(
                "GET", "/api", params, {}
            )
            
            result = await self._make_request("/api", params=params, headers=headers)
            if result and 'result' in result:
                # 处理API返回的结果
                if isinstance(result['result'], list):
                    # 将地址信息添加到每个部署信息中
                    for j, item in enumerate(result['result']):
                        if isinstance(item, dict):
                            # 如果没有地址信息，添加地址
                            if 'address' not in item and j < len(batch):
                                item['address'] = batch[j]
                            results.append(item)
                        else:
                            # 如果项不是字典，创建一个包含地址的字典
                            addr = batch[j] if j < len(batch) else "unknown"
                            results.append({
                                'address': addr,
                                'contractCreator': 'error',
                                'txHash': 'error',
                                'error': str(item)
                            })
                elif isinstance(result['result'], str):
                    # 如果结果是字符串(可能是错误消息)
                    for addr in batch:
                        results.append({
                            'address': addr,
                            'contractCreator': 'error',
                            'txHash': 'error',
                            'error': result['result']
                        })
                else:
                    # 处理其他类型的结果
                    for addr in batch:
                        results.append({
                            'address': addr,
                            'contractCreator': 'error',
                            'txHash': 'error',
                            'error': f"Unexpected result type: {type(result['result'])}"
                        })
                
        return results
        
    @RateLimitMixin.rate_limited('account_balance')
    async def get_eth_balance(self, address: str) -> Optional[str]:
        """Get ETH balance for an address
        
        Args:
            address: Ethereum address
            
        Returns:
            Balance in wei as string, or None if error
        """
        params = {
            "module": "account",
            "action": "balance",
            "address": address,
            "tag": "latest"
        }
        
        params, headers = await self.authenticate_request("GET", "/api", params, {})
        result = await self._make_request("/api", params=params, headers=headers)
        return result.get('result') if result else None
        
    async def get_eth_balances(self, addresses: List[str]) -> Dict[str, Optional[str]]:
        """Get ETH balances for multiple addresses
        
        Args:
            addresses: List of Ethereum addresses
            
        Returns:
            Dict mapping addresses to balances in wei
        """
        config = self.ENDPOINTS['account_balance']
        results = {}
        
        for i in range(0, len(addresses), config.batch_size):
            batch = addresses[i:i + config.batch_size]
            params = {
                "module": "account",
                "action": "balancemulti",
                "address": ','.join(batch),
                "tag": "latest"
            }
            
            params, headers = await self.authenticate_request("GET", "/api", params, {})
            result = await self._make_request("/api", params=params, headers=headers)
            
            if result and 'result' in result:
                for item in result['result']:
                    results[item['account']] = item['balance']

        return results
        
    @RateLimitMixin.rate_limited('account_txlist')
    async def get_normal_txs(self, address: str, startblock: int = 0, endblock: int = 99999999, 
                           page: int = 1, offset: int = 100, sort: str = "asc") -> List[Dict[str, Any]]:
        """Get list of normal transactions for an address
        
        Args:
            address: Ethereum address
            startblock: Start block number
            endblock: End block number
            page: Page number
            offset: Max records to return
            sort: Sort order (asc/desc)
            
        Returns:
            List of transaction objects
        """
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": str(startblock),
            "endblock": str(endblock),
            "page": str(page),
            "offset": str(offset),
            "sort": sort
        }
        
        params, headers = await self.authenticate_request("GET", "/api", params, {})
        result = await self._make_request("/api", params=params, headers=headers)
        return result.get('result', []) if result else []
        
    @RateLimitMixin.rate_limited('account_internal_txs')
    async def get_internal_txs(self, address: str, startblock: int = 0, endblock: int = 99999999,
                             page: int = 1, offset: int = 100, sort: str = "asc") -> List[Dict[str, Any]]:
        """Get list of internal transactions for an address
        
        Args:
            address: Ethereum address
            startblock: Start block number
            endblock: End block number
            page: Page number
            offset: Max records to return
            sort: Sort order (asc/desc)
            
        Returns:
            List of transaction objects
        """
        params = {
            "module": "account",
            "action": "txlistinternal",
            "address": address,
            "startblock": str(startblock),
            "endblock": str(endblock),
            "page": str(page),
            "offset": str(offset),
            "sort": sort
        }
        
        params, headers = await self.authenticate_request("GET", "/api", params, {})
        result = await self._make_request("/api", params=params, headers=headers)
        return result.get('result', []) if result else []
        
    @RateLimitMixin.rate_limited('account_tokentx')
    async def get_token_transfers(self, address: str, contractaddress: Optional[str] = None,
                                startblock: int = 0, endblock: int = 99999999,
                                page: int = 1, offset: int = 100, sort: str = "asc") -> List[Dict[str, Any]]:
        """Get list of ERC20 token transfers for an address
        
        Args:
            address: Ethereum address
            contractaddress: Token contract address (optional)
            startblock: Start block number
            endblock: End block number
            page: Page number
            offset: Max records to return
            sort: Sort order (asc/desc)
            
        Returns:
            List of token transfer objects
        """
        params = {
            "module": "account",
            "action": "tokentx",
            "address": address,
            "startblock": str(startblock),
            "endblock": str(endblock),
            "page": str(page),
            "offset": str(offset),
            "sort": sort
        }
        
        if contractaddress:
            params["contractaddress"] = contractaddress
            
        params, headers = await self.authenticate_request("GET", "/api", params, {})
        result = await self._make_request("/api", params=params, headers=headers)
        return result.get('result', []) if result else []
        
    @RateLimitMixin.rate_limited('account_nfttx')
    async def get_nft_transfers(self, address: str, contractaddress: Optional[str] = None,
                              startblock: int = 0, endblock: int = 99999999,
                              page: int = 1, offset: int = 100, sort: str = "asc") -> List[Dict[str, Any]]:
        """Get list of ERC721/ERC1155 NFT transfers for an address
        
        Args:
            address: Ethereum address
            contractaddress: NFT contract address (optional)
            startblock: Start block number
            endblock: End block number
            page: Page number
            offset: Max records to return
            sort: Sort order (asc/desc)
            
        Returns:
            List of NFT transfer objects
        """
        params = {
            "module": "account",
            "action": "tokennfttx",
            "address": address,
            "startblock": str(startblock),
            "endblock": str(endblock),
            "page": str(page),
            "offset": str(offset),
            "sort": sort
        }
        
        if contractaddress:
            params["contractaddress"] = contractaddress
            
        params, headers = await self.authenticate_request("GET", "/api", params, {})
        result = await self._make_request("/api", params=params, headers=headers)
        return result.get('result', []) if result else []



async def main():
    # Initialize client
    client = EtherscanClient(config_path="config.yml")
    
    # Example contract addresses
    contract_addresses = [
        "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",  # WETH
        "0x6b175474e89094c44da98b954eedeac495271d0f"   # DAI
    ]
    
    # Example wallet addresses
    wallet_addresses = [
        "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
        "0x2B5AD5c4795c026514f8317c7a215E218DcCD6cF"
    ]
    
    print("\n1. Getting Contract Deployment Information:")
    for address in contract_addresses:
        deployment = await client.get_deployment(address)
        print(f"\nContract {address}:")
        print(f"Deployed by: {deployment.get('contractCreator', 'Unknown')}")
        print(f"At transaction: {deployment.get('txHash', 'Unknown')}")
    
    print("\n2. Getting ETH Balances:")
    # Get single balance
    balance = await client.get_eth_balance(wallet_addresses[0])
    print(f"\nSingle address {wallet_addresses[0]} balance: {balance} wei")
    
    # Get multiple balances
    balances = await client.get_eth_balances(wallet_addresses)
    print("\nMultiple address balances:")
    for addr, bal in balances.items():
        print(f"{addr}: {bal} wei")
    
    print(f"\n3. Getting Transaction History for {wallet_addresses[0]}:")
    # Get normal transactions
    print("\nNormal transactions:")
    txs = await client.get_normal_txs(wallet_addresses[0], offset=5)
    for tx in txs[:5]:
        print(f"Hash: {tx.get('hash')}")
        print(f"From: {tx.get('from')}")
        print(f"To: {tx.get('to')}")
        print(f"Value: {tx.get('value')} wei")
        print("---")
    
    # Get internal transactions
    print("\nInternal transactions:")
    internal_txs = await client.get_internal_txs(wallet_addresses[0], offset=5)
    for tx in internal_txs[:5]:
        print(f"Parent Hash: {tx.get('hash')}")
        print(f"From: {tx.get('from')}")
        print(f"To: {tx.get('to')}")
        print(f"Value: {tx.get('value')} wei")
        print("---")
    
    print(f"\n4. Getting Token Transfers for {wallet_addresses[0]}:")
    # Get ERC20 token transfers
    print("\nERC20 token transfers:")
    token_txs = await client.get_token_transfers(wallet_addresses[0], offset=5)
    for tx in token_txs[:5]:
        print(f"Token: {tx.get('tokenName')} ({tx.get('tokenSymbol')})")
        print(f"From: {tx.get('from')}")
        print(f"To: {tx.get('to')}")
        print(f"Value: {tx.get('value')} (decimals: {tx.get('tokenDecimal')})")
        print("---")
    
    # Get NFT transfers
    print("\nNFT transfers:")
    nft_txs = await client.get_nft_transfers(wallet_addresses[0], offset=5)
    for tx in nft_txs[:5]:
        print(f"NFT Contract: {tx.get('contractAddress')}")
        print(f"From: {tx.get('from')}")
        print(f"To: {tx.get('to')}")
        print(f"Token ID: {tx.get('tokenID')}")
        print("---")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())