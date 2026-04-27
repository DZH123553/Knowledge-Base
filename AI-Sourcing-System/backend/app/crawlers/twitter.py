"""
Sourcing System — Twitter/X 爬虫
使用 Twitter API v2 搜索投资相关推文
"""
import os
import httpx
from typing import List, Dict, Any
from datetime import datetime, timedelta

from .base import BaseCrawler
from ..core.config import get_settings

settings = get_settings()

# 投资相关搜索关键词
SEARCH_QUERIES = [
    "startup funding",
    "seed round",
    "series A",
    "venture capital",
    "AI startup",
    "Web3 funding",
    "crypto investment",
    "deep tech",
    "climate tech funding",
]

class TwitterCrawler(BaseCrawler):
    """Twitter/X 数据抓取"""
    
    def __init__(self):
        super().__init__("twitter")
        self.bearer_token = settings.TWITTER_BEARER_TOKEN or os.getenv("TWITTER_BEARER_TOKEN", "")
        self.base_url = "https://api.twitter.com/2"
    
    async def fetch(self, max_results: int = 50) -> List[Dict[str, Any]]:
        """搜索近期投资相关推文"""
        if not self.bearer_token:
            # Mock mode
            return self._mock_data()
        
        all_signals = []
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            headers = {"Authorization": f"Bearer {self.bearer_token}"}
            
            for query in SEARCH_QUERIES[:3]:  # 每次只搜3个关键词，避免限流
                params = {
                    "query": f"{query} -is:retweet lang:en",
                    "max_results": min(max_results // 3, 25),
                    "tweet.fields": "created_at,public_metrics,author_id",
                    "expansions": "author_id",
                    "user.fields": "public_metrics,username",
                }
                
                try:
                    resp = await client.get(
                        f"{self.base_url}/tweets/search/recent",
                        headers=headers,
                        params=params,
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    
                    tweets = data.get("data", [])
                    users = {u["id"]: u for u in data.get("includes", {}).get("users", [])}
                    
                    for tweet in tweets:
                        author = users.get(tweet.get("author_id", ""), {})
                        metrics = tweet.get("public_metrics", {})
                        
                        signal = self.normalize_signal({
                            "id": tweet["id"],
                            "text": tweet["text"],
                            "url": f"https://twitter.com/i/web/status/{tweet['id']}",
                            "author": f"@{author.get('username', 'unknown')}",
                            "followers": author.get("public_metrics", {}).get("followers_count", 0),
                            "engagement": metrics.get("like_count", 0) + metrics.get("retweet_count", 0) * 2,
                            "created_at": tweet.get("created_at"),
                        })
                        signal["tags"] = [query]
                        all_signals.append(signal)
                        
                except Exception as e:
                    print(f"Twitter crawl error for '{query}': {e}")
                    continue
        
        return all_signals
    
    def _mock_data(self) -> List[Dict[str, Any]]:
        """Mock数据：未配置API key时返回模拟信号"""
        return [
            {
                "source": "twitter",
                "source_id": "mock-1",
                "raw_content": "Just led the seed round in an AI agent startup building autonomous VC sourcing tools. Incredible team from OpenAI + Sequoia. $3M seed.",
                "url": "https://twitter.com/mock/1",
                "author": "@MockVC",
                "author_followers": 15000,
                "engagement_score": 245,
                "created_at": datetime.now().isoformat(),
                "tags": ["AI startup", "seed round"],
            },
            {
                "source": "twitter",
                "source_id": "mock-2",
                "raw_content": "Web3 infrastructure is heating up. Saw 3 DeFi protocols raise $10M+ this week alone. The infra layer is where the real value accrues.",
                "url": "https://twitter.com/mock/2",
                "author": "@CryptoAnalyst",
                "author_followers": 52000,
                "engagement_score": 1890,
                "created_at": (datetime.now() - timedelta(hours=2)).isoformat(),
                "tags": ["Web3 funding", "DeFi"],
            },
        ]
