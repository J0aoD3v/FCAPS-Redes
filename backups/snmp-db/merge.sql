ATTACH DATABASE 'C:\Projetos\FCAPS-Redes\backups\snmp-db\cloud_backup_original.db' AS cloud;

-- Inserir mÃ©tricas do cloud que nÃ£o existem no local
INSERT OR IGNORE INTO metrics (timestamp, host, cpu, memory, processes, uptime)
SELECT timestamp, host, cpu, memory, processes, uptime 
FROM cloud.metrics
WHERE NOT EXISTS (
    SELECT 1 FROM metrics 
    WHERE metrics.timestamp = cloud.metrics.timestamp 
    AND metrics.host = cloud.metrics.host
);

-- Atualizar last_metrics com dados mais recentes
INSERT OR REPLACE INTO last_metrics (host, timestamp, cpu, memory, processes, uptime, sysname)
SELECT host, timestamp, cpu, memory, processes, uptime, sysname
FROM cloud.last_metrics
WHERE timestamp > (
    SELECT COALESCE(MAX(timestamp), 0) 
    FROM last_metrics 
    WHERE last_metrics.host = cloud.last_metrics.host
);

DETACH DATABASE cloud;
