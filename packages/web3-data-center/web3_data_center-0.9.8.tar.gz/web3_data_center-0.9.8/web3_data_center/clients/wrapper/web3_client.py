# web3_data_center/web3_data_center/clients/wrapper/web3_client.py
from typing import Any, Dict, Optional, List
import logging
import time
import asyncio
from web3 import AsyncWeb3 as Web3Lib
from web3.types import TxParams, BlockData, TxData
from .base_wrapper_client import BaseWrapperClient
from ..batch.executor import BatchExecutor
from ..batch.types import BatchItem

logger = logging.getLogger(__name__)

class Web3Client(BaseWrapperClient[Web3Lib]):
    """Client for interacting with Ethereum blockchain via Web3.py
    
    Features:
    - Ethereum node connection management
    - Transaction retrieval and sending
    - Contract interaction
    - Rate limiting and batch processing
    """
    
    def __init__(self, config_path: str = "config.yml"):
        """Initialize Web3 client"""
        super().__init__(
            wrapped_class=Web3Lib,
            wrapper_name='web3',
            config_path=config_path
        )
        
        # Configure web3.py logging
        logging.getLogger('web3').setLevel(logging.WARNING)
        logging.getLogger('web3.RequestManager').setLevel(logging.WARNING)
        logging.getLogger('web3.providers').setLevel(logging.WARNING)
        logging.getLogger('web3.manager').setLevel(logging.WARNING)
        
        # Initialize batch executor
        self.batch_executor = BatchExecutor(self._execute_batch)
        self.batch_size = self.wrapper_config.get('batch_size', 10)
        self.max_concurrent = self.wrapper_config.get('max_concurrent', 20)
        
        # Initialize rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0 / (self.wrapper_config.get('rpm', 6000) / 60.0)  # Convert RPM to seconds per request
        
    async def setup(self) -> None:
        """Set up the Web3 client"""
        await super().setup()
        logger.debug("Web3 client connected to %s", self.wrapper_config['base_url'])
        
    async def close(self) -> None:
        """Close the Web3 client"""
        await super().close()
        logger.debug("Web3 client closed")
        
    async def _create_connection(self) -> Any:
        """Create Web3 instance and connect to node"""
        # Get provider URL from config
        provider_url = self.wrapper_config.get('base_url', 'http://localhost:8545')
        
        # Create Web3 instance with HTTP provider
        web3 = self.wrapped_class(Web3Lib.AsyncHTTPProvider(provider_url))
        
        # Test connection
        if not await web3.is_connected():
            raise ConnectionError(f"Failed to connect to Ethereum node at {provider_url}")
            
        return web3
        
    async def _close_connection(self, connection: Any) -> None:
        """Close Web3 connection"""
        # Web3.py doesn't require explicit cleanup
        pass
        
    @property
    def eth(self):
        """Access to Eth API"""
        if not self.is_connected:
            raise RuntimeError("Web3 client not connected")
        return self._connection.eth
        
    async def _execute_batch(self, batch: List[BatchItem]) -> List[Any]:
        """Execute a batch of Web3 requests
        
        Args:
            batch: List of batch items to execute
            
        Returns:
            List of results in same order as batch items
        """
        results = []
        for item in batch:
            method = getattr(self.eth, item.method)
            try:
                result = await method(*item.args, **item.kwargs)
                results.append(result)
            except Exception as e:
                logger.error(f"Error executing {item.method}: {str(e)}")
                results.append(None)
        return results
        
    async def execute_batch(self, items: List[BatchItem]) -> List[Any]:
        """Execute a batch of requests
        
        Args:
            items: List of batch items to execute
            
        Returns:
            List of results in same order as items
        """
        await self._apply_rate_limit()  # Apply rate limit before batch
        return await self.batch_executor.execute_batch(
            items=items,
            batch_size=self.batch_size,
            max_concurrent=self.max_concurrent
        )
        
    async def _apply_rate_limit(self):
        """Apply rate limiting before making a request"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            await asyncio.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()
        
    async def get_transaction(self, tx_hash: str) -> Optional[Dict[str, Any]]:
        """Get transaction by hash
        
        Args:
            tx_hash: Transaction hash
            
        Returns:
            Transaction data if found, None otherwise
        """
        try:
            await self._apply_rate_limit()
            tx = await self.eth.get_transaction(tx_hash)
            if tx:
                return dict(tx)  # Convert AttributeDict to regular dict
            return None
        except Exception as e:
            logger.error(f"Error getting transaction {tx_hash}: {str(e)}")
            return None
            
    async def get_transaction_receipt(self, tx_hash: str) -> Optional[Dict[str, Any]]:
        """Get transaction receipt
        
        Args:
            tx_hash: Transaction hash
            
        Returns:
            Transaction receipt if found, None otherwise
        """
        try:
            await self._apply_rate_limit()
            receipt = await self.eth.get_transaction_receipt(tx_hash)
            if receipt:
                return dict(receipt)
            return None
        except Exception as e:
            logger.error(f"Error getting transaction receipt {tx_hash}: {str(e)}")
            return None
            
    async def get_block(self, block_identifier: Any) -> Optional[Dict[str, Any]]:
        """Get block by number or hash
        
        Args:
            block_identifier: Block number or hash
            
        Returns:
            Block data if found, None otherwise
        """
        try:
            await self._apply_rate_limit()
            block = await self.eth.get_block(block_identifier)
            if block:
                return dict(block)
            return None
        except Exception as e:
            logger.error(f"Error getting block {block_identifier}: {str(e)}")
            return None
            
    async def get_transactions(self, tx_hashes: List[str]) -> List[Optional[Dict[str, Any]]]:
        """Get multiple transactions by hash
        
        Args:
            tx_hashes: List of transaction hashes
            
        Returns:
            List of transaction data in same order as hashes
        """
        try:
            batch_items = [
                BatchItem(method='get_transaction', args=(tx_hash,))
                for tx_hash in tx_hashes
            ]
            results = await self.execute_batch(batch_items)
            return [dict(tx) if tx else None for tx in results]
        except Exception as e:
            logger.error(f"Error getting transactions: {str(e)}")
            return [None] * len(tx_hashes)
        
    async def get_balances(self, addresses: List[str]) -> List[Optional[int]]:
        """Get multiple balances by address
        
        Args:
            addresses: List of addresses
            
        Returns:
            List of balances (in wei) in same order as addresses
        """
        try:
            addresses = [Web3Lib.to_checksum_address(address) for address in addresses]
            batch_items = [
                BatchItem(method='get_balance', args=(address,))
                for address in addresses
            ]
            results = await self.execute_batch(batch_items)
            return results
        except Exception as e:
            logger.error(f"Error getting balances: {str(e)}")
            return [None] * len(addresses)

    async def get_code(self, address: str) -> str:
        """Get the code of a contract"""
        try:
            await self._apply_rate_limit()
            code = await self.eth.get_code(address)
            return code
        except Exception as e:
            logger.error(f"Error getting code for address {address}: {str(e)}")
            return None
