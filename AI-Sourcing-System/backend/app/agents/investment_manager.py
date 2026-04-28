"""
Sourcing System — 投资经理 Agent
共26个，按赛道分配：AI/Web3/Healthcare/HardTech/Consumer/Enterprise/Fintech/Climate
每个赛道2-4个Agent，模拟不同投资风格
"""
import json
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from .base import BaseAgent
from ..services.llm_service import LLMMessage, get_llm_service
from ..models.schemas import (
    Signal, Company, InvestmentReport, SignalStatus, CompanyStatus
)

# Agent 配置矩阵：赛道 → Agent列表
SECTOR_AGENTS = {
    "AI": [
        {"id": "im-ai-01", "name": "AI-Growth", "style": "growth", "focus": "应用层AI和Agent"},
        {"id": "im-ai-02", "name": "AI-Infra", "style": "infrastructure", "focus": "AI基础设施和模型层"},
        {"id": "im-ai-03", "name": "AI-Hardware", "style": "deep_tech", "focus": "AI芯片和硬件"},
        {"id": "im-ai-04", "name": "AI-Robotics", "style": "frontier", "focus": "具身智能和机器人"},
    ],
    "Web3": [
        {"id": "im-web3-01", "name": "Web3-DeFi", "style": "defi", "focus": "去中心化金融"},
        {"id": "im-web3-02", "name": "Web3-Infra", "style": "infrastructure", "focus": "公链和基础设施"},
        {"id": "im-web3-03", "name": "Web3-Consumer", "style": "consumer", "focus": "消费级Web3应用"},
    ],
    "Healthcare": [
        {"id": "im-hc-01", "name": "HC-Bio", "style": "biotech", "focus": "生物技术和基因治疗"},
        {"id": "im-hc-02", "name": "HC-Digital", "style": "digital_health", "focus": "数字医疗和AI诊断"},
        {"id": "im-hc-03", "name": "HC-Device", "style": "medtech", "focus": "医疗器械"},
    ],
    "HardTech": [
        {"id": "im-ht-01", "name": "HT-Semiconductor", "style": "semiconductor", "focus": "半导体"},
        {"id": "im-ht-02", "name": "HT-Space", "style": "frontier", "focus": "商业航天"},
        {"id": "im-ht-03", "name": "HT-Energy", "style": "climate", "focus": "新能源和储能"},
        {"id": "im-ht-04", "name": "HT-Advanced", "style": "deep_tech", "focus": "先进制造和材料"},
    ],
    "Consumer": [
        {"id": "im-cs-01", "name": "CS-Brand", "style": "brand", "focus": "新品牌和DTC"},
        {"id": "im-cs-02", "name": "CS-Platform", "style": "platform", "focus": "消费平台"},
    ],
    "Enterprise": [
        {"id": "im-en-01", "name": "EN-SaaS", "style": "saas", "focus": "企业SaaS"},
        {"id": "im-en-02", "name": "EN-Security", "style": "security", "focus": "网络安全"},
        {"id": "im-en-03", "name": "EN-Data", "style": "data", "focus": "数据基础设施"},
    ],
    "Fintech": [
        {"id": "im-ft-01", "name": "FT-Payment", "style": "payments", "focus": "支付和跨境"},
        {"id": "im-ft-02", "name": "FT-Wealth", "style": "wealth", "focus": "财富管理和保险科技"},
        {"id": "im-ft-03", "name": "FT-Credit", "style": "credit", "focus": "信贷和风控"},
    ],
    "Climate": [
        {"id": "im-cl-01", "name": "CL-Carbon", "style": "carbon", "focus": "碳中和和ESG"},
        {"id": "im-cl-02", "name": "CL-CleanTech", "style": "cleantech", "focus": "清洁技术"},
    ],
}

def get_agent_for_sector(sector: str, index: int = 0) -> Dict[str, Any]:
    """获取赛道对应的Agent配置"""
    agents = SECTOR_AGENTS.get(sector, SECTOR_AGENTS["AI"])
    return agents[index % len(agents)]

def get_all_agents() -> List[Dict[str, Any]]:
    """获取全部26个Agent配置"""
    all_agents = []
    for sector, agents in SECTOR_AGENTS.items():
        for a in agents:
            all_agents.append({**a, "sector": sector})
    return all_agents

class InvestmentManagerAgent(BaseAgent):
    """投资经理Agent：负责信号筛选、公司建档、DD报告生成"""
    
    def __init__(self, agent_config: Dict[str, Any]):
        super().__init__(
            agent_id=agent_config["id"],
            name=agent_config["name"],
            role="investment_manager",
            sector=agent_config.get("sector"),
            llm_service=get_llm_service(),
        )
        self.style = agent_config.get("style", "general")
        self.focus = agent_config.get("focus", "")
    
    async def screen_signal(self, db: Session, signal: Signal) -> Dict[str, Any]:
        """Step 1: 信号初筛"""
        messages = self.llm.build_screening_prompt(
            signal.raw_content,
            self.sector or signal.sector or "unknown",
        )
        result = await self.think(messages)
        
        # 记录监控日志
        self.log_action(
            db, signal.id, "screen",
            score=result.get("confidence", 0),
            reasoning=result.get("reason", ""),
        )
        
        return result
    
    async def create_company(self, db: Session, signal: Signal, screen_result: Dict) -> Company:
        """Step 2: 从信号创建公司实体"""
        company = Company(
            name=screen_result.get("company_name", "Unknown"),
            slug=screen_result.get("company_name", "unknown").lower().replace(" ", "-"),
            sector=screen_result.get("sector", self.sector or "AI"),
            description=signal.parsed_content or signal.raw_content[:500],
            status=CompanyStatus.SCREENING.value,
            assigned_manager=self.agent_id,
            source_signal_id=signal.id,
        )
        db.add(company)
        
        # 更新信号状态
        signal.status = SignalStatus.SCREENED.value
        db.commit()
        db.refresh(company)
        
        return company
    
    async def generate_dd_report(
        self,
        db: Session,
        company: Company,
    ) -> InvestmentReport:
        """Step 3: 生成DD报告"""
        messages = self.llm.build_dd_prompt(
            company_name=company.name,
            description=company.description or "",
            sector=company.sector or "",
        )
        result = await self.think(messages)
        
        report = InvestmentReport(
            company_id=company.id,
            agent_id=self.agent_id,
            agent_name=self.name,
            tam=result.get("tam", ""),
            sam=result.get("sam", ""),
            som=result.get("som", ""),
            market_position=result.get("market_position", ""),
            team_summary=result.get("team_summary", ""),
            investor_background=result.get("investor_background", ""),
            product_analysis=result.get("product_analysis", ""),
            traction=result.get("traction", ""),
            moat=result.get("moat", ""),
            market_score=result.get("market_score", 5.0),
            team_score=result.get("team_score", 5.0),
            product_score=result.get("product_score", 5.0),
            traction_score=result.get("traction_score", 5.0),
            moat_score=result.get("moat_score", 5.0),
            overall_score=result.get("overall_score", 5.0),
            recommendation=result.get("recommendation", "watch"),
            conviction=result.get("conviction", 5.0),
        )
        db.add(report)
        
        # 更新公司状态
        company.status = CompanyStatus.DD.value
        db.commit()
        db.refresh(report)
        
        # 保存记忆
        self.save_memory(
            db,
            content=f"生成DD报告: {company.name}, 综合评分={report.overall_score}, 推荐={report.recommendation}",
            memory_type="dd_report",
            company_id=company.id,
            importance=report.overall_score / 10.0,
        )
        
        return report
    
    async def run(self, db: Session, **kwargs) -> Dict[str, Any]:
        """Agent主入口：根据输入参数执行对应步骤"""
        action = kwargs.get("action")
        
        if action == "screen":
            signal = kwargs.get("signal")
            return await self.screen_signal(db, signal)
        
        elif action == "create_company":
            signal = kwargs.get("signal")
            screen_result = kwargs.get("screen_result")
            company = await self.create_company(db, signal, screen_result)
            return {"company_id": company.id, "name": company.name}
        
        elif action == "dd":
            company = kwargs.get("company")
            report = await self.generate_dd_report(db, company)
            return {"report_id": report.id, "score": report.overall_score}
        
        return {"error": "unknown action"}
