#!/bin/sh
set -e

echo "================================"
echo "  FCAPS SNMP Collector Service"
echo "================================"

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
