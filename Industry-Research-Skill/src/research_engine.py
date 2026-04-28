"""
Industry Research Engine
Autonomous data collection from authoritative sources.
Python 3.8+ compatible.
"""

import re
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urlparse

from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup


class SearchDimension:
    """Defines a research dimension with search queries and extraction rules."""
    
    def __init__(self, name: str, queries: List[str], max_results: int = 8):
        self.name = name
        self.queries = queries
        self.max_results = max_results


class ResearchEngine:
    """
    Autonomous research engine that collects industry data from web sources.
    """
    
    # Pre-defined research dimensions for comprehensive industry analysis
    DIMENSIONS = {
        "overview": SearchDimension(
            name="行业概览与市场规模",
            queries=[
                "{industry} 行业 市场规模 增长率 2025 2026",
                "{industry} market size growth rate 2025 2026",
                "{industry} industry report market analysis global",
                "{industry} 行业报告 市场分析",
            ],
            max_results=8
        ),
        "chain": SearchDimension(
            name="产业链结构与价值链",
            queries=[
                "{industry} 产业链 上下游 价值链 结构分析",
                "{industry} industry chain value chain ecosystem",
                "{industry} supply chain key players profit pool",
                "{industry} 供应链 核心环节 进入壁垒",
            ],
            max_results=8
        ),
        "companies": SearchDimension(
            name="主要公司与竞争格局",
            queries=[
                "{industry} 主要公司 龙头企业 市场份额 竞争格局",
                "{industry} leading companies market share competitors startup",
                "{industry} funding series A seed venture capital",
                "{industry} 融资 独角兽 估值 早期公司",
            ],
            max_results=10
        ),
        "technology": SearchDimension(
            name="技术发展与演进路径",
            queries=[
                "{industry} 技术趋势 核心技术 发展方向 2025 2026",
                "{industry} technology trends core technology roadmap",
                "{industry} patent R&D breakthrough innovation",
                "{industry} 专利 研发投入 技术突破",
            ],
            max_results=8
        ),
        "policy": SearchDimension(
            name="政策环境与监管动态",
            queries=[
                "{industry} 政策 监管 法规 2025 2026",
                "{industry} policy regulation government support",
                "{industry} regulation compliance legal framework US EU",
                "{industry} 行业标准 合规要求",
            ],
            max_results=6
        ),
        "trends": SearchDimension(
            name="未来趋势与投资启示",
            queries=[
                "{industry} 未来趋势 投资前景 预测 2026 2027",
                "{industry} future trends investment outlook forecast",
                "{industry} VC insight investment thesis a16z sequoia",
                "{industry} 风险因素 投资机会 早期投资",
            ],
            max_results=8
        ),
    }
    
    # Trusted domain whitelist for source quality scoring
    # 覆盖中/美/欧/日/韩/东南亚等多区域权威信源
    TRUSTED_DOMAINS = {
        "high": [
            # 国际咨询与研究机构
            "mckinsey.com", "bcg.com", "bain.com", "deloitte.com", "pwc.com",
            "gartner.com", "idc.com", "forrester.com", "grandviewresearch.com",
            "marketsandmarkets.com", "frost.com", "counterpointresearch.com",
            "cbinsights.com", "pitchbook.com", "crunchbase.com",
            "reuters.com", "bloomberg.com", "wsj.com", "ft.com",
            "economist.com", "mit.edu", "stanford.edu", "harvard.edu",
            # 中国权威机构
            "eastmoney.com", "cls.cn", "36kr.com", "ithome.com",
            "gov.cn", "sec.gov", "nasdaq.com", "nyse.com",
            "cs.com.cn", "gtja.com", "htsc.com", "cicc.com", "chinastock.com.cn",
            # 海外创投与科技媒体
            "techcrunch.com", "theinformation.com", "venturebeat.com",
            "a16z.com", "sequoiacap.com", "bessemer.com", "insightpartners.com",
            "accel.com", "indexventures.com", "benchmark.com",
            "openai.com", "anthropic.com", "deepmind.google",
            # 日本/韩国/东南亚
            "nikkei.com", "asia.nikkei.com", "thejakartapost.com",
            "techinasia.com", "e27.co", "dealstreetasia.com",
        ],
        "medium": [
            "arxiv.org", "ieee.org", "nature.com", "science.org",
            "researchgate.net", "semanticscholar.org",
            "sina.com.cn", "sohu.com", "qq.com", "ifeng.com",
            "tmtpost.com", "pedaily.cn", "chinaventure.com.cn",
            "coindesk.com", "cointelegraph.com", "decrypt.co",
            "substack.com", "medium.com",
            "twitter.com", "x.com", "linkedin.com",
            "producthunt.com", "ycombinator.com",
        ]
    }
    
    def __init__(self, timeout: int = 15, request_delay: float = 1.0):
        self.timeout = timeout
        self.request_delay = request_delay
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        })
    
    def _score_source(self, url: str) -> str:
        """Score source reliability based on domain."""
        domain = urlparse(url).netloc.lower()
        for d in self.TRUSTED_DOMAINS["high"]:
            if d in domain:
                return "high"
        for d in self.TRUSTED_DOMAINS["medium"]:
            if d in domain:
                return "medium"
        return "low"
    
    def search_dimension(self, industry: str, dimension_key: str) -> List[Dict]:
        """
        Search a specific research dimension and return structured results.
        """
        dim = self.DIMENSIONS.get(dimension_key)
        if not dim:
            return []
        
        all_results = []
        seen_urls = set()
        
        with DDGS() as ddgs:
            for query_template in dim.queries:
                query = query_template.format(industry=industry)
                try:
                    results = ddgs.text(query, max_results=dim.max_results, region="wt-wt")
                    for r in results:
                        url = r.get("href", "")
                        if url in seen_urls:
                            continue
                        seen_urls.add(url)
                        
                        result = {
                            "title": r.get("title", ""),
                            "snippet": r.get("body", ""),
                            "url": url,
                            "source_score": self._score_source(url),
                            "dimension": dimension_key,
                            "query": query,
                            "fetched_at": datetime.now().isoformat(),
                        }
                        all_results.append(result)
                    
                    time.sleep(self.request_delay)
                    
                except Exception as e:
                    print(f"[WARN] Search failed for query '{query}': {e}")
                    continue
        
        # Sort by source reliability
        all_results.sort(key=lambda x: {"high": 0, "medium": 1, "low": 2}[x["source_score"]])
        return all_results
    
    def fetch_page_content(self, url: str, max_chars: int = 4000) -> Optional[str]:
        """Fetch and extract main text content from a URL."""
        try:
            resp = self.session.get(url, timeout=self.timeout)
            resp.raise_for_status()
            
            soup = BeautifulSoup(resp.content, "lxml")
            
            # Remove script/style/nav/footer/header tags
            for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                tag.decompose()
            
            # Try to find main content
            main = soup.find("main") or soup.find("article") or soup.find("div", class_=re.compile("content|article|main", re.I))
            if main:
                text = main.get_text(separator="\n", strip=True)
            else:
                text = soup.get_text(separator="\n", strip=True)
            
            # Clean up whitespace
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            text = "\n".join(lines)
            
            return text[:max_chars]
            
        except Exception as e:
            print(f"[WARN] Failed to fetch {url}: {e}")
            return None
    
    def extract_data_points(self, results: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Extract structured data points from search results.
        Uses regex-based extraction for numbers, dates, company names.
        """
        extracted = {
            "numbers": [],
            "companies": [],
            "dates": [],
            "quotes": [],
            "technologies": [],
        }
        
        # Regex patterns
        number_pattern = re.compile(
            r'(?:(?:USD|美元|\$|€|£|¥|人民币|RMB|CNY|EUR|GBP)\s*)?'
            r'\d+(?:\.\d+)?\s*(?:trillion|billion|million|千万|百万|亿|万|千|百|十)?'
            r'\s*(?:USD|美元|\$|€|£|¥|%|percent|百分比|亿元|万美元)?',
            re.IGNORECASE
        )
        
        date_pattern = re.compile(
            r'\b(?:20\d{2}|19\d{2})\b|'  # Years
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+20\d{2}\b|'  # English dates
            r'\d{4}年\d{1,2}月\d{0,2}日?',  # Chinese dates
            re.IGNORECASE
        )
        
        tech_keywords = [
            "AI", "artificial intelligence", "machine learning", "deep learning",
            "LLM", "large language model", "NLP", "computer vision",
            "blockchain", "web3", "metaverse", "cloud computing", "edge computing",
            "5G", "6G", "IoT", "robotics", "automation", "quantum",
            "GPU", "TPU", "ASIC", "chip", "semiconductor", "foundry",
            "SaaS", "PaaS", "IaaS", "API", "microservices",
            "neural network", "transformer", "diffusion", "GAN",
        ]
        
        for r in results:
            text = f"{r.get('title', '')} {r.get('snippet', '')}"
            
            # Extract numbers
            for match in number_pattern.finditer(text):
                extracted["numbers"].append({
                    "value": match.group(),
                    "context": text[max(0, match.start()-50):match.end()+50],
                    "source": r.get("url", ""),
                    "source_score": r.get("source_score", "low"),
                })
            
            # Extract dates
            for match in date_pattern.finditer(text):
                extracted["dates"].append({
                    "value": match.group(),
                    "context": text[max(0, match.start()-30):match.end()+30],
                    "source": r.get("url", ""),
                })
            
            # Extract technology mentions
            for tech in tech_keywords:
                if re.search(rf'\b{re.escape(tech)}\b', text, re.IGNORECASE):
                    extracted["technologies"].append({
                        "name": tech,
                        "context": text[:200],
                        "source": r.get("url", ""),
                    })
            
            # Extract quotes (statements in quotes)
            for match in re.finditer(r'"([^"]{20,300})"', text):
                extracted["quotes"].append({
                    "text": match.group(1),
                    "source": r.get("url", ""),
                })
        
        # Deduplicate
        for key in extracted:
            seen = set()
            unique = []
            for item in extracted[key]:
                val = item.get("value", item.get("name", item.get("text", "")))
                if val and val not in seen:
                    seen.add(val)
                    unique.append(item)
            extracted[key] = unique[:30]  # Limit per category
        
        return extracted
    
    def run_full_research(self, industry: str, deep_fetch: bool = False) -> Dict:
        """
        Run comprehensive research across all dimensions.
        Returns structured research data.
        """
        print(f"\n{'='*60}")
        print(f"启动行业深度研究: {industry}")
        print(f"{'='*60}\n")
        
        research_data = {
            "industry": industry,
            "research_date": datetime.now().isoformat(),
            "dimensions": {},
            "extracted_data": {},
            "sources": [],
        }
        
        all_results = []
        
        for dim_key, dim in self.DIMENSIONS.items():
            print(f"[维度 {dim_key}] 正在搜索: {dim.name}")
            results = self.search_dimension(industry, dim_key)
            research_data["dimensions"][dim_key] = results
            all_results.extend(results)
            print(f"  -> 获取 {len(results)} 条结果")
            
            if deep_fetch and results:
                print(f"  -> 深度抓取前 3 个高权重页面...")
                high_quality = [r for r in results if r["source_score"] == "high"][:3]
                for r in high_quality:
                    content = self.fetch_page_content(r["url"])
                    if content:
                        r["page_content"] = content
                    time.sleep(self.request_delay)
        
        # Extract structured data points
        print("\n[信息提取] 正在从搜索结果中提取结构化数据...")
        research_data["extracted_data"] = self.extract_data_points(all_results)
        
        # Build source index
        source_map = {}
        for r in all_results:
            url = r.get("url", "")
            if url not in source_map:
                source_map[url] = {
                    "url": url,
                    "title": r.get("title", ""),
                    "score": r.get("source_score", "low"),
                    "dimensions": set(),
                }
            source_map[url]["dimensions"].add(r.get("dimension", ""))
        
        research_data["sources"] = [
            {
                "url": s["url"],
                "title": s["title"],
                "reliability": s["score"],
                "dimensions": list(s["dimensions"]),
            }
            for s in source_map.values()
        ]
        
        print(f"\n[完成] 共搜集 {len(all_results)} 条信息，来自 {len(source_map)} 个独立来源")
        return research_data
