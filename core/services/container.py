from dataclasses import dataclass
from core.config.settings import Settings
from core.adapters.apis.siterastreio_adapter import SiteRastreioAdapter
from core.adapters.excel.excel_repository_impl import ExcelRepositoryImpl
from core.adapters.cache.memory_cache import MemoryCache
from core.utils.rate_limiter import RateLimiter
from core.utils.retry_policy import RetryPolicy

@dataclass
class ServiceContainer:
    """Container para injeção de dependência"""
    settings: Settings
    api_adapter: SiteRastreioAdapter
    excel_repository: ExcelRepositoryImpl
    cache_service: MemoryCache

    @classmethod
    def create(cls) -> 'ServiceContainer':
        settings = Settings()

        # Criar dependências
        rate_limiter = RateLimiter(
            max_requests=settings.api_rate_limit_requests,
            period_seconds=settings.api_rate_limit_period
        )

        retry_policy = RetryPolicy(
            max_attempts=settings.api_retries
        )

        cache_service = MemoryCache(
            ttl_seconds=settings.cache_ttl_seconds,
            max_size_mb=settings.cache_max_size_mb
        )

        api_adapter = SiteRastreioAdapter(
            api_url=settings.api_base_url,
            api_key=settings.api_api_key,
            timeout=settings.api_timeout,
            rate_limiter=rate_limiter,
            cache=cache_service,
            retry_policy=retry_policy
        )

        excel_repository = ExcelRepositoryImpl(settings)

        return cls(
            settings=settings,
            api_adapter=api_adapter,
            excel_repository=excel_repository,
            cache_service=cache_service
        )