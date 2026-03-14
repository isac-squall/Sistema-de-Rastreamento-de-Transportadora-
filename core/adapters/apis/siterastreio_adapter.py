import requests
from typing import Optional, Dict, Any, Tuple
from core.adapters.apis.base_api_adapter import BaseAPIAdapter
from core.domain.value_objects.tracking_code import TrackingCode
from core.utils.retry_policy import RetryPolicy
from core.utils.rate_limiter import RateLimiter
from core.adapters.cache.memory_cache import MemoryCache
from core.config.settings import settings

class SiteRastreioAdapter(BaseAPIAdapter):
    """Adapter para API do SiteRastreio"""

    def __init__(self):
        self.base_url = settings.api.base_url
        self.session = requests.Session()
        self.retry_policy = RetryPolicy()
        self.rate_limiter = RateLimiter(requests_per_minute=settings.api.rate_limit)
        self.cache = MemoryCache()

    def get_tracking_info(self, code: TrackingCode) -> Optional[Dict[str, Any]]:
        """Busca informações de rastreamento"""
        # Verificar cache primeiro
        cache_key = f"tracking_{code.value}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result

        # Aplicar rate limiting
        self.rate_limiter.wait_if_needed()

        # Fazer requisição com retry
        result = self.retry_policy.execute(
            lambda: self._make_request(code)
        )

        if result:
            # Salvar no cache
            self.cache.set(cache_key, result, ttl=settings.cache.ttl_seconds)

        return result

    def _make_request(self, code: TrackingCode) -> Optional[Dict[str, Any]]:
        """Faz a requisição HTTP"""
        try:
            url = f"{self.base_url}/{code.value}"
            response = self.session.get(url, timeout=settings.api.timeout)

            if response.status_code == 200:
                # Aqui seria o parsing do HTML/JSON da resposta
                # Por enquanto, retorna dados mockados
                return {
                    "codigo": str(code),
                    "status": "Em trânsito",
                    "ultima_atualizacao": "2024-01-15 10:30:00",
                    "detalhes": {
                        "origem": "São Paulo, SP",
                        "destino": "Rio de Janeiro, RJ",
                        "previsao_entrega": "2024-01-20"
                    }
                }
            else:
                return None

        except Exception as e:
            print(f"Erro na requisição: {e}")
            return None

    def test_connection(self) -> Tuple[bool, str]:
        """Testa conexão com a API"""
        try:
            # Tentar uma requisição simples
            response = self.session.get(self.base_url, timeout=10)
            if response.status_code == 200:
                return True, "Conexão OK"
            else:
                return False, f"Status code: {response.status_code}"
        except Exception as e:
            return False, f"Erro: {str(e)}"

    def supports_nf_lookup(self) -> bool:
        """Este adapter suporta busca por NF?"""
        return False