$ErrorActionPreference = 'Stop'

Set-Location "$PSScriptRoot/../../app"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run streamlit_app.py --server.port 8501
