# web3_data_center/web3_data_center/clients/batch/types.py
from dataclasses import dataclass
from typing import Any, Tuple, Dict, Optional

@dataclass
class BatchItem:
    """Represents a single item in a batch operation"""
    method: str
    args: Tuple[Any, ...] = ()
    kwargs: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}
