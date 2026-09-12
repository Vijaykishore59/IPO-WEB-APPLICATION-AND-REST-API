from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from app.api import auth, ipos
from app.core.config import settings
from app.db.session import Base, SessionLocal, engine
from app.models import IPO, User
from app.services.seed import seed_admin, seed_csv

app = FastAPI(title=settings.app_name, version="1.0.0", description="Production-ready IPO information REST API")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_list, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(ipos.router, prefix="/api/v1")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_admin(db)
        csv_path = Path(__file__).resolve().parents[2] / "sample_ipos.csv"
        if csv_path.exists(): seed_csv(db, str(csv_path))
        db.commit()
    finally: db.close()

@app.get("/health", tags=["System"])
def health():
    db = SessionLocal()
    try: db.execute(text("SELECT 1")); return {"status":"ok", "database":"ok"}
    finally: db.close()
