$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$pythonDemo = Join-Path (Get-Location) '.venv\Scripts\python.exe'
if (-not (Test-Path $pythonDemo)) { throw 'Execute preparar.ps1 com internet primeiro.' }
New-Item -ItemType Directory -Force offline/wheels | Out-Null
& $pythonDemo -m pip download --only-binary=:all: --dest offline/wheels -r requirements-lock.txt
if ($LASTEXITCODE -ne 0) { throw 'Falha ao baixar pacotes Python.' }
docker save -o offline/keycloak.tar quay.io/keycloak/keycloak:26.8.2
if ($LASTEXITCODE -ne 0) { throw 'Falha ao exportar a imagem.' }
& $pythonDemo -c "import platform; print(platform.python_version(), platform.machine())" | Set-Content offline/ambiente.txt
Get-FileHash offline/keycloak.tar,offline/wheels/* -Algorithm SHA256 | Format-Table -AutoSize | Out-String -Width 300 | Set-Content offline/SHA256.txt
Write-Host 'Copie o projeto e offline para o notebook, sem .venv, .git ou .demo. Use a mesma versao/arquitetura Python; veja offline/ambiente.txt.'
