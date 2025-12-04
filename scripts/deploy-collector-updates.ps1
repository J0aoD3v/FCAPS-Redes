#!/usr/bin/env pwsh

# Script para fazer deploy das atualizações do SNMP Collector na Oracle Cloud
# Envia apenas os arquivos modificados

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Deploy Atualizacoes SNMP Collector     " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$SSH_CONFIG = "$env:USERPROFILE\.ssh\config"
$SSH_HOST = "oracle-cloud"
$REMOTE_DIR = "/home/opc/fcaps-snmp-collector"
$LOCAL_COLLECTOR_DIR = "docker\snmp-collector"

# Verificar se SSH config existe
if (-not (Test-Path $SSH_CONFIG)) {
    Write-Host "ERRO: Arquivo SSH config nao encontrado: $SSH_CONFIG" -ForegroundColor Red
    exit 1
}

# Verificar se diretório local existe
if (-not (Test-Path $LOCAL_COLLECTOR_DIR)) {
    Write-Host "ERRO: Diretorio local nao encontrado: $LOCAL_COLLECTOR_DIR" -ForegroundColor Red
    exit 1
}

Write-Host "[1/4] Parando container snmp-collector..." -ForegroundColor Yellow
ssh -F $SSH_CONFIG $SSH_HOST "docker stop snmp-collector 2>/dev/null; docker rm snmp-collector 2>/dev/null; echo 'Container parado e removido'"
Write-Host "Container parado" -ForegroundColor Green
Write-Host ""

Write-Host "[2/4] Enviando arquivos atualizados..." -ForegroundColor Yellow
# Enviar apenas os arquivos modificados
scp -F $SSH_CONFIG "$LOCAL_COLLECTOR_DIR\collector-cloud.py" "${SSH_HOST}:${REMOTE_DIR}/"
scp -F $SSH_CONFIG "$LOCAL_COLLECTOR_DIR\entrypoint.sh" "${SSH_HOST}:${REMOTE_DIR}/"
Write-Host "Arquivos atualizados enviados" -ForegroundColor Green
Write-Host ""

Write-Host "[3/4] Reconstruindo container..." -ForegroundColor Yellow
$buildCmd = "cd $REMOTE_DIR ; docker build -t snmp-collector:latest ."
ssh -F $SSH_CONFIG $SSH_HOST $buildCmd
Write-Host "Container reconstruido" -ForegroundColor Green
Write-Host ""

Write-Host "[4/4] Iniciando container..." -ForegroundColor Yellow
$runCmd = "docker run -d --name snmp-collector --restart unless-stopped -p 8090:8090 -v $REMOTE_DIR/data:/data snmp-collector:latest"
ssh -F $SSH_CONFIG $SSH_HOST $runCmd
Write-Host "Container iniciado" -ForegroundColor Green
Write-Host ""

Write-Host "Verificando status..." -ForegroundColor Yellow
Start-Sleep -Seconds 5
ssh -F $SSH_CONFIG $SSH_HOST "docker ps | grep snmp-collector"
Write-Host ""
Write-Host "Ultimos logs do container:" -ForegroundColor Yellow
ssh -F $SSH_CONFIG $SSH_HOST "docker logs --tail 20 snmp-collector"
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "  Deploy concluido com sucesso!          " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Teste a API em: http://137.131.133.165:8090/api/latest" -ForegroundColor Cyan
Write-Host "Dashboard em: http://137.131.133.165:8090/" -ForegroundColor Cyan