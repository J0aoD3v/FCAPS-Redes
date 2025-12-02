#!/usr/bin/env python3
"""
SNMP Data Collector for FCAPS Dashboard
Coleta métricas SNMP dos containers e armazena em SQLite
"""

import time
import sqlite3
from datetime import datetime
from pysnmp.hlapi import *
import sys

# Configurações
DB_PATH = '/data/snmp_metrics.db'
HOSTS = [
    {'name': 'nginx-web', 'ip': 'nginx-web', 'community': 'public'},
    {'name': 'python-app', 'ip': 'python-app', 'community': 'public'},
    {'name': 'alpine-host', 'ip': 'alpine-host', 'community': 'public'}
]

# OIDs SNMP
OIDS = {
    'cpu': '1.3.6.1.2.1.25.3.3.1.2.1',           # hrProcessorLoad
    'memory_size': '1.3.6.1.2.1.25.2.3.1.5.1',  # hrStorageSize
    'memory_used': '1.3.6.1.2.1.25.2.3.1.6.1',  # hrStorageUsed
    'processes': '1.3.6.1.2.1.25.1.6.0',        # hrSystemProcesses
    'uptime': '1.3.6.1.2.1.1.3.0',              # sysUpTime
    'sysname': '1.3.6.1.2.1.1.5.0',             # sysName
}

def init_db():
    """Inicializa o banco de dados SQLite"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabela para métricas históricas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER NOT NULL,
            host TEXT NOT NULL,
            cpu REAL,
            memory REAL,
            processes INTEGER,
            uptime INTEGER,
            INDEX idx_host_time (host, timestamp)
        )
    ''')
    
    # Tabela para última coleta (cache)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS last_metrics (
            host TEXT PRIMARY KEY,
            timestamp INTEGER,
            cpu REAL,
            memory REAL,
            processes INTEGER,
            uptime INTEGER,
            sysname TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✓ Database initialized at {DB_PATH}")

def snmp_get(host, oid):
    """Executa SNMP GET"""
    try:
        iterator = getCmd(
            SnmpEngine(),
            CommunityData(host['community']),
            UdpTransportTarget((host['ip'], 161), timeout=2, retries=1),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )
        
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
        
        if errorIndication or errorStatus:
            return None
            
        for varBind in varBinds:
            return varBind[1]
    except Exception as e:
        return None

def collect_metrics(host):
    """Coleta métricas de um host via SNMP"""
    print(f"  Collecting from {host['name']}...", end=' ')
    
    metrics = {}
    
    # CPU
    cpu_raw = snmp_get(host, OIDS['cpu'])
    metrics['cpu'] = float(cpu_raw) if cpu_raw else 0
    
    # Memory
    mem_size = snmp_get(host, OIDS['memory_size'])
    mem_used = snmp_get(host, OIDS['memory_used'])
    if mem_size and mem_used and int(mem_size) > 0:
        metrics['memory'] = (int(mem_used) / int(mem_size)) * 100
    else:
        metrics['memory'] = 0
    
    # Processes
    processes = snmp_get(host, OIDS['processes'])
    metrics['processes'] = int(processes) if processes else 0
    
    # Uptime
    uptime = snmp_get(host, OIDS['uptime'])
    metrics['uptime'] = int(uptime) if uptime else 0
    
    # Sysname
    sysname = snmp_get(host, OIDS['sysname'])
    metrics['sysname'] = str(sysname) if sysname else host['name']
    
    print(f"CPU={metrics['cpu']:.1f}% MEM={metrics['memory']:.1f}%")
    return metrics

def store_metrics(host_name, metrics):
    """Armazena métricas no banco de dados"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = int(time.time())
    
    # Inserir no histórico
    cursor.execute('''
        INSERT INTO metrics (timestamp, host, cpu, memory, processes, uptime)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, host_name, metrics['cpu'], metrics['memory'], 
          metrics['processes'], metrics['uptime']))
    
    # Atualizar cache (última métrica)
    cursor.execute('''
        INSERT OR REPLACE INTO last_metrics 
        (host, timestamp, cpu, memory, processes, uptime, sysname)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (host_name, timestamp, metrics['cpu'], metrics['memory'],
          metrics['processes'], metrics['uptime'], metrics['sysname']))
    
    conn.commit()
    conn.close()

def cleanup_old_data():
    """Remove dados com mais de 7 dias"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    week_ago = int(time.time()) - (7 * 24 * 3600)
    cursor.execute('DELETE FROM metrics WHERE timestamp < ?', (week_ago,))
    deleted = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    if deleted > 0:
        print(f"  Cleaned up {deleted} old records")

def main():
    """Loop principal de coleta"""
    print("=" * 50)
    print("  FCAPS SNMP Collector Starting")
    print("=" * 50)
    
    init_db()
    
    # Modo contínuo ou single run
    continuous = '--daemon' in sys.argv
    interval = 60  # 1 minuto entre coletas
    
    iteration = 0
    while True:
        iteration += 1
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Collection #{iteration}")
        
        for host in HOSTS:
            try:
                metrics = collect_metrics(host)
                store_metrics(host['name'], metrics)
            except Exception as e:
                print(f"  ERROR collecting {host['name']}: {e}")
        
        # Limpeza periódica (a cada 60 coletas = ~1 hora)
        if iteration % 60 == 0:
            cleanup_old_data()
        
        if not continuous:
            print("\nCollection completed (single run mode)")
            break
        
        print(f"  Next collection in {interval}s...")
        time.sleep(interval)

if __name__ == '__main__':
    main()
