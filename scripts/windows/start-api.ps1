Param(
    [string]$Host = "127.0.0.1",
    [int]$Port = 8000,
    [string]$DatabaseUrl = "sqlite:///./crud_app.db"
)

$env:DATABASE_URL = $DatabaseUrl
python -m uvicorn app.main:app --host $Host --port $Port --reload
