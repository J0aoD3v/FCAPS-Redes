#!/usr/bin/env python3
"""
Aplicação Flask com SQLite para monitoramento FCAPS
Objeto de Monitoramento #2: Aplicação Python
"""

from flask import Flask, jsonify, render_template_string
import sqlite3
import os
import time
import psutil
from datetime import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Configuração do banco de dados SQLite
DB_PATH = '/app/data/fcaps.db'
START_TIME = time.time()

def init_db():
    """Inicializa o banco de dados SQLite"""
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
    
    conn.commit()
    conn.close()

def log_access(endpoint, ip='127.0.0.1'):
    """Registra acesso ao endpoint"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO access_log (timestamp, endpoint, ip_address) VALUES (?, ?, ?)',
            (datetime.now().isoformat(), endpoint, ip)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao registrar acesso: {e}")

def save_metric(metric_name, metric_value):
    """Salva métrica no banco de dados"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO metrics (timestamp, metric_name, metric_value) VALUES (?, ?, ?)',
            (datetime.now().isoformat(), metric_name, metric_value)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao salvar métrica: {e}")

def get_system_metrics():
    """Coleta métricas do sistema"""
    return {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'memory_used_mb': psutil.virtual_memory().used / (1024 * 1024),
        'disk_usage_percent': psutil.disk_usage('/').percent,
        'uptime_seconds': int(time.time() - START_TIME)
    }

@app.route('/')
def index():
    """Página inicial"""
    log_access('/')
    
    html = '''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FCAPS - Aplicação Python</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                color: #f5576c;
                text-align: center;
                margin-bottom: 20px;
            }
            .status {
                background: #10b981;
                color: white;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                margin: 20px 0;
                font-weight: bold;
            }
            .info {
                background: #f3f4f6;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
            }
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }
            .metric-card {
                background: #fef3c7;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }
            .metric-value {
                font-size: 28px;
                font-weight: bold;
                color: #f59e0b;
            }
            .metric-label {
                font-size: 12px;
                color: #78716c;
                margin-top: 5px;
            }
            .endpoints {
                background: #e0f2fe;
                padding: 20px;
                border-radius: 10px;
                margin-top: 20px;
            }
            .endpoint-link {
                display: block;
                background: white;
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
                text-decoration: none;
                color: #0284c7;
                font-weight: bold;
                transition: all 0.3s;
            }
            .endpoint-link:hover {
                background: #0284c7;
                color: white;
                transform: translateX(5px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🐍 Aplicação Python + SQLite</h1>
            <div class="status">
                ✅ Aplicação Flask Operacional
            </div>
            
            <div class="info">
                <h2>📊 Objeto de Monitoramento #2</h2>
                <p><strong>Tipo:</strong> Aplicação Web + Banco de Dados</p>
                <p><strong>Tecnologia:</strong> Python Flask + SQLite</p>
                <p><strong>Porta:</strong> 5000</p>
                <p><strong>Monitorado por:</strong> Zabbix Agent 2</p>
            </div>

            <div class="metrics-grid" id="metrics">
                <div class="metric-card">
                    <div class="metric-value">Carregando...</div>
                    <div class="metric-label">CPU</div>
                </div>
            </div>

            <div class="endpoints">
                <h3>🔗 Endpoints Disponíveis</h3>
                <a href="/health" class="endpoint-link">/health - Healthcheck</a>
                <a href="/metrics" class="endpoint-link">/metrics - Métricas JSON</a>
                <a href="/stats" class="endpoint-link">/stats - Estatísticas do DB</a>
                <a href="/api/test" class="endpoint-link">/api/test - Teste de API</a>
            </div>

            <div class="info">
                <h3>🔍 Métricas Monitoradas</h3>
                <p>• CPU e Memória da aplicação</p>
                <p>• Tempo de resposta de queries</p>
                <p>• Tamanho do banco SQLite</p>
                <p>• Operações de I/O</p>
                <p>• Status HTTP da aplicação</p>
            </div>
        </div>

        <script>
            async function updateMetrics() {
                try {
                    const response = await fetch('/metrics');
                    const data = await response.json();
                    
                    const metricsDiv = document.getElementById('metrics');
                    metricsDiv.innerHTML = `
                        <div class="metric-card">
                            <div class="metric-value">${data.cpu_percent.toFixed(1)}%</div>
                            <div class="metric-label">CPU</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">${data.memory_percent.toFixed(1)}%</div>
                            <div class="metric-label">Memória</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">${data.memory_used_mb.toFixed(0)}MB</div>
                            <div class="metric-label">RAM Usada</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">${Math.floor(data.uptime_seconds / 60)}m</div>
                            <div class="metric-label">Uptime</div>
                        </div>
                    `;
                } catch (error) {
                    console.error('Erro ao carregar métricas:', error);
                }
            }

            updateMetrics();
            setInterval(updateMetrics, 5000);
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/health')
def health():
    """Endpoint de healthcheck"""
    log_access('/health')
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'uptime_seconds': int(time.time() - START_TIME)
    })

@app.route('/metrics')
def metrics():
    """Retorna métricas do sistema"""
    log_access('/metrics')
    metrics_data = get_system_metrics()
    
    # Salva métricas no banco
    for key, value in metrics_data.items():
        save_metric(key, value)
    
    return jsonify(metrics_data)

@app.route('/stats')
def stats():
    """Estatísticas do banco de dados"""
    log_access('/stats')
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM metrics')
        metrics_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM access_log')
        access_count = cursor.fetchone()[0]
        
        # Tamanho do arquivo do banco
        db_size = os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0
        
        conn.close()
        
        return jsonify({
            'database_size_bytes': db_size,
            'database_size_kb': round(db_size / 1024, 2),
            'total_metrics': metrics_count,
            'total_accesses': access_count,
            'database_path': DB_PATH
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test')
def api_test():
    """Endpoint de teste da API"""
    log_access('/api/test')
    
    return jsonify({
        'message': 'API funcionando corretamente!',
        'timestamp': datetime.now().isoformat(),
        'python_version': '3.11',
        'framework': 'Flask',
        'database': 'SQLite'
    })

if __name__ == '__main__':
    # Inicializa o banco de dados
    init_db()
    print("=" * 50)
    print("🐍 Aplicação Python Flask + SQLite")
    print("📊 Objeto de Monitoramento FCAPS")
    print("🚀 Servidor iniciado na porta 5000")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
