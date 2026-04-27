"""
Sourcing System — 核心配置
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Optional

class Settings(BaseSettings):
    # App
    APP_NAME: str = "AI Sourcing System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "sqlite:///./sourcing.db"
    
    # LLM
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_BASE_URL: Optional[str] = None
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 4096
    
    # Data Sources
    TWITTER_BEARER_TOKEN: Optional[str] = None
    REDDIT_CLIENT_ID: Optional[str] = None
    REDDIT_CLIENT_SECRET: Optional[str] = None
    REDDIT_USER_AGENT: str = "AI-Sourcing-System/1.0"
    POLYMARKET_API_URL: str = "https://api.polymarket.com"
    
    # Agent Config
    INVESTMENT_MANAGER_COUNT: int = 26
    RISK_CONTROL_COUNT: int = 4
    IC_MEMBER_COUNT: int = 4
    IC_PROCEED_THRESHOLD: float = 6.0
    IC_ABANDON_THRESHOLD: float = 4.0
    
    # Sectors
    SECTORS: List[str] = [
        "AI", "Web3", "Healthcare", "HardTech",
        "Consumer", "Enterprise", "Fintech", "Climate"
    ]
    
    # Crawler
    CRAWLER_INTERVAL_MINUTES: int = 30
    MAX_SIGNALS_PER_RUN: int = 100
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
