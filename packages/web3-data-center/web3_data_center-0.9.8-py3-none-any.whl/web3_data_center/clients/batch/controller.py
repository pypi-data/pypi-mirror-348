# web3_data_center/web3_data_center/clients/batch/controller.py
from typing import TypeVar, Generic, List, Optional, Dict, Any, Callable
from dataclasses import dataclass
import time
import logging
import statistics
from collections import deque
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

T = TypeVar('T')
R = TypeVar('R')

@dataclass
class BatchConfig:
    """Batch operation configuration"""
    batch_size: int
    max_concurrency: int
    cost_weight: float = 1.0
    adaptive: bool = False
    min_batch_size: Optional[int] = None
    max_batch_size: Optional[int] = None
    target_success_rate: float = 0.95
    target_response_time: float = 1.0

class BatchMetrics:
    """Performance metrics tracking"""
    def __init__(self, window_size: int = 100):
        self.response_times = deque(maxlen=window_size)
        self.success_counts = deque(maxlen=window_size)
        self.error_counts = deque(maxlen=window_size)
        
    def update(self, response_time: float, successes: int, errors: int):
        self.response_times.append(response_time)
        self.success_counts.append(successes)
        self.error_counts.append(errors)
        
    def get_stats(self) -> Dict[str, float]:
        if not self.response_times:
            return {"success_rate": 1.0, "avg_response_time": 0.0, "error_rate": 0.0}
        
        total = sum(self.success_counts) + sum(self.error_counts)
        if total == 0:
            return {"success_rate": 1.0, "avg_response_time": 0.0, "error_rate": 0.0}
        
        return {
            "success_rate": sum(self.success_counts) / total,
            "avg_response_time": statistics.mean(self.response_times),
            "error_rate": sum(self.error_counts) / total,
            "throughput": total / sum(self.response_times) if self.response_times else 0
        }

class BatchController(Generic[T, R]):
    """Controls batch processing operations"""
    
    def __init__(self, config: BatchConfig):
        self.config = config
        self.metrics = BatchMetrics()
        self.current_batch_size = config.batch_size
        self.current_concurrency = config.max_concurrency
        self._adjustment_count = 0
        
    async def process_batch(self,
                          items: List[T],
                          operation: Callable[[List[T]], List[R]],
                          rate_limiter: Optional[Callable] = None) -> List[R]:
        """Process a single batch of items"""
        if not items:
            return []
            
        try:
            if rate_limiter:
                await rate_limiter()
                
            start_time = time.time()
            results = await operation(items)
            response_time = time.time() - start_time
            
            self.metrics.update(
                response_time=response_time,
                successes=len(results),
                errors=len(items) - len(results)
            )
            
            if self.config.adaptive:
                self._adjustment_count += 1
                if self._adjustment_count >= 10:  # Adjust every 10 batches
                    await self._adjust_parameters()
                    self._adjustment_count = 0
                    
            return results
            
        except Exception as e:
            logger.error(f"Batch processing error: {str(e)}")
            self.metrics.update(
                response_time=time.time() - start_time,
                successes=0,
                errors=len(items)
            )
            raise
            
    async def _adjust_parameters(self):
        """Adjust batch size and concurrency based on performance"""
        if not self.config.adaptive:
            return
            
        stats = self.metrics.get_stats()
        
        # Adjust batch size
        if stats["success_rate"] < self.config.target_success_rate:
            self.current_batch_size = max(
                self.config.min_batch_size or 1,
                int(self.current_batch_size * 0.8)
            )
        elif stats["avg_response_time"] > self.config.target_response_time:
            self.current_batch_size = max(
                self.config.min_batch_size or 1,
                int(self.current_batch_size * 0.9)
            )
        else:
            self.current_batch_size = min(
                self.config.max_batch_size or self.config.batch_size,
                int(self.current_batch_size * 1.1)
            )
            
        # Adjust concurrency based on error rate and throughput
        if stats["error_rate"] > 0.1:
            self.current_concurrency = max(1, self.current_concurrency - 1)
        elif stats["throughput"] < 1.0 / stats["avg_response_time"]:
            self.current_concurrency = min(
                self.config.max_concurrency,
                self.current_concurrency + 1
            )
            
        logger.debug(
            f"Adjusted parameters: batch_size={self.current_batch_size}, "
            f"concurrency={self.current_concurrency}"
        )
