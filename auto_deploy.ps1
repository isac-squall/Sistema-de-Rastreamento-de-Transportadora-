# PowerShell helper to update git and optionally start the local Streamlit app
# Usage examples:
#   .\auto_deploy.ps1 -CommitMessage "Minhas alterações"          # faz git add/commit/pull/push
#   .\auto_deploy.ps1 -RunLocalStreamlit                         # atualiza git e inicia o servidor local
#   .\auto_deploy.ps1 -CommitMessage "foo" -RunLocalStreamlit   # ambas ações

param(
    [string]$CommitMessage = "Atualização automática",
    [switch]$RunLocalStreamlit
)

# garanta que estamos na raiz do repositório
Set-Location -Path $PSScriptRoot

Write-Host "[auto_deploy] iniciando operação..." -ForegroundColor Cyan

# Git workflow
Write-Host "[auto_deploy] git add/commit/pull/push" -ForegroundColor Green
git add .
try {
    git commit -m $CommitMessage -q
} catch {
    Write-Host "[auto_deploy] Nada para commitar ou mensagem vazia" -ForegroundColor Yellow
}

# atualiza a branch principal (ajuste se for outra)
git pull --rebase origin main
git push origin main

if ($RunLocalStreamlit) {
    Write-Host "[auto_deploy] iniciando Streamlit localmente" -ForegroundColor Green
    & .\executar_streamlit.bat
}

Write-Host "[auto_deploy] operação concluída." -ForegroundColor Cyan
