cd D:\dev\agricheck_backend
.venv\Scripts\Activate.ps1
Write-Host "Starting Agricheck Backend Server..." -ForegroundColor Green
Write-Host "Backend will be available at http://192.168.1.10:8000" -ForegroundColor Yellow
Write-Host ""
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

