#!/bin/sh
set -e

echo "================================"
echo "  FCAPS SNMP Collector Service"
echo "================================"

# Criar diretórios necessários
mkdir -p /data /etc/snmp /var/net-snmp

# Configurar SNMP daemon para auto-monitoramento
echo "Configuring SNMP daemon..."
cat > /etc/snmp/snmpd.conf << 'EOF'
rocommunity public
syslocation "SNMP Collector Container"
syscontact "fcaps-monitoring@localhost"
sysservices 72
master agentx
agentaddress udp:161
EOF

# Iniciar SNMP daemon
echo "Starting SNMP daemon..."
/usr/sbin/snmpd -Lsd -Lf /dev/null -p /var/run/snmpd.pid

# Criar diretório de dados
mkdir -p /data

echo "Starting SNMP Collector..."

# Inicializar banco de dados (primeira execução)
echo "Initializing database..."
python3 /app/collector.py

# Iniciar coletor em modo daemon (background)
echo "Starting SNMP collector daemon..."
python3 /app/collector.py --daemon &

# Iniciar API REST (foreground)
echo "Starting API server..."
python3 /app/api.py
