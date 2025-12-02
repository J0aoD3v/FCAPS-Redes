# Servidor HTTP simples para o Dashboard FCAPS
# Execute: .\scripts\start-dashboard.ps1

Write-Host ""
Write-Host "=== Iniciando FCAPS Dashboard ===" -ForegroundColor Cyan
Write-Host ""

$port = 3000
$path = "$PSScriptRoot\..\dashboard"

Write-Host "Dashboard disponivel em: http://localhost:$port" -ForegroundColor Green
Write-Host "Zabbix API: http://localhost:8080" -ForegroundColor Yellow
Write-Host ""
Write-Host "Pressione Ctrl+C para parar o servidor" -ForegroundColor Gray
Write-Host ""

# Verifica se Python está disponível
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue

if ($pythonCmd) {
    Set-Location $path
    python -m http.server $port
} else {
    # Fallback: PowerShell HTTP Server
    Write-Host "Python nao encontrado, usando servidor PowerShell..." -ForegroundColor Yellow
    
    $listener = New-Object System.Net.HttpListener
    $listener.Prefixes.Add("http://localhost:$port/")
    $listener.Start()
    
    Write-Host "Servidor PowerShell iniciado!" -ForegroundColor Green
    
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response
        
        $file = Join-Path $path "index.html"
        
        if (Test-Path $file) {
            $content = [System.IO.File]::ReadAllBytes($file)
            $response.ContentType = "text/html"
            $response.ContentLength64 = $content.Length
            $response.OutputStream.Write($content, 0, $content.Length)
        }
        
        $response.Close()
    }
}
