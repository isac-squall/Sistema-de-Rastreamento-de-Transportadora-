from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.tracking_record import TrackingRecord

class ExcelRepository(ABC):
    """Interface para persistência em Excel"""

    @abstractmethod
    def get_all_records(self) -> List[TrackingRecord]:
        """Recupera todos os registros"""
        pass

    @abstractmethod
    def get_record_by_tracking_code(self, code: str) -> Optional[TrackingRecord]:
        """Busca por código de rastreamento"""
        pass

    @abstractmethod
    def save(self, record: TrackingRecord) -> bool:
        """Salva um registro"""
        pass

    @abstractmethod
    def save_batch(self, records: List[TrackingRecord]) -> int:
        """Salva múltiplos registros, retorna quantidade salva"""
        pass

    @abstractmethod
    def delete(self, code: str) -> bool:
        """Deleta um registro"""
        pass

    @abstractmethod
    def create_backup(self) -> str:
        """Criar backup, retorna caminho do arquivo"""
        pass