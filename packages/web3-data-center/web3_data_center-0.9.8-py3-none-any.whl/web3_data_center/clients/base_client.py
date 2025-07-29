from abc import ABC
from typing import Optional
import logging
from .mixins import ConfigMixin, ConnectionMixin

logger = logging.getLogger(__name__)

class BaseClient(ConfigMixin, ConnectionMixin, ABC):
    """Base class for all clients
    
    This class combines the basic functionality needed by all clients:
    - Configuration management (from ConfigMixin)
    - Connection management (from ConnectionMixin)
    
    It serves as the foundation for all specific client types
    (API clients, database clients, wrapper clients).
    """
    
    def __init__(self, 
                 config_path: str = "config.yml",
                 max_retries: int = 3,
                 retry_delay: float = 1.0):
        """Initialize base client
        
        Args:
            config_path: Path to configuration file
            max_retries: Maximum number of connection retry attempts
            retry_delay: Delay between retry attempts in seconds
        """
        # Initialize mixins
        ConfigMixin.__init__(self, config_path)
        ConnectionMixin.__init__(self, max_retries, retry_delay)
        
        # Validate configuration
        self.validate_config()
        
    def __repr__(self) -> str:
        """String representation of the client"""
        return (f"{self.__class__.__name__}("
                f"config_path='{self.config_path}', "
                f"connected={self.is_connected})")