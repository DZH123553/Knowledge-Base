"""
Sourcing System — 数据库 Schema
完全复刻原系统数据流：signals → monitoring → companies + reports → ic_meetings → feedback
"""
from sqlalchemy import (
    Column, Integer, String, Text, Float, DateTime, Boolean,
    ForeignKey, Enum, JSON, Index, create_engine
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum as PyEnum
import uuid

from ..core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

# ────────────────────────────── Enums ──────────────────────────────

class SignalStatus(str, PyEnum):
    RAW = "raw"           # 刚抓取
    PARSED = "parsed"     # 已解析出公司
    SCREENED = "screened" # 已初筛
    REJECTED = "rejected" # 已拒
    ARCHIVED = "archived" # 已归档

class CompanyStatus(str, PyEnum):
    SOURCING = "sourcing"       # 信号阶段
    SCREENING = "screening"     # 初筛中
    DD = "due_diligence"        # DD中
    IC_PENDING = "ic_pending"   # 等IC
    IC_APPROVED = "ic_approved" # IC通过
    IC_REJECTED = "ic_rejected" # IC拒绝
    PORTFOLIO = "portfolio"     # 已投
    PASSED = "passed"           # 已放弃

class ContactStatus(str, PyEnum):
    NOT_CONTACTED = "not_contacted"
    CONTACTING = "contacting"
    CONTACTED = "contacted"

class DecisionSignal(str, PyEnum):
    STRONG_BUY = "strong_buy"
    BUY = "buy"
    HOLD = "hold"
    PASS = "pass"
    STRONG_PASS = "strong_pass"

# ────────────────────────────── Core Tables ──────────────────────────────

class Signal(Base):
    """原始信号表 — 从各数据源抓取的非结构化信号"""
    __tablename__ = "signals"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    source = Column(String(50), nullable=False, index=True)  # twitter / reddit / polymarket / manual / rss
    source_id = Column(String(200))  # 外部ID，如 tweet_id
    raw_content = Column(Text, nullable=False)  # 原始文本
    parsed_content = Column(Text)  # LLM解析后的结构化内容
    url = Column(String(500))
    author = Column(String(100))
    author_followers = Column(Integer, default=0)
    engagement_score = Column(Float, default=0.0)  # 互动量归一化
    sentiment = Column(String(20))  # positive / neutral / negative
    mentioned_company = Column(String(200), index=True)  # 提及的公司名
    mentioned_ticker = Column(String(20))
    sector = Column(String(50), index=True)
    tags = Column(JSON, default=list)  # 标签数组
    status = Column(String(20), default=SignalStatus.RAW.value, index=True)
    confidence = Column(Float, default=0.0)  # 信号置信度
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    parsed_at = Column(DateTime(timezone=True))
    
    # Relations
    monitorings = relationship("SignalMonitoring", back_populates="signal", cascade="all, delete-orphan")
    company = relationship("Company", back_populates="source_signal", uselist=False)
    
    __table_args__ = (
        Index('ix_signals_created', 'created_at'),
        Index('ix_signals_sector_status', 'sector', 'status'),
    )

class SignalMonitoring(Base):
    """信号监控表 — Agent 对信号的追踪记录"""
    __tablename__ = "signal_monitoring"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    signal_id = Column(String(36), ForeignKey("signals.id"), nullable=False)
    agent_id = Column(String(50), nullable=False, index=True)  # 哪个Agent在处理
    agent_role = Column(String(50))  # investment_manager / risk_control / ic_member
    action = Column(String(50))  # screen / analyze / flag / pass
    score = Column(Float)  # Agent给出的评分
    reasoning = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    signal = relationship("Signal", back_populates="monitorings")

class Company(Base):
    """公司汇总表 — 信号聚合后的公司实体"""
    __tablename__ = "companies"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(200), nullable=False, index=True)
    slug = Column(String(200), unique=True, index=True)  # URL友好名
    description = Column(Text)
    sector = Column(String(50), index=True)
    sub_sector = Column(String(100))
    stage = Column(String(50))  # pre-seed / seed / series-a / etc
    website = Column(String(500))
    location = Column(String(200))
    founded_year = Column(Integer)
    team_size = Column(Integer)
    
    # 联系状态
    contact_status = Column(String(20), default=ContactStatus.NOT_CONTACTED.value)
    contact_person = Column(String(100))
    contact_notes = Column(Text)
    
    # 资金
    funding_total = Column(Float, default=0.0)  # 万美元
    last_funding_round = Column(String(50))
    last_funding_amount = Column(Float)
    last_funding_date = Column(DateTime(timezone=True))
    investors = Column(JSON, default=list)
    
    # 评分聚合
    avg_ic_score = Column(Float)
    final_decision = Column(String(20))  # approved / rejected / pending
    decision_signal = Column(String(20))  # strong_buy / buy / hold / pass / strong_pass
    
    # 状态机
    status = Column(String(20), default=CompanyStatus.SOURCING.value, index=True)
    assigned_manager = Column(String(50), index=True)  # 分配的投资经理Agent ID
    
    # 元数据
    source_signal_id = Column(String(36), ForeignKey("signals.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    source_signal = relationship("Signal", back_populates="company")
    reports = relationship("InvestmentReport", back_populates="company", cascade="all, delete-orphan")
    risk_reports = relationship("RiskReport", back_populates="company", cascade="all, delete-orphan")
    ic_meetings = relationship("ICMeeting", back_populates="company", cascade="all, delete-orphan")
    feedbacks = relationship("HumanFeedback", back_populates="company", cascade="all, delete-orphan")
    memories = relationship("AgentMemory", back_populates="company", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('ix_companies_status_sector', 'status', 'sector'),
        Index('ix_companies_manager', 'assigned_manager'),
    )

class InvestmentReport(Base):
    """DD报告表 — 投资经理Agent生成的尽调报告"""
    __tablename__ = "investment_reports"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    agent_id = Column(String(50), nullable=False, index=True)
    agent_name = Column(String(100))
    
    # 报告核心内容
    tam = Column(Text)  # Total Addressable Market
    sam = Column(Text)  # Serviceable Addressable Market
    som = Column(Text)  # Serviceable Obtainable Market
    market_position = Column(Text)  # 市场身位/竞争格局
    team_summary = Column(Text)  # 团队简介
    investor_background = Column(Text)  # 投资人背景
    product_analysis = Column(Text)  # 产品分析
    traction = Column(Text)  # 增长数据
    moat = Column(Text)  # 护城河
    
    # 结构化评分
    market_score = Column(Float)
    team_score = Column(Float)
    product_score = Column(Float)
    traction_score = Column(Float)
    moat_score = Column(Float)
    overall_score = Column(Float)
    
    # 推荐
    recommendation = Column(String(20))  # proceed / abandon / watch
    conviction = Column(Float)  # 0-10 信心度
    
    # 元数据
    report_version = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    company = relationship("Company", back_populates="reports")

class RiskReport(Base):
    """风险报告表 — 风控Agent独立分析"""
    __tablename__ = "risk_reports"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    agent_id = Column(String(50), nullable=False, index=True)
    agent_name = Column(String(100))
    
    # 风险维度
    market_risk = Column(Text)
    team_risk = Column(Text)
    financial_risk = Column(Text)
    regulatory_risk = Column(Text)
    competitive_risk = Column(Text)
    execution_risk = Column(Text)
    
    # 风险评分（越低越安全）
    risk_level = Column(Float)  # 0-10，10=极高风险
    red_flags = Column(JSON, default=list)
    mitigations = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    company = relationship("Company", back_populates="risk_reports")

class ICMeeting(Base):
    """IC会议表 — 投决会纪要"""
    __tablename__ = "ic_meetings"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    meeting_date = Column(DateTime(timezone=True), server_default=func.now())
    week_number = Column(Integer, index=True)  # 用于周排名
    
    # 投票统计
    total_votes = Column(Integer, default=0)
    invest_votes = Column(Integer, default=0)
    pass_votes = Column(Integer, default=0)
    
    # 结果
    final_score = Column(Float)  # 加权平均分
    decision_signal = Column(String(20))  # strong_buy / buy / hold / pass / strong_pass
    outcome = Column(String(20))  # proceed / abandon / table
    
    # 纪要
    summary = Column(Text)
    key_concerns = Column(JSON, default=list)
    key_strengths = Column(JSON, default=list)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    company = relationship("Company", back_populates="ic_meetings")
    votes = relationship("ICMeetingVote", back_populates="meeting", cascade="all, delete-orphan")

class ICMeetingVote(Base):
    """IC投票明细表"""
    __tablename__ = "ic_meeting_votes"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    meeting_id = Column(String(36), ForeignKey("ic_meetings.id"), nullable=False)
    agent_id = Column(String(50), nullable=False)
    agent_name = Column(String(100))
    agent_role = Column(String(50))  # ic_member / investment_manager / risk_control
    
    # 原系统：6=proceed, 4=abandon（没有5分制）
    score = Column(Float, nullable=False)  # 0-10
    vote = Column(String(20))  # invest / pass / abstain
    reasoning = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    meeting = relationship("ICMeeting", back_populates="votes")

class HumanFeedback(Base):
    """人类反馈表 — 投资经理人类对Agent输出的反馈"""
    __tablename__ = "human_feedback"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    manager_name = Column(String(100), nullable=False, index=True)  # Peter Chen / Bin / TQT / Jianing
    
    # 状态更新
    contact_status = Column(String(20))
    
    # 评分 1-10
    project_rating = Column(Float)
    team_rating = Column(Float)
    market_rating = Column(Float)
    product_rating = Column(Float)
    
    # 文字反馈
    text_feedback = Column(Text)
    ic_opinion = Column(Text)  # 人类对IC会议的意见
    
    # 元数据
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    company = relationship("Company", back_populates="feedbacks")

class AgentMemory(Base):
    """Agent记忆表 — 压缩存储反馈用于自主学习"""
    __tablename__ = "agent_memories"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    agent_id = Column(String(50), nullable=False, index=True)
    agent_role = Column(String(50))
    company_id = Column(String(36), ForeignKey("companies.id"))
    
    # 压缩记忆
    memory_type = Column(String(50))  # feedback / case / threshold_adjustment
    content = Column(Text)  # 压缩后的文本
    embedding = Column(Text)  # 可选：向量嵌入JSON
    importance = Column(Float, default=1.0)  # 重要性权重
    
    # 关联
    related_feedback_id = Column(String(36))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    company = relationship("Company", back_populates="memories")

class CrawlerLog(Base):
    """爬虫日志表"""
    __tablename__ = "crawler_logs"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    source = Column(String(50), nullable=False)
    status = Column(String(20))  # success / error / partial
    items_fetched = Column(Integer, default=0)
    items_new = Column(Integer, default=0)
    error_message = Column(Text)
    started_at = Column(DateTime(timezone=True))
    finished_at = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
