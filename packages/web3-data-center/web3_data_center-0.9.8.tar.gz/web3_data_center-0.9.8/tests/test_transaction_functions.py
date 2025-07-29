import pytest
from typing import List, Dict, Any, Optional
from web3_data_center.core.data_center import DataCenter

@pytest.mark.asyncio
async def test_sample_transactions():
    """Test sample_transactions with various filters"""
    async with DataCenter(config_path="config.yml") as data_center:
        # Test basic transaction sampling
        result = await data_center.sample_transactions(
            start_block=15000000,
            end_block=15000100,
            sample_size=5
        )
        assert isinstance(result, list)
        assert len(result) <= 5
        
        # Test with method filter
        transfer_result = await data_center.sample_transactions(
            start_block=15000000,
            end_block=15000100,
            sample_size=5,
            method_contains="transfer"
        )
        assert all("transfer" in tx.get("method", "").lower() for tx in transfer_result)

@pytest.mark.asyncio
async def test_get_specific_txs():
    """Test get_specific_txs functionality"""
    async with DataCenter(config_path="config.yml") as data_center:
        # Test with Uniswap V2 Router
        uniswap_v2 = "0x7a250d5630b4cf539739df2c5dacb4c659f2488d"
        
        result = await data_center.get_specific_txs(
            uniswap_v2,
            start_block=15000000,
            end_block=15000100
        )
        assert isinstance(result, list)
        assert all(isinstance(tx, dict) for tx in result)
        
        # Test with invalid address
        invalid_result = await data_center.get_specific_txs(
            "0xinvalid",
            start_block=15000000,
            end_block=15000100
        )
        assert len(invalid_result) == 0

@pytest.mark.asyncio
async def test_get_deployed_contracts():
    """Test get_deployed_contracts for known deployers"""
    async with DataCenter(config_path="config.yml") as data_center:
        # Test with a known contract deployer
        deployer = "0x3cD751E6b0078Be393132286c442345e5DC49699"  # Example deployer
        
        result = await data_center.get_deployed_contracts(deployer, chain='eth')
        assert isinstance(result, list)
        assert all(isinstance(contract, dict) for contract in result)
        
        if result:
            contract = result[0]
            assert 'address' in contract
            assert 'deployedBlock' in contract

@pytest.mark.asyncio
async def test_get_deployed_block():
    """Test get_deployed_block for known contracts"""
    async with DataCenter(config_path="config.yml") as data_center:
        # Test with USDT contract
        usdt = "0xdac17f958d2ee523a2206206994597c13d831ec7"
        
        block = await data_center.get_deployed_block(usdt, chain='eth')
        assert isinstance(block, int)
        assert block > 0
        
        # Test with invalid contract
        invalid_block = await data_center.get_deployed_block("0xinvalid", chain='eth')
        assert invalid_block is None

@pytest.mark.asyncio
async def test_is_contract():
    """Test is_contract detection"""
    async with DataCenter(config_path="config.yml") as data_center:
        # Test known contracts
        contracts = [
            "0xdac17f958d2ee523a2206206994597c13d831ec7",  # USDT
            "0x7a250d5630b4cf539739df2c5dacb4c659f2488d"   # Uniswap V2 Router
        ]
        
        for contract in contracts:
            result = await data_center.is_contract(contract, chain='eth')
            assert result is True
        
        # Test known EOA
        eoa = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"  # Example EOA
        eoa_result = await data_center.is_contract(eoa, chain='eth')
        assert eoa_result is False

@pytest.mark.asyncio
async def test_is_contract_batch():
    """Test batch contract detection"""
    async with DataCenter(config_path="config.yml") as data_center:
        addresses = [
            "0xdac17f958d2ee523a2206206994597c13d831ec7",  # USDT (contract)
            "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",  # EOA
            "0x7a250d5630b4cf539739df2c5dacb4c659f2488d"   # Uniswap V2 Router (contract)
        ]
        
        results = await data_center.is_contract_batch(addresses, chain='eth')
        assert len(results) == len(addresses)
        assert results[0] is True   # USDT
        assert results[1] is False  # EOA
        assert results[2] is True   # Uniswap
