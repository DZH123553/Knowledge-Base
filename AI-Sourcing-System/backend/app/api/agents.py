"""
Sourcing System — Agent 触发 API
核心工作流入口：手动触发Pipeline、IC自动讨论、人类反馈
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any

from ..core.database import get_db
from ..agents.pipeline import SourcingPipeline
from ..agents.investment_manager import get_all_agents as get_im_agents
from ..agents.risk_control import get_all_risk_agents
from ..agents.ic_member import get_all_ic_agents

router = APIRouter(prefix="/agents", tags=["Agents"])

# ─── Pydantic Schemas ───

class AutoICRequest(BaseModel):
    company_name: str
    description: str = ""

class HumanFeedbackRequest(BaseModel):
    company_id: str
    manager_name: str  # Peter Chen / Bin / TQT / Jianing
    contact_status: Optional[str] = None
    project_rating: Optional[float] = None
    team_rating: Optional[float] = None
    market_rating: Optional[float] = None
    product_rating: Optional[float] = None
    text_feedback: Optional[str] = None
    ic_opinion: Optional[str] = None

class BatchProcessRequest(BaseModel):
    max_signals: int = 10

# ─── Endpoints ───

@router.get("/config")
def get_agent_config():
    """获取全部Agent配置"""
    return {
        "investment_managers": get_im_agents(),
        "risk_controls": get_all_risk_agents(),
        "ic_members": get_all_ic_agents(),
        "total_agents": len(get_im_agents()) + len(get_all_risk_agents()) + len(get_all_ic_agents()),
    }

@router.post("/process-signal/{signal_id}")
async def process_signal(signal_id: str, db: Session = Depends(get_db)):
    """
    手动触发单个信号的完整Pipeline
    Signal → Screen → Company → DD → Risk → IC
    """
    result = await SourcingPipeline.process_signal(db, signal_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/auto-ic")
async def auto_trigger_ic(data: AutoICRequest, db: Session = Depends(get_db)):
    """
    手动输入公司 → 自动触发IC讨论
    （复刻原系统核心功能）
    """
    result = await SourcingPipeline.auto_trigger_ic(
        db, data.company_name, data.description
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/human-feedback")
async def submit_human_feedback(
    data: HumanFeedbackRequest,
    db: Session = Depends(get_db),
):
    """
    提交人类反馈
    投资经理人类对Agent输出的评价，触发Agent记忆更新
    """
    feedback_data = {
        "contact_status": data.contact_status,
        "project_rating": data.project_rating,
        "team_rating": data.team_rating,
        "market_rating": data.market_rating,
        "product_rating": data.product_rating,
        "text_feedback": data.text_feedback,
        "ic_opinion": data.ic_opinion,
    }
    
    result = await SourcingPipeline.process_human_feedback(
        db, data.company_id, data.manager_name, feedback_data
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/batch-process")
async def batch_process(data: BatchProcessRequest, db: Session = Depends(get_db)):
    """
    批量处理待处理信号
    """
    result = await SourcingPipeline.run_batch(db, data.max_signals)
    return result
