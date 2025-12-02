# Planejamento do Projeto FCAPS

## Visão Geral do Projeto

Projeto de gerenciamento de redes utilizando o modelo FCAPS com foco em monitoramento e gerenciamento de dispositivos e serviços em ambiente TCP/IP.

**Data de Apresentação:** 04/12/2025

---

## Tecnologias Selecionadas

### 1. **Zabbix (Configuração Leve)**

- Ferramenta open-source de monitoramento de infraestrutura
- Suporte nativo a SNMP, agentes e monitoramento passivo/ativo
- Interface web intuitiva para visualização de métricas
- Sistema robusto de alertas e notificações
- Dashboards personalizáveis e relatórios
- **Otimização:** Usar SQLite ao invés de MySQL/PostgreSQL (~500MB economizados)

### 2. **Docker**

- Containerização dos serviços para facilitar deploy e portabilidade
- Isolamento de ambientes
- Facilita replicação do ambiente de teste/produção
- Gerenciamento simplificado de dependências

### 3. **WSL (Windows Subsystem for Linux)**

- Ambiente Linux integrado ao Windows
- Facilita uso de ferramentas Linux e Docker
- Melhor compatibilidade com ferramentas de rede e monitoramento

### 4. **Otimizações para 8GB RAM** 💡

- **SQLite** ao invés de MySQL/PostgreSQL (economiza ~500MB)
- **Nginx** ao invés de Apache (menor footprint de memória)
- **Alpine Linux** como base dos containers (imagens ~5MB vs ~100MB Ubuntu)
- Limitar número de containers simultâneos a 3-4
- Usar Zabbix Agent ao invés de SNMP quando possível (mais leve)
- Configurar limits de memória em cada container

---

## Arquitetura do Ambiente

```
┌──────────────────────────────────────────────┐
│      Windows Host (8GB RAM, i5 8ª gen)      │
│           WSL2 (4GB alocado)                 │
│  ┌────────────────────────────────────────┐  │
│  │     Docker Environment (Otimizado)     │  │
│  │  ┌──────────────────────────────────┐  │  │
│  │  │  Zabbix Container (~800MB RAM)   │  │  │
│  │  │  - Zabbix Server + Frontend      │  │  │
│  │  │  - SQLite (leve, ~10MB RAM)      │  │  │
│  │  │  - Alpine Linux base             │  │  │
│  │  └──────────────────────────────────┘  │  │
│  │  ┌──────────────────────────────────┐  │  │
│  │  │  Containers Monitorados (leves)  │  │  │
│  │  │  - Nginx Alpine (~20MB)          │  │  │
│  │  │  - SQLite Container (~15MB)      │  │  │
│  │  │  - Python App Alpine (~50MB)     │  │  │
│  │  └──────────────────────────────────┘  │  │
│  │  Total estimado: ~1.5GB RAM usado       │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

---

## Objetos Gerenciados (Mínimo 3)

### Objeto 1: Servidor Web Nginx (Alpine) 🪶

- **Tipo:** Serviço HTTP
- **Container:** `nginx:alpine` (~20MB RAM)
- **Métricas:**
  - Disponibilidade do serviço
  - Tempo de resposta HTTP
  - Número de requisições por segundo
  - Taxa de erros (4xx, 5xx)
  - Conexões ativas

### Objeto 2: Banco de Dados SQLite 🪶

- **Tipo:** Serviço de banco de dados leve
- **Container:** Alpine + SQLite (~15MB RAM)
- **Métricas:**
  - Disponibilidade do serviço
  - Tamanho do arquivo .db
  - Tempo de resposta de queries
  - Uso de memória e CPU
  - Operações de I/O (leitura/escrita)

### Objeto 3: Aplicação Python (Alpine) 🪶

- **Tipo:** Serviço de aplicação web
- **Container:** `python:3.11-alpine` (~50MB RAM)
- **Métricas:**
  - CPU usage (system.cpu.util)
  - Memória (vm.memory.size)
  - Disco (vfs.fs.size, vfs.fs.inode)
  - Tráfego de rede (net.if.in, net.if.out)
  - Processos ativos
  - Status HTTP da aplicação

---

## Área FCAPS Selecionada

**[Definir qual área será focada pelo grupo]**

Opções:

- [ ] Gerência de Falhas
- [ ] Gerência de Configuração
- [ ] Gerência de Contabilização
- [ ] Gerência de Desempenho
- [ ] Gerência de Segurança

---

## Etapas de Implementação

### Fase 1: Preparação do Ambiente (Semana 1)

#### 1.1. Configuração do WSL

- [ ] Instalar WSL2 no Windows: `wsl --install`
- [ ] Instalar distribuição Linux (Ubuntu 22.04 ou Debian)
- [ ] **IMPORTANTE:** Limitar memória do WSL2 para não travar o Windows
  - Criar arquivo `C:\Users\<SeuUsuario>\.wslconfig`:
  ```ini
  [wsl2]
  memory=4GB
  processors=2
  swap=2GB
  localhostForwarding=true
  ```
  - Reiniciar WSL no PowerShell: `wsl --shutdown`
- [ ] Atualizar sistema: `sudo apt update && sudo apt upgrade`
- [ ] Configurar recursos de rede no WSL

#### 1.2. Instalação do Docker

- [ ] Instalar Docker no WSL2

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

- [ ] Instalar Docker Compose

```bash
sudo apt install docker-compose
```

- [ ] Verificar instalação: `docker --version` e `docker-compose --version`

### Fase 2: Deploy do Zabbix (Semana 1-2)

#### 2.1. Preparar Docker Compose do Zabbix (Versão Leve)

- [ ] Criar arquivo `docker-compose.yml` para o Zabbix
- [ ] Configurar containers otimizados:
  - Zabbix Server (Alpine) com limites de memória
  - Zabbix Frontend (Alpine + Nginx)
  - **SQLite** ao invés de MySQL/PostgreSQL (economiza ~500MB)
  - Zabbix Agent (para auto-monitoramento)
- [ ] Exemplo de configuração com limites:
  ```yaml
  services:
    zabbix-server:
      image: zabbix/zabbix-server-sqlite3:alpine-latest
      mem_limit: 512m
      cpus: 1.0
  ```

#### 2.2. Inicializar Zabbix

- [ ] Executar: `docker-compose up -d`
- [ ] Acessar interface web: `http://localhost:8080`
- [ ] Configurar usuário admin
- [ ] Verificar conectividade com banco de dados

### Fase 3: Configuração dos Objetos Monitorados (Semana 2)

#### 3.1. Deploy dos Containers Monitorados

- [ ] Criar containers para cada objeto gerenciado
- [ ] Instalar Zabbix Agent em cada container
- [ ] Configurar comunicação entre agents e server

#### 3.2. Habilitar SNMP (se aplicável)

- [ ] Instalar snmpd nos containers
- [ ] Configurar community strings
- [ ] Testar conectividade SNMP: `snmpwalk -v2c -c public localhost`

### Fase 4: Configuração do Monitoramento (Semana 2-3)

#### 4.1. Adicionar Hosts no Zabbix

- [ ] Cadastrar cada objeto como host
- [ ] Associar templates apropriados
- [ ] Configurar interfaces (Agent, SNMP, JMX, IPMI)

#### 4.2. Definir Items/Métricas

Para cada objeto, configurar:

- [ ] Items baseados em MIB-II (SNMP)
  - system.sysDescr (.1.3.6.1.2.1.1.1)
  - system.sysUpTime (.1.3.6.1.2.1.1.3)
  - ifOperStatus (.1.3.6.1.2.1.2.2.1.8)
  - ifInOctets/ifOutOctets (.1.3.6.1.2.1.2.2.1.10/16)
- [ ] Documentar OIDs selecionados e justificativas
- [ ] Definir intervalo de polling (ex: 1m, 5m, 10m)

#### 4.3. Configurar Triggers (Alarmes)

- [ ] Definir thresholds para cada métrica
- [ ] Configurar níveis de severidade:
  - Information
  - Warning
  - Average
  - High
  - Disaster
- [ ] Exemplo: CPU > 80% por 5 minutos = Warning

#### 4.4. Configurar Actions (Notificações)

- [ ] Configurar mídia de notificação (email, Telegram, etc.)
- [ ] Criar actions baseadas em triggers
- [ ] Testar envio de alertas

### Fase 5: Definição de KPIs (Semana 3)

#### 5.1. KPIs por Objeto

**Servidor Web:**

- [ ] Disponibilidade (uptime %) - Meta: 99.9%
- [ ] Tempo médio de resposta - Meta: < 200ms
- [ ] Taxa de sucesso de requisições - Meta: > 95%

**Banco de Dados:**

- [ ] Disponibilidade - Meta: 99.95%
- [ ] Conexões simultâneas vs. limite
- [ ] Tempo médio de query - Meta: < 100ms

**Host/Container:**

- [ ] CPU utilization - Threshold: 80%
- [ ] Memory utilization - Threshold: 85%
- [ ] Disk usage - Threshold: 80%
- [ ] Network throughput

#### 5.2. Dashboards

- [ ] Criar dashboard principal com visão geral
- [ ] Criar dashboards específicos por objeto
- [ ] Incluir gráficos de tendência
- [ ] Adicionar widgets de status atual

### Fase 6: Testes e Validação (Semana 3-4)

#### 6.1. Testes de Coleta de Dados

- [ ] Verificar recebimento de dados de todos os items
- [ ] Validar precisão das métricas
- [ ] Confirmar funcionamento do SNMP

#### 6.2. Testes de Alarmes

- [ ] Simular situações de alerta:
  - Parar um serviço
  - Gerar carga de CPU/memória
  - Desconectar interface de rede
- [ ] Verificar disparo de triggers
- [ ] Confirmar recebimento de notificações
- [ ] Medir tempo de detecção

#### 6.3. Testes de Recuperação

- [ ] Verificar limpeza automática de alarmes
- [ ] Testar restauração de serviços
- [ ] Documentar tempo de resposta

### Fase 7: Documentação (Semana 4)

#### 7.1. Documentação Técnica

- [ ] Arquitetura do ambiente
- [ ] Lista de objetos monitorados
- [ ] Tabela de OIDs MIB-II utilizados
- [ ] Justificativa técnica de cada métrica
- [ ] Configurações de polling e thresholds
- [ ] Procedimentos de gerenciamento
- [ ] Prints de tela do Zabbix

#### 7.2. Artigo SBC

- [ ] Baixar template da SBC
- [ ] Escrever seções:
  - Resumo/Abstract
  - Introdução
  - Fundamentação Teórica (FCAPS)
  - Metodologia
  - Implementação
  - Resultados
  - Conclusão
  - Referências
- [ ] Revisar formatação
- [ ] Revisar ortografia e gramática

#### 7.3. Apresentação

- [ ] Criar slides (10 minutos)
- [ ] Distribuir tópicos entre membros
- [ ] Preparar demonstração ao vivo
- [ ] Ensaiar apresentação

---

## Cronograma

| Semana | Atividades                                        | Responsável |
| ------ | ------------------------------------------------- | ----------- |
| 1      | Configuração WSL, Docker e Deploy Zabbix          | [Nome]      |
| 2      | Deploy objetos monitorados e configuração inicial | [Nome]      |
| 3      | Configuração de métricas, KPIs e alarmes          | [Nome]      |
| 4      | Testes, validação e documentação                  | [Todos]     |

---

## OIDs MIB-II Relevantes

### System Group (.1.3.6.1.2.1.1)

| OID                | Nome      | Descrição               | Justificativa                |
| ------------------ | --------- | ----------------------- | ---------------------------- |
| .1.3.6.1.2.1.1.1.0 | sysDescr  | Descrição do sistema    | Identificação do dispositivo |
| .1.3.6.1.2.1.1.3.0 | sysUpTime | Tempo desde último boot | Monitorar disponibilidade    |
| .1.3.6.1.2.1.1.5.0 | sysName   | Nome do host            | Identificação                |

### Interfaces Group (.1.3.6.1.2.1.2)

| OID                     | Nome         | Descrição            | Justificativa     |
| ----------------------- | ------------ | -------------------- | ----------------- |
| .1.3.6.1.2.1.2.1.0      | ifNumber     | Número de interfaces | Inventário        |
| .1.3.6.1.2.1.2.2.1.8.x  | ifOperStatus | Status operacional   | Detectar falhas   |
| .1.3.6.1.2.1.2.2.1.10.x | ifInOctets   | Bytes recebidos      | Monitorar tráfego |
| .1.3.6.1.2.1.2.2.1.16.x | ifOutOctets  | Bytes enviados       | Monitorar tráfego |

### Host Resources (.1.3.6.1.2.1.25)

| OID                     | Nome            | Descrição           | Justificativa            |
| ----------------------- | --------------- | ------------------- | ------------------------ |
| .1.3.6.1.2.1.25.3.3.1.2 | hrProcessorLoad | Carga da CPU        | Monitorar desempenho     |
| .1.3.6.1.2.1.25.2.3.1.6 | hrStorageUsed   | Armazenamento usado | Prevenir falta de espaço |

---

## Recursos Necessários

### Hardware/Software

- [x] Máquina Windows com WSL2 habilitado
- [x] 8GB RAM (suficiente com otimizações) ✅
- [x] Intel Core i5 8ª geração ✅
- [ ] 15GB espaço em disco livre (imagens Alpine são menores)
- [ ] Conexão com internet

### Dicas de Otimização para 8GB RAM 💡

- [ ] Alocar 4GB para WSL2 via arquivo `.wslconfig`
- [ ] Usar exclusivamente imagens Alpine Linux (5-10x menores)
- [ ] Limitar memória de cada container no docker-compose
- [ ] Fechar navegador e aplicações pesadas durante testes
- [ ] Monitorar uso de RAM em tempo real: `docker stats`
- [ ] Habilitar swap se necessário
- [ ] Fazer limpeza periódica: `docker system prune -a`

### Conhecimentos

- [ ] Conceitos de SNMP e MIB
- [ ] Docker e containerização
- [ ] Linux básico
- [ ] Redes TCP/IP
- [ ] Modelo FCAPS

---

## Referências

- [Documentação Zabbix](https://www.zabbix.com/documentation)
- [Docker Documentation](https://docs.docker.com/)
- [RFC 1213 - MIB-II](https://datatracker.ietf.org/doc/html/rfc1213)
- [WSL Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
- Template SBC: https://www.sbc.org.br/wp-content/uploads/2024/07/modelosparapublicaodeartigos.zip

---

## Checklist Final

- [ ] Ambiente funcional e testado
- [ ] Mínimo 3 objetos monitorados
- [ ] OIDs MIB-II documentados com justificativas
- [ ] KPIs definidos e funcionando
- [ ] Alarmes configurados e testados
- [ ] Dashboards criados
- [ ] Artigo SBC completo
- [ ] Apresentação preparada
- [ ] Todos os integrantes treinados

---

## Exemplo de Docker Compose Otimizado

```yaml
version: "3.8"

services:
  zabbix-server:
    image: zabbix/zabbix-server-sqlite3:alpine-latest
    container_name: zabbix-server
    mem_limit: 512m
    cpus: 1.0
    environment:
      - ZBX_DEBUGLEVEL=3
    volumes:
      - ./zabbix-data:/var/lib/zabbix
    ports:
      - "10051:10051"
    restart: unless-stopped

  zabbix-web:
    image: zabbix/zabbix-web-nginx-sqlite3:alpine-latest
    container_name: zabbix-web
    mem_limit: 256m
    cpus: 0.5
    environment:
      - ZBX_SERVER_HOST=zabbix-server
    ports:
      - "8080:8080"
    depends_on:
      - zabbix-server
    restart: unless-stopped

  nginx-monitor:
    image: nginx:alpine
    container_name: nginx-web
    mem_limit: 50m
    cpus: 0.25
    ports:
      - "80:80"
    restart: unless-stopped

  sqlite-app:
    image: alpine:latest
    container_name: sqlite-db
    mem_limit: 50m
    cpus: 0.25
    command: sh -c "apk add sqlite && tail -f /dev/null"
    restart: unless-stopped

  python-app:
    image: python:3.11-alpine
    container_name: python-app
    mem_limit: 100m
    cpus: 0.5
    command: sh -c "pip install flask && python -m flask run --host=0.0.0.0"
    ports:
      - "5000:5000"
    restart: unless-stopped
```

**Uso total estimado:** ~968MB RAM (deixa ~3GB livres no WSL)

---

## Observações

- Manter backups regulares das configurações
- Documentar problemas e soluções encontradas
- Tirar screenshots durante todo o processo
- Testar com antecedência para evitar problemas de última hora
- **Com 8GB RAM:** Fechar Chrome/Edge durante testes intensivos
- Monitorar temperatura do notebook durante operação prolongada
