from dataclasses import dataclass
from core.config.settings import settings
from core.adapters.apis.siterastreio_adapter import SiteRastreioAdapter
from core.adapters.excel.excel_repository_impl import ExcelRepositoryImpl
from core.adapters.cache.memory_cache import MemoryCache
from core.utils.rate_limiter import RateLimiter
from core.utils.retry_policy import RetryPolicy

@dataclass
class ServiceContainer:
    """Container IoC para gerenciar dependências"""

    # Adapters
    api_adapter: SiteRastreioAdapter
    excel_repository: ExcelRepositoryImpl
    cache: MemoryCache

    # Utils
    rate_limiter: RateLimiter
    retry_policy: RetryPolicy

    @classmethod
    def create(cls) -> 'ServiceContainer':
        """Factory method para criar container com todas as dependências"""
        return cls(
            api_adapter=SiteRastreioAdapter(),
            excel_repository=ExcelRepositoryImpl(),
            cache=MemoryCache(),
            rate_limiter=RateLimiter(requests_per_minute=settings.api.rate_limit),
            retry_policy=RetryPolicy(max_retries=settings.api.retries)
        )