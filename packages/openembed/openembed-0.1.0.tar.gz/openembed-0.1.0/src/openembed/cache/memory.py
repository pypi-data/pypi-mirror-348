"""In-memory cache implementation."""

import logging
import time
from typing import Any, Dict, List, Optional, Union

from openembed.cache.base import CacheManager, CacheKeyType, CacheValueType

logger = logging.getLogger(__name__)


class MemoryCache(CacheManager):
    """In-memory cache implementation."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the memory cache.

        Args:
            config: Configuration for the memory cache.
                Example: {
                    "max_size": 1000,  # Maximum number of items in the cache
                    "ttl": 3600,  # Time-to-live in seconds
                }
        """
        super().__init__(config)
        self.max_size = self.config.get("max_size", 1000)
        self.ttl = self.config.get("ttl")  # None means no expiration
        self.cache: Dict[CacheKeyType, Dict[str, Any]] = {}
        self.access_times: Dict[CacheKeyType, float] = {}

    def _is_expired(self, key: CacheKeyType) -> bool:
        """Check if a cache entry is expired.

        Args:
            key: The cache key.

        Returns:
            True if the entry is expired, False otherwise.
        """
        if self.ttl is None:
            return False
        
        last_access = self.access_times.get(key)
        if last_access is None:
            return True
        
        return time.time() - last_access > self.ttl

    def _evict_if_needed(self) -> None:
        """Evict items from the cache if it's full."""
        if len(self.cache) <= self.max_size:
            return
        
        # Evict the least recently used items
        items_to_evict = len(self.cache) - self.max_size
        if items_to_evict <= 0:
            return
        
        # Sort by access time (oldest first)
        sorted_keys = sorted(self.access_times.items(), key=lambda x: x[1])
        
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
        if key not in self.cache:
            return None
        
        if self._is_expired(key):
            self.delete(key)
            return None
        
        # Update access time
        self.access_times[key] = time.time()
        
        return self.cache[key]["value"]

    def set(self, key: CacheKeyType, value: CacheValueType) -> None:
        """Set a value in the cache.

        Args:
            key: The cache key.
            value: The value to cache.
        """
        # Evict items if needed
        self._evict_if_needed()
        
        # Store the value
        self.cache[key] = {"value": value}
        self.access_times[key] = time.time()

    def delete(self, key: CacheKeyType) -> None:
        """Delete a value from the cache.

        Args:
            key: The cache key.
        """
        if key in self.cache:
            del self.cache[key]
        
        if key in self.access_times:
            del self.access_times[key]

    def clear(self) -> None:
        """Clear the cache."""
        self.cache.clear()
        self.access_times.clear()

    def contains(self, key: CacheKeyType) -> bool:
        """Check if a key is in the cache.

        Args:
            key: The cache key.

        Returns:
            True if the key is in the cache, False otherwise.
        """
        if key not in self.cache:
            return False
        
        if self._is_expired(key):
            self.delete(key)
            return False
        
        return True