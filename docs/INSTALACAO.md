# 🚀 Guia de Instalação - Projeto FCAPS

Este guia contém os passos detalhados para configurar o ambiente de monitoramento.

## 📋 Pré-requisitos

- Windows 10/11 com WSL2 habilitado
- 8GB RAM (4GB alocados para WSL)
- 15GB de espaço livre em disco
- Conexão com internet

---

## 🔧 Passo 1: Configuração do WSL2

### 1.1. Instalar WSL (se não estiver instalado)

Abra o **PowerShell como Administrador** e execute:

```powershell
wsl --install
```

Reinicie o computador após a instalação.

### 1.2. Configurar limites de memória

Execute o script de configuração:

```powershell
cd C:\Projetos\FCAPS-Redes
.\scripts\setup-wsl.ps1
```

Ou crie manualmente o arquivo `.wslconfig`:

```powershell
notepad $env:USERPROFILE\.wslconfig
```

Cole o conteúdo:

```ini
[wsl2]
memory=4GB
processors=2
swap=2GB
localhostForwarding=true
```

Salve e reinicie o WSL:

```powershell
wsl --shutdown
```

### 1.3. Verificar instalação

```powershell
wsl --list --verbose
```

---

## 🐳 Passo 2: Docker

### Opção A: Você já tem Docker Desktop (Recomendado) ✅

Se você já tem Docker Desktop instalado no Windows:

1. **Certifique-se que o Docker Desktop está rodando**

   - Abra o Docker Desktop
   - Aguarde até ver o ícone do Docker na bandeja do sistema (verde)

2. **Verificar instalação** (no PowerShell):

```powershell
docker --version
docker compose version
```

**Pronto! Pule para o Passo 3.**

---

### Opção B: Instalar Docker no WSL (Alternativa)

Se preferir instalar Docker diretamente no WSL (sem Docker Desktop):

#### 2.1. Abrir WSL Ubuntu

```powershell
wsl -d Ubuntu
```

Se não tiver Ubuntu instalado:

```powershell
wsl --install -d Ubuntu
```

#### 2.2. Navegar até o projeto

```bash
cd /mnt/c/Projetos/FCAPS-Redes
```

#### 2.3. Executar script de instalação

```bash
chmod +x scripts/install-docker.sh
bash scripts/install-docker.sh
```

#### 2.4. Fechar e reabrir o terminal WSL

```bash
exit
wsl -d Ubuntu
```

#### 2.5. Verificar Docker

```bash
docker --version
docker compose version
docker ps
```

Se o Docker não estiver rodando:

```bash
sudo service docker start
```

---

## 🚀 Passo 3: Iniciar o Ambiente

### Opção A: Usando Docker Desktop (PowerShell) ⚡ Mais Fácil!

**No PowerShell:**

```powershell
cd C:\Projetos\FCAPS-Redes\docker
docker compose up -d --build
```

Aguarde alguns minutos para os containers iniciarem...

---

### Opção B: Usando WSL Ubuntu

**No WSL Ubuntu:**

#### 3.1. Navegar até o diretório do projeto

```bash
cd /mnt/c/Projetos/FCAPS-Redes
```

#### 3.2. Dar permissão ao script

```bash
chmod +x scripts/start-monitoring.sh
```

#### 3.3. Iniciar ambiente

```bash
bash scripts/start-monitoring.sh
```

Ou manualmente:

```bash
cd docker
docker compose up -d --build
```

### 3.4. Verificar containers

**PowerShell ou WSL:**

```powershell
docker compose ps
```

Todos os containers devem estar com status **Up**.

### 3.5. Verificar uso de recursos

```powershell
docker stats
```

Pressione `Ctrl+C` para sair.

---

## 🌐 Passo 4: Acessar os Serviços

Abra o navegador e acesse:

### Zabbix Web Interface

- **URL:** http://localhost:8080
- **Usuário:** Admin
- **Senha:** zabbix

### Objeto 1: Servidor Web Nginx

- **URL:** http://localhost:8081
- **Status:** http://localhost:8081/nginx_status

### Objeto 2: Aplicação Python + SQLite

- **URL:** http://localhost:5000
- **Métricas:** http://localhost:5000/metrics
- **Estatísticas:** http://localhost:5000/stats

---

## 🔍 Passo 5: Configurar Zabbix

### 5.1. Fazer login no Zabbix

1. Acesse http://localhost:8080
2. Usuário: `Admin`
3. Senha: `zabbix`

### 5.2. Adicionar Hosts Monitorados

#### Host 1: Nginx Web Server

1. Vá em **Configuration** → **Hosts** → **Create host**
2. Preencha:
   - **Host name:** Nginx-Web-Server
   - **Groups:** Linux servers
   - **Agent interfaces:**
     - DNS name: `nginx-agent`
     - Port: `10050`
3. Clique em **Add**

#### Host 2: Python App Server

1. **Create host**
2. Preencha:
   - **Host name:** Python-App-Server
   - **Groups:** Linux servers
   - **Agent interfaces:**
     - DNS name: `python-agent`
     - Port: `10050`
3. Clique em **Add**

#### Host 3: Alpine Linux Host

1. **Create host**
2. Preencha:
   - **Host name:** Alpine-Host-Linux
   - **Groups:** Linux servers
   - **Agent interfaces:**
     - DNS name: `alpine-agent`
     - Port: `10050`
3. Clique em **Add**

### 5.3. Associar Templates

Para cada host criado:

1. Clique no host
2. Aba **Templates**
3. Adicione os templates:
   - `Linux by Zabbix agent`
   - `Linux CPU by Zabbix agent`
   - `Linux memory by Zabbix agent`
   - `Linux filesystems by Zabbix agent`
   - `Linux network interfaces by Zabbix agent`
4. Clique em **Update**

### 5.4. Aguardar coleta de dados

- Aguarde 2-5 minutos para o Zabbix começar a coletar dados
- Vá em **Monitoring** → **Latest data** para ver as métricas

---

## 📊 Comandos Úteis

### Gerenciar containers

```bash
# Ver logs
docker compose logs -f

# Ver logs de um container específico
docker compose logs -f zabbix-server

# Parar ambiente
docker compose down

# Reiniciar ambiente
docker compose restart

# Parar um container específico
docker compose stop nginx-web

# Iniciar um container específico
docker compose start nginx-web

# Reconstruir containers
docker compose up -d --build
```

### Monitorar recursos

```bash
# Uso de recursos em tempo real
docker stats

# Espaço em disco
docker system df

# Limpar recursos não utilizados
docker system prune -a
```

### Acessar containers

```bash
# Acessar Zabbix Server
docker exec -it zabbix-server sh

# Acessar Nginx
docker exec -it nginx-monitored sh

# Acessar Python App
docker exec -it python-app-monitored sh
```

### Verificar conectividade

```bash
# Testar Nginx
curl http://localhost:8081

# Testar Python App
curl http://localhost:5000/health

# Testar Zabbix
curl http://localhost:8080
```

---

## ❌ Resolução de Problemas

### Docker não inicia

```bash
sudo service docker start
```

### Container não inicia

```bash
# Ver logs do container
docker compose logs container-name

# Reconstruir container
docker compose up -d --build container-name
```

### Porta já em uso

```bash
# Ver o que está usando a porta
sudo lsof -i :8080

# Ou no Windows PowerShell:
netstat -ano | findstr :8080
```

### Memória insuficiente

```bash
# Ver uso de memória
docker stats

# Parar containers desnecessários
docker compose stop container-name

# Limpar cache
docker system prune -a
```

### Zabbix não coleta dados

1. Verificar se os agents estão rodando:

   ```bash
   docker compose ps
   ```

2. Verificar logs do agent:

   ```bash
   docker compose logs nginx-agent
   ```

3. Testar conectividade:
   ```bash
   docker exec -it zabbix-server zabbix_get -s nginx-agent -k agent.ping
   ```

---

## 🎯 Próximos Passos

1. ✅ Configurar triggers e alarmes no Zabbix
2. ✅ Criar dashboards personalizados
3. ✅ Configurar notificações
4. ✅ Documentar OIDs MIB-II utilizados
5. ✅ Realizar testes de carga
6. ✅ Capturar screenshots para o artigo

---

## 📚 Referências

- [Documentação Zabbix](https://www.zabbix.com/documentation)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [WSL Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
