from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from core.domain.value_objects.tracking_code import TrackingCode

class TrackingRecord(BaseModel):
    """Entidade principal para registros de rastreamento"""
    tracking_code: TrackingCode
    nf_number: Optional[str] = None
    status: str = ""
    last_update: Optional[datetime] = None
    details: Optional[Dict[str, Any]] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True

    def update_status(self, new_status: str, details: Optional[Dict[str, Any]] = None):
        """Atualiza o status do rastreamento"""
        self.status = new_status
        self.last_update = datetime.now()
        if details:
            self.details.update(details)

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário compatível com Excel"""
        return {
            "NF": self.nf_number or "",
            "Rastreamento": str(self.tracking_code),
            "Status": self.status,
            "Última Atualização": self.last_update.strftime("%Y-%m-%d %H:%M:%S") if self.last_update else "",
            "Detalhes": str(self.details) if self.details else ""
        }