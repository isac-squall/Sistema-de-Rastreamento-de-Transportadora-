"""
Aplicação Streamlit para Sistema de Rastreamento de Transportadora
Execute com: streamlit run app.py
"""

import os
import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, cast
import glob

# prepare streamlit configuration for headless/cloud environments
# avoid first-run email prompt by creating credentials file in home dir
home_streamlit = os.path.expanduser("~/.streamlit")
os.makedirs(home_streamlit, exist_ok=True)
cred_file = os.path.join(home_streamlit, "credentials.toml")
if not os.path.exists(cred_file):
    try:
        with open(cred_file, "w", encoding="utf-8") as f:
            f.write("[general]\nemail = \"\"\n")
    except Exception:
        pass

# force headless (cloud) mode
os.environ.setdefault("STREAMLIT_SERVER_HEADLESS", "true")

# Importar módulos do projeto
from main import OrquestradorRastreamento
from utils import BackupManager
from config import EXCEL_FILE_PATH, COLUNA_RASTREAMENTO

# helper to show logs
import glob

def mostrar_ultimos_logs(limit: int = 20):
    """Retorna as últimas linhas do mais recente arquivo de log."""
    padrao = os.path.join("logs", "*.log")
    arquivos = glob.glob(padrao)
    if not arquivos:
        return "Nenhum log encontrado."
    mais_recente = max(arquivos, key=os.path.getmtime)
    try:
        with open(mais_recente, "r", encoding="utf-8", errors="ignore") as f:
            linhas = f.readlines()
        return "\n".join(linhas[-limit:])
    except Exception as e:
        return f"Erro ao ler log: {e}"

# Configurar página do Streamlit
st.set_page_config(
    page_title="🚚 Rastreamento de Transportadora",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .main-header {
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subheader {
        color: #555;
        font-size: 1.2em;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Título
st.markdown('<p class="main-header">🚚 Sistema de Rastreamento de Transportadora</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Automate, rastreie e atualize seus envios em tempo real</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # largura fixa para evitar warning de parâmetro em desuso
    st.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=Rastreamento", width=300)
    st.markdown("---")
    
    opcao = st.radio(
        "📋 Menu Principal",
        [
            "🏠 Início",
            "⚙️ Processar Rastreamentos",
            "📊 Visualizar Dados",
            "💾 Backup e Restauração",
            "📈 Relatórios",
            "ℹ️ Sobre"
        ],
        index=0
    )
    
    st.markdown("---")
    st.info("💡 Dica: Use o menu acima para navegar entre as funcionalidades")

# ============================================================================
# PÁGINA: INÍCIO
# ============================================================================
if opcao == "🏠 Início":
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✨ Bem-vindo!")
        st.write("""
        Esta aplicação automiza o rastreamento de pacotes de transportadoras.
        
        **Estrutura da planilha de rastreamento:**
        - Coluna A (NF): Número da Nota Fiscal (opcional)
        - Coluna B (Rastreamento): Código de rastreamento dos Correios ← **insira os códigos aqui**
        - Coluna C (Status): Será preenchido automaticamente pelo sistema
        - Coluna D (Última Atualização): Data/hora da última consulta
        - Coluna E (Detalhes): Informações adicionais
        
        **Funcionalidades principais:**
        - 🚀 Processar rastreamentos em massa
        - 📁 Gerenciar planilhas Excel
        - 💾 Backup automático
        - 📊 Visualizar dados e relatórios
        - 🔄 Restaurar versões anteriores
        """ )
        # campo para inserir código manualmente
        codigo_manual = st.text_area(
            "✏️ Insira códigos de rastreamento (um por linha)",
            help="Digite ou cole os códigos dos Correios aqui em vez de carregar uma planilha",
            height=100
        )
        if codigo_manual:
            st.session_state['codigos_manua'] = codigo_manual.splitlines()
        # upload também na página inicial
        uploaded_start = st.file_uploader(
            "📁 Carregar planilha de rastreamento (XLSX)", type=["xlsx"]
        )
        if uploaded_start is not None:
            try:
                with open(EXCEL_FILE_PATH, "wb") as f:
                    f.write(uploaded_start.getbuffer())
                st.success("✅ Planilha carregada com sucesso!")
            except Exception as e:
                    st.error(f"Falha ao salvar planilha: {e}")
    with col2:
        st.subheader("🚀 Comece Agora")
        if st.button("Processar Rastreamentos", use_container_width=True):
            st.session_state.navigation = "⚙️ Processar Rastreamentos"
            st.rerun()
        
        if st.button("Ver Planilha", use_container_width=True):
            st.session_state.navigation = "📊 Visualizar Dados"
            st.rerun()
        
        if st.button("Gerenciar Backups", use_container_width=True):
            st.session_state.navigation = "💾 Backup e Restauração"
            st.rerun()
    
    st.markdown("---")
    
    # Status do sistema
    st.subheader("📊 Status do Sistema")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Verificar arquivo Excel
    excel_existe = os.path.exists(EXCEL_FILE_PATH)
    with col1:
        if excel_existe:
            st.metric("📁 Planilha", "✅ Encontrada")
        else:
            st.metric("📁 Planilha", "❌ Não encontrada")
    
    # Contar Backups
    backups = cast(List[Dict[str, Any]], BackupManager.listar_backups())  # type: ignore
    with col2:
        st.metric("💾 Backups", f"{len(backups)}")
    
    # Logs
    log_folder = "logs"
    num_logs = len([f for f in os.listdir(log_folder) if f.endswith('.log')]) if os.path.exists(log_folder) else 0
    with col3:
        st.metric("📝 Logs", f"{num_logs}")
    
    # Status da API
    with col4:
        try:
            from api_rastreamento import ConsultadorAPI
            api = ConsultadorAPI()
            sucesso, _ = api.teste_conexao()
            status = "✅ Online" if sucesso else "⚠️ Offline"
        except Exception:
            status = "❌ Erro"
        st.metric("🔗 API", status)
    
    st.markdown("---")
    
    # Instruções rápidas
    st.subheader("📚 Instruções Rápidas")
    
    with st.expander("Como começar", expanded=False):
        st.write("""
        1. **Prepare sua planilha**: Certifique-se que tem as colunas conforme a estrutura abaixo:
           - **Coluna A (NF)**: Número da Nota Fiscal (opcional)
           - **Coluna B (Rastreamento)**: Código de rastreamento dos Correios ← AQUI você insere os códigos!
           - **Coluna C (Status)**: Será preenchido automaticamente pelo sistema
           - **Coluna D (Última Atualização)**: Data/hora da última consulta
           - **Coluna E (Detalhes)**: Informações adicionais
        
        2. **Configure a API**: Edite `.env` com sua URL e chave de API
        
        3. **Processe**: Use a opção "Processar Rastreamentos"
        
        4. **Verifique**: Veja os resultados em "Visualizar Dados"
        """)

# ============================================================================
# PÁGINA: PROCESSAR RASTREAMENTOS
# ============================================================================
elif opcao == "⚙️ Processar Rastreamentos":
    st.subheader("⚙️ Processar Rastreamentos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        criar_backup = st.checkbox("💾 Criar backup antes", value=True)
    with col2:
        salvar_relatorio = st.checkbox("📊 Salvar relatório", value=True)
    with col3:
        limpar_logs = st.checkbox("🗑️ Limpar logs antigos", value=False)
    
    st.markdown("---")
    
    if st.button("🚀 Iniciar Processamento", use_container_width=True, type="primary"):
        with st.spinner("⏳ Processando rastreamentos..."):
            try:
                # Se o usuário inseriu códigos manualmente, gera um Excel temporário
                if st.session_state.get('codigos_manua'):
                    codigos = st.session_state.get('codigos_manua')
                    # montar DataFrame básico com apenas coluna de rastreamento
                    # usa o nome da coluna definido em config para permitir customização
                    df_temp = pd.DataFrame({
                        COLUNA_RASTREAMENTO: codigos
                    })
                    try:
                        df_temp.to_excel(EXCEL_FILE_PATH, index=False)
                        st.info(f"📝 Planilha gerada com {len(codigos)} códigos manuais.")
                    except Exception as e:
                        st.error(f"Falha ao salvar planilha manual: {e}")
                        raise

                orquestrador = OrquestradorRastreamento()
                sucesso = orquestrador.processar_rastreamentos(criar_backup=criar_backup)
                
                if sucesso:
                    st.markdown('<div class="success-box"><strong>✅ Processamento concluído com sucesso!</strong></div>', unsafe_allow_html=True)
                    
                    # Mostra estatísticas
                    atualizacoes = cast(Dict[str, Any], orquestrador.obter_atualizacoes())  # type: ignore
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Processado", atualizacoes['total_processados'])
                    with col2:
                        st.metric("Com Sucesso", atualizacoes['sucesso'])
                    with col3:
                        st.metric("Mudanças", atualizacoes['mudancas'])
                    with col4:
                        st.metric("Erros", atualizacoes['erros'])
                    
                    st.markdown("---")
                    
                    # Distribuição de status
                    st.subheader("📊 Distribuição de Status")
                    if atualizacoes['status_distribuicao']:
                        status_df = pd.DataFrame(
                            list(atualizacoes['status_distribuicao'].items()),
                            columns=['Status', 'Quantidade']
                        )
                        st.bar_chart(status_df.set_index('Status'))  # type: ignore
                    
                else:
                    st.markdown('<div class="error-box"><strong>❌ Erro durante processamento</strong></div>', unsafe_allow_html=True)
                    st.error("Verifique os logs para mais detalhes")
                    with st.expander("Visualizar últimos logs", expanded=False):
                        st.code(mostrar_ultimos_logs(20))
            
            except Exception as e:
                st.markdown(f'<div class="error-box"><strong>❌ Erro: {str(e)}</strong></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("💡 Dica: O processamento cria backup automático se ativado acima")

# ============================================================================
# PÁGINA: VISUALIZAR DADOS
# ============================================================================
elif opcao == "📊 Visualizar Dados":
    st.subheader("📊 Visualizar Planilha")

    # upload opcional: permite ao usuário fornecer diretamente um Excel
    uploaded = st.file_uploader("📁 Carregar planilha de rastreamento (XLSX)", type=["xlsx"])
    if uploaded is not None:
        try:
            with open(EXCEL_FILE_PATH, "wb") as f:
                f.write(uploaded.getbuffer())
            st.success("✅ Planilha carregada com sucesso!")
        except Exception as e:
            st.error(f"Falha ao salvar planilha: {e}")

    if not os.path.exists(EXCEL_FILE_PATH):
        st.warning("⚠️ Planilha não encontrada! Faça upload ou crie uma usando 'Processar Rastreamentos'")
        
        if st.button("Criar Planilha Modelo"):
            orquestrador = OrquestradorRastreamento()
            if orquestrador.criar_planilha_modelo():
                st.success("✅ Planilha modelo criada com sucesso!")
                st.rerun()
    else:
        try:
            # Ler planilha
            df = cast(pd.DataFrame, pd.read_excel(EXCEL_FILE_PATH))  # type: ignore
            
            # Filtros
            col1, col2 = st.columns(2)
            
            with col1:
                status_filter = st.multiselect(
                    "Filtrar por Status:",
                    df.iloc[:, 2].unique() if len(df.columns) > 2 else [],
                    default=None
                )
            
            with col2:
                # slider requires min < max; ajuste dinâmico conforme tamanho do df
                max_linhas = len(df)
                if max_linhas <= 1:
                    linhas_mostrar = 1
                else:
                    min_linhas = 1 if max_linhas < 5 else 5
                    default_linhas = min(20, max_linhas)
                    linhas_mostrar = st.slider("Linhas a mostrar:", min_linhas, max_linhas, default_linhas)
            
            # Filtrar dados
            df_filtrado = df.copy()
            if status_filter and len(df.columns) > 2:
                df_filtrado = df[df.iloc[:, 2].isin(status_filter)]
            
            # Mostrar dados (usa largura do container)
            st.dataframe(df_filtrado.head(linhas_mostrar), use_container_width=True)  # type: ignore
            
            # Estatísticas
            st.markdown("---")
            st.subheader("📈 Estatísticas")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total de Registros", len(df))
            
            with col2:
                st.metric("Registros Filtrados", len(df_filtrado))
            
            with col3:
                if len(df.columns) > 2:
                    status_series = df.iloc[:, 2]
                    mais_comum = status_series.mode()[0] if len(status_series.mode()) > 0 else "N/A"
                    st.metric("Status Mais Comum", mais_comum[:20])
            
            # Download
            st.markdown("---")
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Baixar como CSV",
                data=csv,
                file_name=f"rastreamento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        except Exception as e:
            st.error(f"Erro ao ler planilha: {str(e)}")

# ============================================================================
# PÁGINA: BACKUP E RESTAURAÇÃO
# ============================================================================
elif opcao == "💾 Backup e Restauração":
    st.subheader("💾 Gerenciar Backups")
    
    backups = cast(List[Dict[str, Any]], BackupManager.listar_backups())  # type: ignore
    
    if not backups:
        st.info("ℹ️ Nenhum backup encontrado. Crie um processando rastreamentos.")
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write(f"**{len(backups)} backup(s) disponível(is)**")
        
        with col2:
            if st.button("🔄 Atualizar Lista"):
                st.rerun()
        
        st.markdown("---")
        
        # Listar backups
        for idx, backup in enumerate(backups):
            with st.expander(f"📦 {backup['arquivo']} ({backup['tamanho']})"):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**Data:** {backup['data']}")
                    st.write(f"**Caminho:** `{backup['caminho']}`")
                
                with col2:
                    if st.button("📥 Restaurar", key=f"restore_{idx}"):
                        try:
                            orquestrador = OrquestradorRastreamento()
                            if orquestrador.restaurar_backup(backup['caminho']):
                                st.success("✅ Backup restaurado com sucesso!")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Erro: {str(e)}")
                
                with col3:
                    if st.button("🗑️ Deletar", key=f"delete_{idx}"):
                        try:
                            os.remove(backup['caminho'])
                            st.success("✅ Backup deletado!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro: {str(e)}")

# ============================================================================
# PÁGINA: RELATÓRIOS
# ============================================================================
elif opcao == "📈 Relatórios":
    st.subheader("📈 Relatórios")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 Logs de Processamento")
        
        log_folder = "logs"
        if os.path.exists(log_folder):
            logs = sorted([f for f in os.listdir(log_folder) if f.endswith('.log')], reverse=True)
            
            if logs:
                log_selecionado = st.selectbox("Selecione um log:", logs)
                
                with open(os.path.join(log_folder, log_selecionado), 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                
                st.text_area("Conteúdo do Log:", conteudo, height=300, disabled=True)
                
                st.download_button(
                    label="📥 Baixar Log",
                    data=conteudo,
                    file_name=log_selecionado,
                    mime="text/plain"
                )
            else:
                st.info("Nenhum log encontrado ainda.")
        else:
            st.warning("Pasta de logs não existe.")
    
    with col2:
        st.subheader("📈 Estatísticas Gerais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            backups = cast(List[Dict[str, Any]], BackupManager.listar_backups())  # type: ignore
            st.metric("Total de Backups", len(backups))
        
        with col2:
            log_folder = "logs"
            num_logs = len([f for f in os.listdir(log_folder) if f.endswith('.log')]) if os.path.exists(log_folder) else 0
            st.metric("Total de Logs", num_logs)

# ============================================================================
# PÁGINA: SOBRE
# ============================================================================
elif opcao == "ℹ️ Sobre":
    st.subheader("ℹ️ Sobre o Sistema")
    
    st.write("""
    ## 🚚 Sistema de Rastreamento de Transportadora
    
    **Versão:** 1.0.0  
    **Data:** 4 de março de 2026  
    **Status:** ✅ Ativo
    
    ---
    
    ### 📋 O Que é?
    
    Um sistema completo de automação para rastreamento de pacotes de transportadoras,
    que integra com APIs de transporte e atualiza automaticamente planilhas Excel.
    
    ### ✨ Características
    
    - ✅ Consumo de API de rastreamento
    - ✅ Atualização automática de Excel
    - ✅ Backup automático de dados
    - ✅ Logging completo de operações
    - ✅ Rate limiting para proteção
    - ✅ Tratamento robusto de erros
    - ✅ Relatórios detalhados
    - ✅ Interface web com Streamlit
    
    ### 🔧 Tecnologias
    
    - **Python** 3.8+
    - **Streamlit** - Interface web
    - **Pandas** - Processamento de dados
    - **Openpyxl** - Manipulação Excel
    - **Requests** - Consumo de APIs
    
    ### 📚 Documentação
    
    - [`README.md`](./README.md) - Documentação completa
    - [`GUIA_RAPIDO.md`](./GUIA_RAPIDO.md) - Começar em 5 minutos
    - [`GUIA_INTEGRACAO.md`](./GUIA_INTEGRACAO.md) - Integração com API
    
    ### 🚀 Começar
    
    ```bash
    streamlit run app.py
    ```
    
    Depois acesse: http://localhost:8501
    
    ### 📞 Suporte
    
    Verifique os logs em `logs/` para mais informações sobre erros.
    """)
    
    st.markdown("---")
    
    st.info("""
    💡 **Dica:** Use o menu lateral para navegar entre as funcionalidades.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.9em; margin-top: 50px;">
    <p>🚚 Sistema de Rastreamento de Transportadora | 
    <a href="https://github.com" target="_blank">GitHub</a> | 
    Desenvolvido com ❤️ e Streamlit</p>
</div>
""", unsafe_allow_html=True)
