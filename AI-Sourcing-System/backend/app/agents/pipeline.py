"""
Sourcing System — Pipeline 编排器
完整工作流：Signal → Screen → Company → DD → Risk → IC → Feedback
"""
import asyncio
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from ..core.database import get_db_context
from ..models.schemas import (
    Signal, Company, InvestmentReport, RiskReport,
    ICMeeting, HumanFeedback, AgentMemory, SignalStatus, CompanyStatus
)
from .investment_manager import InvestmentManagerAgent, get_agent_for_sector
from .risk_control import RiskControlAgent, get_all_risk_agents
from .ic_member import run_ic_meeting

class SourcingPipeline:
    """完整工作流编排"""
    
    @staticmethod
    async def process_signal(db: Session, signal_id: str) -> Dict[str, Any]:
        """
        处理单个信号的全流程
        """
        signal = db.query(Signal).filter(Signal.id == signal_id).first()
        if not signal:
            return {"error": "Signal not found"}
        
        if signal.status != SignalStatus.RAW.value:
            return {"error": f"Signal already processed: {signal.status}"}
        
        # ── Step 1: 信号解析 ──
        sector = signal.sector or "AI"
        agent_config = get_agent_for_sector(sector, 0)
        im_agent = InvestmentManagerAgent(agent_config)
        
        screen_result = await im_agent.screen_signal(db, signal)
        
        if not screen_result.get("has_value", False):
            signal.status = SignalStatus.REJECTED.value
            db.commit()
            return {
                "signal_id": signal_id,
                "step": "screen",
                "result": "rejected",
                "reason": screen_result.get("reason", "")
            }
        
        # ── Step 2: 创建公司 ──
        company = await im_agent.create_company(db, signal, screen_result)
        
        # ── Step 3: 生成DD报告 ──
        dd_report = await im_agent.generate_dd_report(db, company)
        
        # ── Step 4: 风控分析（4个风控Agent并行）──
        dd_dict = {
            "tam": dd_report.tam,
            "sam": dd_report.sam,
            "som": dd_report.som,
            "market_position": dd_report.market_position,
            "team_summary": dd_report.team_summary,
            "investor_background": dd_report.investor_background,
            "product_analysis": dd_report.product_analysis,
            "traction": dd_report.traction,
            "moat": dd_report.moat,
            "overall_score": dd_report.overall_score,
            "key_risks": [],
        }
        
        risk_configs = get_all_risk_agents()
        risk_reports = []
        for rc_config in risk_configs:
            rc_agent = RiskControlAgent(rc_config)
            risk_report = await rc_agent.analyze_risk(db, company, dd_dict)
            risk_reports.append({
                "agent_id": risk_report.agent_id,
                "agent_name": risk_report.agent_name,
                "risk_level": risk_report.risk_level,
                "red_flags": risk_report.red_flags,
                "mitigations": risk_report.mitigations,
            })
        
        # ── Step 5: IC会议 ──
        meeting = await run_ic_meeting(db, company, dd_dict, risk_reports)
        
        return {
            "signal_id": signal_id,
            "company_id": company.id,
            "company_name": company.name,
            "dd_score": dd_report.overall_score,
            "risk_level_avg": sum(r["risk_level"] for r in risk_reports) / len(risk_reports),
            "ic_score": meeting.final_score,
            "decision": meeting.outcome,
            "steps_completed": ["screen", "create_company", "dd", "risk", "ic"],
        }
    
    @staticmethod
    async def auto_trigger_ic(db: Session, company_name: str, description: str = "") -> Dict[str, Any]:
        """
        手动输入公司 → 自动触发IC讨论
        （原系统的核心功能）
        """
        # 创建公司和信号
        signal = Signal(
            source="manual",
            raw_content=f"手动输入: {company_name}\n{description}",
            parsed_content=description,
            mentioned_company=company_name,
            status=SignalStatus.SCREENED.value,
        )
        db.add(signal)
        db.commit()
        db.refresh(signal)
        
        # 直接走完整pipeline
        return await SourcingPipeline.process_signal(db, signal.id)
    
    @staticmethod
    async def process_human_feedback(
        db: Session,
        company_id: str,
        manager_name: str,
        feedback_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        处理人类反馈，更新Agent记忆和阈值
        """
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            return {"error": "Company not found"}
        
        # 保存反馈
        feedback = HumanFeedback(
            company_id=company_id,
            manager_name=manager_name,
            contact_status=feedback_data.get("contact_status"),
            project_rating=feedback_data.get("project_rating"),
            team_rating=feedback_data.get("team_rating"),
            market_rating=feedback_data.get("market_rating"),
            product_rating=feedback_data.get("product_rating"),
            text_feedback=feedback_data.get("text_feedback"),
            ic_opinion=feedback_data.get("ic_opinion"),
        )
        db.add(feedback)
        
        # 更新公司联系状态
        if feedback_data.get("contact_status"):
            company.contact_status = feedback_data.get("contact_status")
        
        db.commit()
        
        # ── 压缩反馈为Agent记忆 ──
        # 找到负责的投资经理
        if company.assigned_manager:
            memory_content = (
                f"人类反馈: 经理{manager_name}对{company.name}的评分="
                f"项目{feedback_data.get('project_rating', 'N/A')}/"
                f"团队{feedback_data.get('team_rating', 'N/A')}/"
                f"市场{feedback_data.get('market_rating', 'N/A')}. "
                f"文字: {feedback_data.get('text_feedback', '')[:200]}"
            )
            
            memory = AgentMemory(
                agent_id=company.assigned_manager,
                agent_role="investment_manager",
                company_id=company_id,
                memory_type="feedback",
                content=memory_content,
                related_feedback_id=feedback.id,
                importance=feedback_data.get("project_rating", 5) / 10.0,
            )
            db.add(memory)
        
        # ── 自主阈值调整逻辑 ──
        # 收集该公司所有人类反馈，计算平均分
        all_feedback = db.query(HumanFeedback).filter(
            HumanFeedback.company_id == company_id
        ).all()
        
        if len(all_feedback) >= 2:
            avg_human_score = sum(
                f.project_rating for f in all_feedback if f.project_rating is not None
            ) / max(len([f for f in all_feedback if f.project_rating is not None]), 1)
            
            # 如果人类评分和IC评分差异大，记录阈值调整建议
            if company.avg_ic_score and abs(avg_human_score - company.avg_ic_score) > 2:
                adjustment = AgentMemory(
                    agent_id="system",
                    agent_role="system",
                    company_id=company_id,
                    memory_type="threshold_adjustment",
                    content=(
                        f"阈值调整: {company.name} 人类评分={avg_human_score:.1f} vs "
                        f"IC评分={company.avg_ic_score:.1f}, 差异={abs(avg_human_score - company.avg_ic_score):.1f}. "
                        f"建议校准该赛道的评分权重。"
                    ),
                    importance=0.8,
                )
                db.add(adjustment)
        
        db.commit()
        
        return {
            "company_id": company_id,
            "feedback_id": feedback.id,
            "manager": manager_name,
            "memories_created": 1 if company.assigned_manager else 0,
        }
    
    @staticmethod
    async def run_batch(db: Session, max_signals: int = 10) -> Dict[str, Any]:
        """
        批量处理待处理信号
        """
        signals = db.query(Signal).filter(
            Signal.status == SignalStatus.RAW.value
        ).order_by(Signal.created_at.desc()).limit(max_signals).all()
        
        results = []
        for signal in signals:
            try:
                result = await SourcingPipeline.process_signal(db, signal.id)
                results.append(result)
            except Exception as e:
                results.append({
                    "signal_id": signal.id,
                    "error": str(e),
                })
        
        return {
            "processed": len(results),
            "success": len([r for r in results if "error" not in r]),
            "failed": len([r for r in results if "error" in r]),
            "details": results,
        }
