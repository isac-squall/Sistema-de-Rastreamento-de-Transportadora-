from typing import Optional, Dict, Any
import time
from threading import Lock

class MemoryCache:
    """Cache em memória com TTL e limite de tamanho"""

    def __init__(self, ttl_seconds: int = 3600, max_size_mb: int = 100):
        self.ttl_seconds = ttl_seconds
        self.max_size_bytes = max_size_mb * 1024 * 1024  # Converter para bytes
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()
        self._current_size = 0

    def get(self, key: str) -> Optional[Any]:
        """Recupera valor do cache se não expirou"""
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                if time.time() < entry['expires_at']:
                    return entry['value']
                else:
                    # Remover entrada expirada
                    del self._cache[key]
            return None

    def set(self, key: str, value: Any) -> None:
        """Armazena valor no cache"""
        with self._lock:
            # Estimar tamanho (aproximado)
            value_size = len(str(value).encode('utf-8'))

            # Se excede tamanho máximo, não armazenar
            if self._current_size + value_size > self.max_size_bytes:
                return

            expires_at = time.time() + self.ttl_seconds

            # Se chave já existe, ajustar tamanho
            if key in self._cache:
                old_size = len(str(self._cache[key]['value']).encode('utf-8'))
                self._current_size -= old_size

            self._cache[key] = {
                'value': value,
                'expires_at': expires_at
            }
            self._current_size += value_size

    def delete(self, key: str) -> None:
        """Remove chave do cache"""
        with self._lock:
            if key in self._cache:
                value_size = len(str(self._cache[key]['value']).encode('utf-8'))
                self._current_size -= value_size
                del self._cache[key]

    def clear(self) -> None:
        """Limpa todo o cache"""
        with self._lock:
            self._cache.clear()
            self._current_size = 0

    def size(self) -> int:
        """Retorna número de entradas no cache"""
        with self._lock:
            return len(self._cache)