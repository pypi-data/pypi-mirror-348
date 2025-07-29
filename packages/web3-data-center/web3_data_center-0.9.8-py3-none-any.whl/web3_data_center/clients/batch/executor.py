# web3_data_center/web3_data_center/clients/batch/executor.py
from typing import TypeVar, Generic, List, Optional, Callable, Any
from .controller import BatchController
from .types import BatchItem
import asyncio
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')

class BatchExecutor:
    """Executes batch operations with concurrency control"""
    
    def __init__(self, operation: Callable[[List[BatchItem]], List[Any]]):
        """Initialize batch executor
        
        Args:
            operation: Function to process a batch of items
        """
        self.operation = operation
        
    async def execute_batch(self,
                          items: List[BatchItem],
                          batch_size: int,
                          max_concurrent: int) -> List[Any]:
        """Execute batch processing with concurrency control
        
        Args:
            items: Items to process
            batch_size: Size of each batch
            max_concurrent: Maximum concurrent batches
            
        Returns:
            Combined results from all batches
        """
        if not items:
            return []
            
        results = []
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_chunk(chunk: List[BatchItem]) -> List[Any]:
            async with semaphore:
                try:
                    return await self.operation(chunk)
                except Exception as e:
                    logger.error(f"Error processing batch: {str(e)}")
                    return [None] * len(chunk)
                
        # Create batches
        batches = [
            items[i:i + batch_size]
            for i in range(0, len(items), batch_size)
        ]
        
        # Process batches concurrently
        tasks = [process_chunk(batch) for batch in batches]
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine results
        for result in batch_results:
            if isinstance(result, Exception):
                logger.error(f"Batch failed: {str(result)}")
                continue
            results.extend(result)

        return results