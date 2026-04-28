"""
Sourcing System — 报告管理 API
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from ..core.database import get_db
from ..models.schemas import InvestmentReport, RiskReport

router = APIRouter(prefix="/reports", tags=["Reports"])

# ─── Pydantic Schemas ───

class InvestmentReportOut(BaseModel):
    id: str
    company_id: str
    agent_id: str
    agent_name: Optional[str]
    tam: Optional[str]
    sam: Optional[str]
    som: Optional[str]
    market_position: Optional[str]
    team_summary: Optional[str]
    investor_background: Optional[str]
    product_analysis: Optional[str]
    traction: Optional[str]
    moat: Optional[str]
    overall_score: Optional[float]
    recommendation: Optional[str]
    conviction: Optional[float]
    created_at: str
    
    class Config:
        from_attributes = True

class RiskReportOut(BaseModel):
    id: str
    company_id: str
    agent_id: str
    agent_name: Optional[str]
    risk_level: Optional[float]
    red_flags: Optional[List[str]]
    mitigations: Optional[str]
    created_at: str
    
    class Config:
        from_attributes = True

# ─── Endpoints ───

@router.get("/investment", response_model=List[InvestmentReportOut])
def list_investment_reports(
    company_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    min_score: Optional[float] = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """获取DD报告列表"""
    query = db.query(InvestmentReport)
    if company_id:
        query = query.filter(InvestmentReport.company_id == company_id)
    if agent_id:
        query = query.filter(InvestmentReport.agent_id == agent_id)
    if min_score:
        query = query.filter(InvestmentReport.overall_score >= min_score)
    
    reports = query.order_by(InvestmentReport.created_at.desc()).limit(limit).all()
    return reports

@router.get("/investment/{report_id}", response_model=InvestmentReportOut)
def get_investment_report(report_id: str, db: Session = Depends(get_db)):
    """获取DD报告详情"""
    report = db.query(InvestmentReport).filter(InvestmentReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.get("/risk", response_model=List[RiskReportOut])
def list_risk_reports(
    company_id: Optional[str] = None,
    max_risk: Optional[float] = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """获取风险报告列表"""
    query = db.query(RiskReport)
    if company_id:
        query = query.filter(RiskReport.company_id == company_id)
    if max_risk:
        query = query.filter(RiskReport.risk_level <= max_risk)
    
    reports = query.order_by(RiskReport.created_at.desc()).limit(limit).all()
    return reports

@router.get("/risk/{report_id}", response_model=RiskReportOut)
def get_risk_report(report_id: str, db: Session = Depends(get_db)):
    """获取风险报告详情"""
    report = db.query(RiskReport).filter(RiskReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
