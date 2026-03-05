@echo off
set API_URL=http://127.0.0.1:8000/v1
python -m streamlit run app/streamlit_app.py --server.address 127.0.0.1 --server.port 8501
