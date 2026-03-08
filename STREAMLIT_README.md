# 🌐 Interface Streamlit - Sistema de Rastreamento

A aplicação Streamlit fornece uma interface web intuitiva para gerenciar rastreamentos de transportadoras.

## 🚀 Como Executar

### Opção 1: Duplo clique no arquivo batch (Windows recomendado)
```
executar_streamlit.bat
```

A aplicação abrirá automaticamente em seu navegador padrão.

### Opção 2: Linha de comando
```bash
# Ative o ambiente virtual
.\venv\Scripts\activate

# Execute o Streamlit
streamlit run app.py
```

### Opção 3: Python direto
```bash
python -m streamlit run app.py
```

## 📍 Acessar a Aplicação

Após iniciar, acesse:
```
http://localhost:8501
```

## 🎯 Funcionalidades da Interface

### 🏠 Início
- Bem-vindo e instruções rápidas
- Status do sistema em tempo real
- Acesso rápido às principais funções

### ⚙️ Processar Rastreamentos
- Opções de processamento:
  - Criar backup antes
  - Salvar relatório
  - Limpar logs antigos
- Visualização em tempo real do progresso
- Estatísticas do processamento
- Gráficos de distribuição de status

### 📊 Visualizar Dados
- Leitura da planilha Excel
- Filtros por status
- Visualização de dados
- Estatísticas em tempo real
- Download em CSV

### 💾 Backup e Restauração
- Listar todos os backups
- Restaurar versão anterior
- Deleter backups antigos
- Ver detalhes (data, tamanho)

### 📈 Relatórios
- Visualizar logs de processamento
- Estatísticas gerais
- Download de logs

### ℹ️ Sobre
- Informações do projeto
- Características
- Tecnologias utilizadas
- Links para documentação

## 🎨 Interface

A interface é dividida em:
- **Sidebar (esquerda):** Menu de navegação
- **Main (centro):** Conteúdo da seção selecionada
- **Top (topo):** Título e subtítulo

## 💡 Dicas

1. **Primeiro acesso:** Comece pela página "Início"
2. **Configurar API:** Edite `.env` antes de processar
3. **Criar planilha:** Use a opção na página "Visualizar Dados"
4. **Erros:** Verifique os logs na seção "Relatórios"

## 🔧 Requisitos

- Python 3.8+
- Streamlit (já instalado)
- Demais dependências em `requirements.txt`

## 📦 Dependências Streamlit

```
streamlit==1.55.0
pandas>=2.0.0
openpyxl
requests
python-dotenv
```

## 🐛 Troubleshooting

### Porta 8501 já em uso
```bash
streamlit run app.py --server.port 8502
```

### Cache do Streamlit
```bash
streamlit cache clear
```

### Resetar Streamlit
```bash
streamlit run app.py --logger.level=debug
```

## 📝 Notas

- A aplicação cria pastas `logs/` e `backups/` automaticamente
- Logs são salvos a cada processamento
- Backups podem ser restaurados a qualquer momento
- Não compartilhe o arquivo `.env` (contém dados sensíveis)

## 🚀 Próximos Passos

1. Execute: `executar_streamlit.bat` (Windows)
2. Configure sua API em `.env`
3. Crie uma planilha modelo
4. Processe seus rastreamentos
5. Monitore em tempo real na interface

---

**Desenvolvido com ❤️ e Streamlit**
