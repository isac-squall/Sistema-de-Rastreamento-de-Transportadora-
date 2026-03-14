from typing import Any, Optional
import time
from core.config.settings import settings

class CacheEntry:
    """Entrada do cache com TTL"""
    def __init__(self, value: Any, ttl: int):
        self.value = value
        self.expires_at = time.time() + ttl

    def is_expired(self) -> bool:
        return time.time() > self.expires_at

class MemoryCache:
    """Cache em memória simples com TTL"""

    def __init__(self):
        self._cache: dict[str, CacheEntry] = {}
        self.max_size = settings.cache.max_size

    def get(self, key: str) -> Optional[Any]:
        """Obtém valor do cache"""
        if key in self._cache:
            entry = self._cache[key]
            if not entry.is_expired():
                return entry.value
            else:
                # Remover entrada expirada
                del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Define valor no cache"""
        if not settings.cache.enabled:
            return

        # Verificar limite de tamanho
        if len(self._cache) >= self.max_size:
            # Remover entradas expiradas
            self._cleanup_expired()

        ttl_value = ttl or settings.cache.ttl_seconds
        self._cache[key] = CacheEntry(value, ttl_value)

    def delete(self, key: str) -> None:
        """Remove valor do cache"""
        if key in self._cache:
            del self._cache[key]

    def clear(self) -> None:
        """Limpa todo o cache"""
        self._cache.clear()

    def _cleanup_expired(self) -> None:
        """Remove entradas expiradas"""
        expired_keys = [
            key for key, entry in self._cache.items()
            if entry.is_expired()
        ]
        for key in expired_keys:
            del self._cache[key]