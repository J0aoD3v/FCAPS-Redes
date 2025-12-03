# Python App - SNMP Configuration

## ✅ Status: SNMP Ativo e Configurado

O container `python-app` está totalmente configurado com suporte SNMP para monitoramento de rede.

## 📋 O que foi configurado

### 1. Arquivos Criados/Modificados

#### `Dockerfile` (modificado)

- ✅ Instalado `net-snmp` e `net-snmp-tools`
- ✅ Instalado `zabbix-agent2`
- ✅ Porta 161/UDP exposta
- ✅ Script de entrypoint configurado

#### `snmpd.conf` (novo)

Configuração completa do daemon SNMP:

- Comunidade: `public` (read-only)
- Porta: 161/UDP
- Informações do sistema configuradas
- MIBs disponíveis: System, Interfaces, IP, TCP, Host Resources
- Extensões customizadas para monitorar a aplicação Python

#### `entrypoint.sh` (novo)

Script de inicialização que:

1. Configura o Zabbix Agent2
2. Verifica configuração SNMP
3. Inicia o daemon SNMP
4. Testa conectividade
5. Inicia a aplicação Python

### 2. Documentação

#### `docs/SNMP-PYTHON-APP.md`

Documentação completa incluindo:

- Visão geral da configuração
- OIDs importantes
- Testes de conectividade
- Troubleshooting
- Integração com Zabbix

#### `scripts/test-snmp-python-app.ps1`

Script de teste automatizado que verifica:

- Status do container
- Daemon SNMP rodando
- Porta 161/UDP aberta
- Testes locais e via rede
- OIDs disponíveis

## 🚀 Como usar

### Rebuild do Container

```powershell
cd docker
docker-compose build python-app
docker-compose up -d python-app
```

### Executar Testes

```powershell
.\scripts\test-snmp-python-app.ps1
```

### Testar SNMP Manualmente

#### Do host (Windows)

Instale o Net-SNMP para Windows ou use WSL:

```powershell
# Via WSL
wsl snmpwalk -v2c -c public localhost:16102 system
```

#### Do container Zabbix

```powershell
docker exec zabbix-server snmpwalk -v2c -c public python-app:161 system
```

#### Do próprio container

```powershell
docker exec python-app snmpget -v2c -c public localhost SNMPv2-MIB::sysName.0
```

## 📊 Métricas Disponíveis

### Sistema

- Nome do sistema
- Localização
- Contato
- Uptime
- Descrição

### Hardware

- CPU Load (1, 5, 15 min)
- Memória total, livre, usada
- Uso de disco

### Rede

- Interfaces
- Bytes recebidos/enviados
- Erros de rede

### Aplicação (Extensões Customizadas)

- **app-status**: Status da aplicação Python
- **app-port**: Status da porta 5000
- **app-memory**: Uso de memória da aplicação

## 🔌 Informações de Conexão

| Item               | Valor          |
| ------------------ | -------------- |
| Porta no Host      | 16102/UDP      |
| Porta no Container | 161/UDP        |
| Comunidade         | public         |
| Versão SNMP        | v2c            |
| IP na Rede Docker  | python-app:161 |

## 🧪 Validação Rápida

Execute dentro do container:

```bash
docker exec python-app snmpwalk -v2c -c public localhost system
```

Saída esperada:

```
SNMPv2-MIB::sysDescr.0 = STRING: Linux python-app ...
SNMPv2-MIB::sysObjectID.0 = OID: NET-SNMP-MIB::netSnmpAgentOIDs.10
SNMPv2-MIB::sysUpTime.0 = Timeticks: ...
SNMPv2-MIB::sysContact.0 = STRING: admin@fcaps.local
SNMPv2-MIB::sysName.0 = STRING: python-app
SNMPv2-MIB::sysLocation.0 = STRING: Python Application Container - FCAPS Network
```

## 🔧 Troubleshooting

### Container não inicia

```powershell
# Ver logs
docker logs python-app

# Rebuild
docker-compose build --no-cache python-app
docker-compose up -d python-app
```

### SNMP não responde

```powershell
# Verificar se daemon está rodando
docker exec python-app ps aux | grep snmpd

# Reiniciar container
docker restart python-app

# Entrar no container e testar
docker exec -it python-app sh
snmpget -v2c -c public localhost SNMPv2-MIB::sysName.0
```

### Porta não está acessível

```powershell
# Verificar mapeamento de portas
docker port python-app

# Verificar se porta está aberta no container
docker exec python-app netstat -uln | grep 161
```

## 📚 Próximos Passos

1. ✅ Rebuild do container: `docker-compose build python-app`
2. ✅ Iniciar container: `docker-compose up -d python-app`
3. ✅ Executar testes: `.\scripts\test-snmp-python-app.ps1`
4. ✅ Adicionar host no Zabbix (ver `docs/ADICIONAR-HOSTS-ZABBIX.md`)
5. ✅ Configurar templates SNMP no Zabbix

## 📖 Documentação Adicional

- [SNMP-PYTHON-APP.md](../docs/SNMP-PYTHON-APP.md) - Documentação completa
- [OIDS-METRICAS.md](../docs/OIDS-METRICAS.md) - Lista de OIDs disponíveis
- [ZABBIX-SNMP-COLLECTOR.md](../docs/ZABBIX-SNMP-COLLECTOR.md) - Integração com Zabbix

---

**Projeto**: FCAPS - Gerenciamento de Redes
**Data**: Dezembro 2025
