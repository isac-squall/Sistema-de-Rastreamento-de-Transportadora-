import time
import random
from typing import Callable, TypeVar, Optional
from core.config.settings import settings

T = TypeVar('T')

class RetryPolicy:
    """Política de retry com backoff exponencial"""

    def __init__(self, max_retries: Optional[int] = None, base_delay: float = 1.0):
        self.max_retries = max_retries or settings.api.retries
        self.base_delay = base_delay

    def execute(self, func: Callable[[], T]) -> Optional[T]:
        """Executa função com retry"""
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                return func()
            except Exception as e:
                last_exception = e

                if attempt < self.max_retries:
                    # Calcular delay com jitter
                    delay = self.base_delay * (2 ** attempt)
                    jitter = random.uniform(0, delay * 0.1)
                    total_delay = delay + jitter

                    print(f"Tentativa {attempt + 1} falhou: {e}. Tentando novamente em {total_delay:.2f}s")
                    time.sleep(total_delay)
                else:
                    print(f"Todas as {self.max_retries + 1} tentativas falharam. Último erro: {e}")

        return None