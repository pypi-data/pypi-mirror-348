from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Dict, Any, Optional, AsyncIterator, Callable, Union
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

T = TypeVar('T')  # Type for input items
R = TypeVar('R')  # Type for result items

@dataclass
class BatchResult(Generic[T, R]):
    """Result of a batch operation"""
    successful: List[R]  # Successfully processed items
    failed: List[tuple[T, Exception]]  # Failed items with their exceptions
    metadata: Dict[str, Any]  # Additional metadata about the batch operation
    
class BatchOperationMixin(ABC, Generic[T, R]):
    """Mixin for batch operations
    
    Provides functionality for processing items in batches with:
    - Configurable batch size
    - Parallel processing
    - Error handling
    - Progress tracking
    - Result aggregation
    """
    
    def __init__(self, default_batch_size: int = 100):
        """Initialize batch operation mixin
        
        Args:
            default_batch_size: Default size for batches
        """
        self.default_batch_size = default_batch_size
        self._executor = ThreadPoolExecutor()
        
    @abstractmethod
    async def _process_batch(self, batch: List[T]) -> List[R]:
        """Process a single batch of items
        
        Args:
            batch: List of items to process
            
        Returns:
            List of processed results
        """
        pass
        
    async def process_batches(self,
                            items: List[T],
                            batch_size: Optional[int] = None,
                            max_concurrent: Optional[int] = None) -> BatchResult[T, R]:
        """Process items in batches
        
        Args:
            items: List of items to process
            batch_size: Size of each batch
            max_concurrent: Maximum number of concurrent batch operations
            
        Returns:
            BatchResult containing successful and failed items
        """
        batch_size = batch_size or self.default_batch_size
        max_concurrent = max_concurrent or asyncio.get_event_loop().default_executor._max_workers
        
        # Split items into batches
        batches = [items[i:i + batch_size] for i in range(0, len(items), batch_size)]
        
        successful = []
        failed = []
        start_time = datetime.now()
        
        # Process batches with semaphore for concurrency control
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_batch_with_error_handling(batch: List[T]) -> None:
            async with semaphore:
                try:
                    results = await self._process_batch(batch)
                    successful.extend(results)
                except Exception as e:
                    logger.error(f"Batch processing failed: {str(e)}")
                    failed.extend((item, e) for item in batch)
                    
        # Create tasks for all batches
        tasks = [process_batch_with_error_handling(batch) for batch in batches]
        
        # Wait for all batches to complete
        await asyncio.gather(*tasks)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        return BatchResult(
            successful=successful,
            failed=failed,
            metadata={
                'total_items': len(items),
                'batch_size': batch_size,
                'num_batches': len(batches),
                'duration_seconds': duration,
                'items_per_second': len(items) / duration if duration > 0 else 0
            }
        )
        
class AsyncOperationMixin:
    """Mixin for asynchronous operations
    
    Provides utilities for:
    - Async operation management
    - Task scheduling
    - Result collection
    """
    
    def __init__(self, max_concurrent: int = 10):
        """Initialize async operation mixin
        
        Args:
            max_concurrent: Maximum number of concurrent operations
        """
        self._semaphore = asyncio.Semaphore(max_concurrent)
        
    async def gather_with_concurrency(self,
                                    *tasks,
                                    return_exceptions: bool = False) -> List[Any]:
        """Execute coroutines with concurrency control
        
        Args:
            *tasks: Coroutines to execute
            return_exceptions: Whether to return exceptions instead of raising
            
        Returns:
            List of results
        """
        async def wrapped_task(task):
            async with self._semaphore:
                return await task
                
        return await asyncio.gather(
            *(wrapped_task(task) for task in tasks),
            return_exceptions=return_exceptions
        )
        
    @staticmethod
    def as_completed_with_timeout(tasks: List[asyncio.Task],
                                timeout: Optional[float] = None) -> AsyncIterator[Any]:
        """Wrapper around asyncio.as_completed with timeout
        
        Args:
            tasks: List of tasks
            timeout: Timeout in seconds for each task
            
        Yields:
            Completed task results
        """
        async def wrapped_task(task):
            try:
                return await asyncio.wait_for(task, timeout=timeout)
            except asyncio.TimeoutError:
                task.cancel()
                raise
                
        return asyncio.as_completed([wrapped_task(task) for task in tasks])
        
class StreamOperationMixin(Generic[T]):
    """Mixin for streaming operations
    
    Provides functionality for:
    - Stream processing
    - Backpressure handling
    - Stream transformation
    - Buffering
    """
    
    def __init__(self, buffer_size: int = 1000):
        """Initialize stream operation mixin
        
        Args:
            buffer_size: Size of the stream buffer
        """
        self.buffer_size = buffer_size
        
    async def stream_with_buffer(self,
                               source: AsyncIterator[T],
                               processor: Callable[[T], Any],
                               buffer_size: Optional[int] = None) -> AsyncIterator[Any]:
        """Process a stream with buffering
        
        Args:
            source: Source stream
            processor: Function to process each item
            buffer_size: Size of the buffer
            
        Yields:
            Processed items
        """
        buffer: List[T] = []
        buffer_size = buffer_size or self.buffer_size
        
        async for item in source:
            buffer.append(item)
            
            if len(buffer) >= buffer_size:
                # Process buffer
                for processed_item in map(processor, buffer):
                    yield processed_item
                buffer.clear()
                
        # Process remaining items
        if buffer:
            for processed_item in map(processor, buffer):
                yield processed_item
                
    @staticmethod
    async def merge_streams(*streams: AsyncIterator[T]) -> AsyncIterator[T]:
        """Merge multiple streams into one
        
        Args:
            *streams: Streams to merge
            
        Yields:
            Items from all streams
        """
        async def drain_stream(stream: AsyncIterator[T], queue: asyncio.Queue):
            try:
                async for item in stream:
                    await queue.put(item)
            finally:
                await queue.put(None)
                
        queue: asyncio.Queue[Optional[T]] = asyncio.Queue()
        drain_tasks = [
            asyncio.create_task(drain_stream(stream, queue))
            for stream in streams
        ]
        
        pending = len(drain_tasks)
        while pending > 0:
            item = await queue.get()
            if item is None:
                pending -= 1
            else:
                yield item
                
        await asyncio.gather(*drain_tasks, return_exceptions=True)