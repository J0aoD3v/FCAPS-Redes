# Script para fazer deploy do SNMP Collector na Oracle Cloud
# Substitui o container antigo pelos arquivos atualizados do desktop local

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Deploy SNMP Collector - Oracle Cloud  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$SSH_CONFIG = "$env:USERPROFILE\.ssh\config"
$SSH_HOST = "oracle-cloud"
$REMOTE_DIR = "/home/opc/fcaps-snmp-collector"
$LOCAL_COLLECTOR_DIR = "docker\snmp-collector"
$LOCAL_INDEX = "index.html"

# Verificar se SSH config existe
if (-not (Test-Path $SSH_CONFIG)) {
    Write-Host "ERRO: Arquivo SSH config nao encontrado: $SSH_CONFIG" -ForegroundColor Red
    exit 1
}

# Verificar se diretórios locais existem
if (-not (Test-Path $LOCAL_COLLECTOR_DIR)) {
    Write-Host "ERRO: Diretorio local nao encontrado: $LOCAL_COLLECTOR_DIR" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $LOCAL_INDEX)) {
    Write-Host "ERRO: index.html nao encontrado: $LOCAL_INDEX" -ForegroundColor Red
    exit 1
}

Write-Host "[1/7] Parando e removendo container antigo..." -ForegroundColor Yellow
ssh -F $SSH_CONFIG $SSH_HOST "docker stop snmp-collector 2>/dev/null; docker rm snmp-collector 2>/dev/null; echo 'Container removido'"
Write-Host "Container antigo removido" -ForegroundColor Green
Write-Host ""

Write-Host "[2/7] Criando diretorio remoto..." -ForegroundColor Yellow
ssh -F $SSH_CONFIG $SSH_HOST "mkdir -p $REMOTE_DIR/data"
Write-Host "Diretorio criado" -ForegroundColor Green
Write-Host ""

Write-Host "[3/7] Enviando arquivos do collector..." -ForegroundColor Yellow
# Enviar arquivos individualmente
ssh -F $SSH_CONFIG $SSH_HOST "mkdir -p $REMOTE_DIR"
scp -F $SSH_CONFIG "$LOCAL_COLLECTOR_DIR\Dockerfile" "${SSH_HOST}:${REMOTE_DIR}/"
scp -F $SSH_CONFIG "$LOCAL_COLLECTOR_DIR\entrypoint.sh" "${SSH_HOST}:${REMOTE_DIR}/"
scp -F $SSH_CONFIG "$LOCAL_COLLECTOR_DIR\api.py" "${SSH_HOST}:${REMOTE_DIR}/"
scp -F $SSH_CONFIG "$LOCAL_COLLECTOR_DIR\collector.py" "${SSH_HOST}:${REMOTE_DIR}/"
scp -F $SSH_CONFIG "$LOCAL_COLLECTOR_DIR\collector-cloud.py" "${SSH_HOST}:${REMOTE_DIR}/"
scp -F $SSH_CONFIG "$LOCAL_COLLECTOR_DIR\requirements.txt" "${SSH_HOST}:${REMOTE_DIR}/"
Write-Host "Arquivos do collector enviados" -ForegroundColor Green
Write-Host ""

Write-Host "[4/7] Enviando index.html..." -ForegroundColor Yellow
ssh -F $SSH_CONFIG $SSH_HOST "mkdir -p $REMOTE_DIR/data"
scp -F $SSH_CONFIG $LOCAL_INDEX "${SSH_HOST}:${REMOTE_DIR}/data/index.html"
Write-Host "index.html enviado" -ForegroundColor Green
Write-Host ""

Write-Host "[5/7] Configurando permissoes..." -ForegroundColor Yellow
ssh -F $SSH_CONFIG $SSH_HOST "chmod +x $REMOTE_DIR/entrypoint.sh"
Write-Host "Permissoes configuradas" -ForegroundColor Green
Write-Host ""

Write-Host "[6/7] Reconstruindo container..." -ForegroundColor Yellow
$buildCmd = "cd $REMOTE_DIR ; docker build -t snmp-collector:latest ."
ssh -F $SSH_CONFIG $SSH_HOST $buildCmd
Write-Host "Container reconstruido" -ForegroundColor Green
Write-Host ""

Write-Host "[7/7] Iniciando container..." -ForegroundColor Yellow
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
Write-Host "  Deploy concluido com sucesso!        " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Teste a API em: http://137.131.133.165:8090/api/latest" -ForegroundColor Cyan
Write-Host "Dashboard em: http://137.131.133.165:8090/" -ForegroundColor Cyan
