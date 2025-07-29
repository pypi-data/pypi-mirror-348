# web3_data_center/web3_data_center/clients/api/funding_client.py
from typing import Dict, Any, List, Optional
import logging
from .base_api_client import BaseAPIClient
from ..mixins.rate_limit import RateLimitMixin
from ..batch.controller import BatchController, BatchConfig
from ..batch.executor import BatchExecutor

logger = logging.getLogger(__name__)

class FundingClient(BaseAPIClient, RateLimitMixin):
    """Client for interacting with the Funding JSON-RPC API
    
    Features:
    - JSON-RPC protocol support
    - Automatic batch processing with adaptive sizing
    - Rate limiting and performance monitoring
    """
    
    ENDPOINTS = {
        'simulate_view_first_fund': {
            'method': 'simulate_viewFirstFund',
            'max_batch_size': 50,
            'rate_limit': 20.0,
            'cost_weight': 1.0
        },
        'simulate_txs': {
            'method': 'simulate_txs',
            'max_batch_size': 50,
            'rate_limit': 20.0,
            'cost_weight': 1.0
        }
    }
    
    def __init__(self, config_path: str = "config.yml", use_proxy: bool = False):
        """Initialize Funding client"""
        super().__init__('funding', config_path=config_path, use_proxy=use_proxy)
        
        # Initialize rate limiting
        self.setup_rate_limits()
        for endpoint, config in self.ENDPOINTS.items():
            self.setup_rate_limit(
                endpoint,
                requests_per_second=config['rate_limit'],
                cost_weight=config['cost_weight']
            )
        
        # Initialize batch processing
        self.batch_controller = BatchController(
            BatchConfig(
                batch_size=200,
                max_concurrency=10,
                adaptive=True,
                min_batch_size=10,
                max_batch_size=200,
                target_success_rate=0.95,
                target_response_time=1.0
            )
        )
        self.batch_executor = BatchExecutor(self.batch_controller)
        
    async def _make_rpc_request(self,
                               method: str,
                               params: List[Any],
                               endpoint: str = "/") -> Dict[str, Any]:
        """Make a JSON-RPC request"""
        data = {
            "method": method,
            "params": params,
            "id": 1,
            "jsonrpc": "2.0"
        }
        
        # logger.debug(f"Making RPC request to {self.base_url}{endpoint}: {data}")
        try:
            response = await self._make_request(
                endpoint,
                method="POST",
                data=data
            )
            # logger.debug(f"Got RPC response: {response}")
            
            if 'error' in response:
                logger.error(f"RPC error for {method}: {response['error']}")
                return None
                
            return response.get('result')
        except Exception as e:
            logger.error(f"RPC request failed: {str(e)}")
            return None
        
    async def _create_connection(self) -> Any:
        """Create a new aiohttp session for API requests"""
        import aiohttp
        return aiohttp.ClientSession(headers=self.headers)

    async def _close_connection(self, connection: Any) -> None:
        """Close the aiohttp session"""
        if connection and not connection.closed:
            await connection.close()

    async def simulate_view_first_fund(self, address: str) -> Optional[Dict[str, Any]]:
        """Simulate and view the first fund for a given address"""
        if address is None:
            return None
        try:
            await self.apply_rate_limit('simulate_view_first_fund')
            # logger.debug(f"Simulating first fund for address: {address}")
            result = await self._make_rpc_request(
                self.ENDPOINTS['simulate_view_first_fund']['method'],
                [address]
            )
            # logger.debug(f"Got simulation result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error simulating first fund for {address}: {str(e)}")
            return None

    async def simulate_txs(self, txs: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Simulate and view the first fund for a given address"""
        try:
            await self.apply_rate_limit('simulate_txs')
            # logger.debug(f"Simulating first fund for address: {address}")
            result = await self._make_rpc_request(
                self.ENDPOINTS['simulate_txs']['method'],
                [txs]
            )
            # logger.debug(f"Got simulation result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error simulating txs: {str(e)}")
            return None
        
    async def simulate_tx(
        self,
        block_number: int,
        block_index: int,
        no_base_fee: bool = False,
        skip_account_check: bool = False,
        skip_balance_check: bool = False,
        debug: bool = False,
        preimage: bool = True,
        custom_codes: Optional[List[Dict[str, str]]] = None,
        tx_type: int = 2,
        from_address: str = None,
        to_address: str = None,
        gas_fee_cap: Any = None,
        gas_tip_cap: Any = None,
        gas: int = None,
        value: Any = None,
        data: str = "0x"
    ) -> Optional[Dict[str, Any]]:
        """Simulate a transaction with specific parameters
        
        Args:
            block_number: Block number to simulate at
            block_index: Transaction index in block
            no_base_fee: Whether to skip base fee check
            skip_account_check: Whether to skip account existence check
            skip_balance_check: Whether to skip balance check
            debug: Enable debug mode
            preimage: Enable preimage mode
            custom_codes: List of custom contract codes to inject
            tx_type: Transaction type
            from_address: Sender address
            to_address: Recipient address
            gas_fee_cap: Maximum total fee per gas (int or hex string)
            gas_tip_cap: Maximum priority fee per gas (int or hex string)
            gas: Gas limit
            value: Transaction value in wei (int or hex string)
            data: Transaction input data
        
        Returns:
            Simulation result or None if failed
        """
        try:
            await self.apply_rate_limit('simulate_txs')

            # print(f"Simulating tx with params: {block_number}, {block_index}, {no_base_fee}, {skip_account_check}, {skip_balance_check}, {debug}, {preimage}, {custom_codes}, {tx_type}, {from_address}, {to_address}, {gas_fee_cap}, {gas_tip_cap}, {gas}, {value}, {data}")
            
            # Convert gas parameters to string if they're integers
            gas_fee_cap_str = str(gas_fee_cap) if isinstance(gas_fee_cap, int) else gas_fee_cap
            gas_tip_cap_str = str(gas_tip_cap) if isinstance(gas_tip_cap, int) else gas_tip_cap
            value_str = str(value) if isinstance(value, int) else value
            
            params = [{
                "Number": block_number,
                "Index": block_index,
                "NoBaseFee": no_base_fee,
                "SkipAccountCheck": skip_account_check, 
                "SkipBalanceCheck": skip_balance_check,
                "debug": debug,
                "preimage": preimage,
                "CustomCodes": custom_codes or []
            },
            [{
                "Type": tx_type,
                "From": from_address,
                "To": to_address,
                "GasFeeCap": gas_fee_cap_str,
                "GasTipCap": gas_tip_cap_str,
                "Gas": gas,
                "Value": value_str,
                "Data": data
            }]]
            
            result = await self._make_rpc_request(
                self.ENDPOINTS['simulate_txs']['method'],
                params
            )
            return result[0]
        except Exception as e:
            logger.error(f"Error simulating tx: {str(e)}")
            return None
            
    async def batch_simulate_view_first_fund(self, addresses: List[str]) -> List[Optional[Dict[str, Any]]]:
        """Process multiple addresses by making individual RPC calls
        
        This method makes separate RPC calls for each address and combines the results.
        For very large lists, consider using simulate_funds() which handles parallel processing.
        """
        if not addresses:
            return []
            
        results = []
        for address in addresses:
            await self.apply_rate_limit('simulate_view_first_fund')
            result = await self._make_rpc_request(
                self.ENDPOINTS['simulate_view_first_fund']['method'],
                [address]  # Pass single address as a list parameter
            )
            results.append(result if result is not None else None)
            
        return results

    async def simulate_funds(self,
                           addresses: List[str],
                           max_retries: int = 3) -> List[Dict[str, Any]]:
        """Process any number of addresses with automatic parallel batching
        
        For lists longer than 50 addresses, this method automatically splits them
        into parallel batches and combines the results.
        """
        try:
            # For small lists, use direct batch capability
            max_size = self.ENDPOINTS['simulate_view_first_fund']['max_batch_size']
            if len(addresses) <= max_size:
                return await self.batch_simulate_view_first_fund(addresses)

            # For larger lists, use parallel processing
            return await self.batch_executor.execute(
                items=[addresses[i:i + max_size] 
                      for i in range(0, len(addresses), max_size)],
                operation=self.batch_simulate_view_first_fund,
                rate_limiter=lambda: self.apply_rate_limit('simulate_view_first_fund')
            )
        except Exception as e:
            logger.error(f"Error in fund simulation: {str(e)}")
            return []
            
    def get_batch_stats(self) -> Dict[str, float]:
        """Get current batch processing statistics"""
        return self.batch_controller.metrics.get_stats()