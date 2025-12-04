# Dockerfile para API SNMP
FROM python:3.11-slim
WORKDIR /app
COPY api.py ./
RUN pip install --no-cache-dir --upgrade pip
EXPOSE 8090
CMD ["python", "api.py"]
