from typing import Dict, Any, List, Optional, Union
import logging
import time
from opensearchpy import AsyncOpenSearch
from ...utils.cache import file_cache
from ..mixins import ConfigMixin, ConnectionMixin, RateLimitMixin, BatchOperationMixin
from ..batch.executor import BatchExecutor
from ..batch.controller import BatchController, BatchConfig
from ..batch.types import BatchItem
from .opensearch_client import OpenSearchDatabaseClient
import asyncio
from pprint import pprint

logger = logging.getLogger(__name__)

class BlockOpenSearchClient(OpenSearchDatabaseClient):
    """Client for interacting with block data in OpenSearch

    Features:
    - Block data indexing and querying
    - Transaction data management
    - Token transfer tracking
    - Smart contract events
    """
    
    def __init__(self, config_path: str = "config.yml"):
        """Initialize block OpenSearch client"""
        # Initialize ConfigMixin and ConnectionMixin without validation
        ConfigMixin.__init__(self, config_path)
        ConnectionMixin.__init__(self, max_retries=3, retry_delay=1.0)
        
        # Set db_name before validation
        self.db_name = "opensearch"
        
        # Initialize rate limiting and batch operations
        RateLimitMixin.__init__(self)
        BatchOperationMixin.__init__(self)
        
        # Now validate the config
        self.validate_config()
        
        # Set up database specific attributes
        db_config = self.get_section_config('database')
        if self.db_name not in db_config:
            raise KeyError(f"Database {self.db_name} not found in config")
            
        self.db_config = db_config[self.db_name]
        
        # Default indices - use eth_ prefix
        self.block_index = "eth_block"
        
        # Initialize batch executor
        self.batch_executor = BatchExecutor(self._execute_batch)
        self.batch_size = self.db_config.get('batch_size', 100)
        self.max_concurrent = self.db_config.get('max_concurrent', 20)
        
        # Initialize rate limiting
        self.setup_rate_limits()  # Initialize rate limiting dictionary first
        self.setup_rate_limit(
            'request',
            requests_per_second=self.db_config.get('rps', 100.0)
        )
        
        # Initialize connection management
        self._connection = None
        self._connected = False
        self._connection_lock = asyncio.Lock()

    async def setup(self) -> None:
        """Set up the client connection"""
        async with self._connection_lock:
            if not self._connected:
                # Build connection string
                self.connection_string = await self._build_connection_string()
                
                # Create connection
                self._connection = await self._create_connection()
                self._connected = True

    @property
    def connection(self) -> Optional[AsyncOpenSearch]:
        """Get the current connection"""
        return self._connection

    @property
    def is_connected(self) -> bool:
        """Check if client is connected"""
        return self._connected

    async def close(self) -> None:
        """Close the connection"""
        async with self._connection_lock:
            if self._connected:
                await self._close_connection()
                self._connected = False

    async def get_block(self, block_number: int) -> Optional[Dict[str, Any]]:
        """Get block by number
        
        Args:
            block_number: Block number to get
            
        Returns:
            Block data if found, None otherwise
        """
        try:
            result = await self.connection.get(
                index=self.block_index,
                id=str(block_number)
            )
            return result['_source']
        except Exception as e:
            logger.error(f"Failed to get block: {str(e)}")
            return None

    async def get_transaction(self, tx_hash: str) -> Optional[Dict[str, Any]]:
        """Get transaction by hash
        
        Args:
            tx_hash: Transaction hash to get
            
        Returns:
            Transaction data if found, None otherwise
        """
        try:
            result = await self.connection.get(
                index=self.transaction_index,
                id=tx_hash
            )
            return result['_source']
        except Exception as e:
            logger.error(f"Failed to get transaction: {str(e)}")
            return None

    async def search_transfers(self,
                             address: Optional[str] = None,
                             token: Optional[str] = None,
                             from_block: Optional[int] = None,
                             to_block: Optional[int] = None,
                             **kwargs) -> List[Dict[str, Any]]:
        """Search token transfers
        
        Args:
            address: Filter by address (from or to)
            token: Filter by token address
            from_block: Filter from block number
            to_block: Filter to block number
            **kwargs: Additional search parameters
            
        Returns:
            List of matching transfers
        """
        # Build query
        query: Dict[str, Any] = {"bool": {"must": []}}
        
        if address:
            query["bool"]["must"].append({
                "bool": {
                    "should": [
                        {"term": {"from": address}},
                        {"term": {"to": address}}
                    ]
                }
            })
            
        if token:
            query["bool"]["must"].append({"term": {"token": token}})
            
        if from_block is not None or to_block is not None:
            range_query: Dict[str, Any] = {"range": {"blockNumber": {}}}
            if from_block is not None:
                range_query["range"]["blockNumber"]["gte"] = from_block
            if to_block is not None:
                range_query["range"]["blockNumber"]["lte"] = to_block
            query["bool"]["must"].append(range_query)
            
        # Execute search
        try:
            result = await self.search(
                index=self.transfer_index,
                body={"query": query},
                **kwargs
            )
            # Extract hits
            return [hit["_source"] for hit in result["hits"]["hits"]]
        except Exception as e:
            logger.error(f"Failed to search transfers: {str(e)}")
            raise


    async def search_events(self,
                          contract: Optional[str] = None,
                          event_name: Optional[str] = None,
                          from_block: Optional[int] = None,
                          to_block: Optional[int] = None,
                          **kwargs) -> List[Dict[str, Any]]:
        """Search contract events

        Args:
            contract: Filter by contract address
            event_name: Filter by event name
            from_block: Filter from block number
            to_block: Filter to block number
            **kwargs: Additional search parameters
            
        Returns:
            List of matching events
        """
        # Build query
        query: Dict[str, Any] = {"bool": {"must": []}}
        
        if contract:
            query["bool"]["must"].append({"term": {"address": contract}})
            
        if event_name:
            query["bool"]["must"].append({"term": {"event": event_name}})
            
        if from_block is not None or to_block is not None:
            range_query: Dict[str, Any] = {"range": {"blockNumber": {}}}
            if from_block is not None:
                range_query["range"]["blockNumber"]["gte"] = from_block
            if to_block is not None:
                range_query["range"]["blockNumber"]["lte"] = to_block
            query["bool"]["must"].append(range_query)

        # Execute search
        try:
            result = await self.search(
                index=self.event_index,
                body={"query": query},
                **kwargs
            )
            # Extract hits
            return [hit["_source"] for hit in result["hits"]["hits"]]
        except Exception as e:
            logger.error(f"Failed to search events: {str(e)}")
            raise

    async def _get_blocks_brief_batch(self,
                                    items: List[BatchItem],
                                    fields: Optional[List[str]] = None,
                                    sort_order: str = "desc") -> List[Dict[str, Any]]:
        """Internal method to get a batch of blocks"""
        # Extract block ranges from batch items
        block_numbers = []
        for item in items:
            if item.method == "get_block":
                block_numbers.extend(item.args)
                
        if not block_numbers:
            return []
            
        start_block = min(block_numbers)
        end_block = max(block_numbers)
        
        batch_size = len(block_numbers)
        logger.info(f"Processing batch: blocks {start_block}-{end_block} (size: {batch_size})")
        
        query = {
            "query": {
                "bool": {
                    "must": [{
                        "range": {
                            "Number": {
                                "gte": start_block,
                                "lte": end_block
                            }
                        }
                    }]
                }
            },
            "size": end_block - start_block + 1,
            "sort": [
                {"Number": sort_order},
                {"Hash": sort_order}
            ],
            "_source": fields if fields is not None else [
                "Number",
                "Hash",
                "Timestamp",
                "GasLimit",
                "GasUsed",
                "BaseFee",
                "Difficulty",
                "Miner",
                "ExtraData",
                "TxnCount",
                "BlobGasUsed",
                "ExcessBlobGas"
            ]
        }
        try:
            start_time = time.time()
            result = await self.execute(
                query=query,
                params={"index": self.block_index}
            )
            hits = [hit["_source"] for hit in result["hits"]["hits"]]
            duration = time.time() - start_time
            logger.info(f"Batch completed: {len(hits)} blocks retrieved in {duration:.2f}s (rate: {len(hits)/duration:.1f} blocks/s)")
            return hits
        except Exception as e:
            logger.error(f"Failed to get blocks batch {start_block}-{end_block}: {str(e)}")
            raise

    async def get_blocks_brief(self, 
                             start_block: Optional[int] = None,
                             end_block: Optional[int] = None,
                             limit: int = 2000,
                             sort_order: str = "desc",
                             fields: Optional[List[str]] = None,
                             batch_size: int = 2000,
                             max_concurrent: int = 5) -> List[Dict[str, Any]]:
        """Get brief information about blocks with automatic batching and concurrency
        
        Args:
            start_block: Optional start block number (inclusive)
            end_block: Optional end block number (inclusive)
            limit: Maximum number of blocks to return when range not specified
            sort_order: Sort order for blocks ("asc" or "desc")
            fields: Optional list of fields to return. If None, returns default fields
            batch_size: Number of blocks per batch (default: 2000)
            max_concurrent: Maximum number of concurrent batches (default: 5)
            
        Returns:
            List of block summaries containing requested fields
        """
        # If no range specified, use limit
        if start_block is None or end_block is None:
            size = min(limit, 10000)
            start = start_block or 0
            end = end_block or (start + size - 1)
        else:
            start = start_block
            end = end_block
            
        total_blocks = end - start + 1
        num_batches = (total_blocks + batch_size - 1) // batch_size
        logger.info(f"Starting block retrieval: {total_blocks} blocks in {num_batches} batches")
        logger.info(f"Batch size: {batch_size}, Max concurrent: {max_concurrent}")
        
        # Create batch items
        items = []
        for block_num in range(start, end + 1):
            items.append(BatchItem(
                method="get_block",
                args=[block_num],
                kwargs={}
            ))
        
        # Initialize batch executor
        start_time = time.time()
        executor = BatchExecutor(
            lambda batch: self._get_blocks_brief_batch(batch, fields, sort_order)
        )
        
        # Execute batches
        results = await executor.execute_batch(items, batch_size, max_concurrent)
        
        # Log final stats
        duration = time.time() - start_time
        blocks_retrieved = len(results)
        logger.info(f"Retrieval completed: {blocks_retrieved} blocks in {duration:.2f}s")
        logger.info(f"Overall rate: {blocks_retrieved/duration:.1f} blocks/s")
        
        # Sort results if needed
        if results:
            if sort_order == "desc":
                results.sort(key=lambda x: x["Number"], reverse=True)
            else:
                results.sort(key=lambda x: x["Number"])
            
        return results

    async def _build_connection_string(self) -> str:
        """Build connection string for OpenSearch"""
        host = self.db_config.get('host')
        port = self.db_config.get('port')
        
        if not host:
            raise ValueError("OpenSearch host not found in config")
            
        # Parse host into components
        if '://' in host:
            scheme, host = host.split('://')
        else:
            scheme = 'http'
            
        if ':' in host:
            host, port = host.split(':')
            port = int(port)
        elif port:
            port = int(port)
        else:
            port = 9200
            
        return f"{scheme}://{host}:{port}"

    async def _create_connection(self) -> AsyncOpenSearch:
        """Create OpenSearch connection"""
        # Get credentials from database config
        username = self.db_config.get('username')
        password = self.db_config.get('password')
        
        # Parse connection string components
        if '://' in self.connection_string:
            scheme, rest = self.connection_string.split('://')
            host = rest.split(':')[0]
            port = int(rest.split(':')[1])
        else:
            scheme = 'http'
            host = self.connection_string.split(':')[0]
            port = int(self.connection_string.split(':')[1])
        
        # logger.debug(f"Connecting to OpenSearch at {scheme}://{host}:{port}")
        # logger.debug(f"Using credentials: {bool(username)}")
        
        # Create OpenSearch client
        client = AsyncOpenSearch(
            hosts=[{'host': host, 'port': port}],
            use_ssl=scheme == 'https',
            verify_certs=False,  # Disable SSL verification for now
            ssl_show_warn=False,
            http_auth=(username, password) if username and password else None,
            timeout=self.db_config.get('timeout', 30),
            maxsize=self.db_config.get('max_concurrent', 20),
            http_compress=True,  # Enable compression for better performance
            sniff_on_start=False,
            sniff_on_connection_fail=False,
            sniffer_timeout=None,
        )
        
        # Test connection
        try:
            info = await client.info()
            logger.info("Successfully connected to OpenSearch cluster: %s", info.get('cluster_name'))
            return client
        except Exception as e:
            logger.error("Failed to connect to OpenSearch: %s", str(e))
            raise

    async def _close_connection(self) -> None:
        """Close OpenSearch connection"""
        if self._connection:
            await self._connection.close()

    async def execute(self, query: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a query
        
        Args:
            query: Query dictionary
            params: Query parameters
            
        Returns:
            Query results
        """
        if not self.is_connected:
            await self.setup()

        # await self.apply_rate_limit('request')
        try:
            res = await self._connection.search(body=query, **params if params else {})
            return res
        except Exception as e:
            logger.error(f"Failed to execute query: {str(e)}")
            raise

    async def execute_many(self, queries: List[Dict[str, Any]], params: Optional[List[Dict[str, Any]]] = None) -> List[Any]:
        """Execute multiple queries
        
        Args:
            queries: List of query dictionaries
            params: List of query parameters
            
        Returns:
            List of query results
        """
        if not self.is_connected:
            await self.setup()
            
        results = []
        for i, query in enumerate(queries):
            query_params = params[i] if params else None
            try:
                results.append(await self.execute(query, query_params))
            except Exception as e:
                logger.error(f"Failed to execute query {i}: {str(e)}")
                raise
        return results

    async def begin_transaction(self) -> None:
        """Begin transaction - OpenSearch doesn't support transactions"""
        pass

    async def commit(self) -> None:
        """Commit transaction - OpenSearch doesn't support transactions"""
        pass

    async def rollback(self) -> None:
        """Rollback transaction - OpenSearch doesn't support transactions"""
        pass

    def _get_create_table_query(self, table_name: str, columns: Dict[str, Any]) -> Dict[str, Any]:
        """Get create table query - For OpenSearch this is create index
        
        Args:
            table_name: Name of index to create
            columns: Column definitions as mapping
            
        Returns:
            Create index body
        """
        return {
            "mappings": {
                "properties": columns
            }
        }

    def _get_insert_query(self, table_name: str, values: Dict[str, Any]) -> Dict[str, Any]:
        """Get insert query - For OpenSearch this is index document
        
        Args:
            table_name: Name of index
            values: Document data
            
        Returns:
            Index document body
        """
        return values

    async def _first_interaction_batch(self,
                                    to_addresses: List[str], index: str = "eth_block") -> Dict:
        """Search for first interactions with specified 'to' addresses.
        
        Args:
            to_addresses: List of 'to' addresses to search for
            index: OpenSearch index to search in
            
        Returns:
            Dict containing the search results for this batch
        """
        query = {
            "size": 1,
            "_source": {
                "includes": ["Number"]
            },
            "query": {
                "nested": {
                    "path": "Transactions",
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "term": {
                                        "Transactions.ToAddress": to_addresses[0]
                                    }
                                }
                            ]
                        }
                    },
                    "inner_hits": {
                        "name": "earliest_txn",
                        "size": 1,
                        "_source": ["Transactions.Hash"],
                        "sort": [
                            {
                                "Transactions.TxnIndex": {
                                    "order": "asc"
                                }
                            }
                        ]
                    }
                }
            },
            "sort": [
                {
                    "Number": { 
                        "order": "asc"
                    }
                }
            ]
        }
        
        try:
            response = await self.execute(query=query, params={"index": index})
            return response
        except Exception as e:
            logger.error(f"Error searching first interaction batch: {str(e)}")
            return None

    async def first_interaction_batch(self, to_addresses: List[str], index: str = "eth_block") -> Dict[str, Dict[str, Any]]:
        """Search for first interactions with specified 'to' addresses efficiently.
        
        Args:
            to_addresses: List of 'to' addresses to search for
            index: OpenSearch index to search in
            
        Returns:
            Dict mapping addresses to their first transaction details including:
            - first_tx: Hash of the first transaction (if any)
            - first_tx_block: Block number of the first transaction (if any)
        """
        to_addresses = [addr.lower() for addr in to_addresses]
        
        # Process addresses one by one for accuracy
        result = {}
        for addr in to_addresses:
            try:
                response = await self._first_interaction_batch([addr])
                addr_result = {
                    'first_tx': None,
                    'first_tx_block': None
                }
                
                if response and response.get('hits', {}).get('hits'):
                    first_hit = response['hits']['hits'][0]
                    block_number = first_hit['_source'].get('Number')
                    
                    if 'inner_hits' in first_hit:
                        inner_hits = first_hit['inner_hits']['earliest_txn']['hits']['hits']
                        if inner_hits:
                            earliest_tx = inner_hits[0]['_source']
                            tx_hash = earliest_tx.get('Hash')
                            addr_result['first_tx'] = tx_hash
                            addr_result['first_tx_block'] = block_number
                            
                            # logger.debug(f"Found first interaction for {addr}: tx={tx_hash} block={block_number}")
                        
                result[addr] = addr_result
                
            except Exception as e:
                logger.error(f"Error processing address {addr}: {str(e)}")
                result[addr] = {
                    'first_tx': None,
                    'first_tx_block': None
                }
                
        return result
    

    async def _first_sent_transaction_batch(self,
                                    from_addresses: List[str], index: str = "eth_block") -> Dict:
        """Search for first sent transactions with specified 'from' addresses efficiently.
        
        Args:
            from_addresses: List of 'from' addresses to search for
            index: OpenSearch index to search in
            
        Returns:
            Dict containing the search results for this batch
        """
        query = {
            "size": 1,
            "_source": {
                "includes": ["Number"]
            },
            "query": {
                "nested": {
                    "path": "Transactions",
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "term": {
                                        "Transactions.FromAddress": from_addresses[0]
                                    }
                                }
                            ]
                        }
                    },
                    "inner_hits": {
                        "name": "earliest_txn",
                        "size": 1,
                        "_source": ["Transactions.Hash"],
                        "sort": [
                            {
                                "Transactions.TxnIndex": {
                                    "order": "asc"
                                }
                            }
                        ]
                    }
                }
            },
            "sort": [
                {
                    "Number": { 
                        "order": "asc"
                    }
                }
            ]
        }
        
        try:
            response = await self.execute(query=query, params={"index": index})
            return response
        except Exception as e:
            logger.error(f"Error searching first interaction batch: {str(e)}")
            return None


    @file_cache(namespace="first_txs", ttl=3600*24*7)  # Cache for 7 days
    async def first_sent_transaction_batch(self, from_addresses: List[str], index: str = "eth_block") -> Dict[str, Dict[str, Any]]:
        """Search for first sent transactions with specified 'from' addresses efficiently.
        
        Args:
            from_addresses: List of 'from' addresses to search for
            index: OpenSearch index to search in
            
        Returns:
            Dict mapping addresses to their first transaction details including:
            - first_tx: Hash of the first transaction (if any)
            - first_tx_block: Block number of the first transaction (if any)
        """
        from_addresses = [addr.lower() for addr in from_addresses]
        
        # Process addresses one by one for accuracy
        result = {}
        for addr in from_addresses:
            try:
                response = await self._first_sent_transaction_batch([addr], index)
                addr_result = {
                    'first_tx': None,
                    'first_tx_block': None
                }
                
                if response and response.get('hits', {}).get('hits'):
                    first_hit = response['hits']['hits'][0]
                    block_number = first_hit['_source'].get('Number')
                    
                    if 'inner_hits' in first_hit:
                        inner_hits = first_hit['inner_hits']['earliest_txn']['hits']['hits']
                        if inner_hits:
                            earliest_tx = inner_hits[0]['_source']
                            tx_hash = earliest_tx.get('Hash')
                            addr_result['first_tx'] = tx_hash
                            addr_result['first_tx_block'] = block_number
                            
                            # logger.debug(f"Found first interaction for {addr}: tx={tx_hash} block={block_number}")
                        
                result[addr] = addr_result
                
            except Exception as e:
                logger.error(f"Error processing address {addr}: {str(e)}")
                result[addr] = {
                    'first_tx': None,
                    'first_tx_block': None
                }
                
        return result

    @file_cache(namespace="sent_tx_count", ttl=3600*24*7)  #
    async def search_sent_transaction_count_batch(self, from_addresses: List[str], index: str = "eth_block") -> Dict[str, Dict]:
        """
        Search for interactions with specified addresses efficiently.
        
        Args:
            from_addresses: List of addresses to search for
            index: OpenSearch index to search in
            
        Returns:
            Dict mapping addresses to their interaction statistics including:
            - totalTxCount: Total number of transactions
            - totalMethodCount: Number of unique methods called
            - totalDCounterpartyCount: Number of unique counterparties
        """
        start_time = time.time()
        from_addresses = [addr.lower() for addr in from_addresses]
        
        # Execute the search query
        response = await self._search_sent_transaction_count_batch(from_addresses, index)
        if not response:
            logger.error("Failed to get response from _search_sent_transaction_count_batch")
            return {addr: {'totalTxCount': 0, 'totalMethodCount': 0, 'totalDCounterpartyCount': 0} for addr in from_addresses}
        
        result = {}
        if 'aggregations' in response:
            transactions = response['aggregations'].get('transactions', {})
            filter_toAddress = transactions.get('filter_toAddress', {})
            buckets = filter_toAddress.get('fromAddress_buckets', {}).get('buckets', [])
            
            for bucket in buckets:
                address = bucket['key'].lower()
                result[address] = {
                    'totalTxCount': bucket['totalTxCount']['value'],
                    'totalMethodCount': bucket['distinct_method_count']['value'],
                    'totalDCounterpartyCount': bucket['distinct_counterparty']['value']
                }
        
        # Handle missing addresses with default values
        for addr in from_addresses:
            if addr not in result:
                result[addr] = {
                    'totalTxCount': 0,
                    'totalMethodCount': 0,
                    'totalDCounterpartyCount': 0
                }
        
        # print(f"Finished processing {len(result)} addresses in {time.time() - start_time:.2f}s")
        return result

    async def _search_sent_transaction_count_batch(self, from_addresses: List[str], index: str) -> Dict:
        """
        Search for interactions with specified addresses efficiently.
        
        Args:
            from_addresses: List of addresses to search for
            index: OpenSearch index to search in
            
        Returns:
            Dict containing the search results for this batch
        """
        query = {
            "size": 0,
            "query": {
                "nested": {
                    "path": "Transactions",
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "terms": {
                                        "Transactions.FromAddress": from_addresses
                                    }
                                },
                                {
                                    "term": {
                                        "Transactions.Status": True
                                    }
                                }
                            ]
                        }
                    }
                }
            },
            "aggs": {
                "transactions": {
                    "nested": {
                        "path": "Transactions"
                    },
                    "aggs": {
                        "filter_toAddress": {
                            "filter": {
                                "bool": {
                                    "must": [
                                        {
                                            "terms": {
                                                "Transactions.FromAddress": from_addresses
                                            }
                                        },
                                        {
                                            "term": {
                                                "Transactions.Status": True
                                            }
                                        }
                                    ]
                                }
                            },
                            "aggs": {
                                "fromAddress_buckets": {
                                    "terms": {
                                        "field": "Transactions.FromAddress",
                                        "size": len(from_addresses)
                                    },
                                    "aggs": {
                                        "totalTxCount": {
                                            "value_count": {
                                                "field": "Transactions.Hash"
                                            }
                                        },
                                        "distinct_method_count": {
                                            "cardinality": {
                                                "field": "Transactions.CallFunction"
                                            }
                                        },
                                        "distinct_counterparty": {
                                            "cardinality": {
                                                "field": "Transactions.ToAddress"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        try:
            # Direct search without scrolling
            response = await self.execute(query=query, params={"index": index})
            
            # Return results directly
            return response

        except Exception as e:
            logger.error(f"Error _searching interactions batch: {str(e)}")
            return None

    async def _interactions_count_batch(self,
                                    contract_addresses: List[str], index: str) -> Dict:
        """Search for interactions with specified contract addresses efficiently.
        
        Args:
            contract_addresses: List of contract addresses to search for
            index: OpenSearch index to search in
            
        Returns:
            Dict containing the search results for this batch
        """
        query = {
            "size": 0,
            "query": {
                "nested": {
                    "path": "Transactions",
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "terms": {
                                        "Transactions.ToAddress": contract_addresses
                                    }
                                },
                                {
                                    "term": {
                                        "Transactions.Status": True
                                    }
                                }
                            ]
                        }
                    },
                    "inner_hits": {
                        "name": "earliest_txn",
                        "size": 1,
                        "_source": ["Transactions.Hash"],
                        "sort": [
                            {
                                "Transactions.TxnIndex": {
                                    "order": "asc"
                                }
                            }
                        ]
                    }
                }
            },
            "aggs": {
                "transactions": {
                    "nested": {
                        "path": "Transactions"
                    },
                    "aggs": {
                        "filter_fromAddress": {
                            "filter": {
                                "bool": {
                                    "must": [
                                        {
                                            "terms": {
                                                "Transactions.ToAddress": contract_addresses
                                            }
                                        },
                                        {
                                            "term": {
                                                "Transactions.Status": True
                                            }
                                        }
                                    ]
                                }
                            },
                            "aggs": {
                                "toAddress_buckets": {
                                    "terms": {
                                        "field": "Transactions.ToAddress",
                                        "size": len(contract_addresses)
                                    },
                                    "aggs": {
                                        "totalTxCount": {
                                            "value_count": {
                                                "field": "Transactions.Hash"
                                            }
                                        },
                                        "distinct_method_count": {
                                            "cardinality": {
                                                "field": "Transactions.CallFunction"
                                            }
                                        },
                                        "distinct_counterparty": {
                                            "cardinality": {
                                                "field": "Transactions.FromAddress"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        try:
            response = await self.execute(
                query=query,
                params={"index": index}
            )
            return response
        except Exception as e:
            logger.error(f"Error searching interactions batch: {str(e)}")
            return None

    async def interactions_count_batch(self, contract_addresses: List[str], index: str = "eth_block") -> Dict[str, Dict]:
        """Search for interactions with specified contract addresses efficiently.
        
        Args:
            contract_addresses: List of contract addresses to search for
            index: OpenSearch index to search in
            
        Returns:
            Dict mapping addresses to their interaction statistics including:
            - totalTxCount: Total number of transactions
            - totalMethodCount: Number of unique methods called
            - totalDCounterpartyCount: Number of unique counterparties
        """
        contract_addresses = [addr.lower() for addr in contract_addresses]
        
        # Process addresses in batches
        result = {}
        batch_size = 50  # Process 50 addresses at a time
        
        for i in range(0, len(contract_addresses), batch_size):
            batch = contract_addresses[i:i + batch_size]
            try:
                response = await self._interactions_count_batch(batch, index)
                
                if response and 'aggregations' in response:
                    transactions = response['aggregations'].get('transactions', {})
                    filter_fromAddress = transactions.get('filter_fromAddress', {})
                    buckets = filter_fromAddress.get('toAddress_buckets', {}).get('buckets', [])
                    
                    for bucket in buckets:
                        address = bucket['key']
                        result[address] = {
                            'totalTxCount': bucket['totalTxCount']['value'],
                            'totalMethodCount': bucket['distinct_method_count']['value'],
                            'totalDCounterpartyCount': bucket['distinct_counterparty']['value']
                        }
                        # logger.debug(f"Found stats for {address}: {result[address]}")
                        
            except Exception as e:
                logger.error(f"Error processing batch {i}-{i+batch_size}: {str(e)}")
                # Set default values for failed addresses
                for addr in batch:
                    if addr not in result:
                        result[addr] = {
                            'totalTxCount': 0,
                            'totalMethodCount': 0,
                            'totalDCounterpartyCount': 0
                        }
                
        # Handle any missing addresses
        for addr in contract_addresses:
            if addr not in result:
                result[addr] = {
                    'totalTxCount': 0,
                    'totalMethodCount': 0,
                    'totalDCounterpartyCount': 0
                }
                
        return result

    async def fetch_all_txhashes_from(self, address: str, index: str = "eth_block") -> List[str]:
        """Search for all transaction hashes where the given address is involved.
        
        Args:
            address: The address to search for (as sender)
            index: OpenSearch index to search in (default: "eth_block")
            
        Returns:
            List[str]: List of transaction hashes from the address
        """
        size = 10000  # Maximum number of results to return
        query = {
            "size": size,
            "_source": ["Transactions.Hash"],
            "query": {
                "nested": {
                    "path": "Transactions",
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "term": {
                                        "Transactions.FromAddress": address.lower()
                                    }
                                },
                                {
                                    "term": {
                                        "Transactions.Status": True
                                    }
                                }
                            ]
                        }
                    },
                    "inner_hits": {
                        "size": size,
                        "_source": ["Transactions.Hash"]
                    }
                }
            }
        }
        
        tx_hashes = []
        try:
            response = await self.execute(
                query=query,
                params={"index": index}
            )
            
            if response and "hits" in response and "hits" in response["hits"]:
                for block_hit in response["hits"]["hits"]:
                    block_number = block_hit['_id']
                    
                    # Process inner hits (transactions)
                    if 'inner_hits' in block_hit and "Transactions" in block_hit["inner_hits"]:
                        for tx in block_hit["inner_hits"]["Transactions"]["hits"]["hits"]:
                            if "Hash" in tx["_source"]:
                                tx_hashes.append(tx["_source"]["Hash"])
            
            logger.info(f"Found {len(tx_hashes)} transactions for address {address}")
            return tx_hashes

        except Exception as e:
            logger.error(f"Error searching transaction hashes for address {address}: {str(e)}")
            return []

    async def fetch_all_txhashes_to(self, address: str, index: str = "eth_block") -> List[str]:
        """Search for all transaction hashes where the given address is involved.
        
        Args:
            address: The address to search for (as sender)
            index: OpenSearch index to search in (default: "eth_block")
            
        Returns:
            List[str]: List of transaction hashes from the address
        """
        size = 10000  # Maximum number of results to return
        query = {
            "size": size,
            "_source": ["Transactions.Hash"],
            "query": {
                "nested": {
                    "path": "Transactions",
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "term": {
                                        "Transactions.ToAddress": address.lower()
                                    }
                                },
                                {
                                    "term": {
                                        "Transactions.Status": True
                                    }
                                }
                            ]
                        }
                    },
                    "inner_hits": {
                        "size": size,
                        "_source": ["Transactions.Hash"]
                    }
                }
            }
        }
        
        tx_hashes = []
        try:
            response = await self.execute(
                query=query,
                params={"index": index}
            )
            
            if response and "hits" in response and "hits" in response["hits"]:
                for block_hit in response["hits"]["hits"]:
                    block_number = block_hit['_id']
                    
                    # Process inner hits (transactions)
                    if 'inner_hits' in block_hit and "Transactions" in block_hit["inner_hits"]:
                        for tx in block_hit["inner_hits"]["Transactions"]["hits"]["hits"]:
                            if "Hash" in tx["_source"]:
                                tx_hashes.append(tx["_source"]["Hash"])
            
            logger.info(f"Found {len(tx_hashes)} transactions for address {address}")
            return tx_hashes

        except Exception as e:
            logger.error(f"Error searching transaction hashes for address {address}: {str(e)}")
            return []

    async def fetch_created_contracts(self, creator_address: Optional[str] = None, 
                                    start_block: Optional[int] = None,
                                    end_block: Optional[int] = None,
                                    index: str = "eth_block") -> List[Dict[str, Any]]:
        """Search for all contracts created within the specified block range or by a specific creator.
        
        Args:
            creator_address: Optional address that created the contracts
            start_block: Optional start block number (inclusive)
            end_block: Optional end block number (inclusive)
            index: OpenSearch index to search in (default: "eth_block")
            
        Returns:
            List[Dict[str, Any]]: List of contract creation details containing:
                - contract_address: The address of the created contract
                - creator_address: Address that created the contract
                - creation_tx: Hash of the creation transaction
                - block_number: Block number where contract was created
                - timestamp: Block timestamp when contract was created
        """
        size = end_block-start_block+1 if start_block and end_block else 1000
        query = {
            "size": size,
            "_source": [
                "Number",
                "Timestamp"
            ],
            "query": {
                "bool": {
                    "must": [
                        {
                            "nested": {
                                "path": "Transactions",
                                "query": {
                                    "bool": {
                                        "must": [
                                            {
                                                "exists": {
                                                    "field": "Transactions.Created.Address"
                                                }
                                            },
                                            {
                                                "term": {
                                                    "Transactions.Status": True
                                                }
                                            }
                                        ]
                                    }
                                },
                                "inner_hits": {
                                    "size": 2000,
                                    "_source": [
                                        "Transactions.Hash",
                                        "Transactions.FromAddress",
                                        "Transactions.Created.Address"
                                    ]
                                }
                            }
                        }
                    ]
                }
            }
        }

        # Add block range filter if specified
        if start_block is not None or end_block is not None:
            range_filter = {"range": {"Number": {}}}
            if start_block is not None:
                range_filter["range"]["Number"]["gte"] = start_block
            if end_block is not None:
                range_filter["range"]["Number"]["lte"] = end_block
            query["query"]["bool"]["must"].append(range_filter)

        # Add creator address filter if specified
        if creator_address:
            creator_filter = {
                "term": {
                    "Transactions.FromAddress": creator_address.lower()
                }
            }
            query["query"]["bool"]["must"][0]["nested"]["query"]["bool"]["must"].append(creator_filter)

        contracts = []
        try:
            # Search with rate limiting
            response = await self.execute(
                query=query,
                params={"index": index}
            )
            
            if response and "hits" in response and "hits" in response["hits"]:
                for block_hit in response["hits"]["hits"]:
                    block_number = block_hit['_source'].get('Number')
                    timestamp = block_hit['_source'].get("Timestamp")
                    
                    if "inner_hits" in block_hit and "Transactions" in block_hit["inner_hits"]:
                        for tx in block_hit["inner_hits"]["Transactions"]["hits"]["hits"]:
                            if "_source" in tx:
                                source = tx["_source"]
                                tx_hash = source.get("Hash")
                                from_address = source.get("FromAddress")
                                created = source.get("Created", [])
                                
                                for contract in created:
                                    if "Address" in contract:
                                        contracts.append({
                                            "contract_address": contract["Address"],
                                            "creator_address": from_address,
                                            "creation_tx": tx_hash,
                                            "block_number": block_number,
                                            "timestamp": timestamp
                                        })
            
            logger.info(f"Found {len(contracts)} contracts {f'created by {creator_address}' if creator_address else 'in total'}")
            return contracts

        except Exception as e:
            logger.error(f"Error searching contracts: {str(e)}")
            return []

    async def search_transaction_batch(self, batch_hashes: List[str], index: str = "eth_block", fields: Optional[List[str]] = None) -> Dict[str, Dict]:
        """Search for a batch of transaction hashes with rate limiting and scroll support.
        Uses parallel processing for better performance.
        
        Args:
            batch_hashes: List of transaction hashes to search for
            index: OpenSearch index to search in (default: "eth_block")
            fields: Optional list of additional transaction fields to fetch.
                   Default fields (always included):
                   - Hash
                   - Block
                   - Timestamp
                   - FromAddress (from)
                   - ToAddress (to)
                   - Value (value)
                   - GasPrice (gasprice)
                   - GasUsed (gasused)
                   - CallFunction (callfunc)
                   - CallParameter (callparam)
        
        Returns:
            Dict mapping transaction hashes to their data:
            {
                "0x123...": {
                    "Hash": "0x123...",
                    "Timestamp": "2022-10-24T06:58:23Z",
                    "Block": "123456",
                    "FromAddress": "0x...",
                    "ToAddress": "0x...",
                    "Value": "0",
                    "GasPrice": "0",
                    "GasUsed": "0",
                    "CallFunction": "transfer",
                    "CallParameter": [...],
                    ...additional fields if specified...
                },
                ...
            }
        """
        # Create batch items for parallel processing
        batches = [batch_hashes[i:i + self.batch_size] for i in range(0, len(batch_hashes), self.batch_size)]
        batch_items = [
            BatchItem(
                method="_search_batch_txs",
                args=(batch,),
                kwargs={
                    'index': index,
                    'fields': fields
                }
            )
            for batch in batches
        ]
        
        # Execute batches using batch executor
        await self.batch_executor.execute_batch(
            items=batch_items,
            batch_size=self.batch_size,
            max_concurrent=self.max_concurrent
        )
        
        # Process results
        tx_data = {}
        for item in batch_items:
            if not item.result:
                logger.error(f"Error processing batch: {item.error}")
                continue
                
            result = item.result
            # import json
            # print(json.dumps(result, indent=2))
            if result and 'hits' in result and 'hits' in result['hits']:
                for block_hit in result['hits']['hits']:
                    block_timestamp = block_hit['_source'].get("Timestamp")
                    block_number = block_hit['_id']
                    # Process inner hits (transactions)
                    if 'inner_hits' in block_hit and "Transactions" in block_hit["inner_hits"]:
                        tx_hits = block_hit["inner_hits"]["Transactions"]["hits"]["hits"]
                        for tx_hit in tx_hits:
                            if "_source" in tx_hit:
                                tx = tx_hit["_source"]
                                if "Hash" in tx:
                                    tx["Block"] = block_number
                                    tx["Timestamp"] = block_timestamp
                                    tx_data[tx["Hash"]] = tx

        return tx_data

    async def _execute_batch(self, items: List[BatchItem]) -> List[Any]:
        """Execute a batch of transaction search operations
        
        Args:
            items: List of batch items to execute
            
        Returns:
            List of results, one for each batch item
        """
        if not items:
            return []
            
        results = []
        # Process each batch item
        for item in items:
            try:
                # Call the method specified in the batch item
                method = getattr(self, item.method)
                result = await method(*item.args, **item.kwargs)
                item.result = result
                results.append(result)
            except Exception as e:
                logger.error(f"Error executing batch: {str(e)}")
                item.error = str(e)
                results.append(None)
                
        return results

    async def _search_batch_txs(self, hashes: List[str], index: str, fields: Optional[List[str]] = None) -> Dict:
        """Search for a single batch of transaction hashes efficiently.
        
        Args:
            hashes: List of transaction hashes to search for
            index: OpenSearch index to search in
            fields: Optional list of transaction fields to fetch. If None, fetches all default fields.
                   Fields should be specified without the "Transactions." prefix.
                   Example: ['Hash', 'FromAddress', 'ToAddress', 'Value']
        
        Returns:
            Dict containing the search results for this batch
        """
        # Default fields to fetch if none specified
        default_fields = [
            'Hash',
            'FromAddress',
            'ToAddress',
            'Value',
            'Status',
            'GasPrice',
            'GasUsed',
            'Logs',
            'CallFunction',
            'CallParameter',
            'BalanceWrite'
        ]
        
        # Use specified fields or defaults
        source_fields = fields if fields is not None else default_fields
        # Add 'Transactions.' prefix to each field
        source_fields = [f"Transactions.{field}" for field in source_fields]

        query = {
            "size": len(hashes),
            "_source": ["Timestamp"],
            "query": {
                "nested": {
                    "path": "Transactions",
                    "query": {
                        "terms": {
                            "Transactions.Hash": hashes
                        }
                    },
                    "inner_hits": {
                        "_source": source_fields,
                        "size": len(hashes)
                    }
                }
            }
        }
        # import json
        # print(json.dumps(query, indent=2))

        try:
            # Use base client's search method which handles rate limiting
            response = await self.search(index=index, body=query)
            # import json
            # print(json.dumps(response, indent=2))
            return {
                'hits': {
                    'hits': response['hits']['hits'],
                    'total': len(response['hits']['hits'])
                }
            }

        except Exception as e:
            logger.error(f"Error searching transaction batch: {str(e)}")
            raise

    async def get_erc20_transfers(self, 
                                token_address: Optional[str] = None,
                                from_address: Optional[str] = None,
                                to_address: Optional[str] = None,
                                start_block: Optional[int] = None,
                                end_block: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get ERC20 transfer events with various filters.
        
        Args:
            token_address: Optional token contract address to filter transfers for
            from_address: Optional address to filter transfers from
            to_address: Optional address to filter transfers to
            start_block: Optional starting block number
            end_block: Optional ending block number
            
        Returns:
            List of transfer events, each containing:
            {
                'block_number': int,
                'transaction_hash': str,
                'log_index': int,
                'token_address': str,
                'from_address': str,
                'to_address': str,
                'amount': str,  # Decimal string to handle large numbers
                'tx_from': str,  # Transaction sender
                'tx_to': str,    # Transaction recipient
            }
        """
        size = 50000  # Increased size limit
        # Build query filters
        must_conditions = [
            # Match Transfer event signature in any topic position
            {
                "nested": {
                    "path": "Transactions.Logs",
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "terms": {
                                        "Transactions.Logs.Topics": [
                                            "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        ]
        
        # Add optional filters
        if token_address:
            must_conditions[0]["nested"]["query"]["bool"]["must"].append({
                "term": {
                    "Transactions.Logs.Address": token_address.lower()
                }
            })
            
        if from_address:
            # Match from_address in any topic position
            must_conditions[0]["nested"]["query"]["bool"]["must"][0]["terms"]["Transactions.Logs.Topics"].append(
                "0x" + from_address[2:].lower()
            )
            if to_address:
                must_conditions[0]["nested"]["query"]["bool"]["must"][0]["terms"]["Transactions.Logs.Topics"].append(
                    "0x" + to_address[2:].lower()
                )
            
        if start_block is not None:
            must_conditions.append({
                "range": {
                    "Number": {
                        "gte": start_block
                    }
                }
            })
            
        if end_block is not None:
            must_conditions.append({
                "range": {
                    "Number": {
                        "lte": end_block
                    }
                }
            })
            
        # Build the full query
        query = {
            "size": size,
            "_source": ["Number", "Transactions"],
            "query": {
                "bool": {
                    "must": must_conditions
                }
            },
            "sort": [
                {"Number": "asc"}
            ]
        }
        
        try:
            # Search with rate limiting
            response = await self.search(index="eth_block", body=query)
            
            # Process results
            transfers = []
            for block_hit in response.get('hits', {}).get('hits', []):
                block_number = block_hit['_source'].get('Number')
                if not block_number:
                    continue
                    
                transactions = block_hit['_source'].get('Transactions', [])
                for tx in transactions:
                    logs = tx.get('Logs', [])
                    tx_hash = tx.get('Hash', '').lower()
                    tx_from = tx.get('FromAddress', '').lower()
                    tx_to = tx.get('ToAddress', '').lower()
                    
                    for log_index, log in enumerate(logs):
                        try:
                            topics = log.get('Topics', [])
                            
                            # Skip non-transfer events or reverted transactions
                            if (not topics or 
                                topics[0] != "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef" or
                                log.get('Revert')):
                                continue
                                
                            # Skip if token address doesn't match
                            if token_address and log.get('Address', '').lower() != token_address.lower():
                                continue
                                
                            # Ensure we have enough topics for a transfer event
                            if len(topics) != 3:
                                continue
                            
                            # Extract transfer data
                            from_addr = '0x' + topics[1][-40:]  # Remove padding and add 0x prefix
                            to_addr = '0x' + topics[2][-40:]    # Remove padding and add 0x prefix
                            
                            # Skip if from/to addresses don't match filters
                            if from_address and from_addr.lower() != from_address.lower():
                                continue
                            if to_address and to_addr.lower() != to_address.lower():
                                continue

                            # Get amount from data field
                            amount_hex = log.get('Data', '0x0')
                            if amount_hex.startswith('0x'):
                                amount_hex = amount_hex[2:]
                            amount = int(amount_hex, 16)
                            
                            # Create transfer record
                            transfer = {
                                'block_number': block_number,
                                'transaction_hash': tx_hash,
                                'log_index': log_index,
                                'token_address': log.get('Address', '').lower(),
                                'from_address': from_addr.lower(),
                                'to_address': to_addr.lower(),
                                'amount': str(amount),  # Convert to string to handle large numbers
                                'tx_from': tx_from,
                                'tx_to': tx_to
                            }
                            
                            transfers.append(transfer)
                            
                        except Exception as e:
                            logger.error(f"Error processing transfer log: {e}")
                            continue
                        
            return transfers
            
        except Exception as e:
            logger.error(f"Error fetching ERC20 transfers: {e}")
            raise

    async def search_logs(self, start_block: int, end_block: int, 
                         event_topics: List[str], size: int = 1000, 
                         address: Optional[str] = None,
                         fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Search for logs in block data within a block range matching given topics.
        
        Args:
            start_block: Starting block number (inclusive)
            end_block: Ending block number (inclusive)
            event_topics: List of event topics to match
            size: Maximum number of results to return
            address: Optional contract address to filter logs
            fields: Optional list of fields to return in results. If None, returns all fields.
                   Available fields: block_number, block_time, transaction_hash, from_address,
                   to_address, txn_index, log_id, topics, data, address
        
        Returns:
            List[Dict[str, Any]]: List of matching log entries with block data
        """
        return await self.search_logs_batch(start_block, end_block, event_topics, size, [address], fields)

    async def search_logs_batch(self, start_block: int, end_block: int, 
                         event_topics: List[str], size: int = 1000, 
                         addresses: Optional[List[str]] = None,
                         fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Search for logs in block data within a block range matching given topics.
        
        Args:
            start_block: Starting block number (inclusive)
            end_block: Ending block number (inclusive)
            event_topics: List of event topics to match
            size: Maximum number of results to return
            addresses: Optional list of contract addresses to filter logs
            fields: Optional list of fields to return in results. If None, returns all fields.
                   Available fields: block_number, block_time, transaction_hash, from_address,
                   to_address, txn_index, log_id, topics, data, address
        
        Returns:
            List[Dict[str, Any]]: List of matching log entries with block data
        """
        must_conditions = [
            {"range": {"Number": {"gte": start_block, "lte": end_block}}}
        ]
        
        log_query = {
            "nested": {
                "path": "Transactions.Logs",
                "query": {
                    "bool": {
                        "must": [
                            {"terms": {"Transactions.Logs.Topics": event_topics}},
                            {"term": {"Transactions.Logs.Revert": False}}
                        ]
                    }
                },
                "inner_hits": {
                    "_source": True,
                    "size": size
                }
            }
        }
        # print(address)
        if addresses:
            log_query["nested"]["query"]["bool"]["must"].append(
                {"terms": {"Transactions.Logs.Address": [address.lower() for address in addresses]}}
            )
            
        must_conditions.append(log_query)
        
        query = {
            "query": {
                "bool": {
                    "must": must_conditions
                }
            },
            "size": size,
            "_source": [
                "Number",
                "Timestamp",
                "Transactions.Hash",
                "Transactions.Logs",
                "Transactions.GasLimit",
                "Transactions.FromAddress",
                "Transactions.ToAddress",
                "Transactions.TxnIndex",
                "Transactions.CallFunction"
            ],
            "sort": [{"Number": {"order": "asc"}}]
        }
        
        try:
            # import json
            # print(json.dumps(query, indent=2))
            response = await self.execute(query=query, params={"index": self.block_index})
            # print(response)
            hits = response['hits']['hits']

            # Process and format the results
            results = []
            for hit in hits:
                block_data = hit['_source']
                transactions = block_data.get('Transactions', [])
                inner_hits = hit['inner_hits']['Transactions.Logs']['hits']['hits']
                
                for inner_hit in inner_hits:
                    log_data = inner_hit['_source']
                    nested_path = inner_hit.get('_nested', {})
                    txn_offset = nested_path.get('offset', 0)
                    
                    # Get transaction data using the offset
                    txn_data = transactions[txn_offset] if txn_offset < len(transactions) else {}
                    
                    result = {}
                    all_fields = {
                        'block_number': block_data['Number'],
                        'block_time': block_data.get('Timestamp'),
                        'transaction_hash': txn_data.get('Hash'),
                        'from_address': txn_data.get('FromAddress'),
                        'to_address': txn_data.get('ToAddress'),
                        'txn_index': txn_data.get('TxnIndex'),
                        'method_id': txn_data.get('CallFunction'),
                        'log_id': log_data.get('Id'),
                        'topics': log_data['Topics'],
                        'data': log_data['Data'],
                        'address': log_data['Address']
                    }
                    
                    # If fields is specified, only include requested fields
                    if fields:
                        result = {field: all_fields[field] for field in fields if field in all_fields}
                    else:
                        result = all_fields
                        
                    results.append(result)
            
            # Sort by block number, transaction index, internal transaction index, and log ID
            return sorted(results, key=lambda x: (
                x['block_number'],
                x['txn_index'] if x['txn_index'] is not None else -1,
                x['log_id'] if x['log_id'] is not None else -1
            ))
            
        except Exception as e:
            logger.error(f"Error searching logs: {str(e)}")
            raise

    async def get_contract_creator_tx(self, contract_address: str) -> Optional[str]:
        """Get the transaction hash that created a contract.
        
        Args:
            contract_address: The contract address to look up
            
        Returns:
            Optional[str]: The transaction hash that created the contract, or None if not found
        """
        query = {
            "query": {
                "nested": {
                    "path": "Transactions.Contracts",
                    "query": {
                        "term": {
                            "Transactions.Contracts.Address": {
                                "value": contract_address.lower()
                            }
                        }
                    },
                    "inner_hits": {
                        "_source": True,
                        "size": 1
                    }
                }
            },
            "_source": ["Transactions"],
            "size": 1
        }
        
        try:
            response = await self.execute(query=query, params={"index": "eth_code_all"})
            hits = response['hits']['hits']
            
            if hits:
                inner_hits = hits[0]['inner_hits']['Transactions.Contracts']['hits']['hits']
                if inner_hits:
                    nested_path = inner_hits[0].get('_nested', {})
                    txn_offset = nested_path.get('offset', 0)
                    transactions = hits[0]['_source'].get('Transactions', [])
                    
                    if txn_offset < len(transactions):
                        return transactions[txn_offset].get('Hash')
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting contract creator tx: {str(e)}")
            return None