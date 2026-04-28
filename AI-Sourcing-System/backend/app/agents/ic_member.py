"""
Sourcing System — IC 成员 Agent
共4个，跨赛道独立投票
原系统规则：6=proceed, 4=abandon，无5分制
"""
import json
from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy.orm import Session

from .base import BaseAgent
from ..services.llm_service import get_llm_service
from ..core.config import get_settings
from ..models.schemas import ICMeeting, ICMeetingVote, Company, CompanyStatus

settings = get_settings()

IC_AGENTS = [
    {
        "id": "ic-01",
        "name": "IC-Chair",
        "persona": "保守型主席，关注退出路径和估值纪律",
        "weight": 1.5,
    },
    {
        "id": "ic-02",
        "name": "IC-Growth",
        "persona": "成长型，关注市场规模和增长曲线",
        "weight": 1.0,
    },
    {
        "id": "ic-03",
        "name": "IC-Tech",
        "persona": "技术型，关注技术壁垒和产品深度",
        "weight": 1.0,
    },
    {
        "id": "ic-04",
        "name": "IC-Ops",
        "persona": "运营型，关注执行力和团队背景",
        "weight": 1.0,
    },
]

class ICMemberAgent(BaseAgent):
    """IC成员Agent：独立投票，加权平均得出最终分数"""
    
    def __init__(self, agent_config: Dict[str, Any]):
        super().__init__(
            agent_id=agent_config["id"],
            name=agent_config["name"],
            role="ic_member",
            llm_service=get_llm_service(),
        )
        self.persona = agent_config.get("persona", "")
        self.weight = agent_config.get("weight", 1.0)
    
    async def vote(
        self,
        db: Session,
        meeting: ICMeeting,
        company: Company,
        dd_report: Dict[str, Any],
        risk_report: Dict[str, Any],
    ) -> ICMeetingVote:
        """投出一票"""
        messages = self.llm.build_ic_prompt(
            company_name=company.name,
            sector=company.sector or "",
            dd_report=dd_report,
            risk_report=risk_report,
            agent_persona=self.persona,
        )
        result = await self.think(messages)
        
        vote = ICMeetingVote(
            meeting_id=meeting.id,
            agent_id=self.agent_id,
            agent_name=self.name,
            agent_role="ic_member",
            score=result.get("score", 5.0),
            vote=result.get("vote", "abstain"),
            reasoning=result.get("reasoning", ""),
        )
        db.add(vote)
        db.commit()
        db.refresh(vote)
        
        # 保存IC记忆
        self.save_memory(
            db,
            content=f"IC投票: {company.name}, 分数={vote.score}, 投票={vote.vote}, 理由={vote.reasoning[:100]}",
            memory_type="ic_vote",
            company_id=company.id,
            importance=abs(vote.score - 5) / 5.0,  # 偏离中位数越多越重要
        )
        
        return vote
    
    async def run(self, db: Session, **kwargs) -> Dict[str, Any]:
        action = kwargs.get("action")
        if action == "vote":
            meeting = kwargs.get("meeting")
            company = kwargs.get("company")
            dd_report = kwargs.get("dd_report", {})
            risk_report = kwargs.get("risk_report", {})
            vote = await self.vote(db, meeting, company, dd_report, risk_report)
            return {"vote_id": vote.id, "score": vote.score}
        return {"error": "unknown action"}

def get_all_ic_agents() -> List[Dict[str, Any]]:
    return IC_AGENTS

async def run_ic_meeting(
    db: Session,
    company: Company,
    dd_report: Dict[str, Any],
    risk_reports: List[Dict[str, Any]],
) -> ICMeeting:
    """
    运行完整IC会议：4个IC成员 + 负责的投资经理 + 风控代表 投票
    加权平均计算最终分数
    """
    # 创建会议记录
    meeting = ICMeeting(
        company_id=company.id,
        week_number=datetime.now().isocalendar()[1],
    )
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    
    # 聚合风控报告
    aggregated_risk = {
        "risk_level_avg": sum(r.get("risk_level", 5) for r in risk_reports) / max(len(risk_reports), 1),
        "red_flags": [],
    }
    for r in risk_reports:
        aggregated_risk["red_flags"].extend(r.get("red_flags", []))
    
    # 获取所有Agent实例
    ic_configs = get_all_ic_agents()
    all_votes: List[ICMeetingVote] = []
    
    # IC成员投票
    for config in ic_configs:
        agent = ICMemberAgent(config)
        vote = await agent.vote(db, meeting, company, dd_report, aggregated_risk)
        all_votes.append(vote)
    
    # 投资经理投票（如果有）
    if company.assigned_manager:
        from .investment_manager import InvestmentManagerAgent, get_all_agents
        all_im = get_all_agents()
        im_config = next((a for a in all_im if a["id"] == company.assigned_manager), None)
        if im_config:
            im_agent = InvestmentManagerAgent(im_config)
            # 投资经理复用dd报告的overall_score作为投票
            im_score = dd_report.get("overall_score", 5.0)
            im_vote = ICMeetingVote(
                meeting_id=meeting.id,
                agent_id=im_agent.agent_id,
                agent_name=im_agent.name,
                agent_role="investment_manager",
                score=im_score,
                vote="invest" if im_score >= 6 else "pass",
                reasoning="基于DD报告综合评分",
            )
            db.add(im_vote)
            all_votes.append(im_vote)
    
    # 风控代表投票：用风险等级反推（风险越低分数越高）
    risk_score = 10 - aggregated_risk["risk_level_avg"]
    rc_vote = ICMeetingVote(
        meeting_id=meeting.id,
        agent_id="rc-rep",
        agent_name="Risk-Rep",
        agent_role="risk_control",
        score=risk_score,
        vote="invest" if risk_score >= 6 else "pass",
        reasoning=f"综合风险等级={aggregated_risk['risk_level_avg']:.1f}",
    )
    db.add(rc_vote)
    all_votes.append(rc_vote)
    
    db.commit()
    
    # 计算加权平均
    total_weight = 0.0
    weighted_sum = 0.0
    invest_count = 0
    pass_count = 0
    
    for vote in all_votes:
        weight = 1.0
        if vote.agent_role == "ic_member":
            ic_cfg = next((c for c in ic_configs if c["id"] == vote.agent_id), None)
            if ic_cfg:
                weight = ic_cfg.get("weight", 1.0)
        
        weighted_sum += vote.score * weight
        total_weight += weight
        
        if vote.vote == "invest":
            invest_count += 1
        elif vote.vote == "pass":
            pass_count += 1
    
    final_score = weighted_sum / total_weight if total_weight > 0 else 5.0
    
    # 更新会议结果
    meeting.total_votes = len(all_votes)
    meeting.invest_votes = invest_count
    meeting.pass_votes = pass_count
    meeting.final_score = round(final_score, 2)
    
    # 决策信号
    if final_score >= 7.5:
        meeting.decision_signal = "strong_buy"
        meeting.outcome = "proceed"
    elif final_score >= 6.0:
        meeting.decision_signal = "buy"
        meeting.outcome = "proceed"
    elif final_score >= 5.0:
        meeting.decision_signal = "hold"
        meeting.outcome = "table"
    elif final_score >= 4.0:
        meeting.decision_signal = "pass"
        meeting.outcome = "abandon"
    else:
        meeting.decision_signal = "strong_pass"
        meeting.outcome = "abandon"
    
    # 关键关注点和亮点
    key_concerns = []
    key_strengths = []
    for v in all_votes:
        if hasattr(v, 'reasoning') and v.reasoning:
            if v.score < 5:
                key_concerns.append(f"{v.agent_name}: {v.reasoning[:80]}")
            else:
                key_strengths.append(f"{v.agent_name}: {v.reasoning[:80]}")
    
    meeting.key_concerns = key_concerns[:5]
    meeting.key_strengths = key_strengths[:5]
    meeting.summary = f"IC会议完成。{len(all_votes)}人投票，最终分数={meeting.final_score}，决议={meeting.outcome}。"
    
    db.commit()
    
    # 更新公司状态
    company.avg_ic_score = meeting.final_score
    company.final_decision = meeting.outcome
    company.decision_signal = meeting.decision_signal
    company.status = CompanyStatus.IC_APPROVED.value if meeting.outcome == "proceed" else CompanyStatus.IC_REJECTED.value
    db.commit()
    
    return meeting
