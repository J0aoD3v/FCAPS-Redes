# Script para executar coleta de métricas SNMP no Zabbix Server
# FCAPS - Projeto de Redes

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  FCAPS - Coletor SNMP via Zabbix Server" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se o container está rodando
$containerRunning = docker ps --filter "name=zabbix-server" --format "{{.Names}}" 2>$null

if (-not $containerRunning) {
    Write-Host "❌ ERRO: Container zabbix-server não está rodando!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Execute primeiro: docker-compose -f docker/docker-compose.yml up -d" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Container zabbix-server detectado" -ForegroundColor Green
Write-Host ""

# Copiar script para o container
Write-Host "📋 Copiando script de coleta para o container..." -ForegroundColor Yellow
$copyResult = docker cp scripts/snmp-collector.sh zabbix-server:/tmp/snmp-collector.sh 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erro ao copiar script: $copyResult" -ForegroundColor Red
    exit 1
}

# Dar permissão de execução
$chmodResult = docker exec zabbix-server chmod +x /tmp/snmp-collector.sh 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erro ao dar permissão: $chmodResult" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Script copiado com sucesso" -ForegroundColor Green
Write-Host ""
Write-Host "🔍 Iniciando coleta de métricas SNMP..." -ForegroundColor Cyan
Write-Host ""

# Executar o script
docker exec zabbix-server /tmp/snmp-collector.sh

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Coleta finalizada!" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Dica: Para executar novamente, use:" -ForegroundColor Yellow
Write-Host "   .\scripts\collect-snmp-metrics.ps1" -ForegroundColor White
Write-Host ""
