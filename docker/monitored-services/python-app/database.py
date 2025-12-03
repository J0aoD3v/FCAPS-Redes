#!/usr/bin/env python3
"""
DATABASE LAYER - Responsável por operações de banco de dados
"""

import sqlite3
from datetime import datetime

DB_PATH = '/app/data/fcaps.db'

def init_db():
    """Inicializa as tabelas do banco de dados"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            metric_name TEXT NOT NULL,
            metric_value REAL NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS access_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            ip_address TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            ip_address TEXT,
            status TEXT DEFAULT 'active',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Database initialized")

def get_connection():
    """Retorna conexão com o banco de dados"""
    return sqlite3.connect(DB_PATH)

class DeviceRepository:
    """Repository Pattern - Gerencia operações CRUD de devices"""
    
    @staticmethod
    def find_all():
        """Busca todos os devices"""
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM devices ORDER BY created_at DESC')
        devices = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return devices
    
    @staticmethod
    def find_by_id(device_id):
        """Busca device por ID"""
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
        device = cursor.fetchone()
        conn.close()
        return dict(device) if device else None
    
    @staticmethod
    def create(name, device_type, ip_address='', status='active'):
        """Cria novo device"""
        conn = get_connection()
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO devices (name, type, ip_address, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, device_type, ip_address, status, now, now))
        
        device_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return device_id
    
    @staticmethod
    def update(device_id, **kwargs):
        """Atualiza device"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar existência
        cursor.execute('SELECT id FROM devices WHERE id = ?', (device_id,))
        if not cursor.fetchone():
            conn.close()
            return False
        
        # Construir query dinâmica
        fields = []
        values = []
        
        for key in ['name', 'type', 'ip_address', 'status']:
            if key in kwargs:
                fields.append(f'{key} = ?')
                values.append(kwargs[key])
        
        fields.append('updated_at = ?')
        values.append(datetime.now().isoformat())
        values.append(device_id)
        
        query = f"UPDATE devices SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def delete(device_id):
        """Remove device"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM devices WHERE id = ?', (device_id,))
        if not cursor.fetchone():
            conn.close()
            return False
        
        cursor.execute('DELETE FROM devices WHERE id = ?', (device_id,))
        conn.commit()
        conn.close()
        return True

class MetricsRepository:
    """Repository Pattern - Gerencia métricas"""
    
    @staticmethod
    def save(metric_name, metric_value):
        """Salva métrica no banco"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO metrics (timestamp, metric_name, metric_value) VALUES (?, ?, ?)',
                (datetime.now().isoformat(), metric_name, metric_value)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao salvar métrica: {e}")
    
    @staticmethod
    def count():
        """Conta total de métricas"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM metrics')
        count = cursor.fetchone()[0]
        conn.close()
        return count

class AccessLogRepository:
    """Repository Pattern - Gerencia logs de acesso"""
    
    @staticmethod
    def log(endpoint, ip='127.0.0.1'):
        """Registra acesso ao endpoint"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO access_log (timestamp, endpoint, ip_address) VALUES (?, ?, ?)',
                (datetime.now().isoformat(), endpoint, ip)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao registrar acesso: {e}")
    
    @staticmethod
    def count():
        """Conta total de acessos"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM access_log')
        count = cursor.fetchone()[0]
        conn.close()
        return count
