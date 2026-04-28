# 🤖 AI Sourcing System

复刻 [sourcing.readtheone.com](https://sourcing.readtheone.com/) 的 AI 驱动 VC 投资情报平台，包含完整的 Agentic Workflow。

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                        前端 (Vue 3)                          │
│   Dashboard │ Signals │ Companies │ IC Meetings │ Reports    │
└──────────────────────┬──────────────────────────────────────┘
                       │ REST API
┌──────────────────────▼──────────────────────────────────────┐
│                     后端 (FastAPI)                           │
│  /signals │ /companies │ /ic-meetings │ /reports │ /agents   │
└──────────────────────┬──────────────────────────────────────┘
                       │
    ┌──────────────────┼──────────────────┐
    │                  │                  │
┌───▼────┐      ┌─────▼─────┐     ┌──────▼──────┐
│ Agents │      │  Database │     │  Crawlers   │
│ 34个   │      │  SQLite   │     │ Twitter/X   │
│        │      │           │     │ Reddit      │
│ 26 IM  │      │ 10 Tables │     │ Polymarket  │
│ 4 RC   │      │           │     │             │
│ 4 IC   │      │           │     │             │
└────────┘      └───────────┘     └─────────────┘
```

## Agent 矩阵 (34 Agents)

| 类型 | 数量 | 说明 |
|------|------|------|
| Investment Manager | 26 | 按赛道分配：AI(4), Web3(3), Healthcare(3), HardTech(4), Consumer(2), Enterprise(3), Fintech(3), Climate(2) |
| Risk Control | 4 | 独立风控：Market, Financial, Team, Tech |
| IC Member | 4 | 投委会：Chair(1.5x权重), Growth, Tech, Ops |

## 数据流

```
Signal(raw) → Parse → Screen → Company → DD Report → Risk Report → IC Meeting → Human Feedback → Agent Memory
     ↑                                                                                                    │
     └──────────────────────────────────── 记忆更新，自主阈值调整 ──────────────────────────────────────────┘
```

## 评分规则

- **6分 = 明确推进 (proceed)**
- **4分 = 明确放弃 (abandon)**
- 无5分制（避免模糊）
- 加权平均得出最终分数

## 快速开始

### 1. 安装依赖

```bash
# 后端
cd backend
pip install -r requirements.txt

# 前端
cd frontend
npm install
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入 OPENAI_API_KEY
```

### 3. 初始化数据库

```bash
cd backend
python ../scripts/init_db.py
```

### 4. 启动服务

```bash
# 后端 (端口 8000)
cd backend
python run.py

# 前端 (端口 3000，新终端)
cd frontend
npm run dev
```

### 5. 访问

- 前端: http://localhost:3000
- API 文档: http://localhost:8000/docs

## 核心功能

### 自动IC讨论
```bash
# 手动输入公司，自动走完 Screen → DD → Risk → IC 全流程
python scripts/run_ic_autogen.py --case "Example AI Startup" --desc "Building AI agents for VC"
```

### API 触发
```bash
curl -X POST http://localhost:8000/agents/auto-ic \
  -H "Content-Type: application/json" \
  -d '{"company_name": "Example", "description": "AI startup"}'
```

## 数据库 Schema

| 表名 | 说明 |
|------|------|
| signals | 原始信号 |
| signal_monitoring | Agent监控日志 |
| companies | 公司实体 |
| investment_reports | DD报告 |
| risk_reports | 风险报告 |
| ic_meetings | IC会议纪要 |
| ic_meeting_votes | IC投票明细 |
| human_feedback | 人类反馈 |
| agent_memories | Agent记忆 |
| crawler_logs | 爬虫日志 |

## 技术栈

- **后端**: Python 3.11, FastAPI, SQLAlchemy, SQLite
- **前端**: Vue 3, TypeScript, Vite, Tailwind CSS
- **AI**: OpenAI GPT-4o-mini (可替换为任意兼容API)
- **爬虫**: Twitter API v2, Reddit API, Polymarket
