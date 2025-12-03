#!/usr/bin/env python3
"""
ROUTES - Definição de rotas da aplicação
"""

from controllers import HealthController, MetricsController, DeviceController

def register_routes(app):
    """Registra todas as rotas da aplicação"""
    
    # ==================== HEALTH & MONITORING ====================
    app.add_url_rule('/health', 'health', HealthController.health, methods=['GET'])
    app.add_url_rule('/metrics', 'metrics', MetricsController.get_metrics, methods=['GET'])
    app.add_url_rule('/stats', 'stats', MetricsController.get_stats, methods=['GET'])
    
    # ==================== DEVICES CRUD API ====================
    app.add_url_rule('/api/devices', 'list_devices', DeviceController.list_devices, methods=['GET'])
    app.add_url_rule('/api/devices/<int:device_id>', 'get_device', DeviceController.get_device, methods=['GET'])
    app.add_url_rule('/api/devices', 'create_device', DeviceController.create_device, methods=['POST'])
    app.add_url_rule('/api/devices/<int:device_id>', 'update_device', DeviceController.update_device, methods=['PUT'])
    app.add_url_rule('/api/devices/<int:device_id>', 'delete_device', DeviceController.delete_device, methods=['DELETE'])
    
    print("✓ Routes registered")
