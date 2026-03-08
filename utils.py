"""
Módulo de utilitários para rate limiting e backup
"""

import os
import shutil
import time
from datetime import datetime
from collections import deque
from config import (
    RATE_LIMIT_REQUESTS,
    RATE_LIMIT_PERIOD,
    BACKUP_FOLDER,
    EXCEL_FILE_PATH
)
from logger_setup import logger


class RateLimiter:
    """Implementa rate limiting para requisições à API"""

    def __init__(self, max_requests: int = RATE_LIMIT_REQUESTS, period: int = RATE_LIMIT_PERIOD):
        """
        Inicializa o limitador de taxa

        Args:
            max_requests: Número máximo de requisições permitidas
            period: Período em segundos para contar as requisições
        """
        self.max_requests = max_requests
        self.period = period
        self.request_times = deque()
        self.lock_until = 0

    def wait_if_needed(self):
        """Aguarda se necessário antes de fazer uma requisição"""
        now = time.time()

        # Remove requisições fora do período
        while self.request_times and self.request_times[0] < now - self.period:
            self.request_times.popleft()

        # Se atingiu o limite, aguarda
        if len(self.request_times) >= self.max_requests:
            sleep_time = self.request_times[0] + self.period - now
            if sleep_time > 0:
                logger.info(f"Rate limit atingido. Aguardando {sleep_time:.2f}s...")
                time.sleep(sleep_time)
                now = time.time()
                # Limpa requisições antigas
                while self.request_times and self.request_times[0] < now - self.period:
                    self.request_times.popleft()

        # Registra nova requisição
        self.request_times.append(now)

    def get_requests_count(self) -> int:
        """Retorna o número de requisições no período atual"""
        now = time.time()
        while self.request_times and self.request_times[0] < now - self.period:
            self.request_times.popleft()
        return len(self.request_times)


class BackupManager:
    """Gerencia backup automático de arquivos"""

    @staticmethod
    def criar_backup(arquivo_origem: str = EXCEL_FILE_PATH) -> str:
        """
        Cria backup de um arquivo

        Args:
            arquivo_origem: Caminho do arquivo a fazer backup

        Returns:
            Caminho do arquivo de backup criado

        Raises:
            FileNotFoundError: Se o arquivo de origem não existir
        """
        if not os.path.exists(arquivo_origem):
            raise FileNotFoundError(f"Arquivo não encontrado: {arquivo_origem}")

        # Criar pasta de backup se não existir
        os.makedirs(BACKUP_FOLDER, exist_ok=True)

        # Gera nome do backup com timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nome_arquivo = os.path.basename(arquivo_origem)
        nome_backup = f"{os.path.splitext(nome_arquivo)[0]}_backup_{timestamp}.xlsx"
        caminho_backup = os.path.join(BACKUP_FOLDER, nome_backup)

        try:
            shutil.copy2(arquivo_origem, caminho_backup)
            logger.info(f"Backup criado com sucesso: {caminho_backup}")
            return caminho_backup
        except Exception as e:
            logger.error(f"Erro ao criar backup: {str(e)}")
            raise

    @staticmethod
    def limpar_backups_antigos(dias: int = 30):
        """
        Remove backups com mais de X dias

        Args:
            dias: Número de dias para manter os backups
        """
        if not os.path.exists(BACKUP_FOLDER):
            return

        tempo_limite = time.time() - (dias * 24 * 60 * 60)

        for arquivo in os.listdir(BACKUP_FOLDER):
            caminho_arquivo = os.path.join(BACKUP_FOLDER, arquivo)
            if os.path.isfile(caminho_arquivo):
                if os.path.getmtime(caminho_arquivo) < tempo_limite:
                    try:
                        os.remove(caminho_arquivo)
                        logger.info(f"Backup antigo removido: {arquivo}")
                    except Exception as e:
                        logger.error(f"Erro ao remover backup antigo: {str(e)}")

    @staticmethod
    def listar_backups() -> list:
        """
        Lista todos os backups disponíveis

        Returns:
            Lista de caminhos dos backups
        """
        if not os.path.exists(BACKUP_FOLDER):
            return []

        backups = []
        for arquivo in sorted(os.listdir(BACKUP_FOLDER), reverse=True):
            caminho_completo = os.path.join(BACKUP_FOLDER, arquivo)
            if os.path.isfile(caminho_completo):
                tamanho = os.path.getsize(caminho_completo)
                data_modificacao = datetime.fromtimestamp(os.path.getmtime(caminho_completo))
                backups.append({
                    'arquivo': arquivo,
                    'caminho': caminho_completo,
                    'tamanho': f"{tamanho / 1024:.2f}KB",
                    'data': data_modificacao.strftime('%d/%m/%Y %H:%M:%S')
                })
        return backups

    @staticmethod
    def restaurar_backup(caminho_backup: str, arquivo_destino: str = EXCEL_FILE_PATH):
        """
        Restaura um backup para o arquivo original

        Args:
            caminho_backup: Caminho do arquivo de backup
            arquivo_destino: Caminho de destino (padrão: arquivo original)

        Raises:
            FileNotFoundError: Se o backup não existir
        """
        if not os.path.exists(caminho_backup):
            raise FileNotFoundError(f"Backup não encontrado: {caminho_backup}")

        try:
            shutil.copy2(caminho_backup, arquivo_destino)
            logger.info(f"Backup restaurado com sucesso: {arquivo_destino}")
        except Exception as e:
            logger.error(f"Erro ao restaurar backup: {str(e)}")
            raise
