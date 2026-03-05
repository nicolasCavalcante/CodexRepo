Param(
    [string]$Host = "127.0.0.1",
    [int]$Port = 8000,
    [string]$DatabaseUrl = "postgresql+psycopg://postgres:postgres@127.0.0.1:5432/crud_app"
)

$env:DATABASE_URL = $DatabaseUrl
python -m uvicorn app.main:app --host $Host --port $Port --reload
