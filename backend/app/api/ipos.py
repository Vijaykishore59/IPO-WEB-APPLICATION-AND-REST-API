from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import require_admin
from app.db.session import get_db
from app.models import IPO
from app.models.user import User
from app.schemas.ipo import IPOCreate, IPOSummary, IPOUpdate
router = APIRouter(prefix="/ipos", tags=["IPOs"])

def to_schema(ipo):
    return IPOSummary.model_validate({**ipo.__dict__, "listing_gain": ipo.listing_gain, "listing_gain_percent": ipo.listing_gain_percent, "current_return": ipo.current_return})

@router.get("", response_model=list[IPOSummary])
def list_ipos(db: Session = Depends(get_db), search: str | None = None, status_filter: str | None = Query(None, alias="status"), issue_type: str | None = None, skip: int = 0, limit: int = Query(20, le=100), sort: str = "open_date"):
    q = db.query(IPO)
    if search: q = q.filter(or_(IPO.company_name.ilike(f"%{search}%"), IPO.issue_size.ilike(f"%{search}%")))
    if status_filter: q = q.filter(IPO.status == status_filter)
    if issue_type: q = q.filter(IPO.issue_type == issue_type)
    column = getattr(IPO, sort.lstrip("-"), IPO.open_date)
    q = q.order_by(column.desc() if sort.startswith("-") else column.asc())
    return [to_schema(x) for x in q.offset(skip).limit(limit).all()]

@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    rows = db.query(IPO).all()
    return {"total": len(rows), "upcoming": sum(x.status=="upcoming" for x in rows), "open": sum(x.status=="open" for x in rows), "closed": sum(x.status=="closed" for x in rows), "listed": sum(x.status=="listed" for x in rows)}

@router.get("/{ipo_id}", response_model=IPOSummary)
def get_ipo(ipo_id: int, db: Session = Depends(get_db)):
    ipo = db.get(IPO, ipo_id)
    if not ipo: raise HTTPException(404, "IPO not found")
    return to_schema(ipo)

@router.post("", response_model=IPOSummary, status_code=201)
def create_ipo(data: IPOCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    ipo = IPO(**data.model_dump()); db.add(ipo); db.commit(); db.refresh(ipo); return to_schema(ipo)

@router.put("/{ipo_id}", response_model=IPOSummary)
def update_ipo(ipo_id: int, data: IPOUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    ipo = db.get(IPO, ipo_id)
    if not ipo: raise HTTPException(404, "IPO not found")
    for k,v in data.model_dump().items(): setattr(ipo,k,v)
    db.commit(); db.refresh(ipo); return to_schema(ipo)

@router.delete("/{ipo_id}", status_code=204)
def delete_ipo(ipo_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    ipo = db.get(IPO, ipo_id)
    if not ipo: raise HTTPException(404, "IPO not found")
    db.delete(ipo); db.commit()

@router.post("/{ipo_id}/documents/{doc_type}")
def upload_document(ipo_id: int, doc_type: str, file: UploadFile = File(...), db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if doc_type not in {"rhp", "drhp"}: raise HTTPException(400, "Document type must be rhp or drhp")
    if file.content_type != "application/pdf": raise HTTPException(400, "Only PDF files are allowed")
    content = file.file.read(settings.max_upload_mb * 1024 * 1024 + 1)
    if len(content) > settings.max_upload_mb * 1024 * 1024: raise HTTPException(413, "File too large")
    ipo = db.get(IPO, ipo_id)
    if not ipo: raise HTTPException(404, "IPO not found")
    folder = Path(settings.upload_dir) / doc_type; folder.mkdir(parents=True, exist_ok=True)
    filename = f"{ipo_id}_{Path(file.filename).name.replace(' ', '_')}"; path = folder / filename; path.write_bytes(content)
    setattr(ipo, f"{doc_type}_pdf", f"/uploads/{doc_type}/{filename}"); db.commit()
    return {"message":"Uploaded", "url":getattr(ipo, f"{doc_type}_pdf")}
