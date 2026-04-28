"""
Sourcing System — 信号管理 API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ..core.database import get_db
from ..models.schemas import Signal, SignalStatus

router = APIRouter(prefix="/signals", tags=["Signals"])

# ─── Pydantic Schemas ───

class SignalCreate(BaseModel):
    source: str
    raw_content: str
    url: Optional[str] = None
    author: Optional[str] = None
    sector: Optional[str] = None
    tags: Optional[List[str]] = []

class SignalOut(BaseModel):
    id: str
    source: str
    raw_content: str
    mentioned_company: Optional[str]
    sector: Optional[str]
    status: str
    confidence: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# ─── Endpoints ───

@router.get("", response_model=List[SignalOut])
def list_signals(
    status: Optional[str] = None,
    sector: Optional[str] = None,
    source: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """获取信号列表，支持筛选"""
    query = db.query(Signal)
    if status:
        query = query.filter(Signal.status == status)
    if sector:
        query = query.filter(Signal.sector == sector)
    if source:
        query = query.filter(Signal.source == source)
    
    total = query.count()
    signals = query.order_by(Signal.created_at.desc()).offset(offset).limit(limit).all()
    return signals

@router.get("/stats")
def signal_stats(db: Session = Depends(get_db)):
    """信号统计"""
    total = db.query(Signal).count()
    today = db.query(Signal).filter(
        Signal.created_at >= datetime.now().replace(hour=0, minute=0, second=0)
    ).count()
    by_status = {}
    for s in SignalStatus:
        by_status[s.value] = db.query(Signal).filter(Signal.status == s.value).count()
    by_source = {}
    for row in db.query(Signal.source, db.func.count(Signal.id)).group_by(Signal.source).all():
        by_source[row[0]] = row[1]
    
    return {
        "total": total,
        "today": today,
        "by_status": by_status,
        "by_source": by_source,
    }

@router.post("", response_model=SignalOut)
def create_signal(data: SignalCreate, db: Session = Depends(get_db)):
    """手动创建信号"""
    signal = Signal(
        source=data.source,
        raw_content=data.raw_content,
        url=data.url,
        author=data.author,
        sector=data.sector,
        tags=data.tags,
        status=SignalStatus.RAW.value,
    )
    db.add(signal)
    db.commit()
    db.refresh(signal)
    return signal

@router.get("/{signal_id}", response_model=SignalOut)
def get_signal(signal_id: str, db: Session = Depends(get_db)):
    """获取单个信号详情"""
    signal = db.query(Signal).filter(Signal.id == signal_id).first()
    if not signal:
        raise HTTPException(status_code=404, detail="Signal not found")
    return signal

@router.delete("/{signal_id}")
def delete_signal(signal_id: str, db: Session = Depends(get_db)):
    """删除信号"""
    signal = db.query(Signal).filter(Signal.id == signal_id).first()
    if not signal:
        raise HTTPException(status_code=404, detail="Signal not found")
    db.delete(signal)
    db.commit()
    return {"deleted": True}

from fastapi import HTTPException
