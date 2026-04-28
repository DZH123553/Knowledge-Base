"""
Sourcing System — FastAPI 主入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import get_settings
from .core.database import init_db
from .api import signals, companies, ic_meetings, reports, agents, dashboard

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered VC Investment Intelligence Platform with Agentic Workflow",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
@app.on_event("startup")
async def startup():
    init_db()

# 注册路由
app.include_router(signals.router)
app.include_router(companies.router)
app.include_router(ic_meetings.router)
app.include_router(reports.router)
app.include_router(agents.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
