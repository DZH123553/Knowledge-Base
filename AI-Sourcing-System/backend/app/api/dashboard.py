"""
Sourcing System — 仪表盘数据 API
复刻原系统：总信号数、总公司数、近七日新增、赛道Top5、IC排名
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta

from ..core.database import get_db
from ..models.schemas import Signal, Company, ICMeeting, InvestmentReport

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """仪表盘核心统计"""
    total_signals = db.query(Signal).count()
    total_companies = db.query(Company).count()
    total_reports = db.query(InvestmentReport).count()
    total_meetings = db.query(ICMeeting).count()
    
    # 近7日新增
    week_ago = datetime.now() - timedelta(days=7)
    signals_7d = db.query(Signal).filter(Signal.created_at >= week_ago).count()
    companies_7d = db.query(Company).filter(Company.created_at >= week_ago).count()
    
    # 今日新增
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    signals_today = db.query(Signal).filter(Signal.created_at >= today).count()
    
    # 按赛道统计
    sector_stats = db.query(
        Company.sector,
        func.count(Company.id).label("count")
    ).group_by(Company.sector).order_by(desc("count")).limit(8).all()
    
    # 按状态统计
    status_stats = db.query(
        Company.status,
        func.count(Company.id).label("count")
    ).group_by(Company.status).all()
    
    # 近期IC决议分布
    ic_outcomes = db.query(
        ICMeeting.outcome,
        func.count(ICMeeting.id).label("count")
    ).group_by(ICMeeting.outcome).all()
    
    # 评分分布
    score_ranges = {
        "excellent_8_10": db.query(Company).filter(Company.avg_ic_score >= 8).count(),
        "good_6_8": db.query(Company).filter(Company.avg_ic_score >= 6, Company.avg_ic_score < 8).count(),
        "average_4_6": db.query(Company).filter(Company.avg_ic_score >= 4, Company.avg_ic_score < 6).count(),
        "poor_0_4": db.query(Company).filter(Company.avg_ic_score < 4).count(),
    }
    
    return {
        "overview": {
            "total_signals": total_signals,
            "total_companies": total_companies,
            "total_reports": total_reports,
            "total_meetings": total_meetings,
            "signals_7d": signals_7d,
            "companies_7d": companies_7d,
            "signals_today": signals_today,
        },
        "sectors": [{"name": s[0] or "Unknown", "count": s[1]} for s in sector_stats],
        "status_breakdown": {s[0]: s[1] for s in status_stats},
        "ic_outcomes": {o[0] or "pending": o[1] for o in ic_outcomes},
        "score_distribution": score_ranges,
    }

@router.get("/recent-activity")
def get_recent_activity(limit: int = 20, db: Session = Depends(get_db)):
    """最近活动流"""
    # 最近的信号
    recent_signals = db.query(Signal).order_by(Signal.created_at.desc()).limit(limit).all()
    
    # 最近的公司
    recent_companies = db.query(Company).order_by(Company.created_at.desc()).limit(limit).all()
    
    # 最近的IC会议
    recent_meetings = db.query(ICMeeting).order_by(ICMeeting.created_at.desc()).limit(limit).all()
    
    activities = []
    
    for s in recent_signals:
        activities.append({
            "type": "signal",
            "time": s.created_at.isoformat() if s.created_at else None,
            "title": f"新信号: {s.mentioned_company or 'Unknown'}",
            "source": s.source,
            "status": s.status,
        })
    
    for c in recent_companies:
        activities.append({
            "type": "company",
            "time": c.created_at.isoformat() if c.created_at else None,
            "title": f"新公司: {c.name}",
            "sector": c.sector,
            "status": c.status,
            "manager": c.assigned_manager,
        })
    
    for m in recent_meetings:
        activities.append({
            "type": "ic_meeting",
            "time": m.meeting_date.isoformat() if m.meeting_date else None,
            "title": f"IC决议: 分数={m.final_score}, 结果={m.outcome}",
            "score": m.final_score,
            "outcome": m.outcome,
        })
    
    # 按时间排序
    activities.sort(key=lambda x: x["time"] or "", reverse=True)
    
    return {"activities": activities[:limit]}

@router.get("/sector-top5")
def get_sector_top5(db: Session = Depends(get_db)):
    """
    各赛道Top 5公司（按IC评分）
    复刻原系统功能
    """
    from ..core.config import get_settings
    settings = get_settings()
    
    result = {}
    for sector in settings.SECTORS:
        top_companies = db.query(Company).filter(
            Company.sector == sector,
            Company.avg_ic_score.isnot(None)
        ).order_by(desc(Company.avg_ic_score)).limit(5).all()
        
        result[sector] = [
            {
                "rank": i + 1,
                "name": c.name,
                "score": c.avg_ic_score,
                "decision": c.final_decision,
                "stage": c.stage,
            }
            for i, c in enumerate(top_companies)
        ]
    
    return {"sector_top5": result}
