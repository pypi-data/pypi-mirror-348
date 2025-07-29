"""Token Bucket Rate Limiter implementation with burst handling and queue management."""
import asyncio
import time
from typing import Optional, Callable, Any
import logging

logger = logging.getLogger(__name__)

class TimeRateLimiter:
    """Rate limiter implementation using asyncio.Lock"""
    def __init__(self, rpm: int = 120):
        self.rate_limit = rpm
        self.time_period = 60.0  # 1 minute in seconds
        self.tokens = rpm
        self.updated_at = asyncio.get_event_loop().time()
        self.lock = asyncio.Lock()

    async def acquire(self):
        async with self.lock:
            now = asyncio.get_event_loop().time()
            time_passed = now - self.updated_at
            self.tokens += time_passed * (self.rate_limit / self.time_period)
            if self.tokens > self.rate_limit:
                self.tokens = self.rate_limit
            self.updated_at = now

            if self.tokens < 1:
                wait_time = (1 - self.tokens) * (self.time_period / self.rate_limit)
                await asyncio.sleep(wait_time)
                self.tokens = 0
                self.updated_at = asyncio.get_event_loop().time()
            else:
                self.tokens -= 1

class TokenBucketRateLimiter:
    def __init__(
        self, 
        rate_limit: int,
        burst_limit: Optional[int] = None,
        max_queue_size: int = 1000
    ):
        """Initialize the token bucket rate limiter.
        
        Args:
            rate_limit: Number of tokens per second
            burst_limit: Maximum number of tokens that can be accumulated (defaults to rate_limit)
            max_queue_size: Maximum number of requests that can be queued
        """
        self.rate_limit = rate_limit
        self.burst_limit = burst_limit or rate_limit
        self.tokens = self.burst_limit  # Start with full bucket
        self.last_update = time.monotonic()
        self.lock = asyncio.Lock()
        self.queue = asyncio.Queue(maxsize=max_queue_size)
        self._running = False
        self._worker_task = None

    async def _add_tokens(self) -> float:
        """Add tokens based on elapsed time and return wait time if needed."""
        now = time.monotonic()
        time_passed = now - self.last_update
        self.tokens = min(
            self.burst_limit,
            self.tokens + time_passed * self.rate_limit
        )
        self.last_update = now
        
        if self.tokens < 1:
            wait_time = (1 - self.tokens) / self.rate_limit
            return wait_time
        return 0

    async def acquire(self):
        """Acquire a token, waiting if necessary."""
        async with self.lock:
            wait_time = await self._add_tokens()
            if wait_time > 0:
                await asyncio.sleep(wait_time)
            self.tokens -= 1

    async def _worker(self):
        """Background worker to process queued requests."""
        while self._running:
            try:
                func, args, kwargs, future = await self.queue.get()
                try:
                    await self.acquire()

                    result = await func(*args, **kwargs)
                    if not future.done():
                        future.set_result(result)
                except Exception as e:
                    if not future.done():
                        future.set_exception(e)
                finally:
                    self.queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in rate limiter worker: {e}")

    def start(self):
        """Start the background worker."""
        if not self._running:
            self._running = True
            self._worker_task = asyncio.create_task(self._worker())

    async def stop(self):
        """Stop the background worker."""
        if self._running:
            self._running = False
            if self._worker_task:
                self._worker_task.cancel()
                try:
                    await self._worker_task
                except asyncio.CancelledError:
                    pass
                self._worker_task = None

    async def execute(self, func: Callable, *args, **kwargs) -> Any:
        """Execute a function with rate limiting.
        
        Args:
            func: Async function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            Result of the function execution
        
        Raises:
            QueueFull: If the request queue is full
        """
        future = asyncio.Future()
        await self.queue.put((func, args, kwargs, future))
        return await future
