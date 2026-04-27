"""
Sourcing System — IC 会议 API
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ..core.database import get_db
from ..models.schemas import ICMeeting, ICMeetingVote, Company

router = APIRouter(prefix="/ic-meetings", tags=["IC Meetings"])

# ─── Pydantic Schemas ───

class ICMeetingOut(BaseModel):
    id: str
    company_id: str
    meeting_date: datetime
    week_number: int
    total_votes: int
    invest_votes: int
    pass_votes: int
    final_score: Optional[float]
    decision_signal: Optional[str]
    outcome: Optional[str]
    summary: Optional[str]
    key_concerns: Optional[List[str]]
    key_strengths: Optional[List[str]]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ICMeetingVoteOut(BaseModel):
    id: str
    meeting_id: str
    agent_id: str
    agent_name: str
    agent_role: str
    score: float
    vote: str
    reasoning: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# ─── Endpoints ───

@router.get("", response_model=List[ICMeetingOut])
def list_ic_meetings(
    company_id: Optional[str] = None,
    week: Optional[int] = None,
    outcome: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """获取IC会议列表"""
    query = db.query(ICMeeting)
    if company_id:
        query = query.filter(ICMeeting.company_id == company_id)
    if week:
        query = query.filter(ICMeeting.week_number == week)
    if outcome:
        query = query.filter(ICMeeting.outcome == outcome)
    
    meetings = query.order_by(ICMeeting.created_at.desc()).offset(offset).limit(limit).all()
    return meetings

@router.get("/weekly-ranking")
def weekly_ranking(
    week: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """
    每周IC排名 — 复刻原系统功能
    """
    if week is None:
        week = datetime.now().isocalendar()[1]
    
    meetings = db.query(ICMeeting).filter(
        ICMeeting.week_number == week
    ).order_by(ICMeeting.final_score.desc()).all()
    
    results = []
    for rank, m in enumerate(meetings, 1):
        company = db.query(Company).filter(Company.id == m.company_id).first()
        results.append({
            "final_rank": rank,
            "company_name": company.name if company else "Unknown",
            "sector": company.sector if company else "Unknown",
            "meeting_date": m.meeting_date.isoformat() if m.meeting_date else None,
            "invest_votes": m.invest_votes,
            "total_votes": m.total_votes,
            "final_score": m.final_score,
            "decision_signal": m.decision_signal,
            "outcome": m.outcome,
        })
    
    return {
        "week": week,
        "total": len(results),
        "rankings": results,
    }

@router.get("/{meeting_id}", response_model=ICMeetingOut)
def get_meeting(meeting_id: str, db: Session = Depends(get_db)):
    """获取会议详情"""
    meeting = db.query(ICMeeting).filter(ICMeeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting

@router.get("/{meeting_id}/votes", response_model=List[ICMeetingVoteOut])
def get_meeting_votes(meeting_id: str, db: Session = Depends(get_db)):
    """获取会议投票明细"""
    votes = db.query(ICMeetingVote).filter(ICMeetingVote.meeting_id == meeting_id).all()
    return votes
