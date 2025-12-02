# Roteiro de Apresentação - FCAPS com Zabbix

**Apresentação:** 04/12/2025  
**Tempo estimado:** 15-20 minutos

---

## 1. Introdução (2 min)

### Objetivo do Projeto

- Implementar sistema de monitoramento baseado no modelo FCAPS
- Gerenciar redes de forma proativa
- Coletar métricas via SNMP (OIDs MIB-II)

### Tecnologias Utilizadas

- **Zabbix 7.2:** Plataforma de monitoramento open-source
- **Docker:** Containerização dos serviços
- **WSL2:** Ambiente Linux no Windows
- **Alpine Linux:** Imagens leves (5-10x menores que Ubuntu)

---

## 2. Arquitetura do Sistema (3 min)

### Componentes

```
┌─────────────────────────────────────────┐
│         Docker Network (bridge)         │
│         172.20.0.0/16                   │
│                                         │
│  ┌──────────────┐                       │
│  │ Zabbix Server│ :8080 :10051         │
│  │ + MySQL DB   │ (Appliance)          │
│  └──────┬───────┘                       │
│         │                               │
│         ├──────────┬──────────┬────────┤
│         │          │          │        │
│  ┌──────▼─────┐ ┌──▼────────┐ ┌───▼───┐│
│  │ nginx-web  │ │python-app │ │alpine-││
│  │ :8081      │ │ :5000     │ │ host  ││
│  │ + Agent    │ │ + Agent   │ │+Agent ││
│  └────────────┘ └───────────┘ └───────┘│
└─────────────────────────────────────────┘
```

### Por que 4 containers?

- **Hardware limitado:** 8GB RAM, i5 8ª geração
- **Otimização:** Alpine Linux (tamanho reduzido)
- **Separação de serviços:** Nginx, Python, Host genérico
- **Persistência:** Volume Docker para banco de dados

---

## 3. Demonstração Prática (8 min)

### 3.1 Acesso ao Zabbix

- Abrir http://localhost:8080
- Login: `Admin` / Senha: `zabbix`

### 3.2 Visualizar Hosts Monitorados

- **Monitoring → Hosts**
- Mostrar 3 hosts: nginx-web, python-app, alpine-host
- Status verde "ZBX" = agentes funcionando

### 3.3 Métricas em Tempo Real

- **Monitoring → Latest data**
- Selecionar um host
- Mostrar categorias:
  - **CPU:** utilização (~10-14%), load average
  - **Memória:** 3.83 GB total, ~20% uso
  - **Disco:** I/O, utilização, writes/s
  - **Processos:** quantidade rodando
  - **Sistema:** uptime, nome, descrição

### 3.4 Gráficos Históricos

- Clicar em "Graph" em qualquer métrica
- Mostrar tendência ao longo do tempo
- Explicar período de coleta (1min)

### 3.5 Dashboard (se criado)

- **Monitoring → Dashboards**
- Visão consolidada dos 3 hosts
- Widgets com CPU, Memória, Disco

---

## 4. Mapeamento FCAPS (4 min)

### **F - Fault Management**

> "Como detectamos e respondemos a falhas?"

- ✅ Triggers configurados para:
  - CPU > 80% por 5 minutos
  - Memória > 90%
  - Disco > 85%
  - Serviço indisponível
- ✅ Notificações (email/Telegram configuráveis)
- ✅ Histórico de problemas

**Demonstração:** Mostrar Configuration → Hosts → Triggers

---

### **C - Configuration Management**

> "Como mantemos inventário e configurações?"

- ✅ Descoberta automática de recursos
- ✅ Inventário de software instalado
- ✅ Templates padronizados (Linux by Zabbix agent)
- ✅ Checksum de arquivos críticos (/etc/passwd)

**Demonstração:** Mostrar Inventory de um host

---

### **A - Accounting Management**

> "Como contabilizamos uso de recursos?"

- ✅ Banco de dados MySQL com histórico
- ✅ Retenção de dados configurável
- ✅ Relatórios de utilização
- ✅ Exportação via API JSON-RPC

**Demonstração:** Mostrar gráfico com histórico de 1 hora

---

### **P - Performance Management**

> "Como medimos e otimizamos desempenho?"

- ✅ 60+ métricas por host
- ✅ Coleta a cada 30-60 segundos
- ✅ KPIs definidos:
  - CPU < 80%
  - Memória < 85%
  - Disco < 80%
- ✅ Análise de tendências

**Demonstração:** Mostrar Latest Data com múltiplas métricas

---

### **S - Security Management**

> "Como garantimos segurança?"

- ✅ Monitoramento de integridade de arquivos
- ✅ Auditoria de usuários logados
- ✅ Detecção de mudanças não autorizadas
- ✅ Logs centralizados

**Demonstração:** Mostrar Security → Checksum of /etc/passwd

---

## 5. OIDs SNMP e MIB-II (2 min)

### Principais OIDs Mapeados

| Categoria | OID                       | Descrição         |
| --------- | ------------------------- | ----------------- |
| CPU       | `.1.3.6.1.2.1.25.3.3.1.2` | hrProcessorLoad   |
| Memória   | `.1.3.6.1.2.1.25.2.3.1.5` | hrStorageSize     |
| Processos | `.1.3.6.1.2.1.25.1.6.0`   | hrSystemProcesses |
| Uptime    | `.1.3.6.1.2.1.1.3.0`      | sysUpTime         |
| Nome      | `.1.3.6.1.2.1.1.5.0`      | sysName           |

**Referência completa:** `docs/OIDS-METRICAS.md`

---

## 6. Conclusões (1 min)

### Objetivos Alcançados

- ✅ Sistema FCAPS completo e funcional
- ✅ 3 objetos monitorados (requisito mínimo atendido)
- ✅ Coleta de métricas em tempo real
- ✅ Mapeamento para OIDs MIB-II
- ✅ Persistência de dados
- ✅ Interface web acessível

### Lições Aprendidas

- Importância do monitoramento proativo
- Otimização de recursos em ambientes limitados
- Docker facilita deployment e reprodutibilidade
- Zabbix é poderoso mas tem curva de aprendizado

### Trabalhos Futuros

- Adicionar mais serviços (PostgreSQL, Redis, Apache)
- Implementar notificações via Telegram/Email
- Criar dashboards customizados
- Integrar com ferramentas de automação (Ansible)

---

## 7. Perguntas e Respostas (tempo restante)

### Perguntas Esperadas

**1. Por que Zabbix e não Prometheus/Grafana?**

> Zabbix é completo (coleta + visualização + alertas) em um único sistema. Prometheus + Grafana requer mais componentes.

**2. Por que Docker e não VMs?**

> Docker é mais leve (menos overhead), inicia em segundos vs minutos, e usa menos memória (128-512MB vs 1-2GB por VM).

**3. Como garantir alta disponibilidade?**

> Em produção: Zabbix Proxy para redundância, múltiplos servidores Zabbix, banco de dados replicado.

**4. Qual o overhead do monitoramento?**

> Agente Zabbix usa ~10-20MB RAM e <1% CPU. Impacto mínimo nos serviços monitorados.

**5. É escalável?**

> Sim! Zabbix suporta 100.000+ hosts com particionamento de BD e Zabbix Proxies distribuídos.

---

## Comandos para Demonstração ao Vivo

### Iniciar ambiente:

```powershell
cd C:\Projetos\FCAPS-Redes\docker
docker compose up -d
```

### Verificar status:

```powershell
docker compose ps
```

### Ver logs em tempo real:

```powershell
docker logs nginx-web --follow
```

### Teste de carga (simular alta CPU):

```powershell
docker exec python-app sh -c "yes > /dev/null &"
# Aguardar 2-3 min e mostrar aumento no Zabbix
docker exec python-app pkill yes
```

### Parar ambiente:

```powershell
docker compose down
```

### Reconstruir (se necessário):

```powershell
docker compose up -d --build --force-recreate
```

---

## Checklist Pré-Apresentação

- [ ] Docker Desktop rodando
- [ ] Containers up há pelo menos 5 minutos (dados coletados)
- [ ] Navegador aberto em http://localhost:8080
- [ ] Login testado (Admin/zabbix)
- [ ] Dashboard criado e configurado
- [ ] Screenshots de backup (caso falhe internet)
- [ ] Documentação impressa (PLANEJAMENTO.md, OIDS-METRICAS.md)
- [ ] Slides preparados (opcional)

---

## Materiais de Apoio

1. `docs/PLANEJAMENTO.md` - Planejamento completo do projeto
2. `docs/OIDS-METRICAS.md` - Tabela de OIDs e métricas
3. `docs/INSTALACAO.md` - Guia de instalação
4. `docs/QUICKSTART.md` - Início rápido
5. `README.md` - Visão geral do repositório

---

**Boa sorte na apresentação! 🚀**
