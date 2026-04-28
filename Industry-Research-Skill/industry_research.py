#!/usr/bin/env python3
"""
Industry Research Skill — Main Entry Point
A rigorous, autonomous industry analysis framework for VC research.

Usage:
    python industry_research.py "AI Manju (AI Comics/Animation)" --deep --output ./output
    python industry_research.py "AI Video Generation" --lang zh

Requirements: Python 3.8+
"""

import argparse
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from research_engine import ResearchEngine
from report_generator import ReportGenerator


def main():
    parser = argparse.ArgumentParser(
        description="自主行业深度研究工具 — 基于公开信息的系统性调研",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python industry_research.py "AI漫剧" --deep
  python industry_research.py "人形机器人" --output ./reports
  python industry_research.py "低空经济" --deep --lang zh
        """
    )
    parser.add_argument(
        "industry",
        help="研究行业名称（支持中英文，如：AI漫剧、AI Video Generation、人形机器人）"
    )
    parser.add_argument(
        "--deep", "-d",
        action="store_true",
        help="启用深度模式：抓取高权重页面的完整内容（更慢但更详尽）"
    )
    parser.add_argument(
        "--output", "-o",
        default="./output",
        help="输出目录（默认：./output）"
    )
    # Language parameter removed — reports are generated in the language
    # that best matches the industry query and source material
    parser.add_argument(
        "--max-results",
        type=int,
        default=None,
        help="每个维度的最大搜索结果数（覆盖默认值）"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="请求间隔秒数（默认：1.0，防封禁）"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("  Industry Research Skill — 行业深度研究工具")
    print("  Version: 1.0.0 | Designed for rigorous VC research")
    print("=" * 70)
    
    # Initialize engine
    engine = ResearchEngine(
        timeout=15,
        request_delay=args.delay,
    )
    
    # Override max results if specified
    if args.max_results:
        for dim in engine.DIMENSIONS.values():
            dim.max_results = args.max_results
    
    # Run research
    try:
        research_data = engine.run_full_research(
            industry=args.industry,
            deep_fetch=args.deep
        )
    except KeyboardInterrupt:
        print("\n[中断] 用户取消研究")
        sys.exit(0)
    except Exception as e:
        print(f"\n[错误] 研究过程中发生错误: {e}")
        sys.exit(1)
    
    # Generate report
    print("\n[报告生成] 正在生成结构化研究报告...")
    generator = ReportGenerator(
        research_data=research_data,
        output_dir=args.output
    )
    
    paths = generator.save()
    
    print("\n" + "=" * 70)
    print("  ✅ 研究完成！")
    print("=" * 70)
    print(f"\n  📄 Markdown 报告: {paths['markdown']}")
    print(f"  📊 原始数据:     {paths['raw_data']}")
    print("\n  ⚠️  重要提醒：")
    print("     1. 本报告基于公开信息的系统性搜集，所有数据均标注来源")
    print("     2. 部分数据可能存在时效滞后，建议对关键数据进行二次核实")
    print("     3. 本报告仅供研究参考，不构成投资建议")
    print("     4. 海外信源已纳入搜索范围，但部分区域信息可能覆盖不足")
    print("=" * 70)


if __name__ == "__main__":
    main()
