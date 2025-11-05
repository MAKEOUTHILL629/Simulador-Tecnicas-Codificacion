"""
Cache manager for storing and retrieving simulation results.

Provides intelligent caching to avoid re-running identical simulations.
"""

import pickle
import hashlib
import json
import os
from typing import Any, Dict, Optional
from pathlib import Path


class CacheManager:
    """
    Manages caching of simulation results to disk.
    
    Uses configuration hashing to determine cache hits/misses.
    """
    
    def __init__(self, cache_dir: str = "./cache"):
        """
        Initialize cache manager.
        
        Args:
            cache_dir: Directory to store cached results
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _config_hash(self, config: Dict) -> str:
        """
        Generate hash of configuration for cache key.
        
        Args:
            config: Configuration dictionary
        
        Returns:
            Hash string
        """
        # Sort keys for consistent hashing
        config_str = json.dumps(config, sort_keys=True)
        return hashlib.md5(config_str.encode()).hexdigest()
    
    def get(self, config: Dict, data_hash: Optional[str] = None) -> Optional[Any]:
        """
        Retrieve cached result if available.
        
        Args:
            config: Configuration dictionary
            data_hash: Optional hash of data (for data-specific caching)
        
        Returns:
            Cached result or None if not found
        """
        cache_key = self._config_hash(config)
        if data_hash:
            cache_key = f"{cache_key}_{data_hash}"
        
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Warning: Failed to load cache: {e}")
                return None
        
        return None
    
    def set(self, config: Dict, result: Any, data_hash: Optional[str] = None):
        """
        Store result in cache.
        
        Args:
            config: Configuration dictionary
            result: Result to cache
            data_hash: Optional hash of data
        """
        cache_key = self._config_hash(config)
        if data_hash:
            cache_key = f"{cache_key}_{data_hash}"
        
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(result, f)
        except Exception as e:
            print(f"Warning: Failed to save cache: {e}")
    
    def clear(self):
        """Clear all cached results."""
        for cache_file in self.cache_dir.glob("*.pkl"):
            cache_file.unlink()
    
    def get_cache_size(self) -> int:
        """
        Get total size of cache in bytes.
        
        Returns:
            Cache size in bytes
        """
        total_size = 0
        for cache_file in self.cache_dir.glob("*.pkl"):
            total_size += cache_file.stat().st_size
        return total_size
    
    def get_cache_count(self) -> int:
        """
        Get number of cached results.
        
        Returns:
            Number of cache files
        """
        return len(list(self.cache_dir.glob("*.pkl")))
