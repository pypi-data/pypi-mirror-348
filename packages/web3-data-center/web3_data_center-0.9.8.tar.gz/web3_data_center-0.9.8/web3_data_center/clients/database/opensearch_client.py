from typing import Any, Dict, Optional, List, Union
import logging
import asyncio
from opensearchpy import AsyncOpenSearch, OpenSearchException
from .base_database_client import BaseDatabaseClient
from ..batch.executor import BatchExecutor
from ..batch.types import BatchItem

logger = logging.getLogger(__name__)

class OpenSearchDatabaseClient(BaseDatabaseClient[AsyncOpenSearch]):
    """Client for interacting with OpenSearch as a database
    
    Features:
    - Connection pooling and management
    - Document indexing and search
    - Batch operations with automatic retries
    - Rate limiting and error handling
    """
    
    def __init__(self, config_path: str = "config.yml", db_name: str = "opensearch"):
        """Initialize OpenSearch database client"""
        # Initialize database client with db_name
        super().__init__(
            db_name=db_name,
            config_path=config_path
        )
        
        # Now validate the config
        self.validate_config()
        
        # Configure opensearch logging
        logging.getLogger('opensearch').setLevel(logging.WARNING)
        logging.getLogger('opensearch.transport').setLevel(logging.WARNING)
        logging.getLogger('opensearch.connection').setLevel(logging.WARNING)
        
        # Initialize batch executor
        self.batch_executor = BatchExecutor(self._execute_batch)
        self.batch_size = self.database_config.get('batch_size', 100)
        self.max_concurrent = self.database_config.get('max_concurrent', 20)
        
        # Initialize rate limiting
        self.setup_rate_limits()  # Initialize rate limiting dictionary first
        self.setup_rate_limit(
            'request',
            requests_per_second=self.database_config.get('rps', 100.0)
        )
        
    async def connect(self) -> AsyncOpenSearch:
        """Connect to OpenSearch database"""
        # Get credentials from database config
        username = self.database_config.get('username')
        password = self.database_config.get('password')
        
        # Get host and port from database config
        host = self.database_config.get('host')
        port = self.database_config.get('port')
        
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
            
        # logger.debug(f"Connecting to OpenSearch at {scheme}://{host}:{port}")
        # logger.debug(f"Using credentials: {bool(username)}")
        
        # Create OpenSearch client
        client = AsyncOpenSearch(
            hosts=[{'host': host, 'port': port}],
            use_ssl=scheme == 'https',
            verify_certs=False,  # Disable SSL verification for now
            ssl_show_warn=False,
            http_auth=(username, password) if username and password else None,
            timeout=self.database_config.get('timeout', 30),
            maxsize=self.database_config.get('max_concurrent', 20),
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
            
    async def close(self) -> None:
        """Close the OpenSearch connection"""
        if self.connection:
            await self.connection.close()
        await super().close()
        
    async def search(self,
                    index: str,
                    body: Dict[str, Any],
                    **kwargs) -> Dict[str, Any]:
        """Perform a search query
        
        Args:
            index: Index to search in
            body: Search query body
            **kwargs: Additional arguments for search
            
        Returns:
            Search results
        """
        await self.apply_rate_limit('request')
        return await self.connection.search(
            index=index,
            body=body,
            **kwargs
        )
        
    async def index(self,
                   index: str,
                   body: Dict[str, Any],
                   id: Optional[str] = None,
                   **kwargs) -> Dict[str, Any]:
        """Index a document
        
        Args:
            index: Index to add document to
            body: Document data
            id: Optional document ID
            **kwargs: Additional arguments for index operation
            
        Returns:
            Index operation result
        """
        await self.apply_rate_limit('request')
        return await self.connection.index(
            index=index,
            body=body,
            id=id,
            **kwargs
        )
        
    async def bulk(self,
                  body: List[Dict[str, Any]],
                  **kwargs) -> Dict[str, Any]:
        """Execute bulk operation
        
        Args:
            body: List of operations to execute
            **kwargs: Additional arguments for bulk operation
            
        Returns:
            Bulk operation result
        """
        await self.apply_rate_limit('request')
        return await self.connection.bulk(
            body=body,
            **kwargs
        )
        
    async def _execute_batch(self, items: List[BatchItem]) -> None:
        """Execute a batch of operations
        
        Args:
            items: List of batch items to execute
        """
        if not items:
            return
            
        operations = []
        for item in items:
            operations.extend([
                {'index': {'_index': item.data['index'], '_id': item.data.get('id')}},
                item.data['body']
            ])
            
        try:
            result = await self.bulk(body=operations)
            if result.get('errors'):
                # Handle failed operations
                for item, info in zip(items, result['items']):
                    if 'error' in info['index']:
                        item.set_error(info['index']['error'])
                    else:
                        item.set_result(info['index'])
            else:
                # All operations succeeded
                for item, info in zip(items, result['items']):
                    item.set_result(info['index'])
        except Exception as e:
            # Mark all items as failed
            for item in items:
                item.set_error(str(e))

    async def _build_connection_string(self) -> str:
        """Build connection string for OpenSearch"""
        host = self.database_config.get('host')
        port = self.database_config.get('port')
        
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
        return await self.connect()

    async def _close_connection(self) -> None:
        """Close OpenSearch connection"""
        if self.connection:
            await self.connection.close()

    async def execute(self, query: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a query
        
        Args:
            query: Query dictionary
            params: Query parameters
            
        Returns:
            Query results
        """
        await self.apply_rate_limit('request')
        return await self.connection.search(body=query, **params if params else {})

    async def execute_many(self, queries: List[Dict[str, Any]], params: Optional[List[Dict[str, Any]]] = None) -> List[Any]:
        """Execute multiple queries
        
        Args:
            queries: List of query dictionaries
            params: List of query parameters
            
        Returns:
            List of query results
        """
        results = []
        for i, query in enumerate(queries):
            query_params = params[i] if params else None
            results.append(await self.execute(query, query_params))
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

    def validate_config(self) -> None:
        """Validate database configuration"""
        super().validate_config()
