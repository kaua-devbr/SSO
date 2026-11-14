$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$dockerCommand = Get-Command docker -ErrorAction SilentlyContinue
if ($dockerCommand) { $script:DockerExe = $dockerCommand.Source } else {
    $locations = @(
        "$env:ProgramFiles\Docker\Docker\resources\bin\docker.exe",
        "$env:LOCALAPPDATA\Programs\DockerDesktop\resources\bin\docker.exe",
        "$env:LOCALAPPDATA\Docker\resources\bin\docker.exe"
    )
    $script:DockerExe = $locations | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
}
if (-not $script:DockerExe) {
    throw 'Docker nao encontrado nesta sessao. Abra Docker Desktop e reabra o terminal. Confira docker --version.'
}
function Invoke-Docker {
    & $script:DockerExe @args
    if ($LASTEXITCODE -ne 0) { throw "Docker falhou (codigo $LASTEXITCODE). Veja a mensagem acima." }
}
# Windows PowerShell trata stderr nativo como erro: consultar o motor com politica temporaria.
$oldPreference = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
$engineType = & $script:DockerExe info --format '{{.OSType}}' 2>$null
$engineExit = $LASTEXITCODE
$ErrorActionPreference = $oldPreference
if ($engineExit -ne 0) { throw 'Docker instalado, mas o motor nao respondeu. Abra Docker Desktop e aguarde; confira WSL 2.' }
if ($engineType -ne 'linux') { throw 'Selecione Linux containers no Docker Desktop.' }
Invoke-Docker compose version
