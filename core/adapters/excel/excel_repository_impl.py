import pandas as pd
from openpyxl import load_workbook
from typing import List, Optional
from core.domain.repositories.excel_repository import ExcelRepository
from core.domain.entities.tracking_record import TrackingRecord
from core.config.settings import Settings

# Mapeamento padrão de colunas
DEFAULT_COLUMNS = {
    'nf': 'NF',
    'rastreamento': 'Rastreamento',
    'status': 'Status',
    'ultima_atualizacao': 'Última Atualização',
    'detalhes': 'Detalhes'
}

class ExcelRepositoryImpl(ExcelRepository):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.file_path = settings.excel_file_path
        self.backup_folder = settings.excel_backup_folder
        self.columns = DEFAULT_COLUMNS  # Usar mapeamento padrão
        self.df: Optional[pd.DataFrame] = None

    def _load_file(self):
        """Carrega arquivo Excel com validação"""
        if self.df is None:
            try:
                self.df = pd.read_excel(self.file_path, dtype=str)
                print(f"Arquivo carregado: {self.file_path}")
            except FileNotFoundError:
                print(f"Arquivo não encontrado: {self.file_path}")
                self._create_template()

    def _create_template(self):
        """Cria template se arquivo não existe"""
        data = {
            self.columns['nf']: [],
            self.columns['rastreamento']: [],
            self.columns['status']: [],
        }
        self.df = pd.DataFrame(data)
        self.save_file()

    def get_all_records(self) -> List[TrackingRecord]:
        self._load_file()
        records = []
        for idx, row in self.df.iterrows():
            try:
                record = TrackingRecord.from_dataframe_row(row, self.columns)
                if record.is_valid():
                    records.append(record)
            except Exception as e:
                print(f"Erro ao parsear linha {idx}: {e}")
        return records

    def get_record_by_tracking_code(self, code: str) -> Optional[TrackingRecord]:
        self._load_file()
        col = self.columns['rastreamento']
        row = self.df[self.df[col] == code]
        if row.empty:
            return None
        return TrackingRecord.from_dataframe_row(row.iloc[0], self.columns)

    def save_batch(self, records: List[TrackingRecord]) -> int:
        """Salva múltiplos registros de forma otimizada"""
        self._load_file()
        saved = 0
        for record in records:
            if self.save(record):
                saved += 1
        self.save_file()
        return saved

    def save(self, record: TrackingRecord) -> bool:
        """Salva um registro individual"""
        try:
            self._load_file()

            # Verificar se já existe
            col_rastreamento = self.columns['rastreamento']
            mask = self.df[col_rastreamento] == record.tracking_code

            if mask.any():
                # Atualizar existente
                idx = self.df[mask].index[0]
                self.df.at[idx, self.columns['nf']] = record.nf
                self.df.at[idx, self.columns['status']] = record.status.value
                if record.last_update:
                    self.df.at[idx, self.columns['ultima_atualizacao']] = record.last_update.isoformat()
                if record.details:
                    self.df.at[idx, self.columns['detalhes']] = record.details
            else:
                # Adicionar novo
                new_row = {
                    self.columns['nf']: record.nf,
                    self.columns['rastreamento']: record.tracking_code,
                    self.columns['status']: record.status.value,
                    self.columns['ultima_atualizacao']: record.last_update.isoformat() if record.last_update else '',
                    self.columns['detalhes']: record.details or ''
                }
                self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)

            return True
        except Exception as e:
            print(f"Erro ao salvar registro: {e}")
            return False

    def delete(self, code: str) -> bool:
        """Remove registro por código de rastreamento"""
        try:
            self._load_file()
            col = self.columns['rastreamento']
            mask = self.df[col] == code
            if mask.any():
                self.df = self.df[~mask]
                self.save_file()
                return True
            return False
        except Exception as e:
            print(f"Erro ao deletar registro: {e}")
            return False

    def create_backup(self) -> str:
        """Cria backup do arquivo"""
        import os
        from datetime import datetime

        os.makedirs(self.backup_folder, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(self.backup_folder, f"backup_{timestamp}_{os.path.basename(self.file_path)}")

        try:
            self.df.to_excel(backup_path, index=False)
            print(f"Backup criado: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"Erro ao criar backup: {e}")
            raise

    def save_file(self):
        """Salva arquivo com backup automático se configurado"""
        try:
            if self.settings.excel_auto_backup:
                self.create_backup()

            self.df.to_excel(self.file_path, index=False, engine='openpyxl')
            print(f"Arquivo salvo: {self.file_path}")
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")
            raise