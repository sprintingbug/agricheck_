@echo off
cd /d D:\dev\agricheck_backend
call .venv\Scripts\activate.bat
echo Starting Agricheck Backend Server...
echo Backend will be available at http://192.168.1.10:8000
echo.
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause

