"""
Cache Manager (In-memory)
"""
from typing import Optional, Any
from datetime import datetime, timedelta
from app.config import settings
import threading


class CacheManager:
    """
    In-memory cache manager with TTL support
    """
    
    def __init__(self):
        self._cache = {}
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or expired
        """
        with self._lock:
            if key not in self._cache:
                return None
            
            entry = self._cache[key]
            
            # Check if expired
            if datetime.utcnow() > entry["expires_at"]:
                del self._cache[key]
                return None
            
            return entry["value"]
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (default: settings.CACHE_TTL)
        """
        if ttl is None:
            ttl = settings.CACHE_TTL
        
        expires_at = datetime.utcnow() + timedelta(seconds=ttl)
        
        with self._lock:
            self._cache[key] = {
                "value": value,
                "expires_at": expires_at
            }
    
    def delete(self, key: str) -> None:
        """
        Delete value from cache
        
        Args:
            key: Cache key
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
    
    def delete_pattern(self, pattern: str) -> None:
        """
        Delete all keys matching pattern
        
        Args:
            pattern: Key pattern (simple string matching)
        """
        with self._lock:
            keys_to_delete = [k for k in self._cache.keys() if pattern in k]
            for key in keys_to_delete:
                del self._cache[key]
    
    def clear(self) -> None:
        """Clear all cache"""
        with self._lock:
            self._cache.clear()


# Global cache instance
cache = CacheManager()
