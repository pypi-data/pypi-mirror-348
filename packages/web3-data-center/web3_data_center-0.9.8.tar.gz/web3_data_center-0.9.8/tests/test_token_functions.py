import pytest
import datetime
from typing import Optional, List, Dict, Any
from web3_data_center.core.data_center import DataCenter
from web3_data_center.models.token import Token, RankedToken

@pytest.mark.asyncio
async def test_get_token_info():
    """Test get_token_info with known tokens"""
    async with DataCenter(config_path="config.yml") as data_center:
        # Test with USDT on Ethereum
        usdt_eth = "0xdac17f958d2ee523a2206206994597c13d831ec7"
        result = await data_center.get_token_info(usdt_eth, chain='eth')
        assert result is not None
        assert isinstance(result, Token)
        assert result.address.lower() == usdt_eth.lower()
        assert result.symbol == "USDT"
        
        # Test with invalid address
        invalid_result = await data_center.get_token_info("0xinvalid", chain='eth')
        assert invalid_result is None

@pytest.mark.asyncio
async def test_get_token_price_at_time():
    """Test get_token_price_at_time with various scenarios"""
    async with DataCenter(config_path="config.yml") as data_center:
        usdt_eth = "0xdac17f958d2ee523a2206206994597c13d831ec7"
        current_time = datetime.datetime.now()
        
        # Test current price
        result = await data_center.get_token_call_performance(usdt_eth, current_time, chain='eth')
        assert isinstance(result, tuple)
        assert len(result) == 3
        assert isinstance(result[0], str)  # Token symbol
        assert isinstance(result[1], float)  # Price
        assert isinstance(result[2], float)  # Market cap

@pytest.mark.asyncio
async def test_get_price_history():
    """Test get_price_history with different intervals"""
    async with DataCenter(config_path="config.yml") as data_center:
        usdt_eth = "0xdac17f958d2ee523a2206206994597c13d831ec7"
        
        # Test with default parameters
        result = await data_center.get_price_history(usdt_eth, chain='eth')
        assert isinstance(result, list)
        assert all(isinstance(point, dict) for point in result)
        if result:
            point = result[0]
            assert 'timestamp' in point
            assert 'price' in point
        
        # Test with custom interval and limit
        custom_result = await data_center.get_price_history(
            usdt_eth, 
            chain='eth',
            interval='1h',
            limit=10
        )
        assert len(custom_result) <= 10
        assert all(isinstance(point, dict) for point in custom_result)

@pytest.mark.asyncio
async def test_get_top_holders():
    """Test get_top_holders functionality"""
    async with DataCenter(config_path="config.yml") as data_center:
        usdt_eth = "0xdac17f958d2ee523a2206206994597c13d831ec7"
        
        result = await data_center.get_top_holders(usdt_eth, chain='eth', limit=10)  # Using valid limit
        assert isinstance(result, list)
        assert len(result) <= 10
        assert all(isinstance(holder, dict) for holder in result)
        
        # Verify holder data structure
        if result:
            holder = result[0]
            assert 'address' in holder
            assert 'balance' in holder
            assert isinstance(holder['address'], str)
            assert isinstance(holder['balance'], (int, float))

@pytest.mark.asyncio
async def test_get_hot_tokens():
    """Test get_hot_tokens across different chains"""
    async with DataCenter(config_path="config.yml") as data_center:
        # Test Ethereum hot tokens
        eth_result = await data_center.get_hot_tokens(chain='eth', limit=10)
        assert isinstance(eth_result, list)
        assert len(eth_result) <= 10
        assert all(isinstance(token, RankedToken) for token in eth_result)
        
        # Test Solana hot tokens
        sol_result = await data_center.get_hot_tokens(chain='sol', limit=10)
        assert isinstance(sol_result, list)
        assert len(sol_result) <= 10
        assert all(isinstance(token, RankedToken) for token in sol_result)
