#!/bin/sh
# Entrypoint script para python-app com SNMP e Zabbix Agent
# FCAPS - Gerenciamento de Redes

set -e

echo "==================================="
echo "Iniciando Python App com SNMP"
echo "==================================="

# Configurar Zabbix Agent2
echo "[1/4] Configurando Zabbix Agent2..."
if [ -f /etc/zabbix/zabbix_agent2.conf ]; then
    sed -i 's/Server=127.0.0.1/Server=zabbix-server/g' /etc/zabbix/zabbix_agent2.conf
    sed -i 's/ServerActive=127.0.0.1/ServerActive=zabbix-server/g' /etc/zabbix/zabbix_agent2.conf
    sed -i 's/Hostname=Zabbix server/Hostname=python-app/g' /etc/zabbix/zabbix_agent2.conf
    /usr/sbin/zabbix_agent2 -c /etc/zabbix/zabbix_agent2.conf &
    echo "✓ Zabbix Agent2 iniciado"
else
    echo "⚠ Zabbix Agent2 não encontrado"
fi

# Verificar configuração SNMP
echo "[2/4] Verificando configuração SNMP..."
if [ -f /etc/snmp/snmpd.conf ]; then
    echo "✓ Arquivo de configuração SNMP encontrado"
else
    echo "✗ Arquivo de configuração SNMP não encontrado"
    exit 1
fi

# Iniciar SNMP daemon
echo "[3/4] Iniciando SNMP daemon..."
/usr/sbin/snmpd -Lsd -Lf /dev/null -p /var/run/snmpd.pid
sleep 2

# Testar SNMP localmente
echo "[4/4] Testando SNMP..."
if snmpget -v2c -c public localhost SNMPv2-MIB::sysName.0 > /dev/null 2>&1; then
    echo "✓ SNMP respondendo corretamente"
    snmpget -v2c -c public localhost SNMPv2-MIB::sysName.0
else
    echo "⚠ SNMP não respondeu ao teste local"
fi

echo "==================================="
echo "Iniciando aplicação Python..."
echo "==================================="

# Iniciar aplicação Python
exec python app.py
