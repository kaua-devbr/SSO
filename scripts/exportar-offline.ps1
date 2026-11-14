. "$PSScriptRoot\docker-comum.ps1"
New-Item -ItemType Directory -Force offline | Out-Null
$portalArch = Invoke-Docker image inspect unifica-portal:demo --format '{{.Architecture}}'
$keycloakArch = Invoke-Docker image inspect quay.io/keycloak/keycloak:26.8.2 --format '{{.Architecture}}'
$mysqlArch = Invoke-Docker image inspect mysql:8.4 --format '{{.Architecture}}'
if ($portalArch -ne $keycloakArch -or $portalArch -ne $mysqlArch) { throw 'As imagens precisam ter a mesma arquitetura.' }
Invoke-Docker save -o offline/imagens.tar unifica-portal:demo quay.io/keycloak/keycloak:26.8.2 mysql:8.4
$manifest = @{
    architecture = $portalArch
    sha256 = (Get-FileHash offline/imagens.tar -Algorithm SHA256).Hash.ToLower()
    images = @('unifica-portal:demo','quay.io/keycloak/keycloak:26.8.2','mysql:8.4')
}
$manifest | ConvertTo-Json | Set-Content offline/manifest.json -Encoding ASCII
Write-Host 'Copie o projeto e offline. Nao copie .demo, .env, .venv ou .git. No destino: preparar.ps1 -Offline.'
