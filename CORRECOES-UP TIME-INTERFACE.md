# Correções: Uptime 0 e Interface Status Unknown

## Problemas Identificados

1. **Uptime 0s**: Vários hosts mostravam uptime 0
2. **Interface Status Unknown**: Status de interface não estava sendo exibido

## Correções Implementadas

### 1. Melhoria no Parsing do Uptime

**Arquivo:** `docker/snmp-collector/collector.py`

- Melhorado o parsing para tratar diferentes formatos que o SNMP pode retornar
- Tratamento de erros mais robusto
- Suporte para valores com "timeticks" e sem

### 2. Melhoria na Coleta de Status de Interface

**Arquivo:** `docker/snmp-collector/collector.py`

- Agora tenta múltiplos índices de interface (1, 2, 3)
- Tratamento de erros melhorado
- Retorna o primeiro valor válido encontrado

### 3. API Retornando Campos de Interface

**Arquivo:** `docker/snmp-collector/api.py`

- Query atualizada para incluir `ifOperStatus`, `ifInErrors`, `ifOutErrors`
- Campos agora são retornados na resposta da API

## Status Após Correções

### Hosts com Uptime Correto:

- ✅ **oracle-cloud**: 48017s (~13h 20m)
- ✅ **api-daora**: 11810s (~3h 17m)
- ✅ **snmp-collector**: Funcionando (recém iniciado)

### Hosts com Uptime 0 (Possíveis Causas):

1. **nginx-web, python-app, alpine-host**:

   - Pode não estar acessível via SNMP da nuvem
   - Pode estar retornando formato diferente
   - Pode estar em containers que foram reiniciados

2. **Soluções Possíveis**:
   - Verificar conectividade SNMP desses hosts
   - Verificar se os containers estão rodando
   - Verificar formato do uptime retornado por cada host

## Próximos Passos

Para hosts que ainda mostram uptime 0:

1. **Verificar conectividade SNMP**:

   ```bash
   ssh oracle-cloud
   docker exec snmp-collector snmpget -v2c -c public nginx-web:161 .1.3.6.1.2.1.1.3.0
   ```

2. **Verificar formato do uptime**:

   ```bash
   docker exec snmp-collector snmpwalk -v2c -c public nginx-web:161 system
   ```

3. **Ajustar parsing se necessário** baseado no formato retornado

## Interface Status

O código agora tenta coletar o status da interface tentando os índices 1, 2 e 3. Se nenhum funcionar, retorna `None` (que é exibido como "Unknown" no dashboard).

Para melhorar:

- Implementar SNMP walk para encontrar interfaces ativas
- Usar OID de descrição de interface para identificar a interface principal
