"""Disk-based cache implementation."""

import json
import logging
import os
import pickle
import shutil
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from openembed.cache.base import CacheManager, CacheKeyType, CacheValueType

logger = logging.getLogger(__name__)


class DiskCache(CacheManager):
    """Disk-based cache implementation."""

    def __init__(self, cache_dir: str, config: Optional[Dict[str, Any]] = None):
        """Initialize the disk cache.

        Args:
            cache_dir: Directory to store cache files.
            config: Configuration for the disk cache.
                Example: {
                    "max_size": 1000,  # Maximum number of items in the cache
                    "ttl": 3600,  # Time-to-live in seconds
                }
        """
        super().__init__(config)
        self.cache_dir = Path(cache_dir)
        self.max_size = self.config.get("max_size", 1000)
        self.ttl = self.config.get("ttl")  # None means no expiration
        self.metadata_file = self.cache_dir / "metadata.json"
        
        # Create cache directory if it doesn't exist
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Load metadata if it exists
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> Dict[str, Dict[str, Any]]:
        """Load metadata from disk.

        Returns:
            The metadata dictionary.
        """
        if not self.metadata_file.exists():
            return {}
        
        try:
            with open(self.metadata_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Error loading cache metadata: {str(e)}")
            return {}

    def _save_metadata(self) -> None:
        """Save metadata to disk."""
        try:
            with open(self.metadata_file, "w") as f:
                json.dump(self.metadata, f)
        except Exception as e:
            logger.warning(f"Error saving cache metadata: {str(e)}")

    def _get_cache_path(self, key: CacheKeyType) -> Path:
        """Get the path to a cache file.

        Args:
            key: The cache key.

        Returns:
            The path to the cache file.
        """
        # Use a hash of the key as the filename to avoid invalid characters
        filename = str(hash(key))
        return self.cache_dir / filename

    def _is_expired(self, key: CacheKeyType) -> bool:
        """Check if a cache entry is expired.

        Args:
            key: The cache key.

        Returns:
            True if the entry is expired, False otherwise.
        """
        if self.ttl is None:
            return False
        
        metadata = self.metadata.get(key, {})
        last_access = metadata.get("last_access")
        if last_access is None:
            return True
        
        return time.time() - last_access > self.ttl

    def _evict_if_needed(self) -> None:
        """Evict items from the cache if it's full."""
        if len(self.metadata) <= self.max_size:
            return
        
        # Evict the least recently used items
        items_to_evict = len(self.metadata) - self.max_size
        if items_to_evict <= 0:
            return
        
        # Sort by access time (oldest first)
        sorted_keys = sorted(
            self.metadata.items(),
            key=lambda x: x[1].get("last_access", 0)
        )
        
        # Evict the oldest items
        for i in range(items_to_evict):
            if i < len(sorted_keys):
                key = sorted_keys[i][0]
                self.delete(key)
                logger.debug(f"Evicted cache key: {key}")

    def get(self, key: CacheKeyType) -> Optional[CacheValueType]:
        """Get a value from the cache.

        Args:
            key: The cache key.

        Returns:
            The cached value, or None if the key is not in the cache.
        """
        if key not in self.metadata:
            return None
        
        if self._is_expired(key):
            self.delete(key)
            return None
        
        cache_path = self._get_cache_path(key)
        if not cache_path.exists():
            # Metadata exists but file doesn't, clean up metadata
            self.delete(key)
            return None
        
        try:
            with open(cache_path, "rb") as f:
                value = pickle.load(f)
            
            # Update access time
            self.metadata[key] = {
                "last_access": time.time(),
                "size": os.path.getsize(cache_path)
            }
            self._save_metadata()
            
            return value
        except Exception as e:
            logger.warning(f"Error loading cache value: {str(e)}")
            self.delete(key)
            return None

    def set(self, key: CacheKeyType, value: CacheValueType) -> None:
        """Set a value in the cache.

        Args:
            key: The cache key.
            value: The value to cache.
        """
        # Evict items if needed
        self._evict_if_needed()
        
        cache_path = self._get_cache_path(key)
        
        try:
            with open(cache_path, "wb") as f:
                pickle.dump(value, f)
            
            # Update metadata
            self.metadata[key] = {
                "last_access": time.time(),
                "size": os.path.getsize(cache_path)
            }
            self._save_metadata()
        except Exception as e:
            logger.warning(f"Error saving cache value: {str(e)}")
            # Clean up if there was an error
            if cache_path.exists():
                try:
                    os.remove(cache_path)
                except:
                    pass

    def delete(self, key: CacheKeyType) -> None:
        """Delete a value from the cache.

        Args:
            key: The cache key.
        """
        if key in self.metadata:
            del self.metadata[key]
            self._save_metadata()
        
        cache_path = self._get_cache_path(key)
        if cache_path.exists():
            try:
                os.remove(cache_path)
            except Exception as e:
                logger.warning(f"Error deleting cache file: {str(e)}")

    def clear(self) -> None:
        """Clear the cache."""
        # Clear metadata
        self.metadata = {}
        self._save_metadata()
        
        # Delete all cache files
        try:
            for file in self.cache_dir.iterdir():
                if file.is_file() and file.name != "metadata.json":
                    os.remove(file)
        except Exception as e:
            logger.warning(f"Error clearing cache: {str(e)}")

    def contains(self, key: CacheKeyType) -> bool:
        """Check if a key is in the cache.

        Args:
            key: The cache key.

        Returns:
            True if the key is in the cache, False otherwise.
        """
        if key not in self.metadata:
            return False
        
        if self._is_expired(key):
            self.delete(key)
            return False
        
        cache_path = self._get_cache_path(key)
        if not cache_path.exists():
            self.delete(key)
            return False
        
        return True