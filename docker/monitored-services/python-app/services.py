#!/usr/bin/env python3
"""
SERVICE LAYER - Lógica de negócio da aplicação
"""

import psutil
import time
import os
from database import MetricsRepository

START_TIME = time.time()
DB_PATH = '/app/data/fcaps.db'

class SystemMetricsService:
    """Service - Coleta métricas do sistema"""
    
    @staticmethod
    def get_metrics():
        """Retorna métricas atuais do sistema"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'memory_used_mb': round(psutil.virtual_memory().used / (1024 * 1024), 2),
            'disk_usage_percent': psutil.disk_usage('/').percent,
            'uptime_seconds': int(time.time() - START_TIME)
        }
    
    @staticmethod
    def collect_and_save():
        """Coleta métricas e salva no banco"""
        metrics = SystemMetricsService.get_metrics()
        for key, value in metrics.items():
            MetricsRepository.save(key, value)
        return metrics

class DatabaseStatsService:
    """Service - Estatísticas do banco de dados"""
    
    @staticmethod
    def get_stats():
        """Retorna estatísticas do banco"""
        db_size = os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0
        
        return {
            'database_size_bytes': db_size,
            'database_size_kb': round(db_size / 1024, 2),
            'database_size_mb': round(db_size / (1024 * 1024), 2),
            'total_metrics': MetricsRepository.count(),
            'total_accesses': 0,  # AccessLogRepository.count() pode ser adicionado
            'database_path': DB_PATH
        }

class DeviceService:
    """Service - Lógica de negócio para devices"""
    
    @staticmethod
    def validate_device_data(data):
        """Valida dados de device"""
        if not data:
            return False, "Nenhum dado fornecido"
        
        if 'name' not in data or not data['name']:
            return False, "Campo 'name' é obrigatório"
        
        if 'type' not in data or not data['type']:
            return False, "Campo 'type' é obrigatório"
        
        # Validar tipos permitidos
        allowed_types = ['router', 'switch', 'server', 'workstation', 'firewall', 'other']
        if data['type'] not in allowed_types:
            return False, f"Tipo inválido. Tipos permitidos: {', '.join(allowed_types)}"
        
        return True, None
