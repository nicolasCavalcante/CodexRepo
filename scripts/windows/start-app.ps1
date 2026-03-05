Param(
    [string]$ApiUrl = "http://127.0.0.1:8000/v1",
    [int]$Port = 8501
)

$env:API_URL = $ApiUrl
python -m streamlit run app/streamlit_app.py --server.address 127.0.0.1 --server.port $Port
