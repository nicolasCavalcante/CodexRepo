Param(
    [string]$ApiUrl,
    [int]$Port = 8501
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

if (-not $ApiUrl) {
    $ApiUrl = $env:API_URL
}
if (-not $ApiUrl) {
    throw "API_URL não definida. Configure no .env ou via -ApiUrl."
}

$env:API_URL = $ApiUrl
python -m streamlit run app/streamlit_app.py --server.address 127.0.0.1 --server.port $Port
