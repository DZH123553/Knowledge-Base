"""
Sourcing System — Reddit 爬虫
监控投资、创业相关subreddit
"""
import os
import httpx
from typing import List, Dict, Any
from datetime import datetime, timedelta

from .base import BaseCrawler
from ..core.config import get_settings

settings = get_settings()

# 目标subreddits
TARGET_SUBREDDITS = [
    "startups",
    "venturecapital",
    "investing",
    "web3",
    "artificial",
    "SaaS",
]

class RedditCrawler(BaseCrawler):
    """Reddit 数据抓取"""
    
    def __init__(self):
        super().__init__("reddit")
        self.client_id = settings.REDDIT_CLIENT_ID or os.getenv("REDDIT_CLIENT_ID", "")
        self.client_secret = settings.REDDIT_CLIENT_SECRET or os.getenv("REDDIT_CLIENT_SECRET", "")
        self.user_agent = settings.REDDIT_USER_AGENT
    
    async def fetch(self, limit: int = 50) -> List[Dict[str, Any]]:
        """抓取热门帖子"""
        if not self.client_id:
            return self._mock_data()
        
        all_signals = []
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # OAuth token
            auth = httpx.BasicAuth(self.client_id, self.client_secret)
            token_resp = await client.post(
                "https://www.reddit.com/api/v1/access_token",
                auth=auth,
                data={"grant_type": "client_credentials"},
                headers={"User-Agent": self.user_agent},
            )
            token = token_resp.json().get("access_token", "")
            
            headers = {
                "Authorization": f"Bearer {token}",
                "User-Agent": self.user_agent,
            }
            
            for subreddit in TARGET_SUBREDDITS[:3]:
                try:
                    resp = await client.get(
                        f"https://oauth.reddit.com/r/{subreddit}/hot",
                        headers=headers,
                        params={"limit": limit // 3},
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    
                    for post in data.get("data", {}).get("children", []):
                        p = post["data"]
                        signal = self.normalize_signal({
                            "id": p["id"],
                            "text": f"[{p.get('subreddit', '')}] {p.get('title', '')}\n{p.get('selftext', '')[:500]}",
                            "url": f"https://reddit.com{p.get('permalink', '')}",
                            "author": f"u/{p.get('author', 'unknown')}",
                            "engagement": p.get("score", 0) + p.get("num_comments", 0) * 3,
                            "created_at": datetime.fromtimestamp(p.get("created_utc", 0)).isoformat(),
                        })
                        signal["tags"] = [subreddit]
                        all_signals.append(signal)
                        
                except Exception as e:
                    print(f"Reddit crawl error for r/{subreddit}: {e}")
                    continue
        
        return all_signals
    
    def _mock_data(self) -> List[Dict[str, Any]]:
        return [
            {
                "source": "reddit",
                "source_id": "mock-r1",
                "raw_content": "[startups] Just closed our Series A! $12M led by Andreessen Horowitz. We're building AI-powered code review tools. AMA!",
                "url": "https://reddit.com/r/startups/mock1",
                "author": "u/founder_ai",
                "author_followers": 0,
                "engagement_score": 892,
                "created_at": datetime.now().isoformat(),
                "tags": ["startups", "Series A"],
            },
        ]
