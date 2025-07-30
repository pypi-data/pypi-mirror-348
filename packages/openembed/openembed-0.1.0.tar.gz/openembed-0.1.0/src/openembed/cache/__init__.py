"""Caching mechanisms for embedding results."""

from openembed.cache.base import CacheManager
from openembed.cache.memory import MemoryCache
from openembed.cache.disk import DiskCache

__all__ = [
    "CacheManager",
    "MemoryCache",
    "DiskCache",
]