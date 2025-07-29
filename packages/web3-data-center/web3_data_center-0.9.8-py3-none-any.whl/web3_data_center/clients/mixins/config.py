from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import os
import yaml
import logging

logger = logging.getLogger(__name__)

class ConfigMixin(ABC):
    """Mixin for configuration management
    
    This mixin provides functionality for loading and managing configuration from YAML files.
    It handles config validation, section management, and credential management.
    
    Attributes:
        config (Dict[str, Any]): Loaded configuration dictionary
        config_path (str): Path to the configuration file
    """
    
    def __init__(self, config_path: str = "config.yml"):
        """Initialize configuration mixin
        
        Args:
            config_path: Path to YAML config file
        """
        self.config_path = config_path
        self.config = self.load_config(config_path)
        
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file
        
        Args:
            config_path: Path to YAML config file
            
        Returns:
            Loaded configuration as dictionary
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config file is invalid YAML
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
            
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                # logger.debug(f"Loaded configuration from {config_path}")
                return config
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing config file: {e}")
            
    @abstractmethod
    def get_config_section(self) -> str:
        """Get the configuration section name for this client type
        
        Returns:
            Name of the configuration section
        """
        pass
        
    @abstractmethod
    def validate_config(self) -> None:
        """Validate client configuration
        
        Raises:
            KeyError: If required configuration sections or keys are missing
            ValueError: If configuration values are invalid
        """
        pass
        
    def get_credentials(self, section: str) -> Dict[str, str]:
        """Get credentials from config file
        
        Args:
            section: Section name in config file
            
        Returns:
            Dictionary of credentials
            
        Raises:
            KeyError: If section not found in config
        """
        if section not in self.config:
            raise KeyError(f"Section {section} not found in config")
        return self.config[section]
        
    def get_section_config(self, section: Optional[str] = None) -> Dict[str, Any]:
        """Get configuration for a specific section
        
        Args:
            section: Section name, defaults to result of get_config_section()
            
        Returns:
            Configuration dictionary for the section
            
        Raises:
            KeyError: If section not found in config
        """
        section = section or self.get_config_section()
        if section not in self.config:
            raise KeyError(f"Section {section} not found in config")
        return self.config[section]