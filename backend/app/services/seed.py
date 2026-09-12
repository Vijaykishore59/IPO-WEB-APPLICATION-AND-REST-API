from datetime import date
import csv
from decimal import Decimal
from pathlib import Path
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import hash_password
from app.models import IPO, User

def seed_admin(db: Session):
    if not db.query(User).filter(User.email == settings.admin_email).first():
        db.add(User(email=settings.admin_email, password_hash=hash_password(settings.admin_password), is_admin=True))

def seed_csv(db: Session, csv_path: str):
    if db.query(IPO).count() > 0: return
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            def dec(k): return Decimal(row[k]) if row.get(k) else None
            def dt(k): return date.fromisoformat(row[k]) if row.get(k) else None
            db.add(IPO(company_name=row["company_name"], price_band_min=dec("price_min"), price_band_max=dec("price_max"), open_date=dt("open_date"), close_date=dt("close_date"), listing_date=dt("listing_date"), issue_size=row.get("issue_size"), issue_type=row.get("issue_type"), status=row.get("status", "upcoming"), ipo_price=dec("ipo_price"), listing_price=dec("listing_price"), cmp=dec("cmp")))
    db.commit()
