FROM ubuntu:latest

# Instalar SNMP e ferramentas de rede
RUN apt-get update && apt-get install -y \
    snmpd \
    snmp \
    libsnmp-dev \
    && rm -rf /var/lib/apt/lists/*

# Configurar o SNMP para escutar em todas as interfaces e definir comunidade
# A configuração abaixo permite acesso de leitura (rocommunity) para 'public'
RUN echo "agentAddress udp:161" > /etc/snmp/snmpd.conf && \
    echo "rocommunity public" >> /etc/snmp/snmpd.conf

# Expor a porta UDP padrão do SNMP
EXPOSE 161/udp

# Rodar o serviço SNMP em primeiro plano (para o container não fechar)
CMD ["/usr/sbin/snmpd", "-f", "-L", "n"]