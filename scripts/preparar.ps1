param([switch]$Offline)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw 'Instale Python 3.12 de 64 bits com PATH.' }
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw 'Instale e inicie Docker Desktop com contêineres Linux.' }
docker info *> $null
if ($LASTEXITCODE -ne 0) { throw 'Inicie o Docker Desktop e aguarde o motor ficar pronto.' }
python -m venv .venv
if ($LASTEXITCODE -ne 0) { throw 'Falha ao criar ambiente Python.' }
$pythonDemo = Join-Path (Get-Location) '.venv\Scripts\python.exe'
if ($Offline) {
    if (-not (Test-Path offline/keycloak.tar)) { throw 'Falta offline/keycloak.tar. Execute exportar-offline.ps1 antes, com internet.' }
    & $pythonDemo -m pip install --no-index --find-links offline/wheels -r requirements-lock.txt
} else {
    & $pythonDemo -m pip install -r requirements-lock.txt
}
if ($LASTEXITCODE -ne 0) { throw 'Falha ao instalar dependencias; confira Python e pacote offline.' }
& $pythonDemo scripts/configurar_demo.py
if ($LASTEXITCODE -ne 0) { throw 'Falha na configuracao local.' }
if ($Offline) { docker load -i offline/keycloak.tar } else { docker compose pull }
if ($LASTEXITCODE -ne 0) { throw 'Falha ao preparar imagem Keycloak.' }
Write-Host 'Preparado. Execute .\scripts\iniciar.ps1 e consulte .demo\acessos.txt.'
