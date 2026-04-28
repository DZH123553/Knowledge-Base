#!/usr/bin/env python3
"""
Sourcing System — IC自动讨论脚本
复刻原系统：手动输入公司 → 自动触发IC讨论
Usage: python run_ic_autogen.py --case "CompanyName" --desc "Description"
"""
import sys
import os
import argparse
import asyncio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.core.database import get_db_context
from app.agents.pipeline import SourcingPipeline

async def main():
    parser = argparse.ArgumentParser(description="自动触发IC讨论")
    parser.add_argument("--case", required=True, help="公司名称")
    parser.add_argument("--desc", default="", help="公司描述")
    parser.add_argument("--sector", default="AI", help="赛道")
    args = parser.parse_args()
    
    print(f"🚀 启动IC自动讨论: {args.case}")
    print(f"   赛道: {args.sector}")
    print(f"   描述: {args.desc[:100]}..." if len(args.desc) > 100 else f"   描述: {args.desc}")
    print()
    
    with get_db_context() as db:
        result = await SourcingPipeline.auto_trigger_ic(db, args.case, args.desc)
        
        if "error" in result:
            print(f"❌ 错误: {result['error']}")
            return
        
        print("✅ IC讨论完成!")
        print(f"   公司ID: {result.get('company_id')}")
        print(f"   DD评分: {result.get('dd_score')}")
        print(f"   平均风险: {result.get('risk_level_avg')}")
        print(f"   IC最终分数: {result.get('ic_score')}")
        print(f"   决议: {result.get('decision')}")
        print()
        print("完成的步骤:", ", ".join(result.get("steps_completed", [])))

if __name__ == "__main__":
    asyncio.run(main())
