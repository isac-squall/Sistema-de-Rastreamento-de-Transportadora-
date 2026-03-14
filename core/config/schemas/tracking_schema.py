from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum

class TrackingStatus(str, Enum):
    ENTREGUE = "✅ Entregue"
    EM_TRANSITO = "🚚 Em Trânsito"
    SAIU_PARA_ENTREGA = "📦 Saiu para Entrega"
    AGUARDANDO = "⏳ Aguardando Retirada"
    NAO_ENTREGUE = "❌ Não Entregue"
    DEVOLVIDO = "↩️ Devolvido"
    CANCELADO = "🚫 Cancelado"
    ERRO = "⚠️ Erro na Busca"

@dataclass
class TrackingEvent:
    timestamp: datetime
    location: str
    status: TrackingStatus
    description: str

    @classmethod
    def from_dict(cls, data: dict) -> 'TrackingEvent':
        # Validação e transformação
        return cls(
            timestamp=datetime.fromisoformat(data['timestamp']),
            location=data['location'],
            status=TrackingStatus(data['status']),
            description=data['description']
        )

@dataclass
class TrackingInfo:
    code: str
    status: TrackingStatus
    last_update: datetime
    location: str
    events: List[TrackingEvent]
    service_type: Optional[str] = None

    def is_delivered(self) -> bool:
        return self.status == TrackingStatus.ENTREGUE