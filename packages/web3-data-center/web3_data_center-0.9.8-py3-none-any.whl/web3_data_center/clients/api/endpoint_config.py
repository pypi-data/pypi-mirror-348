
from dataclasses import dataclass
from typing import Optional

@dataclass
class EndpointConfig:
    """Configuration for API endpoints"""
    path: str
    method: str = "GET"
    batch_size: Optional[int] = None
    rate_limit: Optional[float] = None
    cost_weight: float = 1.0