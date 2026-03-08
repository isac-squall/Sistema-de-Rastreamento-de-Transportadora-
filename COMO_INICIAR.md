# 🚀 Como Iniciar o Streamlit

Existem **3 formas** para iniciar o sistema de rastreamento:

## Opção 1️⃣ - Arquivo BAT (Mais Fácil)

**Clique duas vezes no arquivo:**
```
executar_streamlit.bat
```

**O que acontece:**
1. ✅ PowerShell/CMD abre automaticamente
2. ✅ Ambiente virtual é ativado
3. ✅ Aguarda 3 segundos
4. ✅ Navegador abre em http://localhost:8501
5. ✅ Streamlit inicia

**Para parar:** Pressione `CTRL+C` na janela do console

---

## Opção 2️⃣ - Script PowerShell (Mais Robusto)

**Abra PowerShell e execute:**
```powershell
.\iniciar_streamlit.ps1
```

**Se der erro de permissão, execute primeiro:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**O que acontece:**
- Similar ao arquivo BAT, mas com melhor tratamento de erros
- Mensagens coloridas no console
- Feedback melhor em caso de problemas

---

## Opção 3️⃣ - Terminal Manual

**Abra o terminal na pasta do projeto e execute:**

```bash
# Ativar ambiente virtual
.\venv\Scripts\activate

# Iniciar Streamlit
streamlit run app.py
```

Então **abra manualmente** no navegador: http://localhost:8501

---

## ✅ Verificar se Está Funcionando

Quando o Streamlit iniciar com sucesso, você verá:

```
  Welcome to Streamlit! 🎈

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

E o navegador deve abrir automaticamente.

---

## ❌ Soluções de Problemas

### "Porta 8501 já está em uso"
```bash
# Altere a porta no comando:
streamlit run app.py --server.port=8502
```

### "Navegador não abre automaticamente"
Abra manualmente: **http://localhost:8501**

### "Erro ao ativar venv"
Recrie o ambiente:
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### "ModuleNotFoundError"
Certifique-se de que o venv está ativado. Você deve ver `(venv)` no prompt do console.

---

## 📊 Interface Streamlit

Após abrir, você verá a página inicial com:

1. 🏠 **Início** - Dashboard e status
2. ⚙️ **Processar Rastreamentos** - Consultar e atualizar Excel
3. 📊 **Visualizar Dados** - Ver conteúdo da planilha
4. 💾 **Backup e Restauração** - Gerenciar backups
5. 📈 **Relatórios** - Logs e estatísticas
6. ℹ️ **Sobre** - Informações do projeto

---

## 🎯 Próximos Passos

1. **Teste a interface** - Clique em cada seção
2. **Configure a API** - Edite o arquivo `.env`
3. **Customize os métodos** - Adapte `api_rastreamento.py` para sua API
4. **Processe dados reais** - Use a seção "Processar Rastreamentos"

Veja os guias para mais detalhes:
- 📖 **GUIA_RAPIDO.md** - Início rápido em 5 minutos
- 📖 **GUIA_INTEGRACAO.md** - Integração com sua API
- 📖 **README.md** - Documentação completa
