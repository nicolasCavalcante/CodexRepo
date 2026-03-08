Param(
    [string]$Host = "127.0.0.1",
    [int]$Port = 8000,
    [string]$DatabaseUrl
)

function Import-DotEnv {
    param([string]$Path)
    if (-not (Test-Path $Path)) {
        return
    }

    Get-Content $Path | ForEach-Object {
        $line = $_.Trim()
        if (-not $line -or $line.StartsWith("#") -or -not $line.Contains("=")) {
            return
        }

        $parts = $line.Split("=", 2)
        $key = $parts[0].Trim()
        $value = $parts[1].Trim().Trim('"').Trim("'")
        if ($key) {
            Set-Item -Path "Env:$key" -Value $value
        }
    }
}

$envPath = Join-Path $PSScriptRoot "..\..\.env"
Import-DotEnv -Path $envPath

if (-not $DatabaseUrl) {
    $DatabaseUrl = $env:DATABASE_URL
}
if (-not $DatabaseUrl) {
    throw "DATABASE_URL não definida. Configure no .env ou via -DatabaseUrl."
}

$env:DATABASE_URL = $DatabaseUrl
python -m uvicorn app.main:app --host $Host --port $Port --reload
