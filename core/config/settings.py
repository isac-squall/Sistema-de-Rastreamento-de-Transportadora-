from pydantic_settings import BaseSettings
from typing import Optional

class APIConfig(BaseSettings):
    """Configurações da API de rastreamento"""
    base_url: str = "https://www.siterastreio.com.br/rastreamento"
    timeout: int = 30
    retries: int = 3
    rate_limit: int = 10  # requests per minute

class ExcelConfig(BaseSettings):
    """Configurações do Excel"""
    default_file: str = "planilha_rastreamento.xlsx"
    backup_dir: str = "backups"
    max_rows_display: int = 100

class CacheConfig(BaseSettings):
    """Configurações do cache"""
    enabled: bool = True
    ttl_seconds: int = 300  # 5 minutes
    max_size: int = 1000

class Settings(BaseSettings):
    """Configurações principais da aplicação"""
    api: APIConfig = APIConfig()
    excel: ExcelConfig = ExcelConfig()
    cache: CacheConfig = CacheConfig()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instância global das configurações
settings = Settings()