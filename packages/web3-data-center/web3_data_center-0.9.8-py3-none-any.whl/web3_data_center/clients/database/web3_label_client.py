from typing import Dict, Any, List, Optional, Union
import logging
import re
import asyncio
from datetime import datetime
import asyncpg
from .pg_client import PGClient

logger = logging.getLogger(__name__)

class Web3LabelClient(PGClient):
    """Client for managing web3 address labels in the database
    
    Provides functionality for:
    - Adding/updating address labels
    - Querying labels by address
    - Managing label categories and types
    - Batch label operations
    """
    
    def __init__(self,
                 config_path: str = "config.yml",
                 pool_size: int = 5,
                 max_overflow: int = 10,
                 db_name: str = "labels"):
        """Initialize Web3LabelClient
        
        Args:
            config_path: Path to config file
            pool_size: Initial size of the connection pool
            max_overflow: Maximum number of connections beyond pool_size
            db_name: Database name in config
        """
        self.db_name = db_name  # Set db_name before parent initialization
        super().__init__(
            db_name=db_name,
            config_path=config_path,
            pool_size=pool_size,
            max_overflow=max_overflow
        )
        self._pool = None
        self._address_pattern = re.compile(r'^0x[a-fA-F0-9]{40}$')
        self._initialization_task = None
        
        # Start initialization task if we're in an event loop
        try:
            loop = asyncio.get_running_loop()
            self._initialization_task = loop.create_task(self.setup())
        except RuntimeError:
            # Not in an event loop, initialization will happen on first use
            pass



    def _validate_address(self, address: str) -> bool:
        """Validate ethereum address format
        
        Args:
            address: Ethereum address to validate
            
        Returns:
            bool: True if valid address format
        """
        return bool(self._address_pattern.match(address))

    async def __getattr__(self, name):
        """Override __getattr__ to ensure lazy loading of the connection pool."""
        if name == "_pool" and self._pool is None:
            await self.setup()  # Use parent's setup method to initialize pool
        # Return the actual attribute value
        return object.__getattribute__(self, name)


    async def get_supported_chains(self) -> List[str]:
        """Get all supported chains"""
        query = """
        SELECT DISTINCT chain_id
        FROM multi_chain_addresses
        LIMIT 1
        """
        return await self.execute(query)


    async def get_addresses_by_label(self,
                                   label: str,
                                   category: Optional[str] = None,
                                   min_confidence: float = 0.0) -> List[Dict[str, Any]]:
        """Get all addresses with a specific label
        
        Args:
            label: Label text to search for
            category: Optional category filter
            min_confidence: Minimum confidence threshold
            
        Returns:
            List[Dict]: List of address records with matching label
        """

        query = """
        SELECT address, label, category, source, confidence, metadata, created_at, updated_at
        FROM address_labels
        WHERE label ILIKE $1
        AND confidence >= $2
        """
        params = [f"%{label}%", min_confidence]
        
        if category:
            query += " AND category = $3"
            params.append(category)
            
        query += " ORDER BY confidence DESC, updated_at DESC"
        
        try:
            return await self.execute(query, *params)
        except Exception as e:
            logger.error(f"Error fetching addresses for label {label}: {str(e)}")
            return []

    async def delete_label(self,
                          address: str,
                          label: Optional[str] = None,
                          category: Optional[str] = None) -> bool:
        pass

    async def get_categories(self) -> List[str]:
        """Get all unique label categories
        
        Returns:
            List[str]: List of category names
        """
        query = "SELECT DISTINCT category FROM multi_entity ORDER BY category"
        try:
            results = await self.execute(query)
            return [r['category'] for r in results]
        except Exception as e:
            logger.error(f"Error fetching categories: {str(e)}")
            return []

    async def get_addresses_labels(self, addresses: List[str]) -> List[Dict[str, Any]]:
        """Get labels for multiple addresses
        
        Args:
            addresses: List of addresses to get labels for

        Returns:
            List of label info dicts for each address
        """
        if not addresses:
            return []

        # Normalize addresses
        addresses = [addr.lower() for addr in addresses if self._address_pattern.match(addr)]
        if not addresses:
            return []

        # Pool initialization is handled by PGClient.ensure_pool_ready()

        # Query labels
        query = """
            SELECT 
                mca.address,
                me.entity,
                me.category AS type,
                mca.name_tag,
                mca.entity,
                mca.labels,
                mca.is_ca,
                mca.is_seed
            FROM multi_chain_addresses mca
            LEFT JOIN multi_entity me ON mca.entity = me.entity
            WHERE mca.chain_id = 0 AND mca.address = ANY($1::text[])
        """
        
        try:
            rows = await self.execute(query, [addresses])
            
            # Process results
            results = []
            seen_addresses = set()
            for row in rows:
                type_str = row['type'] if row['type'] is not None else ''
                addr = row['address']
                seen_addresses.add(addr)
                results.append({
                    'address': addr,
                    'label': row['labels'].split(',')[0] if row['labels'] else None,  # Use first label as primary
                    'name_tag': row['name_tag'],
                    'type': type_str,
                    'entity': row['entity'],
                    'is_cex': 'CEX' in type_str.upper() or 'EXCHANGE' in type_str.upper()
                })
                
            # Add empty results for addresses without labels
            for addr in addresses:
                if addr not in seen_addresses:
                    results.append({
                        'address': addr,
                        'label': None,
                        'name_tag': None,
                        'type': None,
                        'entity': None,
                        'is_cex': False
                    })
                    
            return results
            
        except Exception as e:
            logger.error(f"Error getting labels for addresses: {str(e)}")
            return [{
                'address': addr,
                'label': None,
                'name_tag': None,
                'type': None,
                'entity': None,
                'is_cex': False
            } for addr in addresses]
            
    async def get_entity_info(self, entity: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific entity
        
        Args:
            entity: Entity name to get info for
            
        Returns:
            Dict containing entity information or None if not found
        """
        query = """
            SELECT 
                entity,
                category AS type
            FROM multi_entity
            WHERE entity = $1
        """
        
        try:
            result = await self.execute(query, [entity])
            if result:
                return result[0]
            return None
        except Exception as e:
            logger.error(f"Error getting entity info: {str(e)}")
            return None

    async def get_addresses_by_label(self, label: str, chain_id: int = 1, limit = 100) -> List[Dict[str, Any]]:
        """Find addresses by label
        
        Args:
            label: Label text to search for
            chain_id: Chain ID (default: 1 for Ethereum mainnet)
            
        Returns:
            List of address info dictionaries
            
        Raises:
            ValueError: If label is invalid
        """
        if not label or not isinstance(label, str):
            raise ValueError("Label must be a non-empty string")
            
        query = """
            WITH filtered_data AS (
                SELECT mca.address, mca.name_tag, mca.labels, mca.is_ca, mca.is_seed, mca.entity
                FROM multi_chain_addresses mca
                WHERE mca.chain_id = $1
                AND mca.labels ILIKE $2
                ORDER BY mca.address DESC  -- 随机调整顺序，避免 bias
                LIMIT $3 * 10  -- 先取 10 倍数据
            )
            SELECT 
                fd.address,
                fd.name_tag,
                fd.labels,
                fd.is_ca,
                fd.is_seed,
                me.category AS type,
                me.entity
            FROM filtered_data fd
            LEFT JOIN multi_entity me ON fd.entity = me.entity
            ORDER BY random()
            LIMIT $3;
        """
        
        try:
            rows = await self.execute(query, [0 if chain_id == 1 else chain_id, f"%{label}%", limit])
            
            results = []
            for row in rows:
                type_str = row['type'] if row['type'] is not None else ''
                results.append({
                    'address': row['address'],
                    'name_tag': row['name_tag'] or '',
                    'labels': row['labels'].split(',') if row['labels'] else [],
                    'is_contract': bool(row['is_ca']),
                    'is_seed': bool(row['is_seed']),
                    'type': type_str,
                    'entity': row['entity'],
                    'is_cex': 'CEX' in type_str.upper() or 'EXCHANGE' in type_str.upper()
                })
            return results
            
        except Exception as e:
            logger.error(f"Error getting addresses by label: {str(e)}")
            return []