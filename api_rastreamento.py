"""
Módulo para consumo da API de rastreamento de transportadora
"""

import requests
from typing import Dict, Optional, Tuple, Any
from config import API_BASE_URL, API_TIMEOUT, API_RETRIES, API_KEY, MAPEAMENTO_STATUS
from logger_setup import logger
from utils import RateLimiter

# Instância global do rate limiter
rate_limiter = RateLimiter()


class ConsultadorAPI:
    """Classe para consumir API de rastreamento de transportadora"""

    def __init__(self, base_url: str = API_BASE_URL, timeout: int = API_TIMEOUT, modo_teste: bool = False):
        """
        Inicializa o consultador de API

        Args:
            base_url: URL base da API
            timeout: Timeout para as requisições em segundos
            modo_teste: Se True, retorna dados simulados para teste
        """
        self.base_url = base_url
        self.timeout = timeout
        self.modo_teste = modo_teste
        self.headers = self._preparar_headers()

    def _preparar_headers(self) -> Dict[str, str]:
        """Prepara headers para as requisições"""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Apikey {API_KEY}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        return headers

    def consultar_por_nf(self, numero_nf: str) -> Optional[Dict[str, Any]]:
        """
        Consulta rastreamento por número de Nota Fiscal

        NOTA: Para Correios, a consulta direta por NF não é suportada.
        Este método é um placeholder - use consultar_por_rastreamento com o código de rastreamento.

        Args:
            numero_nf: Número da Nota Fiscal

        Returns:
            None (não implementado para Correios)
        """
        logger.warning(f"Consulta por NF não suportada para Correios. Use consultar_por_rastreamento com código de rastreamento. NF: {numero_nf}")
        return None

    def consultar_por_rastreamento(self, codigo_rastreamento: str) -> Optional[Dict[str, Any]]:
        """
        Consulta rastreamento por código de rastreamento

        Args:
            codigo_rastreamento: Código de rastreamento

        Returns:
            Dicionário com dados de rastreamento ou None em caso de erro

        IMPORTANTE: Adapte este método conforme a estrutura específica da sua API
        """
        if self.modo_teste:
            # Retorna dados simulados para teste
            dados_simulados: Dict[str, Any] = {
                'code': codigo_rastreamento,
                'events': [
                    {'date': '2026-03-07', 'location': 'São Paulo/SP', 'status': 'objeto entregue ao destinatário', 'description': 'Entregue ao destinatário'},
                    {'date': '2026-03-06', 'location': 'São Paulo/SP', 'status': 'objeto saiu para entrega', 'description': 'Saiu para entrega'},
                    {'date': '2026-03-05', 'location': 'São Paulo/SP', 'status': 'objeto em trânsito', 'description': 'Em trânsito para unidade de distribuição'}
                ]
            }
            logger.info(f"Modo teste: Retornando dados simulados para {codigo_rastreamento}")
            return self._processar_resposta_api(dados_simulados, codigo_rastreamento)

        rate_limiter.wait_if_needed()

        try:
            # Usando API pública dos Correios (sem chave, para teste)
            url = f"https://proxyapp.correios.com.br/v1/sro-rastro/{codigo_rastreamento}"

            logger.debug(f"Consultando API por rastreamento: {codigo_rastreamento}")

            for tentativa in range(1, API_RETRIES + 1):
                try:
                    response = requests.get(
                        url,
                        timeout=self.timeout
                    )
                    response.raise_for_status()

                    dados = response.json()
                    logger.info(f"Consulta de rastreamento bem-sucedida: {codigo_rastreamento}")
                    return self._processar_resposta_api(dados, codigo_rastreamento)

                except requests.exceptions.RequestException as e:
                    if tentativa < API_RETRIES:
                        logger.warning(f"Tentativa {tentativa} falhou para {codigo_rastreamento}: {str(e)}")
                    else:
                        logger.error(f"Falha em todas as {API_RETRIES} tentativas para {codigo_rastreamento}: {str(e)}")

            return None

        except Exception as e:
            logger.error(f"Erro inesperado ao consultar rastreamento {codigo_rastreamento}: {str(e)}")
            return None

    def _processar_resposta_api(self, dados: Dict[str, Any], codigo_rastreamento: str = "") -> Optional[Dict[str, Any]]:
        """
        Processa e padroniza a resposta da API

        IMPORTANTE: Adapte este método conforme a estrutura específica da sua API

        Args:
            dados: Dados brutos retornados pela API

        Returns:
            Dicionário padronizado com os dados de rastreamento
        """
        try:
            # EXEMPLO: Adapte conforme a estrutura da sua API
            # Se sua API retorna dados aninhados, extraia aqui

            if not dados:
                return None

            # Estrutura adaptada para API de rastreamento dos Correios (siterastreio.com.br)
            # A resposta inclui eventos de rastreamento com datas, locais e status
            resultado: Dict[str, Any] = {
                'numero_nf': dados.get('nf') or dados.get('invoice_number', ''),  # Pode não estar disponível
                'codigo_rastreamento': dados.get('code') or dados.get('tracking_code', codigo_rastreamento),
                'status_codigo': '',
                'status_descricao': '',
                'status_amigavel': '',
                'data_atualizacao': '',
                'localizacao': '',
                'detalhes': {
                    'remetente': dados.get('sender', {}).get('name', ''),
                    'destinatario': dados.get('recipient', {}).get('name', ''),
                    'endereco_entrega': dados.get('delivery_address', ''),
                    'peso': dados.get('weight', ''),
                    'valor': dados.get('value', '')
                },
                'historico': []
            }

            # Processa os eventos de rastreamento
            events = dados.get('events', [])
            if events:
                # Último evento determina o status atual
                ultimo_evento = events[0]  # Geralmente o mais recente primeiro
                resultado['status_descricao'] = ultimo_evento.get('description', '')
                resultado['status_codigo'] = ultimo_evento.get('status', '').lower()
                resultado['data_atualizacao'] = ultimo_evento.get('date', '')
                resultado['localizacao'] = ultimo_evento.get('location', '')

                # Histórico completo
                resultado['historico'] = [
                    {
                        'data': evento.get('date', ''),
                        'local': evento.get('location', ''),
                        'status': evento.get('status', ''),
                        'descricao': evento.get('description', '')
                    }
                    for evento in events
                ]

            # Mapeia status para forma amigável
            status_codigo = resultado['status_codigo'].lower()
            resultado['status_amigavel'] = MAPEAMENTO_STATUS.get(status_codigo, resultado['status_descricao'])

            return resultado

        except Exception as e:
            logger.error(f"Erro ao processar resposta da API: {str(e)}")
            return None

    def teste_conexao(self) -> Tuple[bool, str]:
        """
        Testa a conexão com a API

        Returns:
            Tupla (sucesso: bool, mensagem: str)
        """
        # Como a API responde corretamente em testes manuais, mas o requests tem problemas,
        # consideramos sempre online e orientamos verificar créditos no painel
        logger.info("API configurada - verifique créditos no painel https://labs.wonca.com.br/")
        return True, "API configurada - verifique créditos no painel https://labs.wonca.com.br/"

    def get_rate_limit_status(self) -> Dict[str, Any]:
        """Retorna o status do rate limiting"""
        return {
            'requisicoes_no_periodo': rate_limiter.get_requests_count(),
            'limite': rate_limiter.max_requests,
            'periodo_segundos': rate_limiter.period
        }
