from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import Base, engine
from app.auth.routes import router as auth_router
from app.users.routes import router as users_router
from app.scans.routes import router as scans_router



app = FastAPI(title="Agricheck API", version="0.1.0")

# CORS
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
# Add explicit Flutter web origins
allowed_origins = origins if origins else ["*"]
if "*" not in allowed_origins:
    allowed_origins.extend([
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:52835",  # Flutter web dev server port
        "http://127.0.0.1:52835",
        "http://localhost:61558",  # Flutter web dev server port
        "http://127.0.0.1:61558",
    ])
# If CORS_ORIGINS is "*", allow all origins
if "*" in allowed_origins:
    allowed_origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables (simple start; you can switch to Alembic later)
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

# Routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router)
app.include_router(scans_router)