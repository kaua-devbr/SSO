. "$PSScriptRoot\docker-comum.ps1"
Invoke-Docker compose stop
Write-Host 'Portal e Keycloak parados. Chaves e volume preservados.'
