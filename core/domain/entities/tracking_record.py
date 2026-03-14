from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict
from core.config.schemas.tracking_schema import TrackingStatus

@dataclass
class TrackingRecord:
    """Entidade principal para registro de rastreamento"""
    nf: str
    tracking_code: str
    status: TrackingStatus
    last_update: Optional[datetime] = None
    details: Optional[str] = None

    def is_valid(self) -> bool:
        """Valida se o registro é válido"""
        return bool(
            self.nf.strip() and
            self.tracking_code.strip() and
            self.status
        )

    @classmethod
    def from_dataframe_row(cls, row: Dict, columns: Dict[str, str]) -> 'TrackingRecord':
        """Cria instância a partir de uma linha do DataFrame"""
        try:
            # Mapeamento de colunas
            nf = str(row.get(columns.get('nf', 'NF'), '')).strip()
            tracking_code = str(row.get(columns.get('rastreamento', 'Rastreamento'), '')).strip()
            status_str = str(row.get(columns.get('status', 'Status'), '')).strip()
            last_update_str = str(row.get(columns.get('ultima_atualizacao', 'Última Atualização'), '')).strip()
            details = str(row.get(columns.get('detalhes', 'Detalhes'), '')).strip()

            # Parse status
            status = TrackingStatus.ERRO
            for status_enum in TrackingStatus:
                if status_enum.value in status_str:
                    status = status_enum
                    break

            # Parse last_update
            last_update = None
            if last_update_str and last_update_str.lower() not in ['nan', 'nat', '']:
                try:
                    last_update = datetime.fromisoformat(last_update_str)
                except ValueError:
                    # Tentar outros formatos
                    pass

            return cls(
                nf=nf,
                tracking_code=tracking_code,
                status=status,
                last_update=last_update,
                details=details if details else None
            )
        except Exception as e:
            # Retornar registro com status de erro
            return cls(
                nf=str(row.get(columns.get('nf', 'NF'), 'ERRO')),
                tracking_code=str(row.get(columns.get('rastreamento', 'Rastreamento'), 'ERRO')),
                status=TrackingStatus.ERRO,
                details=f"Erro ao parsear: {str(e)}"
            )