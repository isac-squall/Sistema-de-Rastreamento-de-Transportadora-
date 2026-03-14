from dataclasses import dataclass
import re

@dataclass(frozen=True)
class TrackingCode:
    """Value object para código de rastreamento (Correios)"""
    value: str

    def __post_init__(self):
        # Validar formato Correios: 2 letras + 8 números + 2 letras
        if not re.match(r'^[A-Z]{2}\d{8}[A-Z]{2}$', self.value):
            raise ValueError(f"Código de rastreamento inválido: {self.value}")

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_string(cls, code: str) -> 'TrackingCode':
        cleaned = code.strip().upper()
        return cls(cleaned)