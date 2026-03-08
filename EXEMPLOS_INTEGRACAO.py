"""
EXEMPLOS DE INTEGRAÇÃO COM DIFERENTES TRANSPORTADORAS
Estes são exemplos de como adaptar o código para APIs reais
"""

# ============================================================================
# EXEMPLO 1: Integração com API Genérica (PADRÃO ATUAL)
# ============================================================================

"""
Estrutura de Resposta Esperada:
{
    "code": "BR123456789ABC",
    "nf": "2026000001",
    "status": {
        "code": "DELIVERED",
        "description": "Entregue"
    },
    "location": "São Paulo - SP",
    "events": [
        {
            "status": "DELIVERED",
            "date": "2026-03-03",
            "location": "São Paulo - SP"
        }
    ]
}
"""

def exemplo_api_generica():
    from api_rastreamento import ConsultadorAPI
    
    api = ConsultadorAPI()
    
    # Consulta por rastreamento
    resultado = api.consultar_por_rastreamento('BR123456789ABC')
    if resultado:
        print(f"Status: {resultado['status_amigavel']}")


# ============================================================================
# EXEMPLO 2: Integração com API do tipo REST Simples
# ============================================================================

"""
Quando a API retorna resposta simples como:
{
    "tracking_number": "BR123456789ABC",
    "current_status": "DELIVERED",
    "estimated_delivery": "2026-03-03",
    "last_location": "São Paulo"
}
"""

def exemplo_rest_simples():
    """
    Adapte _processar_resposta_api em api_rastreamento.py:
    """
    codigo_adaptacao = '''
    def _processar_resposta_api(self, dados: Dict) -> Optional[Dict]:
        try:
            if not dados:
                return None

            # Para APIs simples, geralmente os dados estão no nível raiz
            resultado = {
                'numero_nf': dados.get('invoice_id', ''),
                'codigo_rastreamento': dados.get('tracking_number', ''),
                'status_codigo': dados.get('current_status', ''),
                'status_descricao': dados.get('status_description', dados.get('current_status', '')),
                'status_amigavel': '',
                'data_atualizacao': dados.get('updated_at', ''),
                'localizacao': dados.get('last_location', ''),
                'detalhes': {
                    'remetente': dados.get('sender', ''),
                    'destinatario': dados.get('recipient', ''),
                    'endereco_entrega': dados.get('delivery_address', ''),
                    'peso': dados.get('weight', ''),
                    'valor': dados.get('value', '')
                },
                'historico': dados.get('timeline', [])
            }

            status_codigo = resultado['status_codigo'].lower()
            resultado['status_amigavel'] = MAPEAMENTO_STATUS.get(status_codigo, resultado['status_descricao'])

            return resultado
        except Exception as e:
            logger.error(f"Erro ao processar resposta da API: {str(e)}")
            return None
    '''
    pass


# ============================================================================
# EXEMPLO 3: Integração com API que requer autenticação OAuth2
# ============================================================================

def exemplo_oauth2():
    """
    Se sua API usa OAuth2, adapte _preparar_headers em ConsultadorAPI:
    """
    codigo_adaptacao = '''
    def _preparar_headers(self) -> Dict:
        """Prepara headers com token OAuth2"""
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Rastreador-Transportadora/1.0'
        }

        # Obter token (implemente conforme sua API)
        token = self._obter_token_oauth2()
        if token:
            headers['Authorization'] = f'Bearer {token}'

        return headers

    def _obter_token_oauth2(self) -> str:
        """Obtém token OAuth2"""
        try:
            url_token = f"{self.base_url}/oauth/token"
            dados = {
                'client_id': API_KEY,
                'client_secret': os.getenv('API_SECRET'),
                'grant_type': 'client_credentials'
            }
            response = requests.post(url_token, json=dados, timeout=self.timeout)
            response.raise_for_status()
            return response.json()['access_token']
        except Exception as e:
            logger.error(f"Erro ao obter token OAuth2: {str(e)}")
            return None
    '''
    pass


# ============================================================================
# EXEMPLO 4: Integração com API que retorna dados aninhados
# ============================================================================

def exemplo_dados_aninhados():
    """
    Quando a API retorna dados aninhados como:
    {
        "success": true,
        "message": "Success",
        "data": {
            "package": {
                "code": "BR123456789ABC",
                "status": {
                    "id": 5,
                    "name": "DELIVERED"
                },
                "tracking": {
                    "events": [...]
                }
            }
        }
    }
    """
    codigo_adaptacao = '''
    def _processar_resposta_api(self, dados: Dict) -> Optional[Dict]:
        try:
            if not dados or not dados.get('success'):
                return None

            # Extrai dados aninhados
            package = dados.get('data', {}).get('package', {})
            if not package:
                return None

            status_info = package.get('status', {})
            
            resultado = {
                'numero_nf': package.get('invoice', ''),
                'codigo_rastreamento': package.get('code', ''),
                'status_codigo': status_info.get('name', ''),
                'status_descricao': status_info.get('name', ''),
                'status_amigavel': '',
                'data_atualizacao': package.get('last_update', ''),
                'localizacao': package.get('current_location', ''),
                'detalhes': {
                    'endereco_entrega': package.get('delivery', {}).get('address', ''),
                },
                'historico': package.get('tracking', {}).get('events', [])
            }

            status_codigo = resultado['status_codigo'].lower()
            resultado['status_amigavel'] = MAPEAMENTO_STATUS.get(status_codigo, resultado['status_descricao'])

            return resultado
        except Exception as e:
            logger.error(f"Erro ao processar resposta da API: {str(e)}")
            return None
    '''
    pass


# ============================================================================
# EXEMPLO 5: Integração com SOAP/XML (em vez de REST/JSON)
# ============================================================================

def exemplo_soap_xml():
    """
    Se sua API usa SOAP/XML, você precisará fazer adaptações maiores:
    """
    codigo_adaptacao = '''
    def consultar_por_rastreamento(self, codigo_rastreamento: str) -> Optional[Dict]:
        """Para SOAP, você precisará usar zeep"""
        try:
            from zeep import Client
            
            # Cliente SOAP
            client = Client(wsdl=f"{self.base_url}?wsdl")
            
            # Chamada SOAP
            resposta = client.service.track(tracking_code=codigo_rastreamento)
            
            # Processar resposta SOAP
            return self._processar_resposta_soap(resposta)
            
        except Exception as e:
            logger.error(f"Erro na consulta SOAP: {str(e)}")
            return None
    '''
    pass


# ============================================================================
# EXEMPLO 6: Mapeamento de Status para Diferentes Transportadoras
# ============================================================================

EXEMPLOS_MAPEAMENTO = {
    'Transportadora Genérica': {
        'DELIVERED': '✅ Entregue',
        'IN_TRANSIT': '🚚 Em Trânsito',
        'OUT_FOR_DELIVERY': '📦 Saiu para Entrega',
        'PENDING': '⏳ Pendente',
        'FAILED': '❌ Falha',
        'RETURNED': '↩️ Devolvido',
        'CANCELLED': '🚫 Cancelado',
    },
    
    'Exemplo com Números': {
        '10': '✅ Entregue',
        '20': '🚚 Em Trânsito',
        '30': '📦 Saiu para Entrega',
        '40': '⏳ Aguardando',
        '50': '❌ Falha',
    },
    
    'Exemplo com Descrições Longas': {
        'object_delivered': '✅ Entregue',
        'object_in_transit': '🚚 Em Trânsito',
        'object_out_for_delivery': '📦 Saiu para Entrega',
        'object_pending_pickup': '⏳ Aguardando Retirada',
        'object_exception': '❌ Exceção',
    }
}


# ============================================================================
# EXEMPLO 7: Tratamento de Respostas com Paginação
# ============================================================================

def exemplo_com_paginacao():
    """
    Se a API retorna dados paginados:
    """
    codigo_adaptacao = '''
    def consultar_por_rastreamento_com_paginacao(self, codigo_rastreamento: str) -> Optional[Dict]:
        """Para APIs com paginação"""
        rate_limiter.wait_if_needed()

        try:
            url = f"{self.base_url}/tracking"
            params = {
                'tracking_code': codigo_rastreamento,
                'page': 1,
                'per_page': 100
            }

            for tentativa in range(1, API_RETRIES + 1):
                try:
                    response = requests.get(
                        url,
                        params=params,
                        headers=self.headers,
                        timeout=self.timeout
                    )
                    response.raise_for_status()

                    dados = response.json()
                    
                    # Processar múltiplas páginas se necessário
                    if dados.get('total_pages', 1) > 1:
                        for page in range(2, dados['total_pages'] + 1):
                            params['page'] = page
                            response = requests.get(url, params=params, headers=self.headers, timeout=self.timeout)
                            # Combinar dados...

                    return self._processar_resposta_api(dados)

                except requests.exceptions.RequestException as e:
                    if tentativa < API_RETRIES:
                        logger.warning(f"Tentativa {tentativa} falhou: {str(e)}")
                    else:
                        logger.error(f"Falha em todas as {API_RETRIES} tentativas: {str(e)}")

            return None

        except Exception as e:
            logger.error(f"Erro inesperado: {str(e)}")
            return None
    '''
    pass


# ============================================================================
# EXEMPLO 8: Cache de Resultados para Reduzir Chamadas à API
# ============================================================================

def exemplo_com_cache():
    """
    Se quiser implementar cache para reduzir chamadas:
    """
    codigo_adaptacao = '''
    from functools import lru_cache
    from datetime import datetime, timedelta
    
    class ConsultadorAPIComCache:
        """Consultador com cache em memória"""
        
        def __init__(self):
            self.cache = {}
            self.tempo_cache = 3600  # 1 hora em segundos
            
        def _cache_expirado(self, chave: str) -> bool:
            if chave not in self.cache:
                return True
            timestamp, _ = self.cache[chave]
            return (datetime.now() - timestamp).seconds > self.tempo_cache
            
        def consultar_com_cache(self, codigo_rastreamento: str) -> Optional[Dict]:
            """Consulta com cache"""
            if codigo_rastreamento in self.cache and not self._cache_expirado(codigo_rastreamento):
                logger.debug(f"Retornando resultado em cache para {codigo_rastreamento}")
                _, dados = self.cache[codigo_rastreamento]
                return dados
                
            # Se não está em cache, consulta API
            resultado = self.consultar_por_rastreamento(codigo_rastreamento)
            
            if resultado:
                self.cache[codigo_rastreamento] = (datetime.now(), resultado)
                
            return resultado
    '''
    pass


# ============================================================================
# EXEMPLO 9: Adaptar Coluna de Status Dinâmica
# ============================================================================

def exemplo_coluna_status_dinamica():
    """
    Se a coluna de status tiver nome dinâmico:
    """
    codigo_adaptacao = '''
    # Em config.py, permitir detecção automática
    def detectar_coluna_status(df) -> str:
        """Detecta automaticamente coluna de status"""
        palavras_chave = ['status', 'estado', 'situação', 'rastreamento']
        for col in df.columns:
            if any(palavra in col.lower() for palavra in palavras_chave):
                return col
        return 'Status'  # Padrão
    '''
    pass


# ============================================================================
# EXEMPLO 10: Integração com Múltiplas Transportadoras
# ============================================================================

def exemplo_multiplas_transportadoras():
    """
    Se precisar consultar múltiplas transportadoras:
    """
    codigo_adaptacao = '''
    class ConsultadorMultipleTransportadoras:
        """Gerencia consultas para múltiplas transportadoras"""
        
        def __init__(self):
            self.apis = {
                'transportadora_a': ConsultadorAPI('https://api-a.com'),
                'transportadora_b': ConsultadorAPI('https://api-b.com'),
            }
            
        def consultar_inteligente(self, numero_nf: str, codigo_rastreamento: str) -> Optional[Dict]:
            """Tenta consultar em múltiplas transportadoras"""
            for nome_transportadora, api in self.apis.items():
                try:
                    # Tenta por rastreamento
                    if codigo_rastreamento:
                        resultado = api.consultar_por_rastreamento(codigo_rastreamento)
                    else:
                        resultado = api.consultar_por_nf(numero_nf)
                        
                    if resultado:
                        resultado['transportadora'] = nome_transportadora
                        return resultado
                except Exception as e:
                    logger.debug(f"Falha em {nome_transportadora}: {str(e)}")
                    
            return None
    '''
    pass


def imprimir_resumo():
    """Imprime resumo dos exemplos"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║     EXEMPLOS DE INTEGRAÇÃO PARA DIFERENTES APIs           ║
    ╚════════════════════════════════════════════════════════════╝
    
    Este arquivo contém 10 exemplos de como adaptar o código:
    
    1. API Genérica (padrão)
    2. REST Simples
    3. OAuth2
    4. Dados Aninhados
    5. SOAP/XML
    6. Diferentes Mapeamentos de Status
    7. Paginação
    8. Cache
    9. Coluna de Status Dinâmica
    10. Múltiplas Transportadoras
    
    Para usar um exemplo:
    - Copie o código do exemplo
    - Adapte para sua API específica
    - Salve em api_rastreamento.py
    - Teste com dados reais
    
    Consulte GUIA_INTEGRACAO.md para instruções detalhadas!
    """)


if __name__ == '__main__':
    imprimir_resumo()
