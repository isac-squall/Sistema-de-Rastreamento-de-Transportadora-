# 📦 Sistema de Rastreamento de Transportadora

Solução completa em Python para consumir APIs de transportadoras, atualizar planilhas Excel e gerenciar status de rastreamentos com segurança e confiabilidade.

## ✨ Características Principais

✅ **Consumo de API** - Consulta por NF ou código de rastreamento
✅ **Backup Automático** - Proteção de dados antes de alterações
✅ **Logging Completo** - Rastreamento detalhado de todas as operações
✅ **Tratamento de Erros** - Robustez contra falhas de rede e API
✅ **Rate Limiting** - Proteção contra sobrecarga da API
✅ **Mapeamento de Status** - Personalizável para diferentes transportadoras
✅ **Relatório Final** - Estatísticas completas do processamento
✅ **Timeout Configurável** - Controle sobre requisições HTTP
✅ **Formatação Visual** - Aplicação automática de cores e estilos no Excel
✅ **Recuperação de Backups** - Restauração simples de versões anteriores

## 📋 Estrutura do Projeto

```
Automação.Transportadora/
├── main.py                    # Módulo principal orquestrador
├── api_rastreamento.py       # Consumo da API da transportadora
├── processador_excel.py      # Manipulação de planilhas Excel
├── utils.py                  # Rate limiter e gerenciador de backup
├── config.py                 # Configurações centralizadas
├── logger_setup.py           # Sistema de logging
├── cli.py                    # Interface de linha de comando
├── requirements.txt          # Dependências Python
├── .env.example              # Exemplo de variáveis de ambiente
└── README.md                 # Esta documentação
```

## 🚀 Instalação

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. **Clone ou copie o projeto:**
```bash
cd c:\Users\Windows\Desktop\Automação.Transportadora
```

2. **Crie um ambiente virtual (recomendado):**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual:**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

5. **Configure as variáveis de ambiente:**
```bash
# Copie o arquivo de exemplo
copy .env.example .env

# Edite o arquivo .env com suas configurações
```

## 💻 Git & Deploy Automático

O repositório já conta com utilitários para automatizar o fluxo de atualização e
implantação da aplicação Streamlit. Existem duas opções:

1. **Script PowerShell local** (`auto_deploy.ps1`):
   - Executa `git add .`, `git commit`, `git pull` e `git push` na branch `main`.
   - Aceita o parâmetro `-CommitMessage` para customizar a mensagem de commit e o
     switch `-RunLocalStreamlit` para iniciar o servidor local após o push.
   - Exemplo:
     ```powershell
     # apenas sincroniza com o remoto
     .\auto_deploy.ps1 -CommitMessage "Atualiza rastreamento"

     # sincroniza e abre o app local
     .\auto_deploy.ps1 -RunLocalStreamlit
     ```

2. **Workflow GitHub Actions** (`.github/workflows/deploy-streamlit.yml`):
   - Dispara automaticamente a cada `push` na branch `main`.
   - Faz checkout do código, instala dependências e usa o [action oficial do
     Streamlit](https://github.com/streamlit/action) para redeploy na Streamlit
     Community Cloud.
   - Basta ter seu app conectado ao repo; o deploy acontece sem intervenção.

> 💡 o deploy local (`-RunLocalStreamlit`) ignora configurações de nuvem, é útil
> para desenvolvimento. A ação do GitHub garante que a versão pública esteja
> atualizada automaticamente sempre que você fizer `git push`.


## ⚙️ Configuração

### Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# URL base da API da transportadora
API_BASE_URL=https://www.siterastreio.com.br/api-correios

# Timeout para requisições (segundos)
API_TIMEOUT=30

# Número de tentativas em caso de falha
API_RETRIES=3

# Chave de API (se necessário)
API_KEY=sua_chave_aqui

# Taxa de requisições permitidas
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60

# Caminho da planilha Excel
EXCEL_FILE_PATH=planilha_rastreamento.xlsx

# Pastas de armazenamento
BACKUP_FOLDER=backups
LOG_FOLDER=logs

# Colunas da planilha
COLUNA_NF=NF
COLUNA_RASTREAMENTO=Rastreamento
COLUNA_STATUS=Status
COLUNA_ULTIMA_ATUALIZACAO=Última Atualização
COLUNA_DETALHES=Detalhes

# Nível de log (INFO, DEBUG, WARNING, ERROR)
LOG_LEVEL=INFO

# Opções de processamento
ATUALIZAR_APENAS_MUDANCAS=True    # Atualizar apenas se status mudar
CRIAR_BACKUP_ANTES=True            # Criar backup antes de processar
SALVAR_RELATORIO=True              # Salvar relatório em arquivo
```

### Adaptar para sua Transportadora

Os métodos principais em `api_rastreamento.py` precisam ser adaptados para sua API específica:

#### 1. **Ajustar URL e Parâmetros** (`consultar_por_nf` e `consultar_por_rastreamento`):

```python
# Adapte conforme sua API
url = f"{self.base_url}/seu_endpoint"
params = {
    'seu_parametro': valor,
    'outro_parametro': outro_valor
}
```

#### 2. **Processar Resposta da API** (`_processar_resposta_api`):

```python
def _processar_resposta_api(self, dados: Dict) -> Optional[Dict]:
    # Extrair campos conforme estrutura da sua API
    resultado = {
        'numero_nf': dados.get('seu_campo_nf', ''),
        'codigo_rastreamento': dados.get('seu_campo_rastreamento', ''),
        'status_codigo': dados.get('status_code', ''),
        'status_descricao': dados.get('status_desc', ''),
        # ... outros campos
    }
    return resultado
```

#### 3. **Mapear Códigos de Status** (em `config.py`):

```python
MAPEAMENTO_STATUS = {
    'seu_status_1': '✅ Status Amigável 1',
    'seu_status_2': '🚚 Status Amigável 2',
    # ... adicione todos os status da sua API
}
```

## 📊 Estrutura da Planilha Excel

A planilha deve conter as seguintes colunas (nomes configuráveis):

| Coluna | Descrição | Obrigatória |
|--------|-----------|------------|
| NF | Número da Nota Fiscal | Sim* |
| Rastreamento | Código de rastreamento | Sim* |
| Status | Status atual do rastreamento | Sim |
| Última Atualização | Data/hora da última atualização | Não |
| Detalhes | Informações adicionais | Não |

*\* Pelo menos uma deve estar preenchida por linha*

### Criar Planilha Modelo

Para criar uma planilha modelo com a estrutura correta:

```bash
python cli.py criar-modelo
```

## 🔧 Modo de Uso

### 1. **Processar Rastreamentos** (Uso Principal)

```bash
# Processa com backup automático
python cli.py processar

# Processa sem backup
python cli.py processar --sem-backup

# Ou execute o script diretamente
python main.py
```

### 2. **Gerenciar Backups**

```bash
# Listar todos os backups
python cli.py listar-backups

# Restaurar um backup específico
python cli.py restaurar-backup backups/planilha_rastreamento_backup_20260304_120000.xlsx
```

### 3. **Criar Planilha Modelo**

```bash
python cli.py criar-modelo
```

## 📝 Log e Relatórios

### Arquivos de Log

Os logs são armazenados em `logs/` com nomes como:
```
rastreamento_20260304_102030.log
```

### Relatório de Processamento

Após cada processamento, um relatório é gerado:

```
================================================================================
                    RELATÓRIO DE ATUALIZAÇÃO DE RASTREAMENTOS
================================================================================

Data/Hora do Processamento: 04/03/2026 10:20:30

ESTATÍSTICAS:
  ✓ Total de registros processados: 150
  ✓ Registros com sucesso: 145
  ✓ Registros com mudança de status: 82
  ✓ Registros com erro: 5
  
DISTRIBUIÇÃO DE STATUS:
  • ✅ Entregue: 45
  • 🚚 Em Trânsito: 62
  • ⏳ Aguardando Retirada: 28
  • ⚠️ Erro na Busca: 5

================================================================================
```

## 🔒 Segurança e Boas Práticas

### Backup Automático

- Antes de cada processamento, um backup é criado automaticamente
- Backups antigos (>30 dias) são removidos automaticamente
- Você pode restaurar qualquer versão anterior

### Rate Limiting

- Evita sobrecarga da API
- Pausa automaticamente se limite é atingido
- Configurável via variáveis de ambiente

### Tratamento de Erros

- Tentativas automáticas em caso de falha
- Logging detalhado de todos os erros
- Processamento continua mesmo se houver falhas isoladas

### Timeout

- Requisições têm timeout configurável
- Evita travamento em caso de API lenta
- Padrão: 30 segundos

## 🐛 Troubleshooting

### Erro: "Arquivo não encontrado"

```
Solução: Crie a planilha modelo primeiro
python cli.py criar-modelo
```

### Erro: "Módulo não encontrado"

```
Solução: Instale as dependências
pip install -r requirements.txt
```

### Erro: "Conexão recusada na API"

```
Verifique:
1. URL da API está correta em .env
2. Chave de API (se necessária) foi preenchida
3. Sua rede tem acesso à API
python -c "from api_rastreamento import ConsultadorAPI; api = ConsultadorAPI(); print(api.teste_conexao())"
```

### Nenhum registro é atualizado

```
Verifique:
1. Os nomes das colunas em .env correspondem à planilha
2. As colunas NF e Rastreamento têm valores preenchidos
3. Os métodos da API foram adaptados para sua transportadora
4. Verifique os logs em logs/ para mais detalhes
```

## 📚 Exemplos de Uso Avançado

### Integração com Agendador (Windows Task Scheduler)

```batch
@echo off
cd c:\Users\Windows\Desktop\Automação.Transportadora
python cli.py processar
```

Agende este arquivo no Task Scheduler para executar periodicamente.

### Integração com Agendador (Linux/macOS - crontab)

```cron
# Executar todos os dias às 10:00
0 10 * * * cd /path/to/Automação.Transportadora && python cli.py processar
```

### Uso Programático (Python)

```python
from main import OrquestradorRastreamento

# Criar orquestrador
orq = OrquestradorRastreamento()

# Processar rastreamentos
sucesso = orq.processar_rastreamentos(criar_backup=True)

# Obter estatísticas
stats = orq.obter_atualizacoes()
print(f"Sucesso: {stats['sucesso']}, Erros: {stats['erros']}")

# Listar backups
backups = orq.listar_backups()
for backup in backups:
    print(f"{backup['arquivo']} - {backup['data']}")
```

## 🤝 Contribuindo

Para melhorar o projeto:

1. Adapte os métodos para sua transportadora específica
2. Teste completamente em ambiente de desenvolvimento
3. Crie backups regulares
4. Monitorar os logs para identificar problemas

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs em `logs/`
2. Verifique a configuração em `.env`
3. Teste a conexão com a API
4. Revise este README

## 📄 Licença

Este projeto é fornecido como está, para uso em automação de transportadoras.

## 🎯 Roadmap

- [ ] Suporte para múltiplas transportadoras
- [ ] Interface gráfica (GUI)
- [ ] Webhook para sincronização em tempo real
- [ ] Suporte a outros formatos (CSV, Google Sheets)
- [ ] Autenticação com OAuth2
- [ ] Dashboard de estatísticas

---

**Desenvolvido para otimizar a automação de rastreamentos de transportadores.**
