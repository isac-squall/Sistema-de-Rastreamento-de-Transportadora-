from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Geral
    app_name: str = "Rastreamento Transportadora"
    version: str = "2.0.0"
    log_level: str = "INFO"

    # API
    api_base_url: str = Field(..., description="URL base da API")
    api_timeout: int = Field(default=30, ge=1, le=300)
    api_retries: int = Field(default=3, ge=0, le=10)
    api_api_key: str = Field(default="", description="Chave de API")
    api_rate_limit_requests: int = Field(default=100, ge=1)
    api_rate_limit_period: int = Field(default=60, ge=1)

    # Excel
    excel_file_path: str = Field(..., description="Caminho do arquivo Excel")
    excel_backup_folder: str = Field(default="backups")
    excel_auto_backup: bool = Field(default=True)
    excel_update_only_changes: bool = Field(default=True)

    # Cache
    cache_enabled: bool = Field(default=True)
    cache_backend: str = Field(default="memory", pattern=r"^(memory|redis)$")
    cache_ttl_seconds: int = Field(default=3600, ge=60)
    cache_max_size_mb: int = Field(default=100, ge=1)

    # Processamento
    atualizar_apenas_mudancas: bool = Field(default=True)
    criar_backup_antes: bool = Field(default=True)
    salvar_relatorio: bool = Field(default=True)

    class Config:
        env_file = ".env"