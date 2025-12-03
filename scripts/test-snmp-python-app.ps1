# Script de teste SNMP para python-app
# Execute: .\scripts\test-snmp-python-app.ps1

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Teste de Configuracao SNMP - python-app" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se o container esta rodando
Write-Host "[1/6] Verificando status do container..." -ForegroundColor Yellow
$containerStatus = docker ps --filter "name=python-app" --format "{{.Status}}"
if ($containerStatus -match "Up") {
    Write-Host "[OK] Container python-app esta rodando" -ForegroundColor Green
    Write-Host "  Status: $containerStatus" -ForegroundColor Gray
} else {
    Write-Host "[ERRO] Container python-app nao esta rodando" -ForegroundColor Red
    Write-Host "  Execute: docker-compose up -d python-app" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Verificar se o daemon SNMP esta rodando
Write-Host "[2/6] Verificando daemon SNMP..." -ForegroundColor Yellow
$snmpdProcess = docker exec python-app ps aux | Select-String "snmpd"
if ($snmpdProcess) {
    Write-Host "[OK] Daemon SNMP esta rodando" -ForegroundColor Green
    Write-Host "  $snmpdProcess" -ForegroundColor Gray
} else {
    Write-Host "[ERRO] Daemon SNMP nao encontrado" -ForegroundColor Red
}
Write-Host ""

# Verificar porta SNMP
Write-Host "[3/6] Verificando porta SNMP (161/udp)..." -ForegroundColor Yellow
$snmpPort = docker exec python-app netstat -uln | Select-String "161"
if ($snmpPort) {
    Write-Host "[OK] Porta 161/udp esta aberta" -ForegroundColor Green
    Write-Host "  $snmpPort" -ForegroundColor Gray
} else {
    Write-Host "[ERRO] Porta 161/udp nao encontrada" -ForegroundColor Red
}
Write-Host ""

# Teste local de SNMP (dentro do container)
Write-Host "[4/6] Testando SNMP localmente (dentro do container)..." -ForegroundColor Yellow
$localTest = docker exec python-app snmpget -v2c -c public localhost SNMPv2-MIB::sysName.0 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] SNMP respondeu ao teste local" -ForegroundColor Green
    Write-Host "  $localTest" -ForegroundColor Gray
} else {
    Write-Host "[ERRO] SNMP nao respondeu" -ForegroundColor Red
    Write-Host "  $localTest" -ForegroundColor Gray
}
Write-Host ""

# Teste de rede Docker (do zabbix-server)
Write-Host "[5/6] Testando SNMP via rede Docker (zabbix-server -> python-app)..." -ForegroundColor Yellow
$networkTest = docker exec zabbix-server snmpget -v2c -c public python-app:161 SNMPv2-MIB::sysName.0 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] SNMP respondeu via rede Docker" -ForegroundColor Green
    Write-Host "  $networkTest" -ForegroundColor Gray
} else {
    Write-Host "[ERRO] SNMP nao respondeu via rede Docker" -ForegroundColor Red
    Write-Host "  $networkTest" -ForegroundColor Gray
}
Write-Host ""

# Listar OIDs disponiveis
Write-Host "[6/6] Listando algumas OIDs disponiveis..." -ForegroundColor Yellow
Write-Host ""
Write-Host "System Information:" -ForegroundColor Cyan
$oids = @(
    @{Name="Sistema"; OID="SNMPv2-MIB::sysDescr.0"},
    @{Name="Nome"; OID="SNMPv2-MIB::sysName.0"},
    @{Name="Localizacao"; OID="SNMPv2-MIB::sysLocation.0"},
    @{Name="Contato"; OID="SNMPv2-MIB::sysContact.0"},
    @{Name="Uptime"; OID="SNMPv2-MIB::sysUpTime.0"}
)

foreach ($item in $oids) {
    $result = docker exec python-app snmpget -v2c -c public localhost $item.OID 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  $($item.Name): " -NoNewline -ForegroundColor Yellow
        Write-Host "$result" -ForegroundColor Gray
    } else {
        Write-Host "  $($item.Name): Nao disponivel" -ForegroundColor Red
    }
}
Write-Host ""

# Sumario
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Testes concluidos!" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Porta SNMP no host: " -NoNewline
Write-Host "localhost:16102" -ForegroundColor Green
Write-Host "Comunidade SNMP: " -NoNewline
Write-Host "public" -ForegroundColor Green
Write-Host "Versao: " -NoNewline
Write-Host "SNMPv2c" -ForegroundColor Green
Write-Host ""
Write-Host "Para mais testes:" -ForegroundColor Yellow
Write-Host "  docker exec python-app snmpwalk -v2c -c public localhost" -ForegroundColor Gray
Write-Host "  docker exec zabbix-server snmpwalk -v2c -c public python-app:161 system" -ForegroundColor Gray
Write-Host ""
Write-Host "Documentacao completa em: docs\SNMP-PYTHON-APP.md" -ForegroundColor Cyan
