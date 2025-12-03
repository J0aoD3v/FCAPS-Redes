# Configuração SNMP - Python App

## Visão Geral

O container `python-app` está configurado com suporte completo a SNMP (Simple Network Management Protocol) para monitoramento via Zabbix e outras ferramentas de gerenciamento de redes.

## Características da Configuração

### 1. Daemon SNMP

- **Software**: net-snmp
- **Versão**: SNMPv2c
- **Porta**: 161/UDP (mapeada para 16102 no host)
- **Comunidade**: public (somente leitura)

### 2. Informações do Sistema

- **sysLocation**: Python Application Container - FCAPS Network
- **sysContact**: admin@fcaps.local
- **sysName**: python-app
- **sysServices**: 72 (Application layer)

### 3. MIBs Disponíveis

- **System MIB** (.1.3.6.1.2.1.1): Informações do sistema
- **Interfaces MIB** (.1.3.6.1.2.1.2): Interfaces de rede
- **IP MIB** (.1.3.6.1.2.1.4): Estatísticas IP
- **TCP MIB** (.1.3.6.1.2.1.6): Estatísticas TCP
- **Host Resources MIB** (.1.3.6.1.2.1.25): CPU, memória, processos

### 4. Extensões Customizadas

#### app-status

Verifica se a aplicação Python está em execução:

```bash
snmpwalk -v2c -c public localhost:16102 NET-SNMP-EXTEND-MIB::nsExtendOutLine.\"app-status\"
```

#### app-port

Verifica se a porta 5000 está em LISTEN:

```bash
snmpwalk -v2c -c public localhost:16102 NET-SNMP-EXTEND-MIB::nsExtendOutLine.\"app-port\"
```

#### app-memory

Mostra o uso de memória da aplicação Python:

```bash
snmpwalk -v2c -c public localhost:16102 NET-SNMP-EXTEND-MIB::nsExtendOutLine.\"app-memory\"
```

## Testes de Conectividade

### Teste Local (dentro do container)

```bash
docker exec python-app snmpget -v2c -c public localhost SNMPv2-MIB::sysName.0
```

### Teste do Host

```bash
snmpwalk -v2c -c public localhost:16102 system
```

### Teste da Rede Docker

```bash
docker exec zabbix-server snmpwalk -v2c -c public python-app:161 system
```

## OIDs Importantes

### Informações do Sistema

- **Nome do sistema**: .1.3.6.1.2.1.1.5.0
- **Localização**: .1.3.6.1.2.1.1.6.0
- **Contato**: .1.3.6.1.2.1.1.4.0
- **Uptime**: .1.3.6.1.2.1.1.3.0
- **Descrição**: .1.3.6.1.2.1.1.1.0

### Recursos do Host

- **CPU Load 1min**: .1.3.6.1.4.1.2021.10.1.3.1
- **CPU Load 5min**: .1.3.6.1.4.1.2021.10.1.3.2
- **CPU Load 15min**: .1.3.6.1.4.1.2021.10.1.3.3
- **Memória Total**: .1.3.6.1.4.1.2021.4.5.0
- **Memória Disponível**: .1.3.6.1.4.1.2021.4.6.0
- **Memória Usada**: .1.3.6.1.4.1.2021.4.11.0

### Processos

- **Lista de Processos**: .1.3.6.1.2.1.25.4.2
- **Número de Processos**: .1.3.6.1.2.1.25.1.6.0

### Rede

- **Interfaces**: .1.3.6.1.2.1.2.2.1
- **Bytes Recebidos**: .1.3.6.1.2.1.2.2.1.10
- **Bytes Enviados**: .1.3.6.1.2.1.2.2.1.16

## Arquivos de Configuração

### snmpd.conf

Localização: `/etc/snmp/snmpd.conf`

Principais configurações:

```conf
rocommunity    public  default
agentaddress   udp:161
sysLocation    Python Application Container - FCAPS Network
sysContact     admin@fcaps.local
```

### entrypoint.sh

Script de inicialização que:

1. Configura o Zabbix Agent2
2. Verifica a configuração SNMP
3. Inicia o daemon SNMP
4. Testa a conectividade SNMP
5. Inicia a aplicação Python

## Troubleshooting

### SNMP não responde

```bash
# Verificar se o daemon está rodando
docker exec python-app ps aux | grep snmpd

# Verificar logs do SNMP
docker exec python-app snmpd -Lsd -Lf /dev/stdout

# Reiniciar o container
docker restart python-app
```

### Testar configuração

```bash
# Entrar no container
docker exec -it python-app sh

# Testar localmente
snmpget -v2c -c public localhost SNMPv2-MIB::sysName.0

# Ver todas as OIDs disponíveis
snmpwalk -v2c -c public localhost
```

### Verificar porta

```bash
# Ver se a porta 161 está aberta no container
docker exec python-app netstat -uln | grep 161

# Ver mapeamento de portas
docker port python-app
```

## Integração com Zabbix

O container já possui:

- ✅ Zabbix Agent2 instalado e configurado
- ✅ SNMP daemon ativo
- ✅ Métricas customizadas via SNMP extends
- ✅ Conectividade com zabbix-server

Para adicionar ao Zabbix:

1. Acesse Configuration → Hosts → Create host
2. Nome: python-app
3. Interface SNMP: python-app:161 (ou IP do container)
4. Comunidade: public
5. Templates: Linux by SNMP + Template App Generic SNMPv2

## Segurança

⚠️ **Importante**: Esta configuração é para ambiente de desenvolvimento/laboratório.

Em produção:

- Use SNMPv3 com autenticação e criptografia
- Altere a comunidade padrão "public"
- Restrinja IPs autorizados
- Use firewall para limitar acesso à porta SNMP

## Referências

- [Net-SNMP Documentation](http://www.net-snmp.org/docs/)
- [RFC 3410 - SNMP](https://www.rfc-editor.org/rfc/rfc3410)
- [Zabbix SNMP Monitoring](https://www.zabbix.com/documentation/current/manual/config/items/itemtypes/snmp)
