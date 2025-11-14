# 🚀 How to Start the Backend Server

## Quick Start

```bash
cd agricheck_backend
.venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Step-by-Step

1. **Open terminal/PowerShell**
2. **Navigate to backend directory:**
   ```bash
   cd C:\dev\agricheck_backend
   ```

3. **Activate virtual environment:**
   ```bash
   .venv\Scripts\activate
   ```
   You should see `(.venv)` in your prompt.

4. **Start the server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Verify it's running:**
   - You should see: `Uvicorn running on http://0.0.0.0:8000`
   - Open browser: `http://localhost:8000/docs` to see API documentation

## Troubleshooting

### Backend Not Starting?

**Check if port 8000 is in use:**
```bash
netstat -ano | findstr :8000
```

**If port is in use, kill the process or use a different port:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```
Then update Flutter `api_service.dart` to use port 8001.

### Missing Dependencies?

```bash
pip install -r requirements.txt
```

### Database Issues?

```bash
python -c "from app.db.session import engine; from app.db.models import Base; Base.metadata.create_all(engine); print('Database ready')"
```

## Verify Backend is Running

1. **Check health endpoint:**
   - Open: `http://localhost:8000/health`
   - Should return: `{"status":"ok"}`

2. **Check API docs:**
   - Open: `http://localhost:8000/docs`
   - Should show Swagger UI with all endpoints

## After Starting Backend

Once the backend is running, you can:
- ✅ Login through Flutter app
- ✅ Register new users
- ✅ Use all features

**Keep the terminal open** - the server needs to stay running!

