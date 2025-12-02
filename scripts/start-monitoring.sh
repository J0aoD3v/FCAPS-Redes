#!/bin/bash
# Script para iniciar o ambiente de monitoramento

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "================================================"
echo "    🚀 Iniciando Ambiente FCAPS               "
echo "================================================"
echo -e "${NC}"

# Verifica se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Docker não está rodando!${NC}"
    echo "Iniciando Docker..."
    sudo service docker start
    sleep 3
fi

# Navega para o diretório do docker
cd "$(dirname "$0")/../docker" || exit 1

echo -e "${YELLOW}[1/4] Verificando arquivos...${NC}"
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}Erro: docker-compose.yml não encontrado!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Arquivos encontrados!${NC}"
echo ""

# Para containers existentes
echo -e "${YELLOW}[2/4] Parando containers anteriores...${NC}"
docker compose down 2>/dev/null || true
echo -e "${GREEN}✓ Containers parados!${NC}"
echo ""

# Inicia containers
echo -e "${YELLOW}[3/4] Iniciando containers...${NC}"
docker compose up -d --build
echo -e "${GREEN}✓ Containers iniciados!${NC}"
echo ""

# Aguarda inicialização
echo -e "${YELLOW}[4/4] Aguardando inicialização (30s)...${NC}"
for i in {30..1}; do
    echo -ne "\rAguardando: ${i}s "
    sleep 1
done
echo ""
echo -e "${GREEN}✓ Ambiente pronto!${NC}"
echo ""

# Mostra status
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}Status dos Containers:${NC}"
echo -e "${BLUE}================================================${NC}"
docker compose ps
echo ""

# Mostra uso de recursos
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}Uso de Recursos:${NC}"
echo -e "${BLUE}================================================${NC}"
docker stats --no-stream
echo ""

# URLs de acesso
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}  ✅ Ambiente Inicializado com Sucesso!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "${YELLOW}📊 Acesse os serviços:${NC}"
echo ""
echo -e "  ${BLUE}Zabbix Web Interface:${NC}"
echo -e "    http://localhost:8080"
echo -e "    Usuário: Admin"
echo -e "    Senha: zabbix"
echo ""
echo -e "  ${BLUE}Objeto 1 - Nginx Web Server:${NC}"
echo -e "    http://localhost:8081"
echo -e "    Status: http://localhost:8081/nginx_status"
echo ""
echo -e "  ${BLUE}Objeto 2 - Python App + SQLite:${NC}"
echo -e "    http://localhost:5000"
echo -e "    Métricas: http://localhost:5000/metrics"
echo -e "    Stats: http://localhost:5000/stats"
echo ""
echo -e "${YELLOW}📝 Comandos úteis:${NC}"
echo -e "  Ver logs:        docker compose logs -f"
echo -e "  Parar ambiente:  docker compose down"
echo -e "  Reiniciar:       docker compose restart"
echo -e "  Status:          docker compose ps"
echo -e "  Recursos:        docker stats"
echo ""
