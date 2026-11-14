$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$pythonDemo = Join-Path (Get-Location) '.venv\Scripts\python.exe'
if (-not (Test-Path $pythonDemo) -or -not (Test-Path .demo/app.env)) { throw 'Execute preparar.ps1 primeiro.' }
foreach ($port in @(5000,5001)) {
    if (Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue) {
        throw "Porta $port ocupada. Encerre o servidor anterior antes de iniciar."
    }
}
docker compose up -d --pull never
if ($LASTEXITCODE -ne 0) { throw 'Falha ao iniciar Keycloak. Confira Docker e porta 8081.' }
Write-Host 'Aguardando Keycloak (pode levar alguns minutos)...'
$ready = $false
for ($i = 0; $i -lt 40; $i++) {
    try {
        $null = Invoke-RestMethod 'http://localhost:8081/realms/unifica-demo/.well-known/openid-configuration' -TimeoutSec 2
        $ready = $true
        break
    } catch { Start-Sleep -Seconds 3 }
}
if (-not $ready) { throw 'Keycloak nao ficou pronto. Execute docker compose logs keycloak.' }
$env:UNIFICA_ENV_FILE = (Resolve-Path .demo/app.env).Path
$portalProcess = Start-Process -FilePath $pythonDemo -ArgumentList '-m waitress --listen=127.0.0.1:5000 app:app' -WorkingDirectory (Get-Location).Path -WindowStyle Hidden -PassThru -RedirectStandardOutput '.demo/portal.log' -RedirectStandardError '.demo/portal-error.log'
$libraryProcess = Start-Process -FilePath $pythonDemo -ArgumentList '-m waitress --listen=127.0.0.1:5001 biblioteca:app' -WorkingDirectory (Get-Location).Path -WindowStyle Hidden -PassThru -RedirectStandardOutput '.demo/biblioteca.log' -RedirectStandardError '.demo/biblioteca-error.log'
@($portalProcess.Id,$libraryProcess.Id) | ConvertTo-Json | Set-Content .demo/processos.json
Start-Sleep -Seconds 2
foreach ($port in @(5000,5001)) {
    try { $null = Invoke-WebRequest "http://localhost:$port/" -UseBasicParsing -TimeoutSec 5 }
    catch { throw "Aplicacao na porta $port falhou. Consulte .demo/*-error.log e execute parar.ps1." }
}
Write-Host 'Portal: http://localhost:5000 | Biblioteca: http://localhost:5001'
Start-Process 'http://localhost:5000'
