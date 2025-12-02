FROM python:3.11-alpine

# Instalar dependências de compilação e runtime
RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    sqlite

WORKDIR /app

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Remover dependências de compilação para reduzir tamanho
RUN apk del gcc musl-dev linux-headers

# Copiar aplicação
COPY . .

# Criar diretório para banco de dados
RUN mkdir -p /app/data

# Expor porta
EXPOSE 5000

# Comando de inicialização
CMD ["python", "app.py"]
