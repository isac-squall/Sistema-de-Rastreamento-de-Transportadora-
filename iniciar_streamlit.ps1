#!/usr/bin/env powershell
# Script para executar Streamlit em Windows (PowerShell)
# Execute: .\iniciar_streamlit.ps1

# Define cores
$ForegroundColorCyan = "Cyan"
$ForegroundColorGreen = "Green"
$ForegroundColorYellow = "Yellow"

# Limpa console
Clear-Host

# Mostra mensagem inicial
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor $ForegroundColorCyan
Write-Host "║      INICIANDO SISTEMA DE RASTREAMENTO DE TRANSPORTADORA   ║" -ForegroundColor $ForegroundColorGreen
Write-Host "║                     COM STREAMLIT                          ║" -ForegroundColor $ForegroundColorCyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor $ForegroundColorCyan
Write-Host ""

# Navega até o diretório do projeto
$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectDir

Write-Host "📁 Diretório do projeto: $projectDir" -ForegroundColor $ForegroundColorYellow
Write-Host "🐍 Ativando ambiente virtual..." -ForegroundColor $ForegroundColorYellow

# Ativa o ambiente virtual
& .\venv\Scripts\Activate.ps1

Write-Host "✅ Ambiente virtual ativado!" -ForegroundColor $ForegroundColorGreen
Write-Host ""
Write-Host "🚀 Iniciando Streamlit..." -ForegroundColor $ForegroundColorYellow
Write-Host "🌐 Acesse: http://localhost:8501" -ForegroundColor $ForegroundColorGreen
Write-Host "⏳ Abrindo navegador em 3 segundos..." -ForegroundColor $ForegroundColorYellow
Write-Host ""

# Aguarda 3 segundos
Start-Sleep -Seconds 3

# Tenta abrir o navegador
try {
    Start-Process "http://localhost:8501"
    Write-Host "✅ Navegador aberto!" -ForegroundColor $ForegroundColorGreen
} catch {
    Write-Host "⚠️ Não foi possível abrir o navegador automaticamente" -ForegroundColor $ForegroundColorYellow
    Write-Host "Abra manualmente: http://localhost:8501" -ForegroundColor $ForegroundColorYellow
}

Write-Host ""
Write-Host "Pressione CTRL+C para parar o servidor" -ForegroundColor $ForegroundColorYellow
Write-Host ""

# Inicia Streamlit
python -m streamlit run app.py --logger.level=info
