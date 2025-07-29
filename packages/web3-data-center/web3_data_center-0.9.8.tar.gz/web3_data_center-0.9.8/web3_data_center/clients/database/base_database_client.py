# web3_data_center/web3_data_center/clients/database/base_database_client.py
from typing import Dict, Any, List, Union, Optional, TypeVar, Generic
from abc import abstractmethod
import logging
import asyncio
from contextlib import asynccontextmanager
from ..base_client import BaseClient
from ..mixins import RateLimitMixin, BatchOperationMixin

logger = logging.getLogger(__name__)

T = TypeVar('T')  # Type for database records

class BaseDatabaseClient(BaseClient, RateLimitMixin, BatchOperationMixin[Dict[str, Any], T], Generic[T]):
    """Base class for database clients
    
    Provides common functionality for database operations:
    - Connection pooling
    - Transaction management
    - Query execution
    - Batch operations
    - Connection string management
    """
    
    def __init__(self,
                 db_name: str,
                 config_path: str = "config.yml",
                 pool_size: int = 5,
                 max_overflow: int = 10):
        """Initialize database client
        
        Args:
            db_name: Database name in config
            config_path: Path to config file
            pool_size: Initial size of the connection pool
            max_overflow: Maximum number of connections that can be created beyond pool_size
        """
        # Set attributes before validation
        self.db_name = db_name
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        
        # Initialize base client and mixins
        BaseClient.__init__(self, config_path)
        RateLimitMixin.__init__(self)
        BatchOperationMixin.__init__(self)
        
        # Validate and load database config
        self.validate_config()
        
        # Load database config
        db_config = self.get_section_config('database')
        if db_name not in db_config:
            raise KeyError(f"Database {db_name} not found in config")
            
        self.db_config = db_config[db_name]
        self.connection_string = self._build_connection_string()
        
        # Transaction management
        self._transaction_lock = asyncio.Lock()
        self._current_transaction = None
        
    def get_config_section(self) -> str:
        """Get configuration section name"""
        return 'database'
        
    def validate_config(self) -> None:
        """Validate database configuration"""
        if 'database' not in self.config:
            raise KeyError("Database section missing from config")
            
        db_config = self.config['database']
        if self.db_name not in db_config:
            raise KeyError(f"Database {self.db_name} not found in config")
            
        required_fields = ['type']
        for field in required_fields:
            if field not in db_config[self.db_name]:
                raise KeyError(f"Required field '{field}' missing from database config")
                
    @abstractmethod
    def _build_connection_string(self) -> str:
        """Build connection string from config
        
        Returns:
            Database connection string
        """
        pass
        
    @abstractmethod
    async def execute(self,
                     query: str,
                     parameters: Optional[Union[List[Any], Dict[str, Any]]] = None,
                     timeout: Optional[float] = None) -> List[T]:
        """Execute a database query
        
        Args:
            query: SQL query
            parameters: Query parameters
            timeout: Query timeout in seconds
            
        Returns:
            Query results
        """
        pass
        
    @abstractmethod
    async def execute_many(self,
                         query: str,
                         parameters: List[Union[List[Any], Dict[str, Any]]],
                         timeout: Optional[float] = None) -> None:
        """Execute same query with multiple sets of parameters
        
        Args:
            query: SQL query
            parameters: List of parameter sets
            timeout: Query timeout in seconds
        """
        pass
        
    @asynccontextmanager
    async def transaction(self):
        """Transaction context manager
        
        Provides transaction isolation for database operations.
        
        Yields:
            Transaction object
        """
        async with self._transaction_lock:
            try:
                self._current_transaction = await self.begin_transaction()
                yield self._current_transaction
                await self.commit()
            except Exception as e:
                await self.rollback()
                raise
            finally:
                self._current_transaction = None
                
    @abstractmethod
    async def begin_transaction(self):
        """Begin a new transaction"""
        pass
        
    @abstractmethod
    async def commit(self):
        """Commit the current transaction"""
        pass
        
    @abstractmethod
    async def rollback(self):
        """Rollback the current transaction"""
        pass
        
    async def _process_batch(self, batch: List[Dict[str, Any]]) -> List[T]:
        """Process a batch of records
        
        This implementation should be overridden by specific database clients
        to provide optimized batch processing.
        
        Args:
            batch: List of records to process
            
        Returns:
            List of processed records
        """
        results = []
        async with self.transaction():
            for record in batch:
                result = await self.execute(
                    self._get_insert_query(),
                    parameters=record
                )
                results.extend(result)
        return results
        
    async def ensure_table(self, table_name: str, schema: Dict[str, Any]):
        """Ensure a table exists with the specified schema
        
        Args:
            table_name: Name of the table
            schema: Table schema definition
        """
        create_query = self._get_create_table_query(table_name, schema)
        await self.execute(create_query)