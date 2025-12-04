# FCAPS SNMP API - Documentação

## Endpoints principais

### 1. `/api/latest`
- **GET**
- Retorna as últimas métricas de todos os hosts monitorados.
- Parâmetros opcionais:
  - `host`: filtra por nome do host
  - `order`: campo para ordenação (ex: `host`, `timestamp`)
  - `limit`: máximo de registros
  - `offset`: deslocamento para paginação
- Exemplo:
  ```http
  GET /api/latest?host=oracle-cloud&order=timestamp&limit=10
  ```
- Resposta:
  ```json
  {
    "hosts": [
      {
        "host": "oracle-cloud",
        "timestamp": 1700000000,
        "sysname": "oracle-cloud",
        "cpu_percent": 15.2,
        "memory_percent": 35.1,
        "process_count": 30,
        "uptime_seconds": 123456,
        "interfaces": { ... },
        "snmp_errors": { ... }
      }
    ]
  }
  ```

### 2. `/api/history`
- **GET**
- Retorna histórico detalhado de uma métrica.
- Parâmetros:
  - `host`: filtra por host
  - `range`: intervalo de tempo (ex: `1h`, `24h`, `7d`)
  - `metric`: nome da métrica (ex: `cpu`, `memory`)
  - `limit`, `offset`: paginação
- Exemplo:
  ```http
  GET /api/history?host=oracle-cloud&range=24h&metric=cpu&limit=100
  ```
- Resposta:
  ```json
  {
    "data": [
      {"timestamp": 1700000000, "host": "oracle-cloud", "value": 15.2},
      ...
    ],
    "metric": "cpu",
    "range": "24h"
  }
  ```

### 3. `/api/export`
- **GET**
- Exporta dados filtrados em CSV.
- Parâmetros:
  - `host`, `metric`, `range`
- Exemplo:
  ```http
  GET /api/export?host=oracle-cloud&metric=cpu&range=24h
  ```
- Resposta: arquivo CSV

### 4. `/api/hosts`
- **GET**
- Lista hosts monitorados (configuração).

### 5. `/api/hosts/add`
- **POST**
- Adiciona host ao monitoramento.
- Corpo JSON:
  ```json
  {"host": "novo-host", "name": "Nome Amigável", "community": "public"}
  ```

### 6. `/api/hosts/remove`
- **POST**
- Remove host do monitoramento.
- Corpo JSON:
  ```json
  {"host": "oracle-cloud"}
  ```

### 7. `/api/docs`
- **GET**
- Retorna documentação Swagger/OpenAPI em JSON.

---

## Status HTTP
- `200`: sucesso
- `404`: não encontrado
- `500`: erro interno

## Exemplos de uso
- Buscar últimas métricas de todos os hosts:
  ```http
  GET /api/latest
  ```
- Buscar histórico de CPU de um host:
  ```http
  GET /api/history?host=oracle-cloud&range=1h&metric=cpu
  ```
- Exportar dados em CSV:
  ```http
  GET /api/export?host=oracle-cloud&metric=cpu&range=1h
  ```

## Observações
- Todos os endpoints aceitam CORS (pode consumir via frontend JS).
- Os campos retornados são agrupados e possuem nomes amigáveis.
- Para mais detalhes, acesse `/api/docs` para o JSON OpenAPI.
