# Zabbix Server como Coletor SNMP

## Visão Geral

O container **zabbix-server** agora possui um papel adicional: além de funcionar como servidor central de monitoramento, ele também atua como **coletor SNMP**, consultando diretamente os outros containers da rede via protocolo SNMP.

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                   Zabbix Server Container                   │
│                                                               │
│  ┌───────────────┐         ┌──────────────────────┐         │
│  │  Zabbix Core  │         │  Ferramentas SNMP    │         │
│  │  (Monitoring) │         │  • snmpwalk          │         │
│  │               │         │  • snmpget           │         │
│  └───────────────┘         │  • net-snmp-tools    │         │
│                            └──────────────────────┘         │
└───────────────────────────────┬─────────────────────────────┘
                                │ SNMP Queries (UDP 161)
                                │ Community: public
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐       ┌───────────────┐     ┌───────────────┐
│  nginx-web    │       │  python-app   │     │  alpine-host  │
│  (Container)  │       │  (Container)  │     │  (Container)  │
│               │       │               │     │               │
│  snmpd:161    │       │  snmpd:161    │     │  snmpd:161    │
│  porta:16101  │       │  porta:16102  │     │  porta:16103  │
└───────────────┘       └───────────────┘     └───────────────┘
```

---

## Modificações no Docker Compose

### Container Zabbix Server

```yaml
zabbix-server:
  image: zabbix/zabbix-appliance:alpine-latest
  entrypoint: >
    sh -c "apk add --no-cache net-snmp net-snmp-tools &&
           echo 'Ferramentas SNMP instaladas no Zabbix Server' &&
           echo 'Testando conectividade SNMP com containers monitorados...' &&
           sleep 5 &&
           (snmpwalk -v2c -c public nginx-web:161 system 2>/dev/null && echo '✓ nginx-web respondendo via SNMP' || echo '✗ nginx-web não respondeu') &
           (snmpwalk -v2c -c public python-app:161 system 2>/dev/null && echo '✓ python-app respondendo via SNMP' || echo '✗ python-app não respondeu') &
           (snmpwalk -v2c -c public alpine-host:161 system 2>/dev/null && echo '✓ alpine-host respondendo via SNMP' || echo '✗ alpine-host não respondeu') &
           /sbin/tini -- /usr/bin/docker-entrypoint.sh"
```

### Funcionalidades Adicionadas

1. **Instalação de Ferramentas SNMP**: `net-snmp` e `net-snmp-tools` instalados no boot
2. **Teste de Conectividade Automático**: Verifica se cada container responde via SNMP
3. **Resolução de Nomes DNS**: Usa nomes dos containers na rede Docker interna

---

## Scripts de Coleta

### Script Shell: `snmp-collector.sh`

Localização: `scripts/snmp-collector.sh`

**Funcionalidades:**

- Coleta informações de todos os 3 containers monitorados
- Exibe métricas formatadas de:
  - **Sistema**: Nome, descrição, uptime, localização, contato
  - **CPU**: Número de processos, carga do processador
  - **Memória**: Total, usado, utilização percentual
  - **Armazenamento**: Discos e partições
  - **Rede**: Interfaces, status, tráfego de entrada/saída

**Execução Manual:**

```bash
# Dentro do container zabbix-server
/tmp/snmp-collector.sh
```

### Script PowerShell: `collect-snmp-metrics.ps1`

Localização: `scripts/collect-snmp-metrics.ps1`

**Funcionalidades:**

- Verifica se o container zabbix-server está rodando
- Copia o script shell para dentro do container
- Executa a coleta e exibe os resultados

**Uso:**

```powershell
.\scripts\collect-snmp-metrics.ps1
```

---

## OIDs SNMP Coletados

### Informações do Sistema

- `.1.3.6.1.2.1.1.1.0` - **sysDescr**: Descrição do sistema operacional
- `.1.3.6.1.2.1.1.3.0` - **sysUpTime**: Tempo desde o último boot
- `.1.3.6.1.2.1.1.5.0` - **sysName**: Nome do host
- `.1.3.6.1.2.1.1.6.0` - **sysLocation**: Localização física/lógica
- `.1.3.6.1.2.1.1.4.0` - **sysContact**: Informações de contato

### CPU e Processos

- `.1.3.6.1.2.1.25.1.6.0` - **hrSystemProcesses**: Número total de processos
- `.1.3.6.1.2.1.25.3.3.1.2` - **hrProcessorLoad**: Carga do processador (%)

### Memória

- `.1.3.6.1.2.1.25.2.3.1.5` - **hrStorageSize**: Tamanho total da memória
- `.1.3.6.1.2.1.25.2.3.1.6` - **hrStorageUsed**: Memória utilizada
- `.1.3.6.1.2.1.25.2.3.1.4` - **hrStorageAllocationUnits**: Unidade de alocação

### Armazenamento

- `.1.3.6.1.2.1.25.2.3.1.3` - **hrStorageDescr**: Descrição do dispositivo
- `.1.3.6.1.2.1.25.2.3.1.5` - **hrStorageSize**: Tamanho total
- `.1.3.6.1.2.1.25.2.3.1.6` - **hrStorageUsed**: Espaço utilizado

### Interfaces de Rede

- `.1.3.6.1.2.1.2.2.1.2` - **ifDescr**: Descrição da interface
- `.1.3.6.1.2.1.2.2.1.8` - **ifOperStatus**: Status operacional (up/down)
- `.1.3.6.1.2.1.2.2.1.10` - **ifInOctets**: Bytes recebidos
- `.1.3.6.1.2.1.2.2.1.16` - **ifOutOctets**: Bytes transmitidos

---

## Exemplo de Saída

```
==========================================
  FCAPS - Coletor de Métricas SNMP
==========================================

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 HOST: nginx-web
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Conectividade: OK

🖥️  INFORMAÇÕES DO SISTEMA
────────────────────────────────────────
Descrição: Linux nginx-web 5.15.0-1071-azure x86_64
Nome: nginx-web
Uptime: 1 day, 2:34:15
Localização: nginx-web-container
Contato: admin@fcaps.local

⚙️  CPU E PROCESSAMENTO
────────────────────────────────────────
Processos: 3
Carga da CPU: 11%

💾 MEMÓRIA
────────────────────────────────────────
Total: 131072 KB
Usado: 26624 KB
Utilização: 20%

💿 ARMAZENAMENTO
────────────────────────────────────────
  /: 45123/256000 blocos (17%)

🌐 INTERFACES DE REDE
────────────────────────────────────────
  eth0: Status=up | In=234MB | Out=189MB
  lo: Status=up | In=12MB | Out=12MB
```

---

## Comandos Úteis

### Teste Manual de Conectividade SNMP

```bash
# Entrar no container
docker exec -it zabbix-server sh

# Testar cada container
snmpwalk -v2c -c public nginx-web:161 system
snmpwalk -v2c -c public python-app:161 system
snmpwalk -v2c -c public alpine-host:161 system
```

### Consultar OID Específico

```bash
# CPU
snmpget -v2c -c public nginx-web:161 .1.3.6.1.2.1.25.3.3.1.2.1

# Uptime
snmpget -v2c -c public python-app:161 .1.3.6.1.2.1.1.3.0

# Número de processos
snmpget -v2c -c public alpine-host:161 .1.3.6.1.2.1.25.1.6.0
```

### Ver Logs do Zabbix Server

```powershell
docker logs zabbix-server | Select-String "SNMP"
```

---

## Vantagens desta Abordagem

### 1. **Centralização**

- Todas as consultas SNMP partem do mesmo ponto (Zabbix Server)
- Facilita troubleshooting e auditoria

### 2. **Rede Interna Docker**

- Comunicação direta entre containers via nomes DNS
- Não precisa expor portas SNMP externamente
- Mais seguro (tráfego fica na bridge network)

### 3. **Automação**

- Teste de conectividade automático no boot
- Scripts prontos para coleta sob demanda
- Integração com interface web do Zabbix (futuramente)

### 4. **Conformidade FCAPS**

- **Fault**: Detecta falhas de comunicação SNMP
- **Configuration**: Inventário de sistemas via SNMP
- **Accounting**: Histórico de coletas
- **Performance**: Métricas de CPU, memória, rede
- **Security**: Auditoria de acessos SNMP

---

## Integração com Zabbix Web

Para adicionar hosts SNMP na interface web do Zabbix:

1. Acesse **Configuration → Hosts → Create host**
2. Configure:
   - **Host name**: `nginx-web-snmp`, `python-app-snmp`, `alpine-host-snmp`
   - **Groups**: Linux servers
   - **Interfaces**: SNMP
     - IP address: `nginx-web` (nome do container)
     - Port: `161`
     - SNMP version: `SNMPv2`
     - SNMP community: `public`
3. Adicione template: **Template Net Linux SNMP**
4. Salve e aguarde a coleta automática

---

## Troubleshooting

### Container não responde via SNMP

```bash
# Verificar se snmpd está rodando
docker exec nginx-web ps aux | grep snmpd

# Testar conectividade de rede
docker exec zabbix-server ping nginx-web

# Ver logs do snmpd
docker exec nginx-web cat /var/log/messages | grep snmpd
```

### Community string incorreta

```bash
# Verificar configuração
docker exec nginx-web cat /etc/snmp/snmpd.conf
```

### Timeout nas queries

```bash
# Aumentar timeout (padrão é 1 segundo)
snmpget -v2c -c public -t 5 nginx-web:161 sysUpTime.0
```

---

## Próximos Passos

1. ✅ **Configuração inicial completa**
2. ⏳ **Adicionar hosts SNMP na interface do Zabbix**
3. ⏳ **Criar triggers para alertas SNMP**
4. ⏳ **Dashboard unificado (Zabbix Agent + SNMP)**
5. ⏳ **Script de exportação de métricas para relatórios**

---

## Referências

- [RFC 1157 - SNMP Protocol](https://www.rfc-editor.org/rfc/rfc1157)
- [RFC 1213 - MIB-II](https://www.rfc-editor.org/rfc/rfc1213)
- [Zabbix SNMP Monitoring](https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/snmp)
- [Net-SNMP Documentation](http://www.net-snmp.org/docs/)

---

**Última atualização:** 02/12/2025  
**Status:** ✅ Operacional
