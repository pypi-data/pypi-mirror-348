# web3_data_center/web3_data_center/clients/api/base_api_client.py
from typing import Dict, Any, Optional
import logging
from ..base_client import BaseClient
from ..mixins import RateLimitMixin
import aiohttp

logger = logging.getLogger(__name__)

class BaseAPIClient(BaseClient):
    """Base class for API clients
    
    Combines base client functionality with:
    - API authentication
    - Request handling
    - Response processing
    """
    
    def __init__(self,
                 api_name: str,
                 config_path: str = "config.yml",
                 use_proxy: bool = False,
                 timeout: float = 30.0):
        """Initialize API client
        
        Args:
            api_name: Name of the API in config
            config_path: Path to config file
            use_proxy: Whether to use proxy
            timeout: Request timeout in seconds (default: 30s)
        """
        self.api_name = api_name
        self.use_proxy = use_proxy
        self.timeout = timeout
        
        # Initialize base client
        super().__init__(config_path)
    
        
        # Load API specific config
        api_config = self.get_section_config('api')
        if self.api_name not in api_config:
            raise KeyError(f"API {self.api_name} not found in config")
            
        self.api_config = api_config[self.api_name]
        self.base_url = self.api_config['base_url']
        
        # Set up rate limiting
        if 'rate_limit' in self.api_config:
            rate_limit = self.api_config['rate_limit']
            self.setup_rate_limit(
                'request',
                requests_per_second=rate_limit.get('requests_per_second', 1.0)
            )
            
        # Initialize headers
        self.headers = self._get_default_headers()
        
    def get_config_section(self) -> str:
        """Get configuration section name"""
        return 'api'
        
    def validate_config(self) -> None:
        """Validate API configuration"""
        if 'api' not in self.config:
            raise KeyError("API section missing from config")
            
        api_config = self.config['api']
        if self.api_name not in api_config:
            raise KeyError(f"API {self.api_name} not found in config")
            
        required_fields = ['base_url']
        for field in required_fields:
            if field not in api_config[self.api_name]:
                raise KeyError(f"Required field '{field}' missing from API config")
                
    def _get_default_headers(self) -> Dict[str, str]:
        """Get default headers for API requests"""
        headers = {
            'Accept': 'application/json',
            # 'User-Agent': 'Web3DataCenter/1.0'
        }
        
        # Add API key if present
        if 'api_key' in self.api_config:
            key_header = self.api_config.get('api_key_header', 'X-API-Key')
            headers[key_header] = self.api_config['api_key']
            
        return headers
        
    async def setup(self) -> None:
        """Set up the API client
        
        This creates the initial connection and performs any necessary initialization.
        """
        await self.connect()
        
    async def close(self) -> None:
        """Close the API client
        
        This closes any open connections and cleans up resources.
        """
        if self.is_connected:
            await self.disconnect()

    async def _create_connection(self) -> aiohttp.ClientSession:
        """Create a new aiohttp session for API requests"""
        return aiohttp.ClientSession(headers=self.headers)

    async def _close_connection(self, connection: aiohttp.ClientSession) -> None:
        """Close the aiohttp session"""
        if connection and not connection.closed:
            await connection.close()

    async def _make_request(self,
                          endpoint: str,
                          method: str = "GET",
                          params: Optional[Dict[str, Any]] = None,
                          data: Optional[Dict[str, Any]] = None,
                          headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Make an API request
        
        Args:
            endpoint: API endpoint
            method: HTTP method
            params: Query parameters
            data: Request body
            headers: Additional headers
            
        Returns:
            API response
            
        Raises:
            ConnectionError: If connection fails
            RequestError: If request fails
        """
        # Ensure we're connected
        await self.ensure_connected()
        
        # Merge headers
        request_headers = self.headers.copy()
        if headers:
            request_headers.update(headers)
            
        # Build URL
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        await self.apply_rate_limit('request')

        try:
            # Create a new session for this request
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            # Use system proxy if configured
            proxy = 'http://127.0.0.1:7890' if self.use_proxy else None
            async with aiohttp.ClientSession(timeout=timeout, trust_env=True, proxy=proxy) as session:
                async with session.request(
                    method,
                    url,
                    params=params,
                    json=data,
                    headers=request_headers
                ) as response:
                    response.raise_for_status()
                    return await response.json()
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise