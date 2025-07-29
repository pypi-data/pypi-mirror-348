import os
import pickle
import time
import hashlib
import functools
import tempfile
import shutil
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar, Dict

from ..utils.logger import get_logger

logger = get_logger(__name__)

T = TypeVar('T')

def get_cache_dir() -> Path:
    """Get the cache directory path."""
    cache_dir = Path.home() / '.web3_data_center' / 'cache'
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir

def make_cache_key(*args, **kwargs) -> str:
    """Create a cache key from function arguments."""
    # Convert args and kwargs to a string representation
    key_parts = []
    
    # Skip the first argument (self) if it's an object instance
    for i, arg in enumerate(args):
        if i == 0 and hasattr(arg, '__class__'):
            # For the first argument (likely 'self'), use the class name instead of the instance
            key_parts.append(arg.__class__.__name__)
        else:
            key_parts.append(str(arg))
    
    key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
    key_str = "|".join(key_parts)
    
    # Create a hash of the key string
    hash_key = hashlib.md5(key_str.encode()).hexdigest()
    logger.debug(f"Cache key generated: {hash_key} from key_str: {key_str}")
    return hash_key

def file_cache(
    namespace: str,
    ttl: Optional[int] = None,
    max_entries: Optional[int] = 1000
):
    """
    A file-based caching decorator for async functions.
    
    Args:
        namespace: Namespace for the cache (used in filename)
        ttl: Time to live in seconds (default: None, meaning no expiration)
        max_entries: Maximum number of entries in cache file (default: 1000)
    """
    cache_dir = get_cache_dir()
    cache_file = cache_dir / f"{namespace}_cache.pkl"
    
    def load_cache() -> Dict[str, Any]:
        """Load cache from file."""
        try:
            if cache_file.exists():
                with open(cache_file, 'rb') as f:
                    try:
                        return pickle.load(f)
                    except (EOFError, pickle.UnpicklingError) as e:
                        logger.error(f"Corrupted cache file detected: {e}")
                        # Backup the corrupted file for debugging
                        backup_file = cache_file.with_suffix('.corrupted')
                        try:
                            shutil.copy(cache_file, backup_file)
                            logger.info(f"Backed up corrupted cache to {backup_file}")
                        except Exception:
                            pass
                        # Remove the corrupted file
                        try:
                            os.remove(cache_file)
                            logger.info(f"Removed corrupted cache file: {cache_file}")
                        except Exception:
                            pass
                        return {}
            return {}
        except Exception as e:
            logger.error(f"Error loading cache: {e}")
            return {}
    
    def save_cache(cache: Dict[str, Any]):
        """Save cache to file safely using atomic write."""
        if not cache:  # Don't save empty cache
            return
            
        try:
            # Create a temporary file in the same directory
            cache_dir.mkdir(parents=True, exist_ok=True)
            fd, temp_path = tempfile.mkstemp(dir=cache_dir)
            
            # Write to the temporary file
            with os.fdopen(fd, 'wb') as temp_file:
                pickle.dump(cache, temp_file, protocol=pickle.HIGHEST_PROTOCOL)
            
            # Atomic rename to the target file
            shutil.move(temp_path, cache_file)
            logger.debug(f"Cache saved successfully to {cache_file}")
        except Exception as e:
            logger.error(f"Error saving cache: {e}")
            # Try to remove the temp file if it exists
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except Exception:
                pass
    
    def clean_expired(cache: Dict[str, Any]):
        """Remove expired entries."""
        if not ttl:
            return cache
            
        current_time = time.time()
        return {
            k: v for k, v in cache.items()
            if v.get('timestamp', 0) + ttl > current_time
        }
    
    def clean_overflow(cache: Dict[str, Any]):
        """Remove oldest entries if cache exceeds max size."""
        if not max_entries or len(cache) <= max_entries:
            return cache
            
        # Sort by timestamp and keep only the newest max_entries
        sorted_items = sorted(
            cache.items(),
            key=lambda x: x[1].get('timestamp', 0),
            reverse=True
        )
        return dict(sorted_items[:max_entries])
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        _cache = {}  # In-memory cache
        _last_clean = 0  # Last time cache was cleaned
        _last_save = 0  # 初始化上次保存时间
        _update_count = 0  # 初始化更新计数器
        _clean_interval = 300  # Clean every 5 minutes
        
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            nonlocal _cache, _last_clean, _last_save, _update_count
            current_time = time.time()
            
            # Generate cache key
            key = make_cache_key(*args, **kwargs)
            
            # Load cache if empty
            if not _cache:
                # logger.info(f"Loading cache from file: {cache_file}")
                loaded_cache = load_cache()
                _cache.update(loaded_cache)
                # logger.info(f"Loaded {len(loaded_cache)} entries from cache file")
            
            # Periodically clean cache
            if current_time - _last_clean > _clean_interval:
                _cache = clean_expired(_cache)
                _cache = clean_overflow(_cache)
                save_cache(_cache)
                _last_clean = current_time
                _last_save = current_time  # 更新保存时间
                _update_count = 0  # 重置计数器
            
            # Check if we have a valid cached result
            # logger.info(f"Checking cache for key: {key[:8]}...")
            if key in _cache:
                # logger.info(f"Cache HIT for {func.__name__}: {key[:8]}")
                # 更新时间戳实现滑动过期（仅在内存中）
                _cache[key]['timestamp'] = current_time
                _update_count += 1
                
                # 只在达到一定更新次数或时间间隔后才保存
                if _update_count >= 50 or (current_time - _last_save > 300):  # 50次更新或5分钟
                    logger.debug(f"Saving cache after {_update_count} updates")
                    save_cache(_cache)
                    _last_save = current_time
                    _update_count = 0
                    
                return _cache[key]['data']
            
            # logger.info(f"Cache MISS for {func.__name__}: {key[:8]}")
            # Call the original function
            result = await func(*args, **kwargs)
            
            # Store result in cache
            _cache[key] = {
                'data': result,
                'timestamp': current_time
            }
            
            # 对于新缓存项，立即保存
            # logger.info(f"Saving result to cache: {key[:8]}")
            save_cache(_cache)
            _last_clean = current_time
            _last_save = current_time
            
            return result
        
        # Add clear cache method
        def clear_cache():
            nonlocal _cache, _last_clean
            _cache.clear()
            _last_clean = 0
            cache_file.unlink(missing_ok=True)
        
        wrapper.cache_clear = clear_cache
        return wrapper
    
    return decorator
