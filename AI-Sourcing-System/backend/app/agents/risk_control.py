"""
Sourcing System — 风控 Agent
共4个，独立分析风险维度，给出客观风险提示
"""
import json
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from .base import BaseAgent
from ..services.llm_service import get_llm_service
from ..models.schemas import RiskReport

RISK_AGENTS = [
    {"id": "rc-01", "name": "Risk-Market", "focus": "市场与宏观风险"},
    {"id": "rc-02", "name": "Risk-Financial", "focus": "财务与合规风险"},
    {"id": "rc-03", "name": "Risk-Team", "focus": "团队与治理风险"},
    {"id": "rc-04", "name": "Risk-Tech", "focus": "技术与竞争风险"},
]

class RiskControlAgent(BaseAgent):
    """风控Agent：独立分析项目风险，给出风险评分和红"""
    
    def __init__(self, agent_config: Dict[str, Any]):
        super().__init__(
            agent_id=agent_config["id"],
            name=agent_config["name"],
            role="risk_control",
            llm_service=get_llm_service(),
        )
        self.focus = agent_config.get("focus", "")
    
    async def analyze_risk(
        self,
        db: Session,
        company,
        dd_report: Dict[str, Any],
    ) -> RiskReport:
        """生成风险报告"""
        messages = self.llm.build_risk_prompt(company.name, dd_report)
        result = await self.think(messages)
        
        report = RiskReport(
            company_id=company.id,
            agent_id=self.agent_id,
            agent_name=self.name,
            market_risk=result.get("market_risk", ""),
            team_risk=result.get("team_risk", ""),
            financial_risk=result.get("financial_risk", ""),
            regulatory_risk=result.get("regulatory_risk", ""),
            competitive_risk=result.get("competitive_risk", ""),
            execution_risk=result.get("execution_risk", ""),
            risk_level=result.get("risk_level", 5.0),
            red_flags=result.get("red_flags", []),
            mitigations=result.get("mitigations", ""),
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        
        # 保存风险记忆
        self.save_memory(
            db,
            content=f"风险分析: {company.name}, 风险等级={report.risk_level}, 红旗={len(report.red_flags)}",
            memory_type="risk_report",
            company_id=company.id,
            importance=report.risk_level / 10.0,
        )
        
        return report
    
    async def run(self, db: Session, **kwargs) -> Dict[str, Any]:
        action = kwargs.get("action")
        if action == "analyze":
            company = kwargs.get("company")
            dd_report = kwargs.get("dd_report", {})
            report = await self.analyze_risk(db, company, dd_report)
            return {"report_id": report.id, "risk_level": report.risk_level}
        return {"error": "unknown action"}

def get_all_risk_agents() -> List[Dict[str, Any]]:
    return RISK_AGENTS
