# OIDs SNMP e Métricas Coletadas - FCAPS

## Mapeamento de Métricas para OIDs MIB-II

### 1. CPU (System Performance)

| Métrica Zabbix  | OID MIB-II Equivalente        | Descrição                              |
| --------------- | ----------------------------- | -------------------------------------- |
| CPU utilization | `.1.3.6.1.2.1.25.3.3.1.2`     | hrProcessorLoad - Carga do processador |
| CPU user time   | `.1.3.6.1.2.1.25.3.3.1.2`     | Tempo de CPU em modo usuário           |
| CPU system time | `.1.3.6.1.2.1.25.3.3.1.2`     | Tempo de CPU em modo kernel            |
| CPU idle time   | Calculado (100 - utilization) | Tempo ocioso                           |
| Load average    | `.1.3.6.1.4.1.2021.10.1.3`    | UCD-SNMP-MIB::laLoad                   |

**Valores Coletados:**

- alpine-host: ~10.5% utilização
- nginx-web: ~11.8% utilização
- python-app: ~13.7% utilização

---

### 2. Memória (Memory Management)

| Métrica Zabbix     | OID MIB-II Equivalente    | Descrição                     |
| ------------------ | ------------------------- | ----------------------------- |
| Total memory       | `.1.3.6.1.2.1.25.2.3.1.5` | hrStorageSize - Tamanho total |
| Available memory   | `.1.3.6.1.2.1.25.2.3.1.6` | hrStorageUsed - Memória usada |
| Memory utilization | Calculado                 | Percentual de uso             |
| Total swap         | `.1.3.6.1.4.1.2021.4.3.0` | memTotalSwap                  |
| Free swap          | `.1.3.6.1.4.1.2021.4.4.0` | memAvailSwap                  |

**Valores Coletados:**

- Total Memory: 3.83 GB em todos os hosts
- Utilização: ~20% (alpine-host: 20.3%, nginx-web: 20.3%, python-app: 19.8%)
- Swap: 2 GB disponível (100% livre)

---

### 3. Disco (Storage)

| Métrica Zabbix   | OID MIB-II Equivalente          | Descrição          |
| ---------------- | ------------------------------- | ------------------ |
| Disk utilization | `.1.3.6.1.2.1.25.2.3.1.6`       | hrStorageUsed      |
| Disk read rate   | `.1.3.6.1.4.1.2021.13.15.1.1.3` | diskIOReads        |
| Disk write rate  | `.1.3.6.1.4.1.2021.13.15.1.1.4` | diskIOWrites       |
| Disk I/O time    | Calculado via /proc/diskstats   | Tempo gasto em I/O |

**Discos Monitorados:**

- sda, sdb, sdc, sdd (devices virtuais)
- **sde (disco principal)**: ~6% utilização, ~24 writes/s

---

### 4. Rede (Network Interfaces)

| Métrica Zabbix      | OID MIB-II Equivalente  | Descrição    |
| ------------------- | ----------------------- | ------------ |
| Network traffic in  | `.1.3.6.1.2.1.2.2.1.10` | ifInOctets   |
| Network traffic out | `.1.3.6.1.2.1.2.2.1.16` | ifOutOctets  |
| Network errors      | `.1.3.6.1.2.1.2.2.1.14` | ifInErrors   |
| Interface status    | `.1.3.6.1.2.1.2.2.1.8`  | ifOperStatus |

**Interfaces Monitoradas:**

- Docker bridge network (172.20.0.0/16)
- Porta 8080 (Zabbix), 8081 (Nginx), 5000 (Python)

---

### 5. Processos e Sistema

| Métrica Zabbix              | OID MIB-II Equivalente    | Descrição         |
| --------------------------- | ------------------------- | ----------------- |
| Number of processes         | `.1.3.6.1.2.1.25.1.6.0`   | hrSystemProcesses |
| Number of running processes | `.1.3.6.1.2.1.25.4.2.1.7` | hrSWRunStatus     |
| System uptime               | `.1.3.6.1.2.1.1.3.0`      | sysUpTime         |
| System name                 | `.1.3.6.1.2.1.1.5.0`      | sysName           |
| System description          | `.1.3.6.1.2.1.1.1.0`      | sysDescr          |

**Valores Coletados:**

- alpine-host: 2 processos, 0 running, uptime 58min
- nginx-web: 3 processos, 0 running, uptime 58min
- python-app: 2 processos, 1 running, uptime 58min

---

## Tabela de Referência MIB-II Completa

### System Group (1.3.6.1.2.1.1)

- `.1.3.6.1.2.1.1.1.0` - sysDescr (Descrição do sistema)
- `.1.3.6.1.2.1.1.3.0` - sysUpTime (Tempo de atividade)
- `.1.3.6.1.2.1.1.5.0` - sysName (Nome do host)

### Host Resources MIB (1.3.6.1.2.1.25)

- `.1.3.6.1.2.1.25.1.6.0` - hrSystemProcesses
- `.1.3.6.1.2.1.25.2.3.1.5` - hrStorageSize
- `.1.3.6.1.2.1.25.2.3.1.6` - hrStorageUsed
- `.1.3.6.1.2.1.25.3.3.1.2` - hrProcessorLoad

### UCD-SNMP-MIB (1.3.6.1.4.1.2021)

- `.1.3.6.1.4.1.2021.10.1.3` - laLoad (Load Average)
- `.1.3.6.1.4.1.2021.4.3.0` - memTotalSwap
- `.1.3.6.1.4.1.2021.4.4.0` - memAvailSwap
- `.1.3.6.1.4.1.2021.13.15.1.1.3` - diskIOReads
- `.1.3.6.1.4.1.2021.13.15.1.1.4` - diskIOWrites

---

## Análise FCAPS

### **F - Fault Management** (Gerenciamento de Falhas)

- ✅ Triggers configurados para CPU/Memória/Disco
- ✅ Alertas quando serviços ficam indisponíveis
- ✅ Monitoramento de processos críticos

### **C - Configuration Management** (Gerenciamento de Configuração)

- ✅ Inventário automático de software instalado
- ✅ Checksum de /etc/passwd para detectar alterações
- ✅ Templates padronizados para Linux

### **A - Accounting Management** (Gerenciamento de Contabilização)

- ✅ Histórico de métricas armazenado no MySQL
- ✅ Gráficos de uso de recursos ao longo do tempo
- ✅ Relatórios de utilização de CPU/Memória/Disco

### **P - Performance Management** (Gerenciamento de Desempenho)

- ✅ Coleta de métricas a cada 30-60 segundos
- ✅ KPIs: CPU < 80%, Memória < 85%, Disco < 80%
- ✅ Gráficos de tendência e análise de capacidade

### **S - Security Management** (Gerenciamento de Segurança)

- ✅ Checksum de arquivos críticos (/etc/passwd)
- ✅ Monitoramento de usuários logados
- ✅ Auditoria de mudanças de configuração

---

## Exportação de Dados

Para exportar dados históricos via API Zabbix:

```bash
# Obter dados de CPU do host nginx-web
curl -X POST http://localhost:8080/api_jsonrpc.php \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "history.get",
    "params": {
      "output": "extend",
      "hostids": "10502",
      "itemids": "44279",
      "limit": 100
    },
    "auth": "your-auth-token",
    "id": 1
  }'
```

---

## Conclusão

O ambiente FCAPS está totalmente operacional com:

- ✅ **3 hosts monitorados** (nginx-web, python-app, alpine-host)
- ✅ **60+ métricas** coletadas por host
- ✅ **Mapeamento completo para OIDs MIB-II**
- ✅ **Dados persistentes** no volume Docker
- ✅ **Conformidade com os 5 pilares FCAPS**

---

**Última atualização:** 02/12/2025 20:17  
**Status do Sistema:** Operacional ✅
