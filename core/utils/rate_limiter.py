import time
import json
import os
from collections import deque
from typing import Optional
from pathlib import Path
from threading import Lock

class RateLimiter:
    """Rate limiter com persistência em arquivo"""

    def __init__(
        self,
        max_requests: int,
        period_seconds: int,
        persist_file: Optional[str] = None
    ):
        self.max_requests = max_requests
        self.period_seconds = period_seconds
        self.persist_file = persist_file or "rate_limiter_state.json"
        self._lock = Lock()
        self.request_times = self._load_state()

    def _load_state(self) -> deque:
        """Carrega estado persistido"""
        if os.path.exists(self.persist_file):
            try:
                with open(self.persist_file, 'r') as f:
                    times = json.load(f)
                    # Remove requisições antigas
                    current_time = time.time()
                    times = [t for t in times if t > current_time - self.period_seconds]
                    return deque(times)
            except Exception as e:
                print(f"Erro ao carregar rate limit state: {e}")
        return deque()

    def _save_state(self):
        """Persiste estado em arquivo"""
        try:
            with open(self.persist_file, 'w') as f:
                json.dump(list(self.request_times), f)
        except Exception as e:
            print(f"Erro ao salvar rate limit state: {e}")

    def wait_if_needed(self):
        """Aguarda se necessário para respeitar rate limit"""
        now = time.time()

        with self._lock:
            # Remove requisições fora do período
            while self.request_times and self.request_times[0] < now - self.period_seconds:
                self.request_times.popleft()

            # Se atingiu limite, aguarda
            if len(self.request_times) >= self.max_requests:
                sleep_time = self.request_times[0] + self.period_seconds - now
                if sleep_time > 0:
                    print(f"Rate limit atingido. Aguardando {sleep_time:.2f}s...")
                    time.sleep(sleep_time)
                    now = time.time()
                    # Limpa novamente após sleep
                    while self.request_times and self.request_times[0] < now - self.period_seconds:
                        self.request_times.popleft()

            # Registra nova requisição
            self.request_times.append(now)
            self._save_state()

    def get_requests_count(self) -> int:
        """Retorna requisições no período atual"""
        now = time.time()
        with self._lock:
            while self.request_times and self.request_times[0] < now - self.period_seconds:
                self.request_times.popleft()
            return len(self.request_times)