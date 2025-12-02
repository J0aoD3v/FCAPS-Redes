#!/bin/bash
# Script de instalação do Docker no WSL
# Executar dentro do WSL (Ubuntu/Debian)

set -e

echo "========================================"
echo "  Instalação Docker - Projeto FCAPS   "
echo "========================================"
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Atualiza sistema
echo -e "${YELLOW}[1/6] Atualizando sistema...${NC}"
sudo apt update
sudo apt upgrade -y
echo -e "${GREEN}✓ Sistema atualizado!${NC}"
echo ""

# Instala dependências
echo -e "${YELLOW}[2/6] Instalando dependências...${NC}"
sudo apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git \
    wget
echo -e "${GREEN}✓ Dependências instaladas!${NC}"
echo ""

# Adiciona repositório do Docker
echo -e "${YELLOW}[3/6] Configurando repositório Docker...${NC}"
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
echo -e "${GREEN}✓ Repositório configurado!${NC}"
echo ""

# Instala Docker
echo -e "${YELLOW}[4/6] Instalando Docker Engine...${NC}"
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
echo -e "${GREEN}✓ Docker instalado!${NC}"
echo ""

# Configura permissões
echo -e "${YELLOW}[5/6] Configurando permissões de usuário...${NC}"
sudo usermod -aG docker $USER
echo -e "${GREEN}✓ Usuário adicionado ao grupo docker!${NC}"
echo ""

# Inicia serviço Docker
echo -e "${YELLOW}[6/6] Iniciando serviço Docker...${NC}"
sudo service docker start

# Verifica instalação
echo ""
echo "Verificando instalação:"
docker --version
docker compose version
echo ""

echo "========================================"
echo -e "${GREEN}  Instalação concluída!${NC}"
echo "========================================"
echo ""
echo "Próximos passos:"
echo "1. Feche e reabra o terminal WSL (para aplicar permissões)"
echo "2. Verifique: docker ps"
echo "3. Execute: cd /mnt/c/Projetos/FCAPS-Redes/docker"
echo "4. Inicie o ambiente: docker compose up -d"
echo ""
echo "IMPORTANTE: Se o Docker não iniciar automaticamente,"
echo "execute sempre: sudo service docker start"
echo ""
