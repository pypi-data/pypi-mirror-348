from typing import Dict, Any
import logging
import aiohttp
from .base_api_client import BaseAPIClient
from ..mixins.rate_limit import RateLimitMixin

logger = logging.getLogger(__name__)

class FWAlertClient(BaseAPIClient):
    """Client for interacting with the FWAlert API
    
    Features:
    - Singleton pattern to ensure single instance per configuration
    - Rate limiting and request throttling
    - Async context manager support
    - Direct class method usage support
    """
    
    _instances = {}
    
    ENDPOINTS = {
        'callme': {
            'method': 'GET',
            'rate_limit': 5.0,
            'cost_weight': 1.0
        },
        'notify': {
            'method': 'GET',
            'rate_limit': 5.0,
            'cost_weight': 1.0
        }
    }
    
    def __new__(cls, config_path: str = "config.yml", use_proxy: bool = False):
        """Ensure singleton instance per configuration"""
        instance_key = (config_path, use_proxy)
        
        if instance_key not in cls._instances:
            cls._instances[instance_key] = super().__new__(cls)
            cls._instances[instance_key]._initialized = False
        
        return cls._instances[instance_key]

    def __init__(self, config_path: str = "config.yml", use_proxy: bool = False):
        """Initialize FWAlert client if not already initialized"""
        if not getattr(self, '_initialized', False):
            super().__init__('fwalert', config_path=config_path, use_proxy=use_proxy)
            
            # Initialize rate limiting
            self.setup_rate_limits()
            for endpoint, config in self.ENDPOINTS.items():
                self.setup_rate_limit(
                    endpoint,
                    requests_per_second=config['rate_limit'],
                    cost_weight=config['cost_weight']
                )
            
            self._initialized = True

    async def _create_connection(self) -> aiohttp.ClientSession:
        """Create a new aiohttp session for API requests"""
        return aiohttp.ClientSession(headers=self.headers)

    async def _close_connection(self, connection: aiohttp.ClientSession) -> None:
        """Close the aiohttp session"""
        if connection and not connection.closed:
            await connection.close()

    @classmethod
    async def callme(cls, topic: str, config_path: str = "config.yml", use_proxy: bool = False) -> Dict[str, Any]:
        """Call the FWAlert API with a topic
        
        Args:
            topic: Topic to query
            config_path: Path to config file
            use_proxy: Whether to use proxy
            
        Returns:
            API response data
        """
        async with cls(config_path, use_proxy) as client:
            actual_params = {"topic": topic}
            endpoint = client.api_config['default_endpoint']
            return await client._make_request(endpoint, method="GET", params=actual_params)

    @classmethod
    async def notify(cls, slug: str, params: Dict[str, Any], config_path: str = "config.yml", use_proxy: bool = False) -> Dict[str, Any]:
        """Send a notification via FWAlert
        
        Args:
            slug: Notification endpoint slug
            params: Parameters for the notification
            config_path: Path to config file
            use_proxy: Whether to use proxy
            
        Returns:
            API response data
        """
        async with cls(config_path, use_proxy) as client:
            endpoint = "/" + slug
            return await client._make_request(endpoint, method="GET", params=params)

    @classmethod
    def get_instance(cls, config_path: str = "config.yml", use_proxy: bool = False) -> 'FWAlertClient':
        """Get or create a singleton instance of FWAlertClient with specific configuration
        
        Args:
            config_path: Path to config file
            use_proxy: Whether to use proxy
            
        Returns:
            FWAlertClient instance
        """
        return cls(config_path=config_path, use_proxy=use_proxy)
