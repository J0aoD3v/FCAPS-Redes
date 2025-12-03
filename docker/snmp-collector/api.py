#!/usr/bin/env python3
"""
API REST para servir dados SNMP do SQLite para o dashboard
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
import time
from urllib.parse import urlparse, parse_qs
import os

DB_PATH = '/data/snmp_metrics.db'
HOSTS_FILE = '/data/hosts.json'
PORT = 8090

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        params = parse_qs(parsed_path.query)
        
        # Servir index.html na raiz (busca do volume compartilhado)
        if path == '/' or path == '/index.html':
            try:
                # Tentar buscar do volume compartilhado ou local
                index_paths = ['/data/index.html', '/app/index.html', '/tmp/index.html']
                content = None
                
                for index_path in index_paths:
                    try:
                        with open(index_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Substituir URL da API para usar API relativa
                            content = content.replace(
                                'let SNMP_API_URL = "http://localhost:8090/api"',
                                'let SNMP_API_URL = window.location.origin + "/api"'
                            )
                            # Ocultar seletor de fonte quando servido pelo servidor
                            content = content.replace(
                                'const saved = localStorage.getItem("fcaps_data_source");',
                                'document.getElementById("dataSourceSelector").style.display = "none"; return; const saved = localStorage.getItem("fcaps_data_source");'
                            )
                            break
                    except:
                        continue
                
                if content:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(content.encode('utf-8'))
                else:
                    raise FileNotFoundError("index.html not found in any location")
            except Exception as e:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f'Dashboard not found: {e}'.encode())
            return
        
        # API endpoints
        if path.startswith('/api/hosts/add') or path.startswith('/api/hosts/remove'):
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode() if length > 0 else ''
            try:
                data = json.loads(body) if body else {}
            except:
                data = {}
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        try:
            if path == '/api/hosts':
                response = self.get_hosts_list()
            elif path == '/api/hosts/add':
                response = self.add_host(data)
            elif path == '/api/hosts/remove':
                response = self.remove_host(data)
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
        """Retorna lista de hosts monitorados (métricas)"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT host, cpu, memory, processes, uptime, sysname, timestamp, ifOperStatus, ifInErrors, ifOutErrors
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
                'timestamp': row[6],
                'ifOperStatus': row[7] if len(row) > 7 else None,
                'ifInErrors': row[8] if len(row) > 8 else None,
                'ifOutErrors': row[9] if len(row) > 9 else None
            })

        conn.close()
        return {'hosts': hosts}

    def get_hosts_list(self):
        """Retorna lista de hosts monitorados (configuração)"""
        if os.path.exists(HOSTS_FILE):
            try:
                with open(HOSTS_FILE, 'r', encoding='utf-8') as f:
                    hosts = json.load(f)
            except Exception as e:
                hosts = []
        else:
            hosts = []
        return {'hosts': hosts}

    def add_host(self, data):
        """Adiciona um host ao arquivo de configuração"""
        if not data or 'host' not in data:
            return {'error': 'Host inválido'}
        hosts = []
        if os.path.exists(HOSTS_FILE):
            try:
                with open(HOSTS_FILE, 'r', encoding='utf-8') as f:
                    hosts = json.load(f)
            except:
                hosts = []
        # Evitar duplicados
        for h in hosts:
            if h.get('host') == data['host']:
                return {'error': 'Host já existe'}
        hosts.append({
            'host': data['host'],
            'name': data.get('name', data['host']),
            'community': data.get('community', 'public')
        })
        try:
            with open(HOSTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(hosts, f, ensure_ascii=False, indent=2)
            return {'success': True, 'hosts': hosts}
        except Exception as e:
            return {'error': str(e)}

    def remove_host(self, data):
        """Remove um host do arquivo de configuração"""
        if not data or 'host' not in data:
            return {'error': 'Host inválido'}
        hosts = []
        if os.path.exists(HOSTS_FILE):
            try:
                with open(HOSTS_FILE, 'r', encoding='utf-8') as f:
                    hosts = json.load(f)
            except:
                hosts = []
        hosts = [h for h in hosts if h.get('host') != data['host']]
        try:
            with open(HOSTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(hosts, f, ensure_ascii=False, indent=2)
            return {'success': True, 'hosts': hosts}
        except Exception as e:
            return {'error': str(e)}
    
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
