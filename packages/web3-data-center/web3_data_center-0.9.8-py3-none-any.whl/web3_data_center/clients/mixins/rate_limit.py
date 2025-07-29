# web3_data_center/web3_data_center/clients/mixins/rate_limit.py
from typing import Dict, Optional
import time
import logging
import asyncio
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class RateLimit:
    """Rate limit configuration"""
    requests_per_second: float
    cost_weight: float = 1.0
    last_request_time: float = 0.0

class RateLimitMixin:
    """Mixin for handling API rate limits"""
    
    @staticmethod
    def rate_limited(endpoint: str):
        """Decorator to apply rate limiting to a method
        
        Args:
            endpoint: Endpoint identifier to rate limit
            
        Returns:
            Decorated method with rate limiting applied
        """
        def decorator(func):
            async def wrapper(self, *args, **kwargs):
                await self.apply_rate_limit(endpoint)
                return await func(self, *args, **kwargs)
            return wrapper
        return decorator
    
    def setup_rate_limits(self, endpoints: Optional[Dict] = None) -> None:
        """Initialize rate limiting
        
        Args:
            endpoints: Optional dictionary of endpoint configurations. If provided,
                      will set up rate limits for each endpoint based on their config.
        """
        self._rate_limits: Dict[str, RateLimit] = {}
        
        # Get global limits from config
        config = getattr(self, 'api_config', {}).get('rate_limit', {})
        self.global_rate_limit = config.get('global_rate_limit')
        self.daily_credit_limit = config.get('daily_credit_limit')
        
        # Initialize credit tracking
        self._credits_used = 0.0
        self._credits_reset_time = time.time() + 86400  # 24 hours
        
        # Set up endpoint-specific rate limits if provided
        if endpoints:
            for endpoint, config in endpoints.items():
                self.setup_rate_limit(
                    endpoint=endpoint,
                    requests_per_second=getattr(config, 'rate_limit', None),
                    cost_weight=getattr(config, 'cost_weight', 1.0)
                )
        
    def setup_rate_limit(self,
                        endpoint: str,
                        requests_per_second: Optional[float] = None,
                        cost_weight: float = 1.0) -> None:
        """Set up rate limiting for an endpoint
        
        Args:
            endpoint: Endpoint identifier
            requests_per_second: Maximum requests per second (None uses global)
            cost_weight: Cost weight for credit tracking
        """
        rate_limit = requests_per_second or self.global_rate_limit
        if rate_limit:
            self._rate_limits[endpoint] = RateLimit(
                requests_per_second=rate_limit,
                cost_weight=cost_weight
            )
            
    async def apply_rate_limit(self, endpoint: str) -> None:
        """Apply rate limiting for an endpoint
        
        Args:
            endpoint: Endpoint identifier to rate limit
        """
        rate_limit = self._rate_limits.get(endpoint)
        if not rate_limit:
            if not self.global_rate_limit:
                return
            # Use global rate limit if no endpoint-specific limit
            rate_limit = RateLimit(
                requests_per_second=self.global_rate_limit,
                cost_weight=1.0
            )
            
        current_time = time.time()
        
        # Calculate wait time based on rate limit
        elapsed = current_time - rate_limit.last_request_time
        wait_time = (1.0 / rate_limit.requests_per_second) - elapsed
        
        if wait_time > 0:
            await asyncio.sleep(wait_time)
            
        # Update last request time
        rate_limit.last_request_time = time.time()
        
        # Track API credits if enabled
        if self.daily_credit_limit:
            if current_time > self._credits_reset_time:
                self._credits_used = rate_limit.cost_weight
                self._credits_reset_time = current_time + 86400
            else:
                self._credits_used += rate_limit.cost_weight
                
            if self._credits_used > self.daily_credit_limit:
                raise Exception(
                    f"Daily API credit limit exceeded: "
                    f"{self._credits_used}/{self.daily_credit_limit}"
                )
                
    def get_rate_limit(self, endpoint: str) -> Optional[RateLimit]:
        """Get rate limit configuration for endpoint
        
        Args:
            endpoint: Endpoint identifier
            
        Returns:
            Rate limit configuration if exists
        """
        return self._rate_limits.get(endpoint)
        
    def get_credits_used(self) -> float:
        """Get current API credits used
        
        Returns:
            Number of credits used in current period
        """
        return self._credits_used

