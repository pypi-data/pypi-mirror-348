import pytest
import pytest_asyncio
from web3_data_center.core.data_center import DataCenter

@pytest_asyncio.fixture
async def data_center():
    """Fixture to create and cleanup DataCenter instance"""
    dc = DataCenter(config_path="config.yml")
    yield dc
    await dc.close()  # This will close all clients and sessions

@pytest.mark.asyncio
async def test_get_address_labels_empty(data_center):
    """Test get_address_labels with empty input"""
    result = await data_center.get_address_labels([])
    assert result == []

@pytest.mark.asyncio
async def test_get_address_labels_invalid(data_center):
    """Test get_address_labels with invalid addresses"""
    invalid_addresses = [
        "not_an_address",
        "0x123",  # Too short
        "0xinvalid",
        "1234567890",
        "0x123456789012345678901234567890123456789g"  # Invalid hex
    ]
    result = await data_center.get_address_labels(invalid_addresses)
    assert isinstance(result, list)
    assert len(result) == 0, "Invalid addresses should return empty list"

@pytest.mark.asyncio
async def test_get_address_labels_with_samples(data_center):
    """Test get_address_labels with sampled addresses"""
    # Known contract addresses by category
    stablecoin_addresses = [
        "0xdac17f958d2ee523a2206206994597c13d831ec7",  # USDT
        "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC
        "0x6b175474e89094c44da98b954eedeac495271d0f"   # DAI
    ]
    
    defi_protocol_addresses = [
        "0x7a250d5630b4cf539739df2c5dacb4c659f2488d",  # Uniswap V2 Router
        "0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45"   # Uniswap V3 Router
    ]
    
    lending_protocol_addresses = [
        "0x7d2768de32b0b80b7a3454c06bdac94a69ddc7a9",  # Aave V2 Lending Pool
        "0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b"   # Compound Comptroller
    ]
    
    # Get some regular addresses from recent blocks
    regular_addresses = await data_center.sample_addresses(
        sample_size=50,
        address_type='from',
        block_range=(15000000, 15100000)
    )
    
    # Combine all addresses
    all_addresses = (
        stablecoin_addresses +
        defi_protocol_addresses +
        lending_protocol_addresses +
        regular_addresses
    )
    
    # Get labels for all addresses
    result = await data_center.get_address_labels(all_addresses)
    
    # Verify structure of results
    assert isinstance(result, list)
    assert len(result) > 0, "Should get at least some labels"
    
    # Create lookup dict for results
    result_dict = {item["address"].lower(): item for item in result}
    
    # Test stablecoin contracts
    labeled_stablecoins = 0
    for addr in stablecoin_addresses:
        addr_lower = addr.lower()
        if addr_lower in result_dict:
            labels = result_dict[addr_lower]
            if any([labels["entity"], labels["type"], labels["name_tag"]]):
                labeled_stablecoins += 1
    assert labeled_stablecoins > 0, "At least one stablecoin should have labels"
    
    # Test DeFi protocol contracts
    labeled_defi = 0
    for addr in defi_protocol_addresses:
        addr_lower = addr.lower()
        if addr_lower in result_dict:
            labels = result_dict[addr_lower]
            if any([labels["entity"], labels["type"], labels["name_tag"]]):
                labeled_defi += 1
    assert labeled_defi > 0, "At least one DeFi protocol should have labels"
    
    # Test lending protocol contracts
    labeled_lending = 0
    for addr in lending_protocol_addresses:
        addr_lower = addr.lower()
        if addr_lower in result_dict:
            labels = result_dict[addr_lower]
            if any([labels["entity"], labels["type"], labels["name_tag"]]):
                labeled_lending += 1
    assert labeled_lending > 0, "At least one lending protocol should have labels"

@pytest.mark.asyncio
async def test_get_address_labels_chain_id(data_center):
    """Test get_address_labels with different chain IDs"""
    # Known addresses that exist on multiple chains
    eth_bsc_addresses = {
        # Stablecoins
        "USDT": {
            "eth": "0xdac17f958d2ee523a2206206994597c13d831ec7",  # USDT on ETH
            "bsc": "0x55d398326f99059ff775485246999027b3197955"   # USDT on BSC
        }
    }
    
    # Get all ETH and BSC addresses
    eth_addresses = [info["eth"] for info in eth_bsc_addresses.values()]
    bsc_addresses = [info["bsc"] for info in eth_bsc_addresses.values()]
    
    # Test with different chain IDs
    result_eth = await data_center.get_address_labels(eth_addresses, chain_id=1)  # Ethereum mainnet
    result_bsc = await data_center.get_address_labels(bsc_addresses, chain_id=56)  # BSC
    
    assert isinstance(result_eth, list)
    assert isinstance(result_bsc, list)
    
    # At least ETH chain should have labels
    assert len(result_eth) > 0, "Should get ETH chain labels"
    
    # Create lookup dicts
    eth_labels = {r["address"].lower(): r for r in result_eth}
    bsc_labels = {r["address"].lower(): r for r in result_bsc}
    
    # Verify USDT has labels on ETH
    eth_usdt = eth_bsc_addresses["USDT"]["eth"].lower()
    eth_label = eth_labels.get(eth_usdt, {})
    assert any([eth_label.get("entity"), eth_label.get("type"), eth_label.get("name_tag")]), \
        f"USDT on ETH ({eth_usdt}) should have labels"

@pytest.mark.asyncio
async def test_get_address_labels_batch_size(data_center):
    """Test get_address_labels with different batch sizes"""
    # Generate a large list of addresses
    known_addresses = [
        "0xdac17f958d2ee523a2206206994597c13d831ec7",  # USDT
        "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC
        "0x6b175474e89094c44da98b954eedeac495271d0f"   # DAI
    ]
    
    # Sample additional addresses
    sampled_addresses = await data_center.sample_addresses(
        sample_size=50,
        block_range=(15000000, 15100000)
    )
    
    all_addresses = known_addresses + sampled_addresses
    
    # Test with different batch sizes
    for batch_size in [1, 10, 100]:
        batch = all_addresses[:batch_size]
        result = await data_center.get_address_labels(batch)
        
        assert isinstance(result, list)
        assert len(result) <= batch_size, f"Result size should not exceed batch size {batch_size}"
        
        # Verify structure of results
        for item in result:
            assert isinstance(item, dict)
            assert "address" in item
            assert isinstance(item["address"], str)
            assert item["address"].lower() in [addr.lower() for addr in batch]
            
            # These fields should exist
            assert "entity" in item
            assert "type" in item
            assert "name_tag" in item
