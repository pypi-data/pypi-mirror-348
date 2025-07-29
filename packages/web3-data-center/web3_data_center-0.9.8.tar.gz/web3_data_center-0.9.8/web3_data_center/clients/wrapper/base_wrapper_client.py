# web3_data_center/web3_data_center/clients/wrapper/base_wrapper_client.py
from typing import TypeVar, Generic, Type, Any, Dict, Optional
import logging
import asyncio
from ..base_client import BaseClient
from ..mixins import RateLimitMixin

logger = logging.getLogger(__name__)

T = TypeVar('T')  # Type for wrapped class

class BaseWrapperClient(BaseClient, RateLimitMixin, Generic[T]):
    """Base class for wrapper clients
    
    Provides functionality for wrapping existing Python packages or libraries:
    - Instance lifecycle management
    - Method delegation
    - Rate limiting
    - Error handling
    """
    
    def __init__(self,
                 wrapped_class: Type[T],
                 wrapper_name: str,
                 config_path: str = "config.yml",
                 **kwargs):
        """Initialize wrapper client
        
        Args:
            wrapped_class: Class to wrap
            wrapper_name: Name of wrapper in config
            config_path: Path to config file
            **kwargs: Additional arguments for wrapped class
        """
        # Set wrapper name first
        self.wrapped_class = wrapped_class
        self.wrapper_name = wrapper_name
        self.init_kwargs = kwargs
        
        # Initialize base client
        super().__init__(config_path)
        
        # Initialize rate limiting
        RateLimitMixin.__init__(self)
        
        # Validate wrapper configuration
        self.validate_config()
        
        # Load wrapper config
        wrapper_config = self.get_section_config('wrapper')
        self.wrapper_config = wrapper_config[self.wrapper_name]
        
        # Set up rate limiting if configured
        if 'rate_limit' in self.wrapper_config:
            rate_limit = self.wrapper_config['rate_limit']
            self.setup_rate_limit(
                'call',
                requests_per_second=rate_limit.get('calls_per_second', 1.0),
                burst_limit=rate_limit.get('burst_limit'),
                max_queue_size=rate_limit.get('max_queue_size')
            )
            
        # Initialize wrapped instance
        self._instance: Optional[T] = None
        
    def get_config_section(self) -> str:
        """Get configuration section name"""
        return 'wrapper'
        
    def validate_config(self) -> None:
        """Validate wrapper configuration"""
        if 'wrapper' not in self.config:
            raise KeyError("Wrapper section missing from config")
            
        wrapper_config = self.config['wrapper']
        if self.wrapper_name not in wrapper_config:
            raise KeyError(f"Wrapper {self.wrapper_name} not found in config")
            
    async def _create_connection(self) -> T:
        """Create wrapped class instance
        
        Returns:
            Instance of wrapped class
        """
        try:
            # Merge config with init kwargs
            init_args = {**self.wrapper_config.get('init_args', {}), **self.init_kwargs}
            
            # Create instance
            if asyncio.iscoroutinefunction(self.wrapped_class.__init__):
                instance = await self.wrapped_class(**init_args)
            else:
                instance = self.wrapped_class(**init_args)
                
            return instance
        except Exception as e:
            logger.error(f"Failed to create wrapped instance: {str(e)}")
            raise
            
    async def _close_connection(self, instance: T) -> None:
        """Close wrapped instance
        
        Args:
            instance: Instance to close
        """
        try:
            if hasattr(instance, 'close'):
                if asyncio.iscoroutinefunction(instance.close):
                    await instance.close()
                else:
                    instance.close()
        except Exception as e:
            logger.error(f"Error closing wrapped instance: {str(e)}")
            
    async def setup(self) -> None:
        """Set up the wrapper client"""
        await self.ensure_connected()
        
    async def close(self) -> None:
        """Close the wrapper client"""
        if self.is_connected:
            await self._close_connection(self._instance)
            self._instance = None
            
    @property
    def instance(self) -> T:
        """Get the wrapped instance
        
        Returns:
            Wrapped instance
            
        Raises:
            ConnectionError: If not connected
        """
        if not self.is_connected:
            raise ConnectionError("Not connected")
        return self._connection
        
    async def call_method(self,
                         method_name: str,
                         *args,
                         **kwargs) -> Any:
        """Call a method on the wrapped instance with rate limiting
        
        Args:
            method_name: Name of method to call
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Method result
        """
        await self.apply_rate_limit('call')
        await self.ensure_connected()
        
        method = getattr(self.instance, method_name)
        if asyncio.iscoroutinefunction(method):
            return await method(*args, **kwargs)
        return method(*args, **kwargs)