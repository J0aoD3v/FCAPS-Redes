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
        print(f"[LOG] Requisição recebida: {self.path}")
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        params = parse_qs(parsed_path.query)

        # Servir index.html na raiz
        if path == '/' or path == '/index.html':
            try:
                index_paths = ['/data/index.html', '/app/index.html', '/tmp/index.html']
                content = None
                for index_path in index_paths:
                    try:
                        with open(index_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            content = content.replace(
                                'let SNMP_API_URL = "http://localhost:8090/api"',
                                'let SNMP_API_URL = window.location.origin + "/api"'
                            )
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
                print(f"[ERRO] Falha ao servir index.html: {e}")
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f'Dashboard not found: {e}'.encode())
            return

        # Documentação Swagger/OpenAPI
        if path == '/api/docs':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            openapi = self.get_openapi_spec()
            self.wfile.write(json.dumps(openapi, ensure_ascii=False, indent=2).encode())
            return

        # Exportação CSV
        if path == '/api/export':
            try:
                host = params.get('host', [None])[0]
                metric = params.get('metric', [None])[0]
                time_range = params.get('range', ['1h'])[0]
                csv_data = self.export_csv(host, metric, time_range)
                self.send_response(200)
                self.send_header('Content-type', 'text/csv; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(csv_data.encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
            return

        # API endpoints
        if path.startswith('/api/hosts/add') or path.startswith('/api/hosts/remove'):
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode() if length > 0 else ''
            try:
                data = json.loads(body) if body else {}
            except:
                data = {}

        # Definir status padrão
        status_code = 200
        response = None

        try:
            if path == '/api/hosts':
                response = self.get_hosts_list()
            elif path == '/api/hosts/add':
                response = self.add_host(data)
            elif path == '/api/hosts/remove':
                response = self.remove_host(data)
            elif path == '/api/latest':
                # Filtros: host, ordenação, limite, offset
                host = params.get('host', [None])[0]
                order = params.get('order', ['host'])[0]
                limit = int(params.get('limit', [100])[0])
                offset = int(params.get('offset', [0])[0])
                response = self.get_latest(host, order, limit, offset)
                if not response['hosts']:
                    status_code = 404
            elif path == '/api/history':
                host = params.get('host', [None])[0]
                time_range = params.get('range', ['1h'])[0]
                metric = params.get('metric', ['cpu'])[0]
                limit = int(params.get('limit', [1000])[0])
                offset = int(params.get('offset', [0])[0])
                response = self.get_history(host, time_range, metric, limit, offset)
                if not response['data']:
                    status_code = 404
            else:
                status_code = 404
                response = {'error': 'Unknown endpoint'}

            self.send_response(status_code)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
        except Exception as e:
            print(f"[ERRO] Exceção na requisição {self.path}: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {'error': str(e)}
            self.wfile.write(json.dumps(error_response).encode())
    
    def get_hosts(self, host=None, order='host', limit=100, offset=0):
        """Retorna lista de hosts monitorados (todas métricas, filtrável)"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('PRAGMA table_info(last_metrics)')
        columns = [col[1] for col in cursor.fetchall()]
        select_fields = ', '.join(columns)
        query = f'SELECT {select_fields} FROM last_metrics'
        params = []
        if host:
            query += ' WHERE host = ?'
            params.append(host)
        query += f' ORDER BY {order} LIMIT ? OFFSET ?'
        params.extend([limit, offset])
        cursor.execute(query, params)
        hosts = []
        for row in cursor.fetchall():
            host_data = {col: row[idx] for idx, col in enumerate(columns)}
            # Campos amigáveis
            host_data = self.friendly_fields(host_data)
            hosts.append(host_data)
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
    
    def get_latest(self, host=None, order='host', limit=100, offset=0):
        """Retorna últimas métricas de todos os hosts, filtrável"""
        return self.get_hosts(host, order, limit, offset)
    
    def get_history(self, host, time_range, metric, limit=1000, offset=0):
        """Retorna histórico de métricas detalhado, filtrável e paginado"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        time_map = {
            '5m': 300, '15m': 900, '30m': 1800, '1h': 3600,
            '3h': 10800, '6h': 21600, '12h': 43200, '24h': 86400,
            '2d': 172800, '7d': 604800, '30d': 2592000
        }
        seconds = time_map.get(time_range, 3600)
        start_time = int(time.time()) - seconds
        query = f'SELECT timestamp, host, {metric} FROM metrics WHERE timestamp >= ?'
        params = [start_time]
        if host:
            query += ' AND host = ?'
            params.append(host)
        query += ' ORDER BY timestamp DESC LIMIT ? OFFSET ?'
        params.extend([limit, offset])
        cursor.execute(query, params)
        data = []
        for row in cursor.fetchall():
            data.append({
                'timestamp': row[0],
                'host': row[1],
                'value': row[2]
            })
        conn.close()
        return {'data': data, 'metric': metric, 'range': time_range}

    def friendly_fields(self, host_data):
        """Renomeia campos para nomes mais amigáveis e agrupa"""
        # Exemplo: agrupar status de interfaces
        return {
            'host': host_data.get('host'),
            'timestamp': host_data.get('timestamp'),
            'sysname': host_data.get('sysname'),
            'cpu_percent': host_data.get('cpu'),
            'memory_percent': host_data.get('memory'),
            'process_count': host_data.get('processes'),
            'uptime_seconds': host_data.get('uptime'),
            'interfaces': {
                'status': [host_data.get(f'ifOperStatus{i}') for i in range(1, 4)],
                'in_errors': [host_data.get(f'ifInErrors{i}') for i in range(1, 4)],
                'out_errors': [host_data.get(f'ifOutErrors{i}') for i in range(1, 4)]
            },
            'snmp_errors': {k: host_data.get(k) for k in [
                'linkDown', 'snmpInBadVersions', 'snmpInBadCommunityNames', 'snmpInBadCommunityUses',
                'snmpInASNParseErrs', 'snmpInGenErrs', 'snmpInReadOnlys', 'snmpOutTooBigs',
                'snmpOutNoSuchNames', 'snmpOutBadValues', 'snmpOutGenErrs', 'snmpInTotalReqVars',
                'snmpInTotalSetVars', 'snmpInGetRequests', 'snmpInGetNexts', 'snmpInSetRequests',
                'snmpOutGetResponses', 'snmpOutTraps']}
        }

    def export_csv(self, host=None, metric=None, time_range='1h'):
        """Exporta dados filtrados em CSV"""
        import csv
        import io
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        time_map = {
            '5m': 300, '15m': 900, '30m': 1800, '1h': 3600,
            '3h': 10800, '6h': 21600, '12h': 43200, '24h': 86400,
            '2d': 172800, '7d': 604800, '30d': 2592000
        }
        seconds = time_map.get(time_range, 3600)
        start_time = int(time.time()) - seconds
        fields = ['timestamp', 'host']
        if metric:
            fields.append(metric)
        else:
            cursor.execute('PRAGMA table_info(metrics)')
            fields += [col[1] for col in cursor.fetchall() if col[1] not in fields]
        query = f'SELECT {", ".join(fields)} FROM metrics WHERE timestamp >= ?'
        params = [start_time]
        if host:
            query += ' AND host = ?'
            params.append(host)
        query += ' ORDER BY timestamp DESC LIMIT 10000'
        cursor.execute(query, params)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(fields)
        for row in cursor.fetchall():
            writer.writerow(row)
        conn.close()
        return output.getvalue()

    def get_openapi_spec(self):
        """Retorna especificação OpenAPI simplificada"""
        return {
            "openapi": "3.0.0",
            "info": {
                "title": "FCAPS SNMP API",
                "version": "1.0.0",
                "description": "API REST para métricas SNMP do dashboard FCAPS"
            },
            "paths": {
                "/api/latest": {
                    "get": {
                        "summary": "Últimas métricas de todos os hosts",
                        "parameters": [
                            {"name": "host", "in": "query", "schema": {"type": "string"}},
                            {"name": "order", "in": "query", "schema": {"type": "string"}},
                            {"name": "limit", "in": "query", "schema": {"type": "integer"}},
                            {"name": "offset", "in": "query", "schema": {"type": "integer"}}
                        ],
                        "responses": {"200": {"description": "OK"}, "404": {"description": "Não encontrado"}}
                    }
                },
                "/api/history": {
                    "get": {
                        "summary": "Histórico detalhado de métricas",
                        "parameters": [
                            {"name": "host", "in": "query", "schema": {"type": "string"}},
                            {"name": "range", "in": "query", "schema": {"type": "string"}},
                            {"name": "metric", "in": "query", "schema": {"type": "string"}},
                            {"name": "limit", "in": "query", "schema": {"type": "integer"}},
                            {"name": "offset", "in": "query", "schema": {"type": "integer"}}
                        ],
                        "responses": {"200": {"description": "OK"}, "404": {"description": "Não encontrado"}}
                    }
                },
                "/api/export": {
                    "get": {
                        "summary": "Exporta dados em CSV",
                        "parameters": [
                            {"name": "host", "in": "query", "schema": {"type": "string"}},
                            {"name": "metric", "in": "query", "schema": {"type": "string"}},
                            {"name": "range", "in": "query", "schema": {"type": "string"}}
                        ],
                        "responses": {"200": {"description": "CSV gerado"}, "500": {"description": "Erro"}}
                    }
                },
                "/api/hosts": {
                    "get": {"summary": "Lista hosts monitorados", "responses": {"200": {"description": "OK"}}}
                },
                "/api/hosts/add": {
                    "post": {"summary": "Adiciona host", "responses": {"200": {"description": "OK"}}}
                },
                "/api/hosts/remove": {
                    "post": {"summary": "Remove host", "responses": {"200": {"description": "OK"}}}
                }
            }
        }
    
    def log_message(self, format, *args):
        """Suprimir logs HTTP padrão"""
        pass

def main():
    print(f"[LOG] Iniciando API Server em http://0.0.0.0:{PORT}")
    print("[LOG] Endpoints disponíveis:")
    print(f"  GET /api/hosts - Lista de hosts e últimas métricas")
    print(f"  GET /api/latest - Mesma coisa que /api/hosts")
    print(f"  GET /api/history?host=X&range=1h&metric=cpu - Histórico")
    server = HTTPServer(('0.0.0.0', PORT), APIHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
