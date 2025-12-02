#!/bin/sh
# Script para coletar informações SNMP dos containers monitorados
# Executar dentro do container zabbix-server

echo "=========================================="
echo "  FCAPS - Coletor de Métricas SNMP"
echo "=========================================="
echo ""

COMMUNITY="public"
CONTAINERS="nginx-web python-app alpine-host"

for HOST in $CONTAINERS; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 HOST: $HOST"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Teste de conectividade
    if ! snmpget -v2c -c $COMMUNITY $HOST:161 sysUpTime.0 > /dev/null 2>&1; then
        echo "❌ ERRO: $HOST não está respondendo via SNMP"
        echo ""
        continue
    fi
    
    echo "✅ Conectividade: OK"
    echo ""
    
    # 1. Informações do Sistema
    echo "🖥️  INFORMAÇÕES DO SISTEMA"
    echo "────────────────────────────────────────"
    SYSDESCR=$(snmpget -v2c -c $COMMUNITY -Oqv $HOST:161 sysDescr.0 2>/dev/null)
    SYSNAME=$(snmpget -v2c -c $COMMUNITY -Oqv $HOST:161 sysName.0 2>/dev/null)
    UPTIME=$(snmpget -v2c -c $COMMUNITY -Oqv $HOST:161 sysUpTime.0 2>/dev/null)
    LOCATION=$(snmpget -v2c -c $COMMUNITY -Oqv $HOST:161 sysLocation.0 2>/dev/null)
    CONTACT=$(snmpget -v2c -c $COMMUNITY -Oqv $HOST:161 sysContact.0 2>/dev/null)
    
    echo "Descrição: $SYSDESCR"
    echo "Nome: $SYSNAME"
    echo "Uptime: $UPTIME"
    echo "Localização: $LOCATION"
    echo "Contato: $CONTACT"
    echo ""
    
    # 2. CPU
    echo "⚙️  CPU E PROCESSAMENTO"
    echo "────────────────────────────────────────"
    PROCESSES=$(snmpget -v2c -c $COMMUNITY -Oqv $HOST:161 hrSystemProcesses.0 2>/dev/null)
    CPULOAD=$(snmpwalk -v2c -c $COMMUNITY -Oqv $HOST:161 hrProcessorLoad 2>/dev/null | head -n 1)
    
    echo "Processos: $PROCESSES"
    echo "Carga da CPU: $CPULOAD%"
    echo ""
    
    # 3. Memória
    echo "💾 MEMÓRIA"
    echo "────────────────────────────────────────"
    # Buscar storage entries (tipo 2 = RAM)
    MEMORY_DATA=$(snmpwalk -v2c -c $COMMUNITY $HOST:161 hrStorageDescr 2>/dev/null | grep -i "Physical memory\|RAM")
    if [ -n "$MEMORY_DATA" ]; then
        MEMORY_INDEX=$(echo "$MEMORY_DATA" | cut -d'.' -f2 | cut -d' ' -f1)
        if [ -n "$MEMORY_INDEX" ]; then
            MEM_SIZE=$(snmpget -v2c -c $COMMUNITY -Oqv $HOST:161 hrStorageSize.$MEMORY_INDEX 2>/dev/null)
            MEM_USED=$(snmpget -v2c -c $COMMUNITY -Oqv $HOST:161 hrStorageUsed.$MEMORY_INDEX 2>/dev/null)
            MEM_UNITS=$(snmpget -v2c -c $COMMUNITY -Oqv $HOST:161 hrStorageAllocationUnits.$MEMORY_INDEX 2>/dev/null | grep -o '[0-9]*')
            
            if [ -n "$MEM_SIZE" ] && [ -n "$MEM_USED" ] && [ -n "$MEM_UNITS" ]; then
                MEM_TOTAL_KB=$((MEM_SIZE * MEM_UNITS / 1024))
                MEM_USED_KB=$((MEM_USED * MEM_UNITS / 1024))
                MEM_UTIL=$((MEM_USED * 100 / MEM_SIZE))
                
                echo "Total: $MEM_TOTAL_KB KB"
                echo "Usado: $MEM_USED_KB KB"
                echo "Utilização: $MEM_UTIL%"
            fi
        fi
    else
        echo "Informações de memória não disponíveis"
    fi
    echo ""
    
    # 4. Armazenamento
    echo "💿 ARMAZENAMENTO"
    echo "────────────────────────────────────────"
    snmpwalk -v2c -c $COMMUNITY $HOST:161 hrStorageDescr 2>/dev/null | while read line; do
        DESC=$(echo "$line" | cut -d':' -f2- | xargs)
        INDEX=$(echo "$line" | cut -d'.' -f2 | cut -d' ' -f1)
        
        # Filtrar apenas discos e partições relevantes
        if echo "$DESC" | grep -qiE "^/|Physical|disk"; then
            SIZE=$(snmpget -v2c -c $COMMUNITY -Oqv $HOST:161 hrStorageSize.$INDEX 2>/dev/null)
            USED=$(snmpget -v2c -c $COMMUNITY -Oqv $HOST:161 hrStorageUsed.$INDEX 2>/dev/null)
            
            if [ -n "$SIZE" ] && [ -n "$USED" ] && [ "$SIZE" != "0" ]; then
                UTIL=$((USED * 100 / SIZE))
                echo "  $DESC: ${USED}/${SIZE} blocos (${UTIL}%)"
            fi
        fi
    done
    echo ""
    
    # 5. Interfaces de Rede
    echo "🌐 INTERFACES DE REDE"
    echo "────────────────────────────────────────"
    snmpwalk -v2c -c $COMMUNITY $HOST:161 ifDescr 2>/dev/null | while read line; do
        IF_NAME=$(echo "$line" | cut -d':' -f2- | xargs)
        IF_INDEX=$(echo "$line" | cut -d'.' -f2 | cut -d' ' -f1)
        
        IF_STATUS=$(snmpget -v2c -c $COMMUNITY -Oqv $HOST:161 ifOperStatus.$IF_INDEX 2>/dev/null)
        IF_IN=$(snmpget -v2c -c $COMMUNITY -Oqv $HOST:161 ifInOctets.$IF_INDEX 2>/dev/null)
        IF_OUT=$(snmpget -v2c -c $COMMUNITY -Oqv $HOST:161 ifOutOctets.$IF_INDEX 2>/dev/null)
        
        # Converter bytes para formato legível
        if [ -n "$IF_IN" ] && [ -n "$IF_OUT" ]; then
            IN_MB=$((IF_IN / 1024 / 1024))
            OUT_MB=$((IF_OUT / 1024 / 1024))
            echo "  $IF_NAME: Status=$IF_STATUS | In=${IN_MB}MB | Out=${OUT_MB}MB"
        fi
    done
    echo ""
    
done

echo "=========================================="
echo "✅ Coleta concluída!"
echo "=========================================="
