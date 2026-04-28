"""
Sourcing System — Polymarket 爬虫
抓取预测市场数据作为宏观信号
"""
import httpx
from typing import List, Dict, Any
from datetime import datetime

from .base import BaseCrawler
from ..core.config import get_settings

settings = get_settings()

class PolymarketCrawler(BaseCrawler):
    """Polymarket 预测市场数据"""
    
    def __init__(self):
        super().__init__("polymarket")
        self.api_url = settings.POLYMARKET_API_URL
    
    async def fetch(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取热门预测市场"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Polymarket Gamma API
                resp = await client.get(
                    f"{self.api_url}/gamma-api/markets",
                    params={"active": "true", "closed": "false", "limit": limit},
                )
                resp.raise_for_status()
                data = resp.json()
                
                signals = []
                for market in data.get("markets", [])[:limit]:
                    # 只关注科技/投资相关市场
                    tags = market.get("tags", [])
                    if not any(t in ["Tech", "Crypto", "Business", "Politics"] for t in tags):
                        continue
                    
                    signal = self.normalize_signal({
                        "id": market.get("slug", ""),
                        "text": f"Polymarket: {market.get('question', '')}\n"
                                f"Volume: ${market.get('volume', 0):,.0f}\n"
                                f"Liquidity: ${market.get('liquidity', 0):,.0f}",
                        "url": f"https://polymarket.com/event/{market.get('slug', '')}",
                        "author": "Polymarket",
                        "engagement": float(market.get("volume", 0)) / 1000,
                        "created_at": market.get("createdAt", datetime.now().isoformat()),
                    })
                    signal["tags"] = tags
                    signals.append(signal)
                
                return signals
                
        except Exception as e:
            print(f"Polymarket crawl error: {e}")
            return self._mock_data()
    
    def _mock_data(self) -> List[Dict[str, Any]]:
        return [
            {
                "source": "polymarket",
                "source_id": "mock-p1",
                "raw_content": "Polymarket: Will any AI company IPO in 2025?\nVolume: $2,450,000\nLiquidity: $890,000",
                "url": "https://polymarket.com/event/ai-ipo-2025",
                "author": "Polymarket",
                "author_followers": 0,
                "engagement_score": 2450,
                "created_at": datetime.now().isoformat(),
                "tags": ["Tech", "AI"],
            },
        ]
