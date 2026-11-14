param([switch]$SemNavegador)
. "$PSScriptRoot\docker-comum.ps1"
if (-not (Test-Path .demo/app.env) -or -not (Test-Path .demo/database.env) -or -not (Test-Path .demo/mysql.env)) { throw 'Execute scripts/preparar.ps1 primeiro.' }
Invoke-Docker compose config --quiet
# Sem downloads ou builds ocultos. Keycloak deve ficar saudavel antes do portal.
Invoke-Docker compose up -d --no-build --pull never --wait --wait-timeout 360
Write-Host 'Portal: http://localhost:5000 | Keycloak: http://localhost:8081'
Write-Host 'Contas: .demo/acessos.txt | Logs: docker compose logs --tail 100'
if (-not $SemNavegador) { Start-Process 'http://localhost:5000' }
