FROM python:3.11-alpine

WORKDIR /app

# Instalar dependências do sistema (easysnmp precisa de net-snmp-dev)
RUN apk add --no-cache gcc musl-dev libffi-dev net-snmp-dev net-snmp-libs

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY collector.py api.py entrypoint.sh ./

# Tornar script executável
RUN chmod +x entrypoint.sh

# Criar diretório de dados
RUN mkdir -p /data

EXPOSE 8090

ENTRYPOINT ["/app/entrypoint.sh"]
