# 🚀 Quick Start - Projeto FCAPS

## Início Rápido

### 1️⃣ Configurar WSL (PowerShell como Admin)

```powershell
cd C:\Projetos\FCAPS-Redes
.\scripts\setup-wsl.ps1
```

### 2️⃣ Instalar Docker (dentro do WSL)

```bash
wsl
cd /mnt/c/Projetos/FCAPS-Redes
bash scripts/install-docker.sh
```

Feche e reabra o terminal WSL.

### 3️⃣ Iniciar Ambiente

```bash
cd /mnt/c/Projetos/FCAPS-Redes
bash scripts/start-monitoring.sh
```

### 4️⃣ Acessar Serviços

- **Zabbix:** http://localhost:8080 (Admin/zabbix)
- **Nginx:** http://localhost:8081
- **Python App:** http://localhost:5000

---

## 📖 Documentação Completa

Consulte o arquivo [INSTALACAO.md](INSTALACAO.md) para o guia completo.

---

## 🏗️ Estrutura do Projeto

```
FCAPS-Redes/
├── docker/
│   ├── docker-compose.yml          # Configuração principal
│   ├── monitored-services/
│   │   ├── nginx/                  # Objeto 1: Servidor Web
│   │   └── python-app/             # Objeto 2: App Python + SQLite
│   └── zabbix/                     # Dados do Zabbix
├── scripts/
│   ├── setup-wsl.ps1              # Config WSL (Windows)
│   ├── install-docker.sh          # Instala Docker (Linux)
│   └── start-monitoring.sh        # Inicia ambiente
├── docs/                          # Documentação adicional
├── PLANEJAMENTO.md               # Planejamento do projeto
├── INSTALACAO.md                 # Guia de instalação completo
└── README.md                     # Este arquivo
```

---

## 🐳 Containers

| Container | Função | Porta | RAM |
|-----------|--------|-------|-----|
| zabbix-server | Servidor de monitoramento | 10051 | 512MB |
| zabbix-web | Interface web | 8080 | 256MB |
| nginx-monitored | Servidor Web (Obj 1) | 8081 | 64MB |
| python-app-monitored | App Python (Obj 2) | 5000 | 128MB |
| alpine-host-monitored | Host Linux (Obj 3) | - | 64MB |
| *-agent | Agentes Zabbix | 10050 | 64MB cada |

**Total estimado:** ~1.5GB RAM

---

## 🔧 Comandos Úteis

```bash
# Ver status
docker compose ps

# Ver logs
docker compose logs -f

# Parar ambiente
docker compose down

# Reiniciar
docker compose restart

# Ver uso de recursos
docker stats

# Iniciar Docker (se necessário)
sudo service docker start
```

---

## 📊 Objetos Monitorados

### 🌐 Objeto 1: Servidor Web Nginx
- **Tecnologia:** Nginx Alpine
- **Métricas:** Disponibilidade, tempo de resposta, requisições/s, erros HTTP

### 🐍 Objeto 2: Aplicação Python + SQLite  
- **Tecnologia:** Flask + SQLite
- **Métricas:** CPU, memória, queries, tamanho do DB, I/O

### 🐧 Objeto 3: Host Linux Alpine
- **Tecnologia:** Alpine Linux
- **Métricas:** CPU, memória, disco, rede, processos

---

## 🎯 Área FCAPS

**[Definir qual área foi escolhida]**

- [ ] Gerência de Falhas
- [ ] Gerência de Configuração
- [ ] Gerência de Contabilização
- [ ] Gerência de Desempenho
- [ ] Gerência de Segurança

---

## ✅ Checklist

- [ ] WSL configurado
- [ ] Docker instalado
- [ ] Ambiente iniciado
- [ ] Zabbix acessível
- [ ] Hosts adicionados no Zabbix
- [ ] Templates configurados
- [ ] Métricas sendo coletadas
- [ ] Triggers configurados
- [ ] Dashboards criados
- [ ] Documentação iniciada

---

## 🆘 Problemas?

Consulte a seção **Resolução de Problemas** em [INSTALACAO.md](INSTALACAO.md)

---

## 📅 Apresentação

**Data:** 04/12/2025  
**Tempo:** 10 minutos  
**Entrega:** Artigo SBC + Apresentação

---

## 👥 Grupo

- [ ] Membro 1
- [ ] Membro 2
- [ ] Membro 3
- [ ] Membro 4
