# Trabalho de Gerência de Redes de Computadores

**Data da Apresentação:** 04/12/2025

## 1. Objetivo do Trabalho

Desenvolver um projeto de gerenciamento de rede contemplando pelo menos 3 objetos (hosts, serviços ou dispositivos), aplicando conceitos de monitoramento, métricas, alarmes e procedimentos de administração.

O grupo deverá identificar as informações relevantes, definir como será realizado o processo de gerenciamento e demonstrar domínio dos conceitos.

## 2. Fundamentação

O trabalho deverá utilizar como base o modelo FCAPS, que define cinco áreas funcionais da gerência de redes:

- **Gerência de Falhas:** Detecção, isolamento, notificação e correção de problemas que afetam o funcionamento dos recursos de rede.
- **Gerência de Configuração:** Controle e documentação das configurações de hardware e software, incluindo atualizações e modificações.
- **Gerência de Contabilização:** Registro e análise de uso da rede para fins de métricas, alocação de recursos ou cobrança.
- **Gerência de Desempenho:** Coleta e análise de indicadores de desempenho para garantir qualidade de serviço e prever tendências.
- **Gerência de Segurança:** Controle e restrição de acesso para evitar uso indevido, intencional ou acidental, garantindo a integridade da operação da rede.

## 3. Descrição do Trabalho

Cada grupo deverá escolher um conjunto de no mínimo 3 objetos dentro de um ambiente de rede TCP/IP (por exemplo: roteadores, switches, servidores, serviços de rede, hosts, impressoras, etc.).

Com base na área funcional do FCAPS atribuída ao grupo, deverá ser desenvolvido o processo de gerenciamento dos objetos, incluindo:

### 3.1. Identificação dos Objetos Gerenciados

Para cada objeto escolhido, o grupo deve:

- Indicar quais objetos da MIB-II (SNMP) são relevantes para o monitoramento.
- Explicar o motivo da seleção de cada OID, relacionando sua importância para o gerenciamento.

### 3.2. Processo de Gerenciamento

Descrever detalhadamente:

- Eventos que devem ser detectados ou gerados (ex.: queda de interface, uso elevado de CPU, indisponibilidade de serviço).
- Frequência de consulta (polling) aos objetos monitorados.
- Alarmes e notificações que devem ser enviados ao administrador (ex.: thresholds, severidades).
- KPIs (Indicadores de Desempenho) aplicáveis (ex.: disponibilidade, latência, throughput, utilização de CPU/memória).
- Fluxo operacional de como o gerenciamento será executado.

### 3.3. Justificativas Técnicas

Cada métrica, evento ou procedimento deve ser acompanhado de:

- Justificativa técnica para seu uso.
- Explicação clara do que significa cada informação coletada.
- Descrição de como ela contribui para o gerenciamento do objeto.

## 4. Implementação Recomendada (Sugestão de Caminho)

Esta parte serve como roteiro para seguirem na prática.

1. **Definir o escopo do projeto:**

   - Quais dispositivos ou serviços serão monitorados?
   - Qual área do FCAPS será contemplada?
   - Quais objetivos devem ser alcançados?

2. **Seleção de uma ferramenta de monitoramento:**

   O grupo pode escolher ferramentas como:

   - Zabbix
   - Nagios
   - PRTG
   - Observium
   - Grafana + Prometheus
   - (ou outra ferramenta similar)

3. **Instalação/configuração da ferramenta:**

   - Instalar a solução em um servidor.
   - Habilitar SNMP ou agentes necessários nos dispositivos monitorados.

4. **Configuração dos KPIs relevantes:**

   Exemplos:

   - Disponibilidade
   - Latência
   - Throughput
   - Uso de CPU/memória
   - Resposta de serviços (HTTP, DB, DNS...)
   - Contabilização de falhas

5. **Planejamento do gerenciamento:**

   - Frequência de polling
   - Configuração de alertas
   - Procedimentos de backup de configuração
   - Rotinas de manutenção (updates, verificações, limpeza de logs)

6. **Testes e validação:**

   - Verificação da leitura dos OIDs da MIB-II
   - Teste de alarmes e thresholds

7. **Documentação completa do processo.**

## 5. Grupos

- Cada grupo poderá ter até 4 integrantes.

## 6. Apresentação (30% da nota)

- Será realizada na mesma data da entrega do trabalho.
- Tempo máximo: 10 minutos por grupo.
- Todos os integrantes devem apresentar.

## 7. Documentação Escrita (70% da nota)

Cada grupo deverá entregar um artigo técnico descrevendo o projeto, seguindo o modelo oficial da SBC:

**Template obrigatório:** https://www.sbc.org.br/wp-content/uploads/2024/07/modelosparapublicaodeartigos.zip
