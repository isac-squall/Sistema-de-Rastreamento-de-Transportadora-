import time
from typing import Deque
from collections import deque

class RateLimiter:
    """Rate limiter simples baseado em janela deslizante"""

    def __init__(self, requests_per_minute: int = 10):
        self.requests_per_minute = requests_per_minute
        self.requests: Deque[float] = deque()
        self.window_seconds = 60  # 1 minuto

    def wait_if_needed(self) -> None:
        """Aguarda se necessário para respeitar o rate limit"""
        current_time = time.time()

        # Remover requests fora da janela
        while self.requests and current_time - self.requests[0] > self.window_seconds:
            self.requests.popleft()

        # Verificar se pode fazer request
        if len(self.requests) >= self.requests_per_minute:
            # Calcular quanto tempo esperar
            oldest_request = self.requests[0]
            wait_time = self.window_seconds - (current_time - oldest_request)

            if wait_time > 0:
                time.sleep(wait_time)

        # Registrar este request
        self.requests.append(time.time())