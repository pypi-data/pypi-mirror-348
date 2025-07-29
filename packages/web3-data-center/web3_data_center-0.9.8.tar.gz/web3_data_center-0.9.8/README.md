# Web3 Data Center

Web3 Data Center is a Python package that integrates multiple APIs to provide comprehensive blockchain data analysis capabilities. It offers a unified interface to access data from various sources, making it easier for developers to gather and analyze blockchain-related information.

## Features

- Integration with multiple blockchain data providers (GeckoTerminal, GMGN, Birdeye, Solscan, GoPlus, DexScreener)
- Asynchronous API calls for improved performance
- Persistent file-based caching system for optimized data retrieval
- Caching mechanism to reduce API calls and improve response times
- Support for multiple blockchains (Ethereum, Solana, and more)
- Token information retrieval (price, market cap, holders, etc.)
- Transaction analysis
- Token security checks

## Installation

You can install Web3 Data Center using pip:


```bash
pip install data_center
```



## Quick Start

Here's a simple example of how to use Web3 Data Center:
```python
import asyncio
from web3_data_center import DataCenter
async def main():
data_center = DataCenter()
# Get token info
token_address = "CzLSujWBLFsSjncfkh59rUFqvafWcY5tzedWJSuypump" # Wrapped SOL
token_info = await data_center.get_token_info(token_address)
print(f"Token Info: {token_info}")
# Get top holders
top_holders = await data_center.get_top_holders(token_address, limit=10)
print(f"Top 10 Holders: {top_holders}")
asyncio.run(main())
```


## Caching System

Web3 Data Center includes a robust file-based caching system to improve performance and reduce API calls. The cache is stored in `~/.web3_data_center/cache/` and is automatically managed.

### Cached Operations

The following operations are cached by default:
- Root funder lookups (24-hour cache)
- Funding path queries (24-hour cache)
- Funding relationship checks (24-hour cache)

### Using the Cache

The cache is automatically used when calling the relevant methods. You can also use the caching decorator for your own functions:

```python
from web3_data_center import file_cache

@file_cache(namespace="my_cache", ttl=3600)  # 1-hour cache
async def my_function():
    # Your code here
    pass
```

### Cache Management

To clear the cache for a specific function:
```python
data_center.get_root_funder.cache_clear()
```

To get the cache directory:
```python
from web3_data_center import get_cache_dir
cache_dir = get_cache_dir()
```

The cache automatically manages:
- Entry expiration (TTL-based)
- Size limits
- Cleanup of old entries

## Documentation

For detailed documentation, please refer to the [docs](./docs) directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all the API providers that make this project possible.
- Special thanks to the open-source community for their invaluable tools and libraries.

# Token Sniper Word Cloud Generator

This script analyzes token sniping data from a database and generates a beautiful word cloud visualization based on the frequency of snipes per token.

## Requirements

Install the required Python packages:

```bash
pip install pandas matplotlib wordcloud numpy sqlalchemy pillow
```

## Configuration

Before running the script, update the database connection parameters in `sniper_wordcloud.py`:

```python
# Database connection parameters
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "your_database"
```

## Usage

Run the script:

```bash
python sniper_wordcloud.py
```

The script will:
1. Connect to your database
2. Execute the SQL query to retrieve token sniping data
3. Generate a word cloud where:
   - Each word represents a token symbol (or shortened address if no symbol available)
   - The size of each word corresponds to its snipe count
   - A beautiful color gradient is applied to enhance visualization
4. Save the word cloud as `token_snipe_wordcloud.png`

## Customization

You can modify the script to change the:
- Word cloud shape (currently circular)
- Color scheme (edit the `colors` list)
- Background color (currently black)
- Maximum number of tokens to display
- Font sizes