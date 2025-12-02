# 📋 Guia: Adicionar Hosts no Zabbix

## Objetivo

Adicionar os 3 containers monitorados no Zabbix para começar a coletar métricas.

---

## 🔧 Host 1: Nginx Web Server

### Passo 1: Criar o Host

1. No menu superior, clique em: **Configuration** → **Hosts**
2. Clique no botão **Create host** (canto superior direito)

### Passo 2: Configurar o Host

Preencha os campos:

**Aba Host:**

- **Host name:** `nginx-web`
- **Visible name:** `Nginx Web Server`
- **Groups:**
  - Clique em **Select**
  - Selecione **Linux servers**
  - Clique em **Select** (confirmar)

**Agent interfaces:**

- Clique em **Add** (se não houver interface)
- **DNS name:** `nginx-web`
- **Connect to:** Selecione **DNS** (bolinha)
- **Port:** `10050`

**Descrição:**

- Deixe em branco ou escreva: "Servidor Web Nginx monitorado"

**Monitored by proxy:**

- Deixe: **(no proxy)**

**Enabled:**

- ✅ Marcado

### Passo 3: Adicionar Templates

1. Clique na aba **Templates**
2. Clique em **Select** ao lado de "Link new templates"
3. Na janela que abrir, procure e selecione:
   - `ICMP Ping`
4. Clique em **Select**

### Passo 4: Salvar

- Clique no botão **Add** no rodapé da página

---

## 🐍 Host 2: Python Application

### Passo 1: Criar o Host

1. **Configuration** → **Hosts** → **Create host**

### Passo 2: Configurar o Host

**Aba Host:**

- **Host name:** `python-app`
- **Visible name:** `Python Application + SQLite`
- **Groups:** **Linux servers**

**Agent interfaces:**

- **DNS name:** `python-app`
- **Connect to:** **DNS**
- **Port:** `10050`

**Enabled:** ✅ Marcado

### Passo 3: Adicionar Templates

Templates:

- `ICMP Ping`

### Passo 4: Salvar

- Clique em **Add**

---

## 🐧 Host 3: Alpine Linux Host

### Passo 1: Criar o Host

1. **Configuration** → **Hosts** → **Create host**

### Passo 2: Configurar o Host

**Aba Host:**

- **Host name:** `alpine-host`
- **Visible name:** `Alpine Linux Host`
- **Groups:** **Linux servers**

**Agent interfaces:**

- **DNS name:** `alpine-host`
- **Connect to:** **DNS**
- **Port:** `10050`

**Enabled:** ✅ Marcado

### Passo 3: Adicionar Templates

Templates:

- `ICMP Ping`

### Passo 4: Salvar

- Clique em **Add**

---

## ✅ Verificar Hosts Adicionados

Após adicionar os 3 hosts:

1. Vá em **Configuration** → **Hosts**
2. Você deve ver 4 hosts no total:
   - ✅ Zabbix server (já existia)
   - ✅ nginx-web
   - ✅ python-app
   - ✅ alpine-host

### Status dos Hosts

Os ícones ao lado de cada host indicam:

- 🟢 Verde = Host ativo e respondendo
- 🔴 Vermelho = Host com problemas
- ⚪ Cinza = Aguardando primeira coleta de dados

**Aguarde 1-2 minutos** para o Zabbix começar a coletar dados.

---

## 📊 Ver Dados Coletados

### Opção 1: Latest Data

1. **Monitoring** → **Latest data**
2. No campo **Hosts**, digite o nome do host (ex: `nginx-web`)
3. Clique em **Apply**
4. Você verá as métricas coletadas

### Opção 2: Graphs

1. **Monitoring** → **Hosts**
2. Clique no nome do host
3. Clique na aba **Graphs**

---

## ⚠️ Observações Importantes

### Limitações Atuais

Como os containers **não têm Zabbix Agent instalado**, o monitoramento atual é limitado a:

- ✅ **ICMP Ping** - Verifica se o host está online
- ❌ **CPU, Memória, Disco** - Não disponível sem agente

### Para Monitoramento Completo

Se quiser monitorar CPU, memória, disco e processos, você precisará:

1. Instalar o Zabbix Agent 2 em cada container
2. Ou atualizar o `docker-compose.yml` para incluir os agentes

**Deseja adicionar agentes Zabbix nos containers para monitoramento completo?**

---

## 🎯 Próximos Passos

Após adicionar os hosts:

1. ✅ Aguardar 2-3 minutos para coleta de dados
2. ✅ Verificar status em **Monitoring** → **Hosts**
3. ✅ Ver gráficos de disponibilidade
4. ✅ Criar dashboards personalizados
5. ✅ Configurar triggers e alarmes

---

## 🆘 Troubleshooting

### Host aparece como "Não disponível" (vermelho)

**Problema:** O Zabbix não consegue alcançar o host

**Soluções:**

1. Verificar se o container está rodando:

   ```powershell
   docker compose ps
   ```

2. Verificar conectividade:

   ```powershell
   docker exec -it zabbix-server ping nginx-web
   ```

3. Verificar se a porta 10050 está aberta (se tiver agente):
   ```powershell
   docker exec -it zabbix-server telnet nginx-web 10050
   ```

### Host não aparece na lista

**Solução:**

- Aguarde 30-60 segundos e recarregue a página
- Verifique se salvou corretamente (botão Add)

### Nenhum dado sendo coletado

**Solução:**

- Aguarde 2-3 minutos para primeira coleta
- Verifique se o template está associado ao host
- Vá em **Monitoring** → **Latest data** e filtre pelo host

---

## 📝 Resumo das Configurações

| Host          | DNS Name    | Port  | Template  | Status        |
| ------------- | ----------- | ----- | --------- | ------------- |
| Zabbix server | localhost   | 10050 | (vários)  | ✅ Ativo      |
| nginx-web     | nginx-web   | 10050 | ICMP Ping | ⏳ Aguardando |
| python-app    | python-app  | 10050 | ICMP Ping | ⏳ Aguardando |
| alpine-host   | alpine-host | 10050 | ICMP Ping | ⏳ Aguardando |

---

**Pronto!** Seus hosts estão configurados e o Zabbix começará a monitorá-los. 🎉
