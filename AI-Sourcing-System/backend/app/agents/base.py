"""
Sourcing System — Agent 基础类
所有Agent继承此类，统一LLM调用、记忆管理、日志记录
"""
import json
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from abc import ABC, abstractmethod

from sqlalchemy.orm import Session
from ..services.llm_service import LLMService, LLMMessage, get_llm_service
from ..models.schemas import AgentMemory, SignalMonitoring

class BaseAgent(ABC):
    """Agent 抽象基类"""
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        role: str,
        sector: Optional[str] = None,
        llm_service: Optional[LLMService] = None,
    ):
        self.agent_id = agent_id
        self.name = name
        self.role = role  # investment_manager / risk_control / ic_member
        self.sector = sector
        self.llm = llm_service or get_llm_service()
        self.memory: List[Dict[str, Any]] = []
    
    async def think(
        self,
        messages: List[LLMMessage],
        json_mode: bool = True,
    ) -> Dict[str, Any]:
        """核心思考方法：调用LLM并解析JSON"""
        raw = await self.llm.chat(messages, json_mode=json_mode)
        try:
            result = json.loads(raw)
            return result
        except json.JSONDecodeError:
            return {
                "error": "JSON解析失败",
                "raw_response": raw[:500],
                "agent_id": self.agent_id,
            }
    
    def save_memory(
        self,
        db: Session,
        content: str,
        memory_type: str = "case",
        company_id: Optional[str] = None,
        importance: float = 1.0,
    ) -> AgentMemory:
        """保存Agent记忆到数据库"""
        memory = AgentMemory(
            agent_id=self.agent_id,
            agent_role=self.role,
            company_id=company_id,
            memory_type=memory_type,
            content=content,
            importance=importance,
        )
        db.add(memory)
        db.commit()
        return memory
    
    def get_memories(
        self,
        db: Session,
        company_id: Optional[str] = None,
        limit: int = 10,
    ) -> List[AgentMemory]:
        """检索相关记忆"""
        query = db.query(AgentMemory).filter(AgentMemory.agent_id == self.agent_id)
        if company_id:
            query = query.filter(AgentMemory.company_id == company_id)
        return query.order_by(AgentMemory.importance.desc()).limit(limit).all()
    
    def log_action(
        self,
        db: Session,
        signal_id: Optional[str],
        action: str,
        score: Optional[float] = None,
        reasoning: str = "",
    ) -> SignalMonitoring:
        """记录Agent操作日志"""
        log = SignalMonitoring(
            signal_id=signal_id or "",
            agent_id=self.agent_id,
            agent_role=self.role,
            action=action,
            score=score,
            reasoning=reasoning,
        )
        db.add(log)
        db.commit()
        return log
    
    @abstractmethod
    async def run(self, db: Session, **kwargs) -> Dict[str, Any]:
        """Agent主执行入口，子类必须实现"""
        pass
