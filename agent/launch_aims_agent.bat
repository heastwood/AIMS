@echo off
cd /d "c:\Users\HEastwoo\OneDrive - Quadient\Claude and Claude Projects\AIMS\agent"
start "AIMS Agent" cmd /k streamlit run app.py --server.headless true --server.address 0.0.0.0 --server.port 8501
timeout /t 4 /nobreak > nul
start "" http://localhost:8501
