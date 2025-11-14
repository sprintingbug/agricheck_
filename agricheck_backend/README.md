# AgriCheck Backend API

FastAPI backend server for the AgriCheck plant disease detection application.

## ⚠️ IMPORTANT: Start Backend Server First!

**The backend server MUST be running before using the Flutter app.**
**Without the backend running, login and sign up will fail!**

## Quick Start (3 Steps)

```bash
# 1. Navigate to backend directory
cd agricheck_backend

# 2. Activate virtual environment
.venv\Scripts\activate

# 3. Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Keep this terminal window open!** The server needs to stay running.

## Full Setup Instructions

### 1. Create Virtual Environment (if not already created)

```bash
# Navigate to backend directory
cd agricheck_backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment (Optional)

The backend uses SQLite by default. If you need to change database settings, edit `app/core/config.py`.

### 4. Start the Server

```bash
# From the agricheck_backend directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Verify Backend is Running

1. **Check health endpoint:**
   - Open browser: `http://localhost:8000/health`
   - Should return: `{"status":"ok"}`

2. **Check API docs:**
   - Open: `http://localhost:8000/docs`
   - Should show Swagger UI with all endpoints

Or using Python module:

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Server Information

- **Base URL**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc` (ReDoc)
- **Health Check**: `http://localhost:8000/health`

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/forgot-password-security-questions` - Get security questions
- `POST /auth/verify-security-answer` - Verify security answer
- `POST /auth/reset-password-security-questions` - Reset password

### Users
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update user profile
- `GET /users/stats` - Get user statistics

### Scans
- `POST /scans/scan` - Upload and scan an image
- `GET /scans/history` - Get scan history (with pagination, filtering, sorting)
- `GET /scans/image/{scan_id}` - Get scan image
- `GET /scans/diseases` - Get unique disease names

## Database

- **Type**: SQLite (default)
- **Location**: `agricheck.db` in the backend directory
- Tables are automatically created on first run

## File Uploads

- **Upload Directory**: `uploads/` in the backend directory
- Images are stored with UUID filenames

## CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:8080`
- `http://localhost:3000`
- `http://localhost:52835` (Flutter web dev server)
- `http://localhost:61558` (Flutter web dev server)
- And any origin if `CORS_ORIGINS` is set to `*`

## Troubleshooting

### Port Already in Use
If port 8000 is already in use, you can change it:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```
Then update the frontend `api_service.dart` baseUrl accordingly.

### Module Not Found Errors
Make sure you're in the virtual environment and all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Database Errors
If you encounter database errors, you can delete `agricheck.db` and restart the server to recreate tables.

## Development

The server runs with `--reload` flag for automatic reloading on code changes.

## Production

For production, remove `--reload` and use a production ASGI server like Gunicorn with Uvicorn workers.

