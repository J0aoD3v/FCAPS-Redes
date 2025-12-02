# Script de configuracao do WSL para o projeto FCAPS
# Executar no PowerShell como Administrador

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Configuracao WSL - Projeto FCAPS     " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/5] Verificando instalacao do WSL..." -ForegroundColor Yellow
$wslVersion = wsl --version 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "WSL nao encontrado. Instalando..." -ForegroundColor Red
    Write-Host "Execute: wsl --install" -ForegroundColor Green
    exit
}

Write-Host "OK - WSL instalado!" -ForegroundColor Green
Write-Host ""

Write-Host "[2/5] Configurando limites de memoria do WSL..." -ForegroundColor Yellow

$wslConfigPath = "$env:USERPROFILE\.wslconfig"
$wslConfigContent = @"
[wsl2]
memory=4GB
processors=2
swap=2GB
localhostForwarding=true
guiApplications=false

[experimental]
autoMemoryReclaim=gradual
"@

Write-Host "Criando arquivo: $wslConfigPath" -ForegroundColor Gray
$wslConfigContent | Out-File -FilePath $wslConfigPath -Encoding UTF8 -Force

Write-Host "OK - Arquivo criado!" -ForegroundColor Green
Write-Host ""

Write-Host "[3/5] Verificando distribuicoes instaladas..." -ForegroundColor Yellow
wsl --list --verbose
Write-Host ""

Write-Host "[4/5] Reiniciando WSL..." -ForegroundColor Yellow
wsl --shutdown
Start-Sleep -Seconds 3
Write-Host "OK - WSL reiniciado!" -ForegroundColor Green
Write-Host ""

Write-Host "[5/5] Proximos passos:" -ForegroundColor Yellow
Write-Host "1. Abra o WSL: wsl"
Write-Host "2. Execute: cd /mnt/c/Projetos/FCAPS-Redes"
Write-Host "3. Execute: bash scripts/install-docker.sh"
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Configuracao concluida!              " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
