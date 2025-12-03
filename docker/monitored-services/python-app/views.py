#!/usr/bin/env python3
"""
VIEWS - Templates HTML da aplicação
"""

def get_index_html():
    """Template da página inicial"""
    return '''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FCAPS - Python REST API</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 1000px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                color: #667eea;
                text-align: center;
                margin-bottom: 10px;
            }
            .subtitle {
                text-align: center;
                color: #6b7280;
                margin-bottom: 30px;
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
            .section {
                margin: 30px 0;
            }
            .section-title {
                font-size: 18px;
                font-weight: 600;
                color: #374151;
                margin-bottom: 15px;
                padding-bottom: 8px;
                border-bottom: 2px solid #e5e7eb;
            }
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }
            .metric-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                color: white;
            }
            .metric-value {
                font-size: 32px;
                font-weight: bold;
            }
            .metric-label {
                font-size: 13px;
                margin-top: 5px;
                opacity: 0.9;
            }
            .api-list {
                display: grid;
                gap: 10px;
            }
            .api-item {
                background: #f9fafb;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }
            .api-method {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
                margin-right: 10px;
            }
            .method-get { background: #10b981; color: white; }
            .method-post { background: #f59e0b; color: white; }
            .method-put { background: #3b82f6; color: white; }
            .method-delete { background: #ef4444; color: white; }
            .api-endpoint {
                font-family: 'Courier New', monospace;
                color: #374151;
                font-weight: 600;
            }
            .api-description {
                font-size: 13px;
                color: #6b7280;
                margin-top: 5px;
            }
            .architecture {
                background: #f3f4f6;
                padding: 20px;
                border-radius: 10px;
                font-size: 14px;
            }
            .architecture ul {
                margin-left: 20px;
                margin-top: 10px;
            }
            .architecture li {
                margin: 5px 0;
                color: #374151;
            }
            .test-section {
                background: #fef3c7;
                padding: 20px;
                border-radius: 10px;
                margin-top: 20px;
            }
            .btn {
                background: #667eea;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                cursor: pointer;
                font-weight: 600;
                margin: 5px;
                transition: all 0.3s;
            }
            .btn:hover {
                background: #5568d3;
                transform: translateY(-2px);
            }
            #testResult {
                margin-top: 15px;
                padding: 15px;
                background: white;
                border-radius: 6px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                max-height: 300px;
                overflow-y: auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 FCAPS Python REST API</h1>
            <p class="subtitle">Aplicação Flask com arquitetura MVC + SQLite</p>
            
            <div class="status">
                ✅ Aplicação operacional | Monitorado via SNMP
            </div>

            <!-- Métricas em tempo real -->
            <div class="section">
                <div class="section-title">📊 Métricas do Sistema</div>
                <div class="metrics-grid" id="metrics">
                    <div class="metric-card">
                        <div class="metric-value">-</div>
                        <div class="metric-label">Carregando...</div>
                    </div>
                </div>
            </div>

            <!-- Arquitetura -->
            <div class="section">
                <div class="section-title">🏗️ Arquitetura da Aplicação</div>
                <div class="architecture">
                    <strong>Padrão MVC + Repository Pattern:</strong>
                    <ul>
                        <li><strong>app.py</strong> - Entry point & configuração</li>
                        <li><strong>routes.py</strong> - Definição de rotas</li>
                        <li><strong>controllers.py</strong> - Manipuladores HTTP</li>
                        <li><strong>services.py</strong> - Lógica de negócio</li>
                        <li><strong>database.py</strong> - Acesso a dados (Repository Pattern)</li>
                        <li><strong>views.py</strong> - Templates HTML</li>
                    </ul>
                </div>
            </div>

            <!-- API Endpoints -->
            <div class="section">
                <div class="section-title">🔗 API Endpoints Disponíveis</div>
                
                <div class="api-list">
                    <div class="api-item">
                        <span class="api-method method-get">GET</span>
                        <span class="api-endpoint">/health</span>
                        <div class="api-description">Health check da aplicação</div>
                    </div>
                    
                    <div class="api-item">
                        <span class="api-method method-get">GET</span>
                        <span class="api-endpoint">/metrics</span>
                        <div class="api-description">Métricas do sistema (CPU, RAM, Uptime)</div>
                    </div>
                    
                    <div class="api-item">
                        <span class="api-method method-get">GET</span>
                        <span class="api-endpoint">/stats</span>
                        <div class="api-description">Estatísticas do banco de dados</div>
                    </div>
                    
                    <div class="api-item">
                        <span class="api-method method-get">GET</span>
                        <span class="api-endpoint">/api/devices</span>
                        <div class="api-description">Lista todos os devices cadastrados</div>
                    </div>
                    
                    <div class="api-item">
                        <span class="api-method method-get">GET</span>
                        <span class="api-endpoint">/api/devices/:id</span>
                        <div class="api-description">Busca device por ID</div>
                    </div>
                    
                    <div class="api-item">
                        <span class="api-method method-post">POST</span>
                        <span class="api-endpoint">/api/devices</span>
                        <div class="api-description">Cria novo device { name, type, ip_address, status }</div>
                    </div>
                    
                    <div class="api-item">
                        <span class="api-method method-put">PUT</span>
                        <span class="api-endpoint">/api/devices/:id</span>
                        <div class="api-description">Atualiza device existente</div>
                    </div>
                    
                    <div class="api-item">
                        <span class="api-method method-delete">DELETE</span>
                        <span class="api-endpoint">/api/devices/:id</span>
                        <div class="api-description">Remove device do banco</div>
                    </div>
                </div>
            </div>

            <!-- Teste da API -->
            <div class="section">
                <div class="test-section">
                    <div class="section-title">🧪 Testar API</div>
                    <button class="btn" onclick="testAPI('GET', '/health')">GET /health</button>
                    <button class="btn" onclick="testAPI('GET', '/metrics')">GET /metrics</button>
                    <button class="btn" onclick="testAPI('GET', '/stats')">GET /stats</button>
                    <button class="btn" onclick="testAPI('GET', '/api/devices')">GET /devices</button>
                    <button class="btn" onclick="testCRUD()">Teste CRUD Completo</button>
                    <div id="testResult"></div>
                </div>
            </div>
        </div>

        <script>
            // Atualizar métricas
            async function updateMetrics() {
                try {
                    const response = await fetch('/metrics');
                    const data = await response.json();
                    
                    document.getElementById('metrics').innerHTML = `
                        <div class="metric-card">
                            <div class="metric-value">${data.cpu_percent.toFixed(1)}%</div>
                            <div class="metric-label">CPU</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">${data.memory_percent.toFixed(1)}%</div>
                            <div class="metric-label">Memória</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">${data.memory_used_mb.toFixed(0)} MB</div>
                            <div class="metric-label">RAM Usada</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">${Math.floor(data.uptime_seconds / 60)}m</div>
                            <div class="metric-label">Uptime</div>
                        </div>
                    `;
                } catch (error) {
                    console.error('Erro:', error);
                }
            }

            // Testar endpoint
            async function testAPI(method, endpoint) {
                const resultDiv = document.getElementById('testResult');
                resultDiv.innerHTML = `<strong>${method} ${endpoint}</strong><br>Aguardando resposta...`;
                
                try {
                    const response = await fetch(endpoint);
                    const data = await response.json();
                    resultDiv.innerHTML = `<strong>${method} ${endpoint}</strong><br>Status: ${response.status}<br><pre>${JSON.stringify(data, null, 2)}</pre>`;
                } catch (error) {
                    resultDiv.innerHTML = `<strong>Erro:</strong> ${error.message}`;
                }
            }

            // Teste CRUD completo
            async function testCRUD() {
                const resultDiv = document.getElementById('testResult');
                resultDiv.innerHTML = '<strong>Executando teste CRUD completo...</strong><br><br>';
                
                try {
                    // CREATE
                    resultDiv.innerHTML += '1️⃣ POST /api/devices (CREATE)<br>';
                    const createRes = await fetch('/api/devices', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({name: 'Router-Teste', type: 'router', ip_address: '192.168.1.1'})
                    });
                    const createData = await createRes.json();
                    resultDiv.innerHTML += `Resultado: ${JSON.stringify(createData)}<br><br>`;
                    
                    const deviceId = createData.device_id;
                    
                    // READ
                    resultDiv.innerHTML += '2️⃣ GET /api/devices/:id (READ)<br>';
                    const readRes = await fetch(`/api/devices/${deviceId}`);
                    const readData = await readRes.json();
                    resultDiv.innerHTML += `Resultado: ${JSON.stringify(readData)}<br><br>`;
                    
                    // UPDATE
                    resultDiv.innerHTML += '3️⃣ PUT /api/devices/:id (UPDATE)<br>';
                    const updateRes = await fetch(`/api/devices/${deviceId}`, {
                        method: 'PUT',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({name: 'Router-Atualizado', status: 'inactive'})
                    });
                    const updateData = await updateRes.json();
                    resultDiv.innerHTML += `Resultado: ${JSON.stringify(updateData)}<br><br>`;
                    
                    // DELETE
                    resultDiv.innerHTML += '4️⃣ DELETE /api/devices/:id (DELETE)<br>';
                    const deleteRes = await fetch(`/api/devices/${deviceId}`, {method: 'DELETE'});
                    const deleteData = await deleteRes.json();
                    resultDiv.innerHTML += `Resultado: ${JSON.stringify(deleteData)}<br><br>`;
                    
                    resultDiv.innerHTML += '<strong style="color: green;">✅ Teste CRUD completo executado com sucesso!</strong>';
                } catch (error) {
                    resultDiv.innerHTML += `<br><strong style="color: red;">❌ Erro: ${error.message}</strong>`;
                }
            }

            // Iniciar
            updateMetrics();
            setInterval(updateMetrics, 5000);
        </script>
    </body>
    </html>
    '''
