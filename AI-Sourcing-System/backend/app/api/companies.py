"""
Sourcing System — 公司管理 API
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ..core.database import get_db
from ..models.schemas import Company, CompanyStatus, ContactStatus

router = APIRouter(prefix="/companies", tags=["Companies"])

# ─── Pydantic Schemas ───

class CompanyCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    sector: Optional[str] = "AI"
    website: Optional[str] = None
    stage: Optional[str] = None

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    sector: Optional[str] = None
    stage: Optional[str] = None
    contact_status: Optional[str] = None
    contact_person: Optional[str] = None
    contact_notes: Optional[str] = None
    status: Optional[str] = None

class CompanyOut(BaseModel):
    id: str
    name: str
    slug: str
    description: Optional[str]
    sector: Optional[str]
    stage: Optional[str]
    status: str
    contact_status: str
    assigned_manager: Optional[str]
    avg_ic_score: Optional[float]
    final_decision: Optional[str]
    decision_signal: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# ─── Endpoints ───

@router.get("", response_model=List[CompanyOut])
def list_companies(
    status: Optional[str] = None,
    sector: Optional[str] = None,
    manager: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """获取公司列表"""
    query = db.query(Company)
    if status:
        query = query.filter(Company.status == status)
    if sector:
        query = query.filter(Company.sector == sector)
    if manager:
        query = query.filter(Company.assigned_manager == manager)
    if search:
        query = query.filter(Company.name.contains(search))
    
    total = query.count()
    companies = query.order_by(Company.created_at.desc()).offset(offset).limit(limit).all()
    return companies

@router.get("/stats")
def company_stats(db: Session = Depends(get_db)):
    """公司统计"""
    total = db.query(Company).count()
    by_status = {}
    for s in CompanyStatus:
        by_status[s.value] = db.query(Company).filter(Company.status == s.value).count()
    by_sector = {}
    for row in db.query(Company.sector, db.func.count(Company.id)).group_by(Company.sector).all():
        by_sector[row[0] or "Unknown"] = row[1]
    by_manager = {}
    for row in db.query(Company.assigned_manager, db.func.count(Company.id)).group_by(Company.assigned_manager).all():
        by_manager[row[0] or "Unassigned"] = row[1]
    
    return {
        "total": total,
        "by_status": by_status,
        "by_sector": by_sector,
        "by_manager": by_manager,
    }

@router.post("", response_model=CompanyOut)
def create_company(data: CompanyCreate, db: Session = Depends(get_db)):
    """手动创建公司"""
    company = Company(
        name=data.name,
        slug=data.name.lower().replace(" ", "-"),
        description=data.description,
        sector=data.sector,
        website=data.website,
        stage=data.stage,
        status=CompanyStatus.SOURCING.value,
        contact_status=ContactStatus.NOT_CONTACTED.value,
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company

@router.get("/{company_id}", response_model=CompanyOut)
def get_company(company_id: str, db: Session = Depends(get_db)):
    """获取公司详情"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.patch("/{company_id}", response_model=CompanyOut)
def update_company(company_id: str, data: CompanyUpdate, db: Session = Depends(get_db)):
    """更新公司信息"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    for field, value in data.dict(exclude_unset=True).items():
        setattr(company, field, value)
    
    db.commit()
    db.refresh(company)
    return company

@router.delete("/{company_id}")
def delete_company(company_id: str, db: Session = Depends(get_db)):
    """删除公司"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(company)
    db.commit()
    return {"deleted": True}
