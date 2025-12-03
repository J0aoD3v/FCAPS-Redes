#!/usr/bin/env python3
"""
CONTROLLER LAYER - Manipuladores de rotas HTTP
"""

from flask import jsonify, request
from datetime import datetime
from database import DeviceRepository, AccessLogRepository
from services import SystemMetricsService, DatabaseStatsService, DeviceService
import time

START_TIME = time.time()

class HealthController:
    """Controller - Endpoints de health check"""
    
    @staticmethod
    def health():
        AccessLogRepository.log('/health')
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': int(time.time() - START_TIME)
        })

class MetricsController:
    """Controller - Endpoints de métricas"""
    
    @staticmethod
    def get_metrics():
        AccessLogRepository.log('/metrics')
        return jsonify(SystemMetricsService.collect_and_save())
    
    @staticmethod
    def get_stats():
        AccessLogRepository.log('/stats')
        try:
            return jsonify(DatabaseStatsService.get_stats())
        except Exception as e:
            return jsonify({'error': str(e)}), 500

class DeviceController:
    """Controller - CRUD de devices"""
    
    @staticmethod
    def list_devices():
        """GET /api/devices - Lista todos"""
        AccessLogRepository.log('/api/devices')
        try:
            devices = DeviceRepository.find_all()
            return jsonify({
                'success': True,
                'count': len(devices),
                'devices': devices
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @staticmethod
    def get_device(device_id):
        """GET /api/devices/:id - Busca por ID"""
        AccessLogRepository.log(f'/api/devices/{device_id}')
        try:
            device = DeviceRepository.find_by_id(device_id)
            if device:
                return jsonify({'success': True, 'device': device})
            else:
                return jsonify({'success': False, 'error': 'Device não encontrado'}), 404
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @staticmethod
    def create_device():
        """POST /api/devices - Cria novo"""
        AccessLogRepository.log('/api/devices')
        try:
            data = request.get_json()
            
            # Validação
            is_valid, error_msg = DeviceService.validate_device_data(data)
            if not is_valid:
                return jsonify({'success': False, 'error': error_msg}), 400
            
            # Criar
            device_id = DeviceRepository.create(
                name=data['name'],
                device_type=data['type'],
                ip_address=data.get('ip_address', ''),
                status=data.get('status', 'active')
            )
            
            return jsonify({
                'success': True,
                'message': 'Device criado com sucesso',
                'device_id': device_id
            }), 201
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @staticmethod
    def update_device(device_id):
        """PUT /api/devices/:id - Atualiza"""
        AccessLogRepository.log(f'/api/devices/{device_id}')
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({'success': False, 'error': 'Nenhum dado fornecido'}), 400
            
            # Atualizar
            success = DeviceRepository.update(device_id, **data)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Device atualizado com sucesso'
                })
            else:
                return jsonify({'success': False, 'error': 'Device não encontrado'}), 404
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @staticmethod
    def delete_device(device_id):
        """DELETE /api/devices/:id - Remove"""
        AccessLogRepository.log(f'/api/devices/{device_id}')
        try:
            success = DeviceRepository.delete(device_id)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Device removido com sucesso'
                })
            else:
                return jsonify({'success': False, 'error': 'Device não encontrado'}), 404
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
