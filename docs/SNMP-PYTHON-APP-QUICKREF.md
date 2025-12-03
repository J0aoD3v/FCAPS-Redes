# Guia Rápido - SNMP no Python App

## 🚀 Quick Start

```powershell
# 1. Rebuild e iniciar o container
cd docker
docker-compose build python-app
docker-compose up -d python-app

# 2. Executar teste automatizado
cd ..
.\scripts\test-snmp-python-app.ps1

# 3. Verificar logs
docker logs python-app
```

## 🔍 Comandos de Teste

### Teste Básico (Sistema)

```bash
docker exec python-app snmpget -v2c -c public localhost SNMPv2-MIB::sysName.0
```

### Listar Todas as OIDs do Sistema

```bash
docker exec python-app snmpwalk -v2c -c public localhost system
```

### Informações do Host

```bash
docker exec python-app snmpwalk -v2c -c public localhost .1.3.6.1.2.1.25.1
```

### Processos em Execução

```bash
docker exec python-app snmpwalk -v2c -c public localhost .1.3.6.1.2.1.25.4.2
```

### Interfaces de Rede

```bash
docker exec python-app snmpwalk -v2c -c public localhost .1.3.6.1.2.1.2.2.1
```

### CPU Load

```bash
docker exec python-app snmpget -v2c -c public localhost .1.3.6.1.4.1.2021.10.1.3.1
docker exec python-app snmpget -v2c -c public localhost .1.3.6.1.4.1.2021.10.1.3.2
docker exec python-app snmpget -v2c -c public localhost .1.3.6.1.4.1.2021.10.1.3.3
```

### Memória

```bash
docker exec python-app snmpget -v2c -c public localhost .1.3.6.1.4.1.2021.4.5.0  # Total
docker exec python-app snmpget -v2c -c public localhost .1.3.6.1.4.1.2021.4.6.0  # Disponível
docker exec python-app snmpget -v2c -c public localhost .1.3.6.1.4.1.2021.4.11.0 # Usada
```

### Extensões Customizadas (Aplicação Python)

```bash
# Status da aplicação
docker exec python-app snmpwalk -v2c -c public localhost NET-SNMP-EXTEND-MIB::nsExtendOutLine.\"app-status\"

# Status da porta 5000
docker exec python-app snmpwalk -v2c -c public localhost NET-SNMP-EXTEND-MIB::nsExtendOutLine.\"app-port\"

# Memória da aplicação
docker exec python-app snmpwalk -v2c -c public localhost NET-SNMP-EXTEND-MIB::nsExtendOutLine.\"app-memory\"
```

## 🌐 Teste via Rede Docker

### Do Zabbix Server

```bash
docker exec zabbix-server snmpwalk -v2c -c public python-app:161 system
docker exec zabbix-server snmpget -v2c -c public python-app:161 SNMPv2-MIB::sysName.0
```

### Do SNMP Collector

```bash
docker exec snmp-collector snmpwalk -v2c -c public python-app:161 system
```

## 🐛 Troubleshooting

### Verificar se SNMP está rodando

```bash
docker exec python-app ps aux | grep snmpd
```

### Verificar porta SNMP

```bash
docker exec python-app netstat -uln | grep 161
```

### Verificar configuração SNMP

```bash
docker exec python-app cat /etc/snmp/snmpd.conf
```

### Ver logs do SNMP em tempo real

```bash
docker exec python-app sh -c "killall snmpd; snmpd -Lsd -Lf /dev/stdout"
```

### Reiniciar apenas o SNMP (sem reiniciar container)

```bash
docker exec python-app sh -c "killall snmpd; /usr/sbin/snmpd -Lsd -Lf /dev/null -p /var/run/snmpd.pid"
```

### Entrar no container para debug

```bash
docker exec -it python-app sh
```

## 📊 Monitoramento Contínuo

### Verificar uptime do SNMP

```bash
docker exec python-app snmpget -v2c -c public localhost SNMPv2-MIB::sysUpTime.0
```

### Monitorar CPU em tempo real

```bash
# PowerShell
while ($true) {
    docker exec python-app snmpget -v2c -c public localhost .1.3.6.1.4.1.2021.10.1.3.1
    Start-Sleep -Seconds 5
}
```

### Monitorar tráfego de rede

```bash
docker exec python-app snmpwalk -v2c -c public localhost .1.3.6.1.2.1.2.2.1.10
docker exec python-app snmpwalk -v2c -c public localhost .1.3.6.1.2.1.2.2.1.16
```

## 🔧 Comandos de Manutenção

### Rebuild completo

```powershell
docker-compose down
docker-compose build --no-cache python-app
docker-compose up -d python-app
```

### Ver logs de inicialização

```powershell
docker logs python-app --tail 50
```

### Remover e recriar container

```powershell
docker-compose stop python-app
docker-compose rm -f python-app
docker-compose up -d python-app
```

### Exportar métricas SNMP para arquivo

```bash
docker exec python-app snmpwalk -v2c -c public localhost > snmp-metrics.txt
```

## 📱 Integração com Ferramentas

### cURL (via API REST do snmp-collector)

```bash
curl http://localhost:8090/metrics/python-app
```

### Python (pysnmp)

```python
from pysnmp.hlapi import *

iterator = getCmd(
    SnmpEngine(),
    CommunityData('public', mpModel=1),
    UdpTransportTarget(('localhost', 16102)),
    ContextData(),
    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0))
)

errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

if errorIndication:
    print(errorIndication)
else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))
```

### Net-SNMP (se instalado no Windows)

```bash
snmpwalk -v2c -c public localhost:16102 system
snmpget -v2c -c public localhost:16102 SNMPv2-MIB::sysName.0
```

## 📋 Checklist de Validação

- [ ] Container está rodando (`docker ps | grep python-app`)
- [ ] Daemon SNMP está ativo (`docker exec python-app ps aux | grep snmpd`)
- [ ] Porta 161 está aberta (`docker exec python-app netstat -uln | grep 161`)
- [ ] Teste local funciona (`docker exec python-app snmpget -v2c -c public localhost SNMPv2-MIB::sysName.0`)
- [ ] Teste via rede funciona (`docker exec zabbix-server snmpwalk -v2c -c public python-app:161 system`)
- [ ] Aplicação Python está rodando (`curl http://localhost:5000`)
- [ ] Zabbix Agent está ativo (se aplicável)

## 📞 Suporte

Ver documentação completa em:

- `docker/monitored-services/python-app/README-SNMP.md`
- `docs/SNMP-PYTHON-APP.md`
- `docs/OIDS-METRICAS.md`

---

**FCAPS - Gerenciamento de Redes**
