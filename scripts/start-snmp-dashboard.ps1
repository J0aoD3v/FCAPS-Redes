# Script para iniciar o coletor SNMP e dashboard
# FCAPS - Projeto de Redes

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  FCAPS - Iniciando Coletor SNMP + Dashboard" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Subir container do coletor SNMP
Write-Host "📊 Iniciando snmp-collector..." -ForegroundColor Yellow
docker-compose -f docker/docker-compose.yml up -d snmp-collector

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erro ao iniciar snmp-collector" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Coletor SNMP iniciado" -ForegroundColor Green
Write-Host ""

# Aguardar alguns segundos para coletar dados
Write-Host "⏳ Aguardando primeira coleta de dados (30s)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Verificar se há dados
Write-Host "🔍 Verificando dados coletados..." -ForegroundColor Yellow
$response = try { Invoke-RestMethod -Uri "http://localhost:8090/api/latest" -TimeoutSec 5 } catch { $null }

if ($response -and $response.hosts) {
    Write-Host "✅ Dados SNMP disponíveis: $($response.hosts.Count) hosts" -ForegroundColor Green
    $response.hosts | ForEach-Object {
        Write-Host "   - $($_.host): CPU=$($_.cpu)% MEM=$($_.memory)%" -ForegroundColor White
    }
} else {
    Write-Host "⚠️  Nenhum dado coletado ainda, aguarde mais alguns segundos..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Serviços Disponíveis" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Dashboard:    " -NoNewline; Write-Host "http://localhost:8081 (nginx)" -ForegroundColor Green
Write-Host "🔌 API SNMP:     " -NoNewline; Write-Host "http://localhost:8090/api/latest" -ForegroundColor Green
Write-Host "⚡ Zabbix:       " -NoNewline; Write-Host "http://localhost:8080 (Admin/zabbix)" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Comandos úteis:" -ForegroundColor Yellow
Write-Host "   docker logs snmp-collector -f     # Ver logs do coletor"
Write-Host "   docker exec snmp-collector ls -lh /data  # Ver banco de dados"
Write-Host ""
