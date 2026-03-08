# 🔧 Guia de Integração - Adaptando para sua Transportadora

Este arquivo fornece instruções passo a passo para adaptar a solução para sua transportadora específica.

## 🔍 Passo 1: Analisar a Documentação da API

### O que você precisa descobrir:

1. **URL Base da API**
   - Exemplo: `https://api.transportadora.com.br/v1`
   - Onde colocar: `config.py` - `API_BASE_URL`

2. **Endpoints Disponíveis**
   - Endpoint para buscar por NF (Nota Fiscal)
   - Endpoint para buscar por código de rastreamento
   - Endpoint de healthcheck (opcional)

3. **Parâmetros de Requisição**
   - Quais parâmetros são necessários (GET ou POST)
   - Quais parâmetros são obrigatórios
   - Formato esperado (JSON, URL params, etc.)

4. **Autenticação**
   - É necessária chave de API?
   - Bearer Token?
   - Basic Auth?
   - OAuth2?

5. **Estrutura da Resposta**
   - Formato da resposta (JSON)
   - Quais campos estão disponíveis
   - Como está estruturada a resposta

### Exemplo de Documentação da API

```
GET /api/tracking/search
Parâmetros:
  - tracking_code: código de rastreamento (obrigatório)
  - apikey: sua chave de API (obrigatório)

Resposta:
{
  "success": true,
  "data": {
    "tracking_number": "BR123456789ABC",
    "status": "DELIVERED",
    "status_name": "Entregue",
    "last_update": "2026-03-03T10:30:00",
    "location": "São Paulo, SP",
    "events": [
      {
        "status": "DELIVERED",
        "date": "2026-03-03",
        "message": "Entregue",
        "location": "São Paulo, SP"
      }
    ]
  }
}
```

## 🛠️ Passo 2: Adaptar Métodos de Consulta (api_rastreamento.py)

### Editar `consultar_por_rastreamento()`

**Encontre:**
```python
def consultar_por_rastreamento(self, codigo_rastreamento: str) -> Optional[Dict]:
    """
    Consulta rastreamento por código de rastreamento
    ...
    IMPORTANTE: Adapte este método conforme a estrutura específica da sua API
    """
    rate_limiter.wait_if_needed()

    try:
        # EXEMPLO: Adapte conforme sua API
        # url = f"{self.base_url}/tracking/{codigo_rastreamento}"
        # Exemplo genérico abaixo - MUDE CONFORME SUA API

        url = f"{self.base_url}/search"
        params = {
            'tracking': codigo_rastreamento,
            'type': 'tracking'
        }
```

**Adapte para sua API:**
```python
def consultar_por_rastreamento(self, codigo_rastreamento: str) -> Optional[Dict]:
    rate_limiter.wait_if_needed()

    try:
        # Adapte conforme sua API
        url = f"{self.base_url}/tracking/search"  # Seu endpoint real
        params = {
            'tracking_code': codigo_rastreamento,  # Seu parâmetro real
            'apikey': API_KEY  # Se usar parâmetro em vez de header
        }

        logger.debug(f"Consultando API por rastreamento: {codigo_rastreamento}")

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
                logger.info(f"Consulta de rastreamento bem-sucedida: {codigo_rastreamento}")
                return self._processar_resposta_api(dados)
                # ... resto do código permanece igual
```

### Editar `_processar_resposta_api()`

**Encontre:**
```python
def _processar_resposta_api(self, dados: Dict) -> Optional[Dict]:
    """
    Processa e padroniza a resposta da API
    IMPORTANTE: Adapte este método conforme a estrutura específica da sua API
    ...
    """
    try:
        # EXEMPLO: Adapte conforme a estrutura da sua API
        # Se sua API retorna dados aninhados, extraia aqui

        if not dados:
            return None

        # Exemplo de estrutura esperada (MUDE CONFORME SUA API):
        resultado = {
            'numero_nf': dados.get('nf') or dados.get('invoice_number', ''),
            'codigo_rastreamento': dados.get('tracking_code') or dados.get('code', ''),
            'status_codigo': dados.get('status', {}).get('code', ''),
            'status_descricao': dados.get('status', {}).get('description', ''),
            'status_amigavel': '',
            'data_atualizacao': dados.get('last_update') or dados.get('updated_at', ''),
            'localizacao': dados.get('location', ''),
            'detalhes': {
                # ...
            },
            'historico': dados.get('events', [])
        }
```

**Adapte para sua API:**
```python
def _processar_resposta_api(self, dados: Dict) -> Optional[Dict]:
    try:
        if not dados:
            return None

        # Adapte conforme a estrutura REAL da sua API
        # Exemplo: sua API responde com {"success": true, "data": {...}}
        
        # Primeiro, extraia os dados se estão aninhados
        dados_reais = dados.get('data', dados)  # Se dados estão em .data
        
        resultado = {
            'numero_nf': dados_reais.get('invoice_number', '') or dados_reais.get('nf', ''),
            'codigo_rastreamento': dados_reais.get('tracking_number', ''),
            'status_codigo': dados_reais.get('status', ''),  # Ex: "DELIVERED"
            'status_descricao': dados_reais.get('status_name', ''),  # Ex: "Entregue"
            'status_amigavel': '',
            'data_atualizacao': dados_reais.get('last_update', ''),
            'localizacao': dados_reais.get('location', ''),
            'detalhes': {
                'endereco_entrega': dados_reais.get('delivery_address', ''),
                'remetente': dados_reais.get('sender_name', ''),
                'destinatario': dados_reais.get('recipient_name', ''),
                'peso': dados_reais.get('weight', ''),
                'valor': dados_reais.get('value', '')
            },
            'historico': dados_reais.get('events', [])
        }

        # Mapeia status para forma amigável
        status_codigo = resultado['status_codigo'].lower()
        resultado['status_amigavel'] = MAPEAMENTO_STATUS.get(status_codigo, resultado['status_descricao'])

        return resultado

    except Exception as e:
        logger.error(f"Erro ao processar resposta da API: {str(e)}")
        return None
```

## 🔂 Passo 3: Configurar Mapeamento de Status (config.py)

### 1. Liste todos os Status Possíveis da API

Consulte a documentação e identifique todos os códigos de status possíveis:

```
DELIVERED = Entregue
IN_TRANSIT = Em Trânsito
OUT_FOR_DELIVERY = Saiu para Entrega
PENDING_PICKUP = Aguardando Retirada
NOT_DELIVERED = Não Entregue
RETURNED = Devolvido
CANCELLED = Cancelado
ERROR = Erro
```

### 2. Atualize `MAPEAMENTO_STATUS` em `config.py`

**Encontre:**
```python
MAPEAMENTO_STATUS = {
    'entregue': '✅ Entregue',
    'em_transito': '🚚 Em Trânsito',
    # ...
}
```

**Adapte:**
```python
# Use os códigos EXATOS que sua API retorna
MAPEAMENTO_STATUS = {
    'delivered': '✅ Entregue',           # Status exato da API
    'in_transit': '🚚 Em Trânsito',
    'out_for_delivery': '📦 Saiu para Entrega',
    'pending_pickup': '⏳ Aguardando Retirada',
    'not_delivered': '❌ Não Entregue',
    'returned': '↩️ Devolvido',
    'cancelled': '🚫 Cancelado',
    'error': '⚠️ Erro na Busca'
}
```

## 🧪 Passo 4: Testar a Integração

### 4.1. Teste de Conexão

```bash
python -c "
from api_rastreamento import ConsultadorAPI
api = ConsultadorAPI()
sucesso, msg = api.teste_conexao()
print(f'Conexão: {msg}')
"
```

### 4.2. Teste Manual de Consulta

```python
# Crie um arquivo teste_api.py
from api_rastreamento import ConsultadorAPI
import json

api = ConsultadorAPI()

# Teste com um rastreamento real
resultado = api.consultar_por_rastreamento('CODIGO_DE_TESTE_REAL')

if resultado:
    print("✓ Sucesso!")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
else:
    print("✗ Falha na consulta")
    print("Verifique os logs em logs/")
```

### 4.3. Teste com Planilha

```bash
# 1. Criar planilha modelo
python cli.py criar-modelo

# 2. Preencher com dados reais
# (Edite planilha_rastreamento.xlsx com dados reais de teste)

# 3. Processar
python cli.py processar

# 4. Verifique os resultados e logs
```

## 🔐 Passo 5: Configurar Variáveis de Ambiente

### Editar `.env`

```env
# URL e chaves da sua API
API_BASE_URL=https://api.sua-transportadora.com.br/v1
API_TIMEOUT=30
API_RETRIES=3
API_KEY=sua_chave_de_api_aqui

# Se usar autenticação em header customizado
# (Edite headers em _preparar_headers())

# Configuração de rate limiting
# Consulte documentação da API para saber o limite
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60

# Arquivo Excel com dados
EXCEL_FILE_PATH=planilha_rastreamento.xlsx

# Adapte aos nomes de coluna da SUA planilha
COLUNA_NF=NF
COLUNA_RASTREAMENTO=Rastreamento
COLUNA_STATUS=Status
COLUNA_ULTIMA_ATUALIZACAO=Última Atualização
COLUNA_DETALHES=Detalhes
```

## 🎯 Checklist de Integração

- [ ] URL da API está correta em `config.py` (API_BASE_URL)
- [ ] Métodos `consultar_por_nf()` e `consultar_por_rastreamento()` foram adaptados
- [ ] Método `_processar_resposta_api()` extrai os campos corretos
- [ ] `MAPEAMENTO_STATUS` foi atualizado com os códigos reais da API
- [ ] Autenticação está configurada (headers e chave)
- [ ] Rate limiting foi ajustado conforme recomendação da API
- [ ] Teste de conexão passou (`api.teste_conexao()`)
- [ ] Teste manual de consulta funcionou
- [ ] Processamento de planilha real funcionou
- [ ] Logs mostram que dados estão sendo extraídos corretamente

## 🐛 Troubleshooting

### "Status code 401 - Unauthorized"
- Verifique `API_KEY` em `.env`
- Verifique se autenticação está correta em `_preparar_headers()`
- Teste a chave na documentação da API

### "Status code 400 - Bad Request"
- Verifique nomes dos parâmetros (case-sensitive)
- Verifique formato dos parâmetros
- Consulte novamente a documentação da API

### "Connection timeout"
- URL da API está correta?
- IP da sua máquina está na whitelist (se houver)?
- Aumentar `API_TIMEOUT` em `config.py`

### "Nenhum status é atualizado"
- Verifique se resposta está sendo processada corretamente
- Adicione logs em `_processar_resposta_api()` para debug
- Veja se códigos de status em (MAPEAMENTO_STATUS correspondem à API

## 📚 Referências Úteis

- [Requests Documentation](https://docs.python-requests.org/)
- [Pandas Excel Documentation](https://pandas.pydata.org/docs/user_guide/io.html#excel-files)
- [Documentação de sua Transportadora]

## 💡 Dicas Finais

1. **Comece pequeno**: Teste com 1-2 registros antes de processar toda a planilha
2. **Use logs**: Ative `LOG_LEVEL=DEBUG` para mais detalhes durante adaptação
3. **Verifique respostas reais**: Use ferramentas como Postman para testar a API diretamente
4. **Backup sempre**: Certifique-se de que backups estão sendo criados
5. **Documentação é ouro**: Salve a documentação da API para referência futura

---

Se precisar de ajuda adicional com sua API específica, consulte a documentação fornecida pela sua transportadora.
