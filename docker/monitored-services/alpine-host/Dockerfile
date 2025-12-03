FROM alpine:latest

# Instalar dependências
RUN apk add --no-cache \
    sqlite \
    zabbix-agent2 \
    net-snmp \
    net-snmp-tools

# Copiar configuração SNMP
COPY snmpd.conf /etc/snmp/snmpd.conf

# Copiar script de entrypoint
COPY entrypoint.sh /entrypoint.sh

# Criar diretórios necessários
RUN mkdir -p /var/net-snmp /var/run

# Configurar permissões
RUN chmod 644 /etc/snmp/snmpd.conf && \
    chmod 755 /var/net-snmp && \
    chmod +x /entrypoint.sh

# Expor porta SNMP
EXPOSE 161/udp

# Comando de inicialização
ENTRYPOINT ["/entrypoint.sh"]
