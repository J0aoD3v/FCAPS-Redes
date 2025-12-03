FROM python:3.11-alpine

# Instalar dependências de compilação e runtime
RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    sqlite \
    net-snmp \
    net-snmp-tools \
    zabbix-agent2

WORKDIR /app

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Remover dependências de compilação para reduzir tamanho
RUN apk del gcc musl-dev linux-headers

# Copiar aplicação
COPY . .

# Copiar configuração SNMP
COPY snmpd.conf /etc/snmp/snmpd.conf

# Copiar script de entrypoint
COPY entrypoint.sh /entrypoint.sh

# Criar diretórios necessários
RUN mkdir -p /app/data /var/net-snmp /var/run

# Configurar permissões
RUN chmod 644 /etc/snmp/snmpd.conf && \
    chmod 755 /var/net-snmp && \
    chmod +x /entrypoint.sh

# Expor portas
EXPOSE 5000
EXPOSE 161/udp

# Comando de inicialização
ENTRYPOINT ["/entrypoint.sh"]
