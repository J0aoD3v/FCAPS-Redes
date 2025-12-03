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
# Informações do sistema
sysLocation    SNMP Collector Service - FCAPS Network
sysContact     admin@fcaps.local
sysName        snmp-collector
sysServices    72

# Comunidade de leitura
rocommunity    public  default
rocommunity6   public  default

# Endereço de escuta
agentaddress   udp:161
agentaddress   udp6:[::1]:161

# Master agentx
master agentx

# Persistência de dados
persistentDir /var/net-snmp

# Métricas de carga
load 5 5 5

# Extensões customizadas para SNMP Collector
extend collector-status /bin/sh -c "ps aux | grep -c '[p]ython3 /app/collector.py'"
extend api-status /bin/sh -c "ps aux | grep -c '[p]ython3 /app/api.py'"
extend collected-metrics /bin/sh -c "ls /data/*.db 2>/dev/null | wc -l"
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
