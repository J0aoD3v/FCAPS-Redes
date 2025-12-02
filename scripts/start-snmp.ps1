# Script para Iniciar SNMP nos Containers
# Execute este script apos subir os containers com docker compose up -d

Write-Host ""
Write-Host "=== Iniciando SNMP em todos os containers ===" -ForegroundColor Cyan
Write-Host ""

# nginx-web
Write-Host "Configurando SNMP em nginx-web..." -ForegroundColor Yellow
docker exec nginx-web sh -c "mkdir -p /etc/snmp /var/net-snmp && echo 'rocommunity public' > /etc/snmp/snmpd.conf && echo 'agentaddress udp:161' >> /etc/snmp/snmpd.conf && echo 'syslocation nginx-web-container' >> /etc/snmp/snmpd.conf && echo 'syscontact admin@fcaps.local' >> /etc/snmp/snmpd.conf && snmpd -Lsd -Lf /dev/null -p /var/run/snmpd.pid"
if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK - SNMP iniciado em nginx-web" -ForegroundColor Green
}

# python-app
Write-Host "Configurando SNMP em python-app..." -ForegroundColor Yellow
docker exec python-app sh -c "mkdir -p /etc/snmp /var/net-snmp && echo 'rocommunity public' > /etc/snmp/snmpd.conf && echo 'agentaddress udp:161' >> /etc/snmp/snmpd.conf && echo 'syslocation python-app-container' >> /etc/snmp/snmpd.conf && echo 'syscontact admin@fcaps.local' >> /etc/snmp/snmpd.conf && snmpd -Lsd -Lf /dev/null -p /var/run/snmpd.pid"
if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK - SNMP iniciado em python-app" -ForegroundColor Green
}

# alpine-host
Write-Host "Configurando SNMP em alpine-host..." -ForegroundColor Yellow
docker exec alpine-host sh -c "mkdir -p /etc/snmp /var/net-snmp && echo 'rocommunity public' > /etc/snmp/snmpd.conf && echo 'agentaddress udp:161' >> /etc/snmp/snmpd.conf && echo 'syslocation alpine-host-container' >> /etc/snmp/snmpd.conf && echo 'syscontact admin@fcaps.local' >> /etc/snmp/snmpd.conf && snmpd -Lsd -Lf /dev/null -p /var/run/snmpd.pid"
if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK - SNMP iniciado em alpine-host" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Testando SNMP ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "Testando nginx-web..." -ForegroundColor Yellow
docker exec nginx-web snmpget -v2c -c public localhost sysDescr.0

Write-Host ""
Write-Host "Testando python-app..." -ForegroundColor Yellow
docker exec python-app snmpget -v2c -c public localhost sysDescr.0

Write-Host ""
Write-Host "Testando alpine-host..." -ForegroundColor Yellow
docker exec alpine-host snmpget -v2c -c public localhost sysDescr.0

Write-Host "`n=== Resumo das Portas SNMP ===`n" -ForegroundColor Cyan
Write-Host "nginx-web:    localhost:16101 (community: public)" -ForegroundColor White
Write-Host "python-app:   localhost:16102 (community: public)" -ForegroundColor White
Write-Host "alpine-host:  localhost:16103 (community: public)" -ForegroundColor White

Write-Host "`n=== Como Testar ===`n" -ForegroundColor Cyan
Write-Host "Dentro do container:" -ForegroundColor Yellow
Write-Host '  docker exec nginx-web snmpwalk -v2c -c public localhost system' -ForegroundColor Gray
Write-Host "`nCom MIB Browser (GUI):" -ForegroundColor Yellow
Write-Host "  Host: localhost" -ForegroundColor Gray
Write-Host "  Port: 16101 (nginx) ou 16102 (python) ou 16103 (alpine)" -ForegroundColor Gray
Write-Host "  Community: public" -ForegroundColor Gray
Write-Host "  Version: SNMPv2c" -ForegroundColor Gray

Write-Host "`nSNMP configurado com sucesso!`n" -ForegroundColor Green
