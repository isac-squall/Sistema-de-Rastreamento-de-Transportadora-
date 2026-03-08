"""
Módulo de logging para a solução de rastreamento
"""

import logging
import os
from datetime import datetime
from config import LOG_LEVEL, LOG_FORMAT, LOG_DATE_FORMAT, LOG_FOLDER


class LoggerSetup:
    """Configuração centralizada de logging"""

    @staticmethod
    def setup_logger(name: str) -> logging.Logger:
        """
        Configura e retorna um logger para o módulo especificado

        Args:
            name: Nome do módulo/logger

        Returns:
            logger configurado
        """
        # Cria pasta de logs se não existir
        os.makedirs(LOG_FOLDER, exist_ok=True)

        logger = logging.getLogger(name)

        # Define nível de logging
        logger.setLevel(getattr(logging, LOG_LEVEL))

        # Evita duplicação de handlers
        if logger.hasHandlers():
            return logger

        # Handler para arquivo
        log_file = os.path.join(
            LOG_FOLDER,
            f"rastreamento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT))

        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, LOG_LEVEL))
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT))

        # Adiciona handlers ao logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger


# Instância global do logger
logger = LoggerSetup.setup_logger('Rastreamento')
