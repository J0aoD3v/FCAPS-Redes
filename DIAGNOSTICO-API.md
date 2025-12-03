# 🔍 Diagnóstico do Problema de Conexão com a API

## Problema Identificado

**Erro:** `ERR_CONNECTION_TIMED_OUT` ao tentar acessar `http://137.131.133.165:8090/api/latest`

## Análise Realizada

### ✅ O que está funcionando:

1. **Container está rodando:** `snmp-collector` está ativo há 2 horas
2. **Porta está escutando:** Porta 8090 está em LISTEN no container
3. **Processo da API está rodando:** `python3 /app/api.py` está ativo
4. **Firewall local está configurado:** Porta 8090 está aberta no firewall do servidor
5. **Coleta de dados funciona:** Logs mostram coletas recentes de métricas

### ❌ O problema:

**A porta 8090 não está acessível EXTERNAMENTE** - o Oracle Cloud Security List não está permitindo conexões de fora.

## Solução

Você precisa adicionar uma regra no **Oracle Cloud Security List** para permitir tráfego HTTP na porta 8090.

### Passos para corrigir:

1. **Acesse o Console da Oracle Cloud:**
   - Vá para: https://cloud.oracle.com/
   - Faça login na sua conta

2. **Navegue até Networking → Virtual Cloud Networks:**
   - Selecione sua VCN
   - Clique em "Security Lists"
   - Selecione a Security List padrão (ou a que está sendo usada)

3. **Adicione regra de Ingress (Entrada):**
   - Clique em "Add Ingress Rules"
   - Configure:
     - **Source Type:** CIDR
     - **Source CIDR:** `0.0.0.0/0` (para permitir de qualquer lugar) ou seu IP específico
     - **IP Protocol:** TCP
     - **Destination Port Range:** `8090`
     - **Description:** "SNMP Collector API Port"
   - Clique em "Add Ingress Rules"

4. **Aguarde alguns segundos** para a regra ser aplicada

5. **Teste novamente** a conexão

## Verificação Rápida

Depois de adicionar a regra, teste com:

```bash
# Do seu computador local
curl http://137.131.133.165:8090/api/latest

# Ou no navegador
http://137.131.133.165:8090/api/latest
```

## Status Atual do Servidor

- **IP Público:** 137.131.133.165
- **IP Privado:** 10.0.0.105
- **Container:** snmp-collector (rodando)
- **Porta:** 8090 (aberta no servidor, mas bloqueada no Security List)
- **Status:** API funcionando internamente, mas inacessível externamente

## Nota de Segurança

⚠️ **Recomendação:** Se possível, restrinja o Source CIDR ao seu IP específico ou a um range confiável, em vez de `0.0.0.0/0`, para maior segurança.

## Alternativa: Usar SSH Tunnel

Se você não quiser abrir a porta publicamente, pode usar um túnel SSH:

```bash
ssh -L 8090:localhost:8090 -F "c:\Users\Joao C\.ssh\config" oracle-cloud
```

Depois acesse: `http://localhost:8090/api/latest`

