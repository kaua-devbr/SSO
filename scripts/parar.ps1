$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$expected = Join-Path (Get-Location) '.venv\Scripts\python.exe'
if (Test-Path .demo/processos.json) {
    foreach ($processId in (Get-Content .demo/processos.json | ConvertFrom-Json)) {
        $process = Get-CimInstance Win32_Process -Filter "ProcessId = $processId" -ErrorAction SilentlyContinue
        if ($process -and $process.ExecutablePath -eq $expected -and $process.CommandLine -match 'waitress.*(app|biblioteca):app') {
            Stop-Process -Id $processId
        }
    }
    Remove-Item -LiteralPath .demo/processos.json
}
docker compose stop
if ($LASTEXITCODE -ne 0) { throw 'Nao foi possivel parar o Keycloak.' }
Write-Host 'Servicos parados. Chaves e dados preservados.'
