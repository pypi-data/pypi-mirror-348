from abc import ABC, abstractmethod
from typing import Optional, Any
import logging
import asyncio
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

class ConnectionMixin(ABC):
    """Mixin for connection management
    
    This mixin provides functionality for managing client connections, including:
    - Connection lifecycle management (connect/disconnect)
    - Connection state tracking
    - Connection pooling
    - Automatic reconnection
    - Context manager support
    
    Attributes:
        _connection: The underlying connection object
        _connected (bool): Connection state flag
        _connection_lock (asyncio.Lock): Lock for connection operations
        max_retries (int): Maximum number of connection retry attempts
        retry_delay (float): Delay between retry attempts in seconds
    """
    
    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0):
        """Initialize connection mixin
        
        Args:
            max_retries: Maximum number of connection retry attempts
            retry_delay: Delay between retry attempts in seconds
        """
        self._connection: Optional[Any] = None
        self._connected: bool = False
        self._connection_lock = asyncio.Lock()
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
    @abstractmethod
    async def _create_connection(self) -> Any:
        """Create a new connection
        
        This method should be implemented by subclasses to create
        the actual connection object.
        
        Returns:
            New connection object
            
        Raises:
            ConnectionError: If connection creation fails
        """
        pass
        
    @abstractmethod
    async def _close_connection(self, connection: Any) -> None:
        """Close an existing connection
        
        This method should be implemented by subclasses to properly
        close the connection object.
        
        Args:
            connection: Connection object to close
        """
        pass
        
    async def connect(self) -> None:
        """Establish connection with retry logic
        
        Attempts to establish a connection with retry logic on failure.
        
        Raises:
            ConnectionError: If connection fails after max retries
        """
        if self.is_connected:
            return
            
        async with self._connection_lock:
            if self.is_connected:  # Double check under lock
                return
                
            for attempt in range(self.max_retries):
                try:
                    self._connection = await self._create_connection()
                    self._connected = True
                    logger.info(f"Successfully connected on attempt {attempt + 1}")
                    return
                except Exception as e:
                    if attempt == self.max_retries - 1:
                        logger.error(f"Failed to connect after {self.max_retries} attempts")
                        raise ConnectionError(f"Failed to connect: {str(e)}")
                    logger.warning(f"Connection attempt {attempt + 1} failed, retrying...")
                    await asyncio.sleep(self.retry_delay)
        
    async def disconnect(self) -> None:
        """Close the connection
        
        Closes the current connection if it exists.
        """
        if not self.is_connected:
            return
            
        async with self._connection_lock:
            if not self.is_connected:  # Double check under lock
                return
                
            try:
                await self._close_connection(self._connection)
            except Exception as e:
                logger.error(f"Error closing connection: {str(e)}")
            finally:
                self._connection = None
                self._connected = False
                
    @property
    def is_connected(self) -> bool:
        """Check if client is connected
        
        Returns:
            True if connected, False otherwise
        """
        return self._connected and self._connection is not None
        
    @property
    def connection(self) -> Optional[Any]:
        """Get the underlying connection object
        
        Returns:
            Current connection object or None if not connected
        """
        return self._connection
        
    async def ensure_connected(self) -> None:
        """Ensure connection is established
        
        Connects if not already connected.
        
        Raises:
            ConnectionError: If connection fails
        """
        if not self.is_connected:
            await self.connect()
            
    @asynccontextmanager
    async def connection_context(self):
        """Async context manager for connection
        
        Provides a context manager that ensures connection is established
        and properly closed.
        
        Yields:
            Connection object
            
        Raises:
            ConnectionError: If connection fails
        """
        await self.ensure_connected()
        try:
            yield self.connection
        finally:
            await self.disconnect()
            
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()