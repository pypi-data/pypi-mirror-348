"""Base cache manager interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

CacheKeyType = str
CacheValueType = Any


class CacheManager(ABC):
    """Base class for cache managers."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the cache manager.

        Args:
            config: Cache-specific configuration.
        """
        self.config = config or {}

    @abstractmethod
    def get(self, key: CacheKeyType) -> Optional[CacheValueType]:
        """Get a value from the cache.

        Args:
            key: The cache key.

        Returns:
            The cached value, or None if the key is not in the cache.
        """
        pass

    @abstractmethod
    def set(self, key: CacheKeyType, value: CacheValueType) -> None:
        """Set a value in the cache.

        Args:
            key: The cache key.
            value: The value to cache.
        """
        pass

    @abstractmethod
    def delete(self, key: CacheKeyType) -> None:
        """Delete a value from the cache.

        Args:
            key: The cache key.
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear the cache."""
        pass

    @abstractmethod
    def contains(self, key: CacheKeyType) -> bool:
        """Check if a key is in the cache.

        Args:
            key: The cache key.

        Returns:
            True if the key is in the cache, False otherwise.
        """
        pass