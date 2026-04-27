#!/usr/bin/env python3
"""
Sourcing System — 数据库初始化脚本
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.core.database import init_db
from app.models.schemas import Signal, SignalStatus

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")
    print("Tables created:")
    print("  - signals")
    print("  - signal_monitoring")
    print("  - companies")
    print("  - investment_reports")
    print("  - risk_reports")
    print("  - ic_meetings")
    print("  - ic_meeting_votes")
    print("  - human_feedback")
    print("  - agent_memories")
    print("  - crawler_logs")
