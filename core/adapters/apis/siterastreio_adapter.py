import requests
from typing import Optional, Dict, Any
from core.adapters.apis.base_api_adapter import BaseAPIAdapter
from core.domain.value_objects.tracking_code import TrackingCode
from core.utils.retry_policy import RetryPolicy
from core.utils.rate_limiter import RateLimiter
from core.adapters.cache.memory_cache import MemoryCache

class SiteRastreioAdapter(BaseAPIAdapter):
    def __init__(
        self,
        api_url: str,
        api_key: Optional[str],
        timeout: int,
        rate_limiter: RateLimiter,
        cache: MemoryCache,
        retry_policy: RetryPolicy
    ):
        self.api_url = api_url
        self.api_key = api_key
        self.timeout = timeout
        self.rate_limiter = rate_limiter
        self.cache = cache
        self.retry_policy = retry_policy

    def get_tracking_info(self, code: TrackingCode) -> Optional[Dict[str, Any]]:
        # Verificar cache primeiro
        cached = self.cache.get(f"tracking:{code}")
        if cached:
            print(f"Cache hit para {code}")
            return cached

        # Rate limiting
        self.rate_limiter.wait_if_needed()

        # Executar com retry policy
        result = self.retry_policy.execute(
            self._fetch_tracking,
            code
        )

        if result:
            self.cache.set(f"tracking:{code}", result)

        return result

    def _fetch_tracking(self, code: TrackingCode) -> Optional[Dict[str, Any]]:
        """Fetch real da API"""
        try:
            url = f"{self.api_url}/{code}"
            headers = self._prepare_headers()

            response = requests.get(
                url,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()

            return self._parse_response(response.json())

        except Exception as e:
            print(f"Erro ao consultar {code}: {e}")
            return None

    def _parse_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse e validação da resposta"""
        # Implementar schema validation com Pydantic
        return {
            'code': data.get('code'),
            'status': self._map_status(data.get('status')),
            'events': self._parse_events(data.get('events', []))
        }

    def _prepare_headers(self) -> Dict[str, str]:
        headers = {'User-Agent': 'Mozilla/5.0...'}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        return headers

    def _map_status(self, raw_status: str) -> str:
        # Usar enum do schema
        status_mapping = {
            'entregue': 'ENTREGUE',
            'em trânsito': 'EM_TRANSITO',
            # ...
        }
        return status_mapping.get(raw_status.lower(), 'ERRO')

    def _parse_events(self, events: list) -> list:
        """Parse eventos com validação"""
        parsed = []
        for event in events:
            try:
                # Usar TrackingEvent.from_dict quando implementado
                parsed.append(event)  # Temporário
            except Exception as e:
                print(f"Erro ao parsear evento: {e}")
        return parsed

    def test_connection(self) -> tuple[bool, str]:
        try:
            response = requests.get(
                self.api_url,
                timeout=5
            )
            return response.status_code == 200, "Conexão OK"
        except Exception as e:
            return False, str(e)

    def supports_nf_lookup(self) -> bool:
        return False  # SiteRastreio não suporta lookup por NF