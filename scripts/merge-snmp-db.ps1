#!/usr/bin/env pwsh
# Merge de bancos de dados SNMP - Combina dados de local e nuvem

param(
    [Parameter()]
    [string]$LocalDB = "C:\Projetos\FCAPS-Redes\backups\snmp-db\local_current.db",
    [Parameter()]
    [string]$CloudDB = "C:\Projetos\FCAPS-Redes\backups\snmp-db\cloud_current.db",
    [Parameter()]
    [string]$OutputDB = "C:\Projetos\FCAPS-Redes\backups\snmp-db\merged.db"
)

$SSH_KEY = "D:\Downloads\fanfics_umina\ssh-key-2025-11-17.key"
$REMOTE_HOST = "opc@137.131.133.165"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  SNMP Database Merge Tool" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# 1. Baixar DB atual da nuvem
Write-Host "[1/4] Baixando DB atual da nuvem..." -ForegroundColor Yellow
ssh -i $SSH_KEY $REMOTE_HOST "sudo docker cp snmp-collector:/data/snmp_metrics.db /tmp/cloud_backup.db"
scp -i $SSH_KEY "${REMOTE_HOST}:/tmp/cloud_backup.db" $CloudDB

# 2. Copiar DB local atual
Write-Host "[2/4] Extraindo DB local..." -ForegroundColor Yellow
docker cp snmp-collector:/data/snmp_metrics.db $LocalDB

$localSize = (Get-Item $LocalDB).Length / 1KB
$cloudSize = (Get-Item $CloudDB).Length / 1KB

Write-Host "  Local: $([math]::Round($localSize, 2)) KB" -ForegroundColor Cyan
Write-Host "  Nuvem: $([math]::Round($cloudSize, 2)) KB" -ForegroundColor Cyan
Write-Host ""

# 3. Mesclar bancos usando SQLite
Write-Host "[3/4] Mesclando dados..." -ForegroundColor Yellow

# Criar banco mesclado
Copy-Item $LocalDB $OutputDB -Force

# Script SQL para mesclar
$mergeSQL = @"
ATTACH DATABASE '$CloudDB' AS cloud;

-- Inserir métricas do cloud que não existem no local
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
"@

# Executar merge no container
$mergeSQL | Out-File -FilePath "C:\Projetos\FCAPS-Redes\backups\snmp-db\merge.sql" -Encoding UTF8

docker cp $CloudDB snmp-collector:/tmp/cloud.db
docker cp $LocalDB snmp-collector:/tmp/local.db
docker cp "C:\Projetos\FCAPS-Redes\backups\snmp-db\merge.sql" snmp-collector:/tmp/merge.sql

docker exec snmp-collector sh -c "cp /tmp/local.db /tmp/merged.db && sqlite3 /tmp/merged.db < /tmp/merge.sql"

docker cp snmp-collector:/tmp/merged.db $OutputDB

$mergedSize = (Get-Item $OutputDB).Length / 1KB
Write-Host "  Mesclado: $([math]::Round($mergedSize, 2)) KB" -ForegroundColor Green
Write-Host ""

# 4. Aplicar banco mesclado
Write-Host "[4/4] Aplicando banco mesclado..." -ForegroundColor Yellow

$choice = Read-Host "Deseja aplicar o banco mesclado? (L)ocal, (N)uvem, (A)mbos, (C)ancelar [A]"

switch ($choice.ToUpper()) {
    'L' {
        docker cp $OutputDB snmp-collector:/data/snmp_metrics.db
        Write-Host "OK Aplicado localmente" -ForegroundColor Green
    }
    'N' {
        scp -i $SSH_KEY $OutputDB "${REMOTE_HOST}:/tmp/merged.db"
        ssh -i $SSH_KEY $REMOTE_HOST "sudo docker cp /tmp/merged.db snmp-collector:/data/snmp_metrics.db"
        Write-Host "OK Aplicado na nuvem" -ForegroundColor Green
    }
    'A' {
        docker cp $OutputDB snmp-collector:/data/snmp_metrics.db
        scp -i $SSH_KEY $OutputDB "${REMOTE_HOST}:/tmp/merged.db"
        ssh -i $SSH_KEY $REMOTE_HOST "sudo docker cp /tmp/merged.db snmp-collector:/data/snmp_metrics.db"
        Write-Host "OK Aplicado em ambos" -ForegroundColor Green
    }
    default {
        Write-Host "Cancelado. Banco mesclado salvo em: $OutputDB" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Merge concluido!" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
