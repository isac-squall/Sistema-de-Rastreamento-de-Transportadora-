"""
Arquivo de configuração para a solução de rastreamento de transportadora
"""

import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# ============== CONFIGURAÇÃO DA API ==============
# URL base padronizada para quem utiliza siterastreio.com.br/correios
API_BASE_URL = os.getenv('API_BASE_URL', "https://www.siterastreio.com.br/api-correios")  # Adapte conforme sua API
API_TIMEOUT = int(os.getenv('API_TIMEOUT', 30))  # Timeout em segundos
API_RETRIES = int(os.getenv('API_RETRIES', 3))  # Número de tentativas
API_KEY = os.getenv('API_KEY', '')  # Chave da API (opcional)
API_USER = os.getenv('API_USER', '')  # Usuário da API (opcional)

# ============== CONFIGURAÇÃO DE RATE LIMITING ==============
RATE_LIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', 100))  # Requisições por período
RATE_LIMIT_PERIOD = int(os.getenv('RATE_LIMIT_PERIOD', 60))  # Periodo em segundos

# ============== CONFIGURAÇÃO DE ARQUIVOS ==============
EXCEL_FILE_PATH = os.getenv('EXCEL_FILE_PATH', 'planilha_rastreamento.xlsx')
BACKUP_FOLDER = os.getenv('BACKUP_FOLDER', 'backups')
LOG_FOLDER = os.getenv('LOG_FOLDER', 'logs')

# ============== CONFIGURAÇÃO DE COLUNAS DO EXCEL ==============
COLUNA_NF = os.getenv('COLUNA_NF', 'NF')  # Coluna com Nota Fiscal
COLUNA_RASTREAMENTO = os.getenv('COLUNA_RASTREAMENTO', 'Rastreamento')  # Coluna com código de rastreamento
COLUNA_STATUS = os.getenv('COLUNA_STATUS', 'Status')  # Coluna de status
COLUNA_ULTIMA_ATUALIZACAO = os.getenv('COLUNA_ULTIMA_ATUALIZACAO', 'Última Atualização')  # Coluna de data
COLUNA_DETALHES = os.getenv('COLUNA_DETALHES', 'Detalhes')  # Coluna com detalhes do rastreamento

# ============== MAPEAMENTO DE STATUS ==============
# Mapeia status da API para status amigável (adaptado para Correios)
MAPEAMENTO_STATUS = {
    'entregue': '✅ Entregue',
    'objeto entregue ao destinatário': '✅ Entregue',
    'objeto entregue ao destinatario': '✅ Entregue',
    'em_transito': '🚚 Em Trânsito',
    'objeto em trânsito': '🚚 Em Trânsito',
    'objeto em transito': '🚚 Em Trânsito',
    'saiu_para_entrega': '📦 Saiu para Entrega',
    'objeto saiu para entrega': '📦 Saiu para Entrega',
    'objeto saiu para entrega ao destinatário': '📦 Saiu para Entrega',
    'aguardando_retirada': '⏳ Aguardando Retirada',
    'objeto aguardando retirada': '⏳ Aguardando Retirada',
    'nao_entregue': '❌ Não Entregue',
    'objeto não entregue': '❌ Não Entregue',
    'devolvido': '↩️ Devolvido',
    'objeto devolvido': '↩️ Devolvido',
    'cancelado': '🚫 Cancelado',
    'objeto cancelado': '🚫 Cancelado',
    'objeto postado': '📮 Objeto Postado',
    'objeto recebido na unidade de distribuição': '📬 Recebido na Unidade',
    'erro': '⚠️ Erro na Busca'
}

# ============== CONFIGURAÇÃO DE LOGGING ==============
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%d/%m/%Y %H:%M:%S'

# ============== CONFIGURAÇÃO DE PROCESSAMENTO ==============
ATUALIZAR_APENAS_MUDANCAS = os.getenv('ATUALIZAR_APENAS_MUDANCAS', 'True').lower() == 'true'
CRIAR_BACKUP_ANTES = os.getenv('CRIAR_BACKUP_ANTES', 'True').lower() == 'true'
SALVAR_RELATORIO = os.getenv('SALVAR_RELATORIO', 'True').lower() == 'true'
