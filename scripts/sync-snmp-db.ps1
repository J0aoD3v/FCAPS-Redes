#!/usr/bin/env pwsh
# Sincronização de Banco de Dados SNMP Collector
# Local <-> Oracle Cloud

param(
    [Parameter()]
    [ValidateSet('push', 'pull', 'both')]
    [string]$Mode = 'both'
)

$SSH_KEY = "D:\Downloads\fanfics_umina\ssh-key-2025-11-17.key"
$REMOTE_HOST = "opc@137.131.133.165"
$LOCAL_DB = "C:\Projetos\FCAPS-Redes\docker\snmp-collector\snmp_metrics.db"
$LOCAL_BACKUP_DIR = "C:\Projetos\FCAPS-Redes\backups\snmp-db"
$REMOTE_BACKUP_DIR = "/home/opc/snmp-backups"

if (-not (Test-Path $LOCAL_BACKUP_DIR)) {
    New-Item -ItemType Directory -Path $LOCAL_BACKUP_DIR -Force | Out-Null
}

ssh -i $SSH_KEY $REMOTE_HOST "mkdir -p $REMOTE_BACKUP_DIR"

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  SNMP Database Sync - Mode: $Mode" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

function Sync-LocalToCloud {
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Copiando DB local do container..." -ForegroundColor Yellow
    
    docker cp snmp-collector:/data/snmp_metrics.db $LOCAL_DB
    
    if ($LASTEXITCODE -eq 0) {
        $size = (Get-Item $LOCAL_DB).Length / 1KB
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] OK DB local extraido: $([math]::Round($size, 2)) KB" -ForegroundColor Green
        
        $backupLocal = Join-Path $LOCAL_BACKUP_DIR "local_$timestamp.db"
        Copy-Item $LOCAL_DB $backupLocal
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] OK Backup local criado" -ForegroundColor Green
        
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Enviando para Oracle Cloud..." -ForegroundColor Yellow
        scp -i $SSH_KEY $LOCAL_DB "${REMOTE_HOST}:${REMOTE_BACKUP_DIR}/cloud_$timestamp.db"
        
        if ($LASTEXITCODE -eq 0) {
            ssh -i $SSH_KEY $REMOTE_HOST "sudo docker cp ${REMOTE_BACKUP_DIR}/cloud_$timestamp.db snmp-collector:/data/snmp_metrics.db"
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] OK DB enviado para nuvem" -ForegroundColor Green
        } else {
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] ERRO ao enviar para nuvem" -ForegroundColor Red
        }
    } else {
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] ERRO ao extrair DB local" -ForegroundColor Red
    }
}

function Sync-CloudToLocal {
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Baixando DB da Oracle Cloud..." -ForegroundColor Yellow
    
    $remoteTemp = "${REMOTE_BACKUP_DIR}/remote_$timestamp.db"
    ssh -i $SSH_KEY $REMOTE_HOST "sudo docker cp snmp-collector:/data/snmp_metrics.db $remoteTemp"
    
    if ($LASTEXITCODE -eq 0) {
        $cloudBackup = Join-Path $LOCAL_BACKUP_DIR "cloud_$timestamp.db"
        scp -i $SSH_KEY "${REMOTE_HOST}:${remoteTemp}" $cloudBackup
        
        if ($LASTEXITCODE -eq 0) {
            $size = (Get-Item $cloudBackup).Length / 1KB
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] OK DB da nuvem baixado: $([math]::Round($size, 2)) KB" -ForegroundColor Green
            
            docker cp $cloudBackup snmp-collector:/data/snmp_metrics.db
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] OK Container local atualizado" -ForegroundColor Green
        } else {
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] ERRO ao baixar DB da nuvem" -ForegroundColor Red
        }
        
        ssh -i $SSH_KEY $REMOTE_HOST "rm -f $remoteTemp"
    } else {
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] ERRO ao extrair DB da nuvem" -ForegroundColor Red
    }
}

switch ($Mode) {
    'push' { 
        Write-Host "AVISO: Push sobrescreve dados na nuvem!" -ForegroundColor Red
        $confirm = Read-Host "Confirmar? (s/N)"
        if ($confirm -eq 's') { Sync-LocalToCloud }
    }
    'pull' { 
        Write-Host "AVISO: Pull sobrescreve dados locais!" -ForegroundColor Red
        $confirm = Read-Host "Confirmar? (s/N)"
        if ($confirm -eq 's') { Sync-CloudToLocal }
    }
    'both' {
        Write-Host "Modo MERGE (mescla dados)..." -ForegroundColor Cyan
        docker cp snmp-collector:/data/snmp_metrics.db "$LOCAL_BACKUP_DIR\local_current.db"
        ssh -i $SSH_KEY $REMOTE_HOST "sudo docker cp snmp-collector:/data/snmp_metrics.db ${REMOTE_BACKUP_DIR}/cloud_current.db"
        scp -i $SSH_KEY "${REMOTE_HOST}:${REMOTE_BACKUP_DIR}/cloud_current.db" "$LOCAL_BACKUP_DIR\cloud_current.db"
        
        $localSize = (Get-Item "$LOCAL_BACKUP_DIR\local_current.db").Length / 1KB
        $cloudSize = (Get-Item "$LOCAL_BACKUP_DIR\cloud_current.db").Length / 1KB
        
        Write-Host "DB Local: $([math]::Round($localSize, 2)) KB" -ForegroundColor Cyan
        Write-Host "DB Nuvem: $([math]::Round($cloudSize, 2)) KB" -ForegroundColor Cyan
        Write-Host ""
        
        # Fazer merge
        Write-Host "Mesclando bancos de dados..." -ForegroundColor Yellow
        $merged = "$LOCAL_BACKUP_DIR\merged_$timestamp.db"
        Copy-Item "$LOCAL_BACKUP_DIR\local_current.db" $merged -Force
        
        docker cp "$LOCAL_BACKUP_DIR\cloud_current.db" snmp-collector:/tmp/cloud.db
        docker cp $merged snmp-collector:/tmp/merged.db
        docker exec snmp-collector sqlite3 /tmp/merged.db "ATTACH DATABASE '/tmp/cloud.db' AS cloud; INSERT OR IGNORE INTO metrics SELECT * FROM cloud.metrics; INSERT OR REPLACE INTO last_metrics SELECT * FROM cloud.last_metrics; DETACH DATABASE cloud;"
        docker cp snmp-collector:/tmp/merged.db $merged
        
        $mergedSize = (Get-Item $merged).Length / 1KB
        Write-Host "DB Mesclado: $([math]::Round($mergedSize, 2)) KB" -ForegroundColor Green
        
        # Aplicar em ambos
        docker cp $merged snmp-collector:/data/snmp_metrics.db
        scp -i $SSH_KEY $merged "${REMOTE_HOST}:/tmp/merged.db"
        ssh -i $SSH_KEY $REMOTE_HOST "sudo docker cp /tmp/merged.db snmp-collector:/data/snmp_metrics.db"
        Write-Host "OK Banco mesclado aplicado em ambos" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "======================================"  -ForegroundColor Cyan
Write-Host "  Sincronizacao concluida!" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
