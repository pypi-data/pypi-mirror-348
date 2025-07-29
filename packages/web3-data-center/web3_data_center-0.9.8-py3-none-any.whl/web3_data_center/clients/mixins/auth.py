from enum import Enum
from typing import Dict, Any, Tuple, Optional, Mapping
import hmac
import hashlib
import time
import logging

logger = logging.getLogger(__name__)

class AuthType(Enum):
    NONE = "none"
    API_KEY = "api_key"
    BEARER = "bearer"
    HMAC = "hmac"
    BASIC = "basic"
    CUSTOM = "custom"

class AuthMixin:
    """Mixin for handling API authentication"""
    
    def setup_auth(self, auth_type: AuthType = AuthType.NONE) -> None:
        """Set up authentication
        
        Args:
            auth_type: Type of authentication to use
        """
        self.auth_type = auth_type
        self.auth_config = getattr(self, 'api_config', {}).get('credentials', {})
        if self.auth_type != AuthType.NONE:
            required_fields = {
                AuthType.API_KEY: ['api_key'],
                AuthType.BEARER: ['api_key'],
                AuthType.HMAC: ['api_key', 'api_secret'],
                AuthType.BASIC: ['username', 'password'],
                AuthType.CUSTOM: ['auth_scheme', 'credentials']
            }.get(self.auth_type, [])
            
            missing = [f for f in required_fields if f not in self.auth_config]
            if missing:
                raise ValueError(f"Missing required auth fields: {missing}")
                
    async def authenticate_request(self,
                                 method: str,
                                 endpoint: str,
                                 params: Dict[str, Any],
                                 headers: Dict[str, str],
                                 data: Any = None) -> Tuple[Dict[str, Any], Dict[str, str]]:
        """Add authentication to request
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            headers: Request headers
            data: Request body
            
        Returns:
            Tuple of (params, headers) with authentication added
        """
        if not hasattr(self, 'auth_type'):
            return params, headers
            
        if self.auth_type == AuthType.API_KEY:
            # Check if api_key_header is explicitly defined in config
            if 'api_key_header' in self.auth_config:
                # If header name is defined, place key in headers
                key_name = self.auth_config['api_key_header']
                headers[key_name] = self.auth_config['api_key']
            else:
                # Default behavior - place in params with name 'apikey'
                params['apikey'] = self.auth_config['api_key']
            
        elif self.auth_type == AuthType.BEARER:
            headers['Authorization'] = f"Bearer {self.auth_config['api_key']}"
            
        elif self.auth_type == AuthType.HMAC:
            timestamp = str(int(time.time()))
            message = f"{method}{endpoint}{timestamp}"
            if data:
                message += str(data)
                
            signature = hmac.new(
                self.auth_config['api_secret'].encode(),
                message.encode(),
                hashlib.sha256
            ).hexdigest()
            
            headers.update({
                'API-Key': self.auth_config['api_key'],
                'API-Timestamp': timestamp,
                'API-Signature': signature
            })
            
        return params, headers