FROM nginx:alpine

# Instalar dependências de monitoramento
RUN apk add --no-cache \
    zabbix-agent2 \
    net-snmp \
    net-snmp-tools

# Copiar configurações
COPY nginx.conf /etc/nginx/nginx.conf
COPY html /usr/share/nginx/html
COPY snmpd.conf /etc/snmp/snmpd.conf
COPY entrypoint.sh /entrypoint.sh

# Criar diretórios necessários
RUN mkdir -p /var/net-snmp /var/run

# Configurar permissões
RUN chmod 644 /etc/snmp/snmpd.conf && \
    chmod 755 /var/net-snmp && \
    chmod +x /entrypoint.sh

# Expor portas
EXPOSE 80
EXPOSE 161/udp

# Comando de inicialização
ENTRYPOINT ["/entrypoint.sh"]
