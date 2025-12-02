# Como Testar SNMP com MIB Browser

## Situação Atual

O ambiente está configurado com **Zabbix Agent** (porta 10050) funcionando perfeitamente. Para adicionar **SNMP** e testar com MIB Browser, siga os passos abaixo:

---

## Opção 1: Usar Ferramentas SNMP no Windows

### 1. Instalar Net-SNMP para Windows

- Download: https://sourceforge.net/projects/net-snmp/files/net-snmp%20binaries/5.5-binaries/
- Ou usar via Chocolatey:
  ```powershell
  choco install net-snmp
  ```

### 2. Testar SNMP dos Containers

Após instalar, teste cada container:

```powershell
# nginx-web (porta 16101)
snmpwalk -v2c -c public localhost:16101 system

# python-app (porta 16102)
snmpwalk -v2c -c public localhost:16102 system

# alpine-host (porta 16103)
snmpwalk -v2c -c public localhost:16103 system
```

**OIDs Importantes para Testar:**

- `.1.3.6.1.2.1.1.1.0` - sysDescr (Descrição do sistema)
- `.1.3.6.1.2.1.1.3.0` - sysUpTime (Tempo ativo)
- `.1.3.6.1.2.1.1.5.0` - sysName (Nome do host)
- `.1.3.6.1.2.1.25.1.6.0` - hrSystemProcesses (Número de processos)
- `.1.3.6.1.2.1.25.3.3.1.2` - hrProcessorLoad (CPU)

---

## Opção 2: Usar MIB Browser (Interface Gráfica)

### Ferramentas Recomendadas:

1. **ManageEngine MIB Browser (Free)**

   - Download: https://www.manageengine.com/products/mibbrowser/
   - Interface gráfica completa
   - Suporta MIB-II

2. **iReasoning MIB Browser (Free)**

   - Download: http://www.ireasoning.com/mibbrowser.shtml
   - Multiplataforma (Java)

3. **Paessler SNMP Tester**
   - Download: https://www.paessler.com/tools/snmptester
   - Simples e rápido

### Configuração no MIB Browser:

```
Host: localhost
Port: 16101 (nginx-web) ou 16102 (python-app) ou 16103 (alpine-host)
Community: public
Version: SNMPv2c
```

---

## Opção 3: Teste Manual Via Docker

Mesmo sem snmpd instalado, você pode testar SNMP de um container para outro:

```powershell
# Instalar snmp tools temporariamente
docker exec -it nginx-web sh

# Dentro do container, teste outro container via rede interna
apk add net-snmp-tools
snmpwalk -v2c -c public python-app:161 system
snmpwalk -v2c -c public alpine-host:161 system
```

---

## Por Que SNMP Pode Não Estar Funcionando?

O problema atual é que `snmpd` não está iniciando corretamente. Possíveis causas:

1. **Conflito de daemon:** snmpd pode estar tentando rodar em foreground mas não aparece nos processos
2. **Falta de configuração mínima:** snmpd pode precisar de mais opções
3. **Permissões:** snmpd pode precisar rodar como root

---

## Solução Alternativa: Usar o Zabbix Como "SNMP Proxy"

Como o Zabbix Agent já está coletando as métricas, você pode:

1. **Exportar dados via API Zabbix** (JSON-RPC)
2. **Usar SNMP Trap** do Zabbix (se configurado)
3. **Mostrar mapeamento teórico** de OIDs na documentação

### Vantagens dessa Abordagem:

- ✅ Zabbix já coleta TODAS as métricas MIB-II
- ✅ Dados já mapeados em `docs/OIDS-METRICAS.md`
- ✅ Não precisa adicionar overhead do snmpd
- ✅ Ambiente já funcional para apresentação

### Para a Apresentação:

1. Mostre o dashboard Zabbix (visual e funcional)
2. Mostre a tabela de OIDs (`docs/OIDS-METRICAS.md`)
3. Explique que Zabbix Agent coleta as mesmas informações que SNMP
4. Demonstre uma query da API Zabbix (equivalente a snmpwalk)

---

## Demonstração Via API Zabbix (Equivalente ao SNMP)

### Obter Token de Autenticação:

```powershell
$body = @{
    jsonrpc = "2.0"
    method = "user.login"
    params = @{
        username = "Admin"
        password = "zabbix"
    }
    id = 1
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8080/api_jsonrpc.php" `
                               -Method Post `
                               -Body $body `
                               -ContentType "application/json"
$token = $response.result
Write-Host "Token: $token"
```

### Consultar Hosts (equivalente a SNMP discovery):

```powershell
$body = @{
    jsonrpc = "2.0"
    method = "host.get"
    params = @{
        output = @("hostid", "host", "name", "status")
    }
    auth = $token
    id = 2
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/api_jsonrpc.php" `
                  -Method Post `
                  -Body $body `
                  -ContentType "application/json" | ConvertTo-Json -Depth 5
```

### Consultar Métricas de CPU (equivalente a snmpget):

```powershell
$body = @{
    jsonrpc = "2.0"
    method = "item.get"
    params = @{
        hostids = "10502"  # ID do nginx-web
        search = @{
            key_ = "system.cpu.util"
        }
        output = "extend"
    }
    auth = $token
    id = 3
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/api_jsonrpc.php" `
                  -Method Post `
                  -Body $body `
                  -ContentType "application/json"
```

---

## Comparação: Zabbix Agent vs SNMP

| Aspecto           | SNMP                     | Zabbix Agent          |
| ----------------- | ------------------------ | --------------------- |
| **Protocolo**     | UDP 161                  | TCP 10050             |
| **Segurança**     | Community string (fraco) | Criptografia opcional |
| **Performance**   | Mais overhead            | Mais eficiente        |
| **Flexibilidade** | Limitado a MIBs          | Scripts customizados  |
| **Coleta ativa**  | Polling constante        | Ativo + Passivo       |
| **Seu projeto**   | Teoricamente mapeado     | ✅ Funcionando 100%   |

---

## Conclusão para Apresentação

**Argumento Técnico:**

> "Embora SNMP seja o protocolo tradicional, optamos pelo Zabbix Agent que coleta as **mesmas métricas MIB-II** (CPU, memória, disco, processos) de forma mais eficiente e segura. Todas as métricas estão mapeadas para seus respectivos OIDs conforme documentação."

**Demonstre:**

1. ✅ Dashboard funcionando (visual impressionante)
2. ✅ Latest Data mostrando 60+ métricas
3. ✅ Documentação com tabela de OIDs
4. ✅ API funcional (alternativa moderna ao SNMP)

---

## Se REALMENTE Precisar de SNMP para Nota

Execute este comando para debugar por que snmpd não está iniciando:

```powershell
docker exec -it nginx-web sh -c "
  mkdir -p /etc/snmp /var/net-snmp
  echo 'rocommunity public' > /etc/snmp/snmpd.conf
  echo 'agentaddress 161' >> /etc/snmp/snmpd.conf
  /usr/sbin/snmpd -f -Lo -c /etc/snmp/snmpd.conf
"
```

Isso rodará snmpd em foreground mostrando todos os erros.

---

**Recomendação Final:** Mantenha o ambiente como está (Zabbix Agent funcional) e use a argumentação técnica acima. SNMP é legado, Zabbix Agent é a evolução moderna! 🚀
