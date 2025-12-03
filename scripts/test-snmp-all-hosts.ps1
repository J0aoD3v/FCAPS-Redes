# Script de teste SNMP para todos os hosts monitorados
# Execute: .\scripts\test-snmp-all-hosts.ps1

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Teste SNMP - Todos os Hosts Monitorados" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

$monitoredHosts = @(
    @{Name="python-app"; Port="16102"},
    @{Name="nginx-web"; Port="16101"},
    @{Name="alpine-host"; Port="16103"},
    @{Name="snmp-collector"; Port="16104"}
)

$allPassed = $true

foreach ($monHost in $monitoredHosts) {
    $hostName = $monHost.Name
    $hostPort = $monHost.Port
    
    Write-Host "-------------------------------------------" -ForegroundColor Yellow
    Write-Host "Testando: $hostName" -ForegroundColor Yellow
    Write-Host "-------------------------------------------" -ForegroundColor Yellow
    
    # 1. Verificar container rodando
    Write-Host "[1/5] Container status..." -NoNewline
    $status = docker ps --filter "name=$hostName" --format "{{.Status}}"
    if ($status -match "Up") {
        Write-Host " [OK]" -ForegroundColor Green
    } else {
        Write-Host " [ERRO]" -ForegroundColor Red
        $allPassed = $false
        continue
    }
    
    # 2. Verificar daemon SNMP
    Write-Host "[2/5] Daemon SNMP..." -NoNewline
    $snmpd = docker exec $hostName ps aux | Select-String "snmpd"
    if ($snmpd) {
        Write-Host " [OK]" -ForegroundColor Green
    } else {
        Write-Host " [ERRO]" -ForegroundColor Red
        $allPassed = $false
    }
    
    # 3. Verificar porta 161
    Write-Host "[3/5] Porta 161/udp..." -NoNewline
    $port = docker exec $hostName netstat -uln | Select-String "0.0.0.0:161"
    if ($port) {
        Write-Host " [OK]" -ForegroundColor Green
    } else {
        Write-Host " [ERRO]" -ForegroundColor Red
        $allPassed = $false
    }
    
    # 4. Teste local SNMP
    Write-Host "[4/5] Teste local..." -NoNewline
    $localTest = docker exec $hostName snmpget -v2c -c public localhost SNMPv2-MIB::sysName.0 2>&1
    if ($LASTEXITCODE -eq 0 -and $localTest -match $hostName) {
        Write-Host " [OK]" -ForegroundColor Green
        Write-Host "  $localTest" -ForegroundColor Gray
    } else {
        Write-Host " [ERRO]" -ForegroundColor Red
        $allPassed = $false
    }
    
    # 5. Teste via rede Docker
    Write-Host "[5/5] Teste via rede..." -NoNewline
    $networkTest = docker exec zabbix-server snmpget -v2c -c public ${hostName}:161 SNMPv2-MIB::sysName.0 2>&1
    if ($LASTEXITCODE -eq 0 -and $networkTest -match $hostName) {
        Write-Host " [OK]" -ForegroundColor Green
    } else {
        Write-Host " [ERRO]" -ForegroundColor Red
        $allPassed = $false
    }
    
    Write-Host ""
}

# Sumario final
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "RESUMO DOS TESTES" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

if ($allPassed) {
    Write-Host "[SUCESSO] Todos os hosts estao configurados corretamente!" -ForegroundColor Green
} else {
    Write-Host "[ATENCAO] Alguns hosts apresentaram problemas" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Hosts monitorados:" -ForegroundColor White
foreach ($monHost in $monitoredHosts) {
    Write-Host "  - $($monHost.Name) -> localhost:$($monHost.Port)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Comunidade SNMP: public" -ForegroundColor Gray
Write-Host "Versao: SNMPv2c" -ForegroundColor Gray
Write-Host ""
Write-Host "Para testes individuais:" -ForegroundColor Yellow
Write-Host "  .\scripts\test-snmp-python-app.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "Documentacao: docs\SNMP-PYTHON-APP.md" -ForegroundColor Cyan
