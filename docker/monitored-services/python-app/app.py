#!/usr/bin/env python3
"""
FCAPS Python REST API - Entry Point
Arquitetura MVC + Repository Pattern
"""

from flask import Flask, render_template_string
from database import init_db, AccessLogRepository
from routes import register_routes
from views import get_index_html

# Configuração da aplicação
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

# Rota principal (VIEW)
@app.route('/')
def index():
    """Página inicial da aplicação"""
    AccessLogRepository.log('/')
    return render_template_string(get_index_html())

# Registrar todas as rotas da API
register_routes(app)

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 FCAPS Python REST API")
    print("=" * 60)
    print("📦 Arquitetura: MVC + Repository Pattern")
    print("🗄️  Banco de Dados: SQLite")
    print("🔧 Framework: Flask")
    print("📊 Monitoramento: SNMP v2c")
    print("=" * 60)
    print("\n🔧 Inicializando componentes...")
    
    # Inicializar banco de dados
    init_db()
    
    print("=" * 60)
    print("✅ Aplicação pronta!")
    print("🌐 Servidor rodando em: http://0.0.0.0:5000")
    print("📚 Documentação da API: http://localhost:5000")
    print("=" * 60)
    
    # Iniciar servidor
    app.run(host='0.0.0.0', port=5000, debug=False)
