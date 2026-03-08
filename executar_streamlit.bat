@echo off
chcp 65001 > nul
cls

cd /d "%~dp0"

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║      INICIANDO SISTEMA DE RASTREAMENTO DE TRANSPORTADORA   ║
echo ║                     COM STREAMLIT                          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo 📁 Diretório: %cd%
echo 🐍 Ativando ambiente virtual...
call .\venv\Scripts\activate.bat

if errorlevel 1 (
    echo ❌ Erro ao ativar o ambiente virtual!
    echo Certifique-se que o venv foi criado corretamente.
    pause
    exit /b 1
)

echo ✅ Ambiente virtual ativado!
echo.
echo 🚀 Iniciando Streamlit...
echo 🌐 Acesse: http://localhost:8501
echo ⏳ Abrindo navegador em 3 segundos...
echo.

timeout /t 3 /nobreak

REM Tenta abrir o navegador
start http://localhost:8501

echo ✅ Navegador aberto!
echo.
echo Pressione CTRL+C para parar o servidor
echo.

python -m streamlit run app.py --logger.level=info
