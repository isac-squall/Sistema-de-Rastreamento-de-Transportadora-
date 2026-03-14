from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from core.domain.value_objects.tracking_code import TrackingCode

class BaseAPIAdapter(ABC):
    """Interface base para adapters de API de rastreamento"""

    @abstractmethod
    def get_tracking_info(self, code: TrackingCode) -> Optional[Dict[str, Any]]:
        """Consulta informações de rastreamento"""
        pass

    @abstractmethod
    def test_connection(self) -> tuple[bool, str]:
        """Testa conexão com API"""
        pass

    @abstractmethod
    def supports_nf_lookup(self) -> bool:
        """Se adapter suporta busca por NF"""
        pass

    def get_name(self) -> str:
        """Nome do adapter"""
        return self.__class__.__name__