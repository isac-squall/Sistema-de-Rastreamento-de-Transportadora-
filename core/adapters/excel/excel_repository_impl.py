import pandas as pd
from typing import List, Dict, Any, Optional
import os
from core.config.settings import settings
from core.domain.entities.tracking_record import TrackingRecord

class ExcelRepositoryImpl:
    """Implementação do repositório Excel"""

    def __init__(self):
        self.default_file = settings.excel.default_file

    def read_excel(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """Lê dados do Excel"""
        file_path = file_path or self.default_file

        if not os.path.exists(file_path):
            # Criar arquivo modelo se não existir
            return self._create_empty_dataframe()

        try:
            df = pd.read_excel(file_path)
            return df
        except Exception as e:
            print(f"Erro ao ler Excel: {e}")
            return self._create_empty_dataframe()

    def save_excel(self, df: pd.DataFrame, file_path: Optional[str] = None) -> bool:
        """Salva dados no Excel"""
        file_path = file_path or self.default_file

        try:
            df.to_excel(file_path, index=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar Excel: {e}")
            return False

    def get_tracking_records(self, file_path: Optional[str] = None) -> List[TrackingRecord]:
        """Converte dados do Excel para TrackingRecord objects"""
        df = self.read_excel(file_path)
        records = []

        for _, row in df.iterrows():
            try:
                # Criar TrackingRecord a partir da linha
                record = TrackingRecord(
                    tracking_code=row['Rastreamento'],
                    nf_number=row.get('NF'),
                    status=row.get('Status', ''),
                    details={'row_data': dict(row)}
                )
                records.append(record)
            except Exception as e:
                print(f"Erro ao processar linha: {e}")
                continue

        return records

    def update_tracking_record(self, record: TrackingRecord, file_path: Optional[str] = None) -> bool:
        """Atualiza um registro no Excel"""
        df = self.read_excel(file_path)

        # Encontrar linha com o código de rastreamento
        mask = df['Rastreamento'] == str(record.tracking_code)

        if mask.any():
            # Atualizar linha existente
            idx = df[mask].index[0]
            df.loc[idx, 'Status'] = record.status
            df.loc[idx, 'Última Atualização'] = record.last_update.strftime("%Y-%m-%d %H:%M:%S") if record.last_update else ""
            df.loc[idx, 'Detalhes'] = str(record.details) if record.details else ""
        else:
            # Adicionar nova linha
            new_row = record.to_dict()
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        return self.save_excel(df, file_path)

    def _create_empty_dataframe(self) -> pd.DataFrame:
        """Cria DataFrame vazio com colunas padrão"""
        columns = ['NF', 'Rastreamento', 'Status', 'Última Atualização', 'Detalhes']
        return pd.DataFrame(columns=columns)