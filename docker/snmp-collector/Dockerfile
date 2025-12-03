FROM python:3.11-alpine

WORKDIR /app

# Instalar dependências do sistema
# gcc, musl-dev, libffi-dev: compilação do easysnmp
# net-snmp-dev, net-snmp-libs: bibliotecas SNMP
# net-snmp, net-snmp-tools: daemon snmpd e ferramentas (snmpwalk, snmpget)
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    net-snmp-dev \
    net-snmp-libs \
    net-snmp \
    net-snmp-tools

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
