#!/usr/bin/env python3
"""
API REST para servir dados SNMP do SQLite para o dashboard
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
import time
from urllib.parse import urlparse, parse_qs

DB_PATH = '/data/snmp_metrics.db'
PORT = 8090

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        params = parse_qs(parsed_path.query)
        
        # Servir index.html na raiz
        if path == '/' or path == '/index.html':
            try:
                with open('/app/dashboard.html', 'r', encoding='utf-8') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except Exception as e:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f'Dashboard not found: {e}'.encode())
            return
        
        # API endpoints
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        try:
            if path == '/api/hosts':
                response = self.get_hosts()
            elif path == '/api/history':
                host = params.get('host', [None])[0]
                time_range = params.get('range', ['1h'])[0]
                metric = params.get('metric', ['cpu'])[0]
                response = self.get_history(host, time_range, metric)
            elif path == '/api/latest':
                response = self.get_latest()
            else:
                response = {'error': 'Unknown endpoint'}
                
            self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            error_response = {'error': str(e)}
            self.wfile.write(json.dumps(error_response).encode())
    
    def get_hosts(self):
        """Retorna lista de hosts monitorados"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT host, cpu, memory, processes, uptime, sysname, timestamp
            FROM last_metrics
            ORDER BY host
        ''')
        
        hosts = []
        for row in cursor.fetchall():
            hosts.append({
                'host': row[0],
                'cpu': row[1],
                'memory': row[2],
                'processes': row[3],
                'uptime': row[4],
                'sysname': row[5],
                'timestamp': row[6]
            })
        
        conn.close()
        return {'hosts': hosts}
    
    def get_latest(self):
        """Retorna últimas métricas de todos os hosts"""
        return self.get_hosts()
    
    def get_history(self, host, time_range, metric):
        """Retorna histórico de métricas"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Calcular timestamp inicial baseado no range
        time_map = {
            '5m': 300, '15m': 900, '30m': 1800, '1h': 3600,
            '3h': 10800, '6h': 21600, '12h': 43200, '24h': 86400,
            '2d': 172800, '7d': 604800, '30d': 2592000
        }
        seconds = time_map.get(time_range, 3600)
        start_time = int(time.time()) - seconds
        
        # Query baseada em host (se especificado) ou todos
        if host:
            cursor.execute(f'''
                SELECT timestamp, host, {metric}
                FROM metrics
                WHERE host = ? AND timestamp >= ?
                ORDER BY timestamp
            ''', (host, start_time))
        else:
            cursor.execute(f'''
                SELECT timestamp, host, {metric}
                FROM metrics
                WHERE timestamp >= ?
                ORDER BY timestamp
            ''', (start_time,))
        
        data = []
        for row in cursor.fetchall():
            data.append({
                'timestamp': row[0],
                'host': row[1],
                'value': row[2]
            })
        
        conn.close()
        return {'data': data, 'metric': metric, 'range': time_range}
    
    def log_message(self, format, *args):
        """Suprimir logs HTTP padrão"""
        pass

def main():
    server = HTTPServer(('0.0.0.0', PORT), APIHandler)
    print(f"API Server running on http://0.0.0.0:{PORT}")
    print("Endpoints:")
    print(f"  GET /api/hosts - Lista de hosts e últimas métricas")
    print(f"  GET /api/latest - Mesma coisa que /api/hosts")
    print(f"  GET /api/history?host=X&range=1h&metric=cpu - Histórico")
    server.serve_forever()

if __name__ == '__main__':
    main()
