param([switch]$Offline)
. "$PSScriptRoot\docker-comum.ps1"
if ($Offline) {
    if (-not (Test-Path offline/imagens.tar) -or -not (Test-Path offline/manifest.json)) {
        throw 'Falta o pacote offline. Exporte-o em uma maquina com internet usando exportar-offline.ps1.'
    }
    $manifest = Get-Content offline/manifest.json -Raw | ConvertFrom-Json
    $hash = (Get-FileHash offline/imagens.tar -Algorithm SHA256).Hash.ToLower()
    if ($hash -ne $manifest.sha256) { throw 'Hash do pacote offline nao confere. Copie o arquivo novamente.' }
    $arch = Invoke-Docker info --format '{{.Architecture}}'
    if ($arch -eq 'x86_64') { $arch = 'amd64' }
    if ($arch -eq 'aarch64') { $arch = 'arm64' }
    if ($arch -ne $manifest.architecture) { throw 'Pacote offline de outra arquitetura. Exporte para a arquitetura deste computador.' }
    Invoke-Docker load -i offline/imagens.tar
} else {
    Invoke-Docker build --pull -t unifica-portal:demo .
    Invoke-Docker pull quay.io/keycloak/keycloak:26.8.2
}
# O Python e executado dentro da imagem, nao precisa existir no Windows.
$projectPath = (Get-Location).Path
Invoke-Docker run --rm --user 0 --mount "type=bind,source=$projectPath,target=/workspace" --workdir /workspace --entrypoint python unifica-portal:demo scripts/configurar_demo.py
# --quiet valida sem imprimir senhas interpoladas no terminal.
Invoke-Docker compose config --quiet
Write-Host 'Preparado. Execute .\scripts\iniciar.ps1. Contas locais: .demo\acessos.txt'
