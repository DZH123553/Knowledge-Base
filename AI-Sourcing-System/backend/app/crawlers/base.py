"""
Sourcing System — 爬虫基类
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime

class BaseCrawler(ABC):
    """爬虫抽象基类"""
    
    def __init__(self, source_name: str):
        self.source_name = source_name
    
    @abstractmethod
    async def fetch(self, **kwargs) -> List[Dict[str, Any]]:
        """抓取数据，返回结构化信号列表"""
        pass
    
    def normalize_signal(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """标准化为系统信号格式"""
        return {
            "source": self.source_name,
            "source_id": raw.get("id", ""),
            "raw_content": raw.get("text", raw.get("content", "")),
            "url": raw.get("url", ""),
            "author": raw.get("author", ""),
            "author_followers": raw.get("followers", 0),
            "engagement_score": raw.get("engagement", 0),
            "created_at": raw.get("created_at", datetime.now().isoformat()),
        }
