# 🚀 Guia Rápido - Começar em 5 Minutos

## 1️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

## 2️⃣ Configurar a API

Edite o arquivo `.env`:

```env
API_BASE_URL=https://sua-api-da-transportadora.com.br
API_KEY=sua_chave_de_api_aqui
```

Para adaptar os métodos de API, veja [GUIA_INTEGRACAO.md](./GUIA_INTEGRACAO.md)

## 3️⃣ Criar Planilha Modelo

```bash
python cli.py criar-modelo
```

Isso cria `planilha_rastreamento.xlsx` com a estrutura correta.

## 4️⃣ Preencher Dados

Abra `planilha_rastreamento.xlsx` e preencha as colunas:
- **NF**: Número da Nota Fiscal
- **Rastreamento**: Código de rastreamento
- Coloque pelo menos um desses dois por linha

## 5️⃣ Processar

```bash
python cli.py processar
```

✅ Pronto! A planilha foi atualizada com os status de rastreamento.

## 📊 Comandos Disponíveis

```bash
# Processar rastreamentos (com backup automático)
python cli.py processar

# Processar sem criar backup
python cli.py processar --sem-backup

# Criar planilha modelo
python cli.py criar-modelo

# Listar backups disponíveis
python cli.py listar-backups

# Restaurar um backup anterior
python cli.py restaurar-backup backups/arquivo_backup.xlsx
```

## 📝 Logs

Os logs são salvos em `logs/` com timestamps. Para ver o log mais recente:

```bash
# Windows
type logs\*.log

# Linux/macOS
cat logs/*.log
```

## 🔧 Adaptar para Sua Transportadora

Sua API pode ter estrutura diferente. Siga estes passos:

1. Edite `api_rastreamento.py` - métodos `consultar_por_rastreamento()` e `_processar_resposta_api()`
2. Atualize `MAPEAMENTO_STATUS` em `config.py` com os códigos de sua API
3. Configure `API_BASE_URL` em `.env`
4. Teste com dados reais

Veja [GUIA_INTEGRACAO.md](./GUIA_INTEGRACAO.md) para instruções detalhadas.

## 🐛 Problemas?

1. **Arquivo não encontrado**: Crie modelo com `python cli.py criar-modelo`
2. **Conexão recusada**: Verifique `API_BASE_URL` e `API_KEY` em `.env`
3. **Sem atualizações**: Veja logs em `logs/` para erros específicos
4. **Restaurar versão anterior**: `python cli.py listar-backups` depois `python cli.py restaurar-backup ...`

## 📚 Documentação Completa

- [README.md](./README.md) - Documentação detalhada
- [GUIA_INTEGRACAO.md](./GUIA_INTEGRACAO.md) - Como adaptar para sua API

---

**Precisa de ajuda?** Consulte os arquivos de documentação acima.
