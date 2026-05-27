@echo off
FOR /F "tokens=5" %%P IN ('netstat -ano ^| findstr :8501') DO taskkill /F /PID %%P
echo AIMS Agent stopped.
timeout /t 2
