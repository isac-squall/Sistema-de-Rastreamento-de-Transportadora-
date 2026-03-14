import time
import random
from typing import Callable, TypeVar, Optional
from enum import Enum

T = TypeVar('T')

class RetryStrategy(str, Enum):
    EXPONENTIAL = "exponential"
    LINEAR = "linear"
    FIXED = "fixed"

class RetryPolicy:
    """Política de retry com exponential backoff"""

    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay_ms: int = 100,
        max_delay_ms: int = 10000,
        strategy: RetryStrategy = RetryStrategy.EXPONENTIAL,
        jitter: bool = True,
        retryable_exceptions: tuple = (Exception,)
    ):
        self.max_attempts = max_attempts
        self.initial_delay_ms = initial_delay_ms
        self.max_delay_ms = max_delay_ms
        self.strategy = strategy
        self.jitter = jitter
        self.retryable_exceptions = retryable_exceptions

    def execute(
        self,
        func: Callable[..., T],
        *args,
        **kwargs
    ) -> Optional[T]:
        """Executa função com retry"""
        for attempt in range(1, self.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except self.retryable_exceptions as e:
                if attempt == self.max_attempts:
                    print(f"Falha após {self.max_attempts} tentativas: {e}")
                    return None

                delay = self._calculate_delay(attempt)
                print(
                    f"Tentativa {attempt}/{self.max_attempts} falhou. "
                    f"Aguardando {delay}ms antes de retry..."
                )
                time.sleep(delay / 1000)

    def _calculate_delay(self, attempt: int) -> int:
        """Calcula delay baseado na estratégia"""
        if self.strategy == RetryStrategy.EXPONENTIAL:
            delay = min(
                self.initial_delay_ms * (2 ** (attempt - 1)),
                self.max_delay_ms
            )
        elif self.strategy == RetryStrategy.LINEAR:
            delay = min(
                self.initial_delay_ms * attempt,
                self.max_delay_ms
            )
        else:  # FIXED
            delay = self.initial_delay_ms

        # Adiciona jitter para evitar thundering herd
        if self.jitter:
            delay = int(delay * (0.5 + random.random()))

        return delay