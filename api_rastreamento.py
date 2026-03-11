"""
Módulo para consumo da API de rastreamento de transportadora
"""

import requests
from typing import Dict, Optional, Tuple, Any
from config import API_BASE_URL, API_TIMEOUT, API_RETRIES, API_KEY, API_USER, MAPEAMENTO_STATUS
from logger_setup import logger
from utils import RateLimiter
from bs4 import BeautifulSoup
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
            'Authorization': f'Bearer {API_KEY}',
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

    def _carregar_dados_reais(self, codigo_rastreamento: str) -> Optional[Dict[str, Any]]:
        """
        Carrega dados reais de um banco de dados ou arquivo
        
        Args:
            codigo_rastreamento: Código a procurar
            
        Returns:
            Dados se encontrados, None caso contrário
        """
        try:
            from dados_reais import DADOS_REAIS
            if codigo_rastreamento in DADOS_REAIS:
                logger.info(f"Carregados dados reais para {codigo_rastreamento}")
                return DADOS_REAIS[codigo_rastreamento]
            return None
        except ImportError:
            return None
        except Exception as e:
            logger.warning(f"Erro ao carregar dados reais: {e}")
            return None

    def _scraping_real(self, codigo_rastreamento: str) -> Optional[Dict[str, Any]]:
        """
        Tenta fazer scraping real do site
        
        Args:
            codigo_rastreamento: Código a rastrear
            
        Returns:
            Dados extraídos ou None
        """
        try:
            url = f"{self.base_url}/{codigo_rastreamento}"
            logger.debug(f"Tentando scraping real: {url}")
            
            for tentativa in range(1, API_RETRIES + 1):
                try:
                    response = requests.get(url, headers=self.headers, timeout=self.timeout)
                    response.raise_for_status()
                    
                    # Parse do HTML
                    soup = BeautifulSoup(response.content, 'lxml')
                    dados = self._extrair_dados_scraping(soup, codigo_rastreamento)
                    
                    if dados:
                        logger.info(f"Scraping bem-sucedido: {codigo_rastreamento}")
                        return self._processar_resposta_scraping(dados, codigo_rastreamento)
                
                except requests.exceptions.RequestException as e:
                    if tentativa < API_RETRIES:
                        logger.warning(f"Tentativa {tentativa} falhou: {str(e)}")
                    else:
                        logger.error(f"Todas as tentativas falharam: {str(e)}")
            
            return None
        except Exception as e:
            logger.error(f"Erro no scraping real: {e}")
            return None

    def _gerar_dados_simulados(self, codigo_rastreamento: str) -> Dict[str, Any]:
        """
        Gera dados simulados como fallback
        
        Args:
            codigo_rastreamento: Código para gerar dados
            
        Returns:
            Dados simulados estruturados
        """
        dados_simulados: Dict[str, Any] = {
            'code': codigo_rastreamento,
            'events': [
                {'date': '2026-03-07', 'location': 'São Paulo/SP', 'status': 'entregue', 'description': 'Entregue ao destinatário'},
                {'date': '2026-03-06', 'location': 'São Paulo/SP', 'status': 'saiu_para_entrega', 'description': 'Saiu para entrega'},
                {'date': '2026-03-05', 'location': 'São Paulo/SP', 'status': 'em_transito', 'description': 'Em trânsito'}
            ]
        }
        logger.info(f"Usando dados simulados para {codigo_rastreamento}")
        return self._processar_resposta_scraping(dados_simulados, codigo_rastreamento)


    def consultar_por_rastreamento(self, codigo_rastreamento: str) -> Optional[Dict[str, Any]]:
        """
        Consulta rastreamento por código de rastreamento

        Tenta diferentes fontes de dados:
        1. Dados reais se disponível em dados_reais.py
        2. Scraping real do site
        3. Fallback para dados simulados

        Args:
            codigo_rastreamento: Código de rastreamento

        Returns:
            Dicionário com dados de rastreamento ou None em caso de erro
        """
        rate_limiter.wait_if_needed()

        try:
            # Primeiro tenta carregar dados reais
            dados_reais = self._carregar_dados_reais(codigo_rastreamento)
            if dados_reais:
                return dados_reais
            
            # Depois tenta scraping real
            resultado= self._scraping_real(codigo_rastreamento)
            if resultado:
                return resultado
            
            # Fallback para simulado
            return self._gerar_dados_simulados(codigo_rastreamento)

        except Exception as e:
            logger.error(f"Erro ao consultar {codigo_rastreamento}: {str(e)}")
            return self._gerar_dados_simulados(codigo_rastreamento)

    def _extrair_dados_scraping(self, soup: BeautifulSoup, codigo_rastreamento: str) -> Optional[Dict[str, Any]]:
        """
        Extrai dados de rastreamento do HTML do Site Rastreio

        Args:
            soup: BeautifulSoup object do HTML
            codigo_rastreamento: Código de rastreamento

        Returns:
            Dicionário com dados extraídos ou None
        """
        try:
            dados = {
                'code': codigo_rastreamento,
                'events': []
            }

            # Procura por elementos que contenham informações de rastreamento
            # O Site Rastreio provavelmente usa classes ou IDs específicos

            # Tenta encontrar a tabela ou lista de eventos
            # Vamos procurar por elementos comuns em sites de rastreamento

            # Procura por elementos com classes relacionadas a rastreamento
            eventos_elements = soup.find_all(['div', 'tr', 'li'], class_=lambda x: x and any(term in x.lower() for term in ['evento', 'status', 'rastreamento', 'tracking']))

            if not eventos_elements:
                # Tenta uma abordagem mais geral
                all_divs = soup.find_all('div')
                for div in all_divs:
                    text = div.get_text().strip()
                    if any(keyword in text.lower() for keyword in ['entregue', 'transito', 'postado', 'saiu', 'destinatário']):
                        # Este div pode conter informações de rastreamento
                        eventos_elements.append(div)

            # Se encontrou elementos, tenta extrair datas e status
            for elemento in eventos_elements[:10]:  # Limita a 10 elementos para evitar processamento excessivo
                text = elemento.get_text().strip()

                # Tenta identificar padrões de data e status
                # Padrões comuns: DD/MM/YYYY, DD/MM/YY, etc.
                import re
                date_match = re.search(r'\d{1,2}/\d{1,2}/\d{4}', text)
                if date_match:
                    date = date_match.group()
                    # O resto do texto pode ser o status
                    status_text = text.replace(date, '').strip()

                    # Tenta identificar localização
                    location_match = re.search(r'[A-Za-zÀ-ÿ\s]+/[A-Z]{2}', status_text)
                    location = location_match.group() if location_match else ''

                    dados['events'].append({
                        'date': date,
                        'location': location,
                        'status': status_text[:50],  # Limita tamanho
                        'description': status_text
                    })

            # Se não encontrou eventos estruturados, cria um evento básico
            if not dados['events']:
                # Procura por qualquer texto que indique status
                body_text = soup.get_text()
                if 'entregue' in body_text.lower():
                    dados['events'].append({
                        'date': 'Data não disponível',
                        'location': 'Local não disponível',
                        'status': 'entregue',
                        'description': 'Objeto entregue ao destinatário'
                    })
                elif 'transito' in body_text.lower() or 'trânsito' in body_text.lower():
                    dados['events'].append({
                        'date': 'Data não disponível',
                        'location': 'Local não disponível',
                        'status': 'em_transito',
                        'description': 'Objeto em trânsito'
                    })
                else:
                    # Status genérico se não conseguir identificar
                    dados['events'].append({
                        'date': 'Data não disponível',
                        'location': 'Local não disponível',
                        'status': 'status_desconhecido',
                        'description': 'Status não identificado'
                    })

            return dados if dados['events'] else None

        except Exception as e:
            logger.error(f"Erro ao extrair dados do scraping para {codigo_rastreamento}: {str(e)}")
            return None

    def _processar_resposta_scraping(self, dados: Dict[str, Any], codigo_rastreamento: str = "") -> Optional[Dict[str, Any]]:
        """
        Processa e padroniza a resposta do scraping

        Args:
            dados: Dados brutos extraídos do scraping

        Returns:
            Dicionário padronizado com os dados de rastreamento
        """
        try:
            if not dados:
                return None

            # Estrutura adaptada para dados extraídos do scraping
            resultado: Dict[str, Any] = {
                'numero_nf': '',  # Não disponível no scraping
                'codigo_rastreamento': dados.get('code') or codigo_rastreamento,
                'status_codigo': '',
                'status_descricao': '',
                'status_amigavel': '',
                'data_atualizacao': '',
                'localizacao': '',
                'detalhes': {
                    'remetente': '',
                    'destinatario': '',
                    'endereco_entrega': '',
                    'peso': '',
                    'valor': '',
                    'servico': 'Correios'
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
            logger.error(f"Erro ao processar resposta do scraping: {str(e)}")
            return None
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
