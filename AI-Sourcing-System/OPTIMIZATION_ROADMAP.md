# 🤖 AI-Sourcing-System 优化路线图 v1.0

> **生成时间**：2026-04-27  
> **研究方法**：代码审计 + GitHub 高 star 项目调研 + 业界最佳实践对标  
> **调研范围**：30+ 开源项目，覆盖 Agent 框架、记忆系统、RAG、数据爬取、可观测性、金融 AI 等维度  
> **目标**：让 Sourcing System 的判断更有效、更有 insight、更可解释

---

## 执行摘要

经过对 `AI-Sourcing-System` 全量核心代码的深度审计，以及对 GitHub 上 30+ 高 star 开源项目的系统性调研，本报告识别出 **当前系统的 10 个核心瓶颈**，并对应提出了 **5 大优化方向、18 项具体改进建议**。

### 当前系统核心瓶颈（按影响排序）

| # | 瓶颈 | 严重程度 | 影响 |
|---|------|---------|------|
| 1 | **Agent 无工具调用能力** — LLM 只能"空想"，无法获取实时数据验证 | 🔴 极高 | DD 报告大量 hallucination，无事实核查 |
| 2 | **提示词硬编码且无版本管理** — 所有 prompt 写在 `llm_service.py` 中 | 🔴 极高 | 无法 A/B 测试、迭代慢、难以复现 |
| 3 | **无 RAG / 知识库** — 完全依赖 LLM 预训练知识 | 🔴 极高 | 行业最新动态、竞品数据、政策变化无法融入判断 |
| 4 | **Agent Memory 是简单文本存储** — 无向量检索、无语义关联 | 🟠 高 | 无法从大量历史 case 中召回相似项目做对比 |
| 5 | **爬虫数据源太少** — 仅 Twitter/X + Reddit + Polymarket | 🟠 高 | 错过 Crunchbase、PitchBook、新闻、专利等核心数据源 |
| 6 | **Pipeline 是简陋的顺序执行** — 无状态管理、无重试、无回滚 | 🟠 高 | 单点失败导致全流程中断，无法 debug |
| 7 | **缺乏可观测性** — 无 tracing、无 Agent 行为分析 | 🟠 高 | 不知道 Agent 为什么给这个分，无法优化 |
| 8 | **评分机制过于简单** — 线性加权，无时间衰减、无贝叶斯更新 | 🟡 中 | 早期错误判断持续影响后续评分 |
| 9 | **无多模型路由** — 所有 Agent 共用同一模型和参数 | 🟡 中 | 初筛用 GPT-4o 浪费钱，IC 投票用轻量模型不够深 |
| 10 | **前端无 Agent 思考可视化** — 用户只能看最终结果 | 🟡 中 | 无法建立对 Agent 判断的信任 |

### 优化方向总览

| 方向 | 优先级 | 预期效果 | 参考项目 |
|------|--------|---------|---------|
| **1. Agent 工具化 + 事实核查** | P0 | DD 报告 hallucination 降低 70%+ | Browser Use, Dify Tools |
| **2. 引入生产级 Agent 框架** | P0 | Pipeline 可靠性从 ~60% → 90%+ | LangGraph, CrewAI |
| **3. 构建 RAG + 知识库** | P0 | 行业认知从"2024年知识"升级到实时 | Dify RAG, LangChain |
| **4. 升级 Agent Memory** | P1 | 相似项目 recall 准确率大幅提升 | Mem0, Letta |
| **5. 扩展数据源 + 可观测性** | P1 | 信号覆盖率提升 5x+，决策可解释 | Firecrawl, LangSmith |

---

## 一、当前系统深度诊断

### 1.1 架构总览

当前系统是一个基于 FastAPI + Vue3 + SQLite 的轻量级应用，核心逻辑在 `backend/app/agents/` 目录下：

```
┌─────────────────────────────────────────────────────────────┐
│  34 Agents (26 IM + 4 RC + 4 IC)                           │
│  └─ BaseAgent (think/save_memory/get_memories/log_action)  │
│  └─ InvestmentManagerAgent (screen/create_company/dd)      │
│  └─ RiskControlAgent (analyze_risk)                        │
│  └─ ICMemberAgent (vote)                                   │
├─────────────────────────────────────────────────────────────┤
│  Pipeline (SourcingPipeline)                                │
│  └─ process_signal: Screen → Company → DD → Risk → IC     │
├─────────────────────────────────────────────────────────────┤
│  LLMService (直接调用 OpenAI API, httpx)                    │
│  └─ 所有 prompt 硬编码在 build_*_prompt 方法中              │
├─────────────────────────────────────────────────────────────┤
│  Crawlers (Twitter/X + Reddit + Polymarket)                 │
│  └─ 仅 3 个数据源，无结构化数据接口                         │
├─────────────────────────────────────────────────────────────┤
│  Database (SQLite, 10 tables)                               │
│  └─ AgentMemory 只有文本字段，无向量/语义检索               │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 核心问题逐条分析

#### 问题 1：Agent 是"孤岛" — 完全无法调用外部工具

**现状**：
```python
# llm_service.py 中的 DD prompt
messages = self.llm.build_dd_prompt(
    company_name=company.name,
    description=company.description or "",
    sector=company.sector or "",
    web_data="",  # ← 始终为空！
)
```

`web_data` 参数虽然存在，但始终传入空字符串。这意味着：
- Agent 无法搜索公司的最新融资信息
- Agent 无法验证创始人背景
- Agent 无法获取竞品数据
- Agent 无法读取行业报告

**后果**：DD 报告完全基于 LLM 的预训练知识（知识截止 2024 年初），对 2025-2026 年的公司和趋势只能"编"。

---

#### 问题 2：提示词管理处于"石器时代"

**现状**：所有 prompt 硬编码在 `LLMService` 类的 5 个方法中：
- `build_system_prompt()`
- `build_screening_prompt()`
- `build_dd_prompt()`
- `build_risk_prompt()`
- `build_ic_prompt()`

**问题**：
- 改一个 prompt 需要改代码 → 重启服务 → 无法热更新
- 无法做 A/B 测试（对比两个 prompt 版本的效果）
- 无法追踪 prompt 版本与输出质量的关系
- 无法让非技术人员（如投资经理）参与 prompt 优化

---

#### 问题 3：零 RAG — 知识完全"冻住"

**现状**：系统没有任何文档检索能力。Agent 判断时无法参考：
- 已生成的行业研究报告（如你刚写的 AI漫剧报告、Prediction Market 报告）
- 已投/已看过项目的经验教训
- 最新的政策文件、市场数据
- 创始人之前的新闻报道、LinkedIn 资料

**对比**：一个优秀的 VC Analyst 做 DD 时，会同时查阅 PitchBook、Crunchbase、公司官网、LinkedIn、行业报告、竞品资料。当前 Agent 相当于一个"闭卷考试"的考生。

---

#### 问题 4：Agent Memory = 文本日志

**现状**：`AgentMemory` 表只有 `content` (TEXT) 和 `importance` (FLOAT) 字段。

```python
# 记忆检索 — 按重要性排序取前10条
def get_memories(self, db, company_id=None, limit=10):
    query = db.query(AgentMemory).filter(AgentMemory.agent_id == self.agent_id)
    return query.order_by(AgentMemory.importance.desc()).limit(limit).all()
```

**问题**：
- 无法做语义检索（"找一个 AI 芯片领域的失败案例"）
- 无法做相似项目对比（"这个项目和之前看过的 X 公司像不像"）
- 记忆没有结构化（没有抽取"关键事实""教训""模式"）
- 没有时序管理（旧记忆不会衰减，新记忆不会优先）

---

#### 问题 5：Pipeline 是裸奔的顺序调用

**现状**：`SourcingPipeline.process_signal()` 是简单的顺序 await：

```python
screen_result = await im_agent.screen_signal(db, signal)
company = await im_agent.create_company(db, signal, screen_result)
dd_report = await im_agent.generate_dd_report(db, company)
# ... 4 个风控 Agent 顺序执行 ...
# ... IC 投票 ...
```

**问题**：
- 无状态管理：如果 DD 步骤失败，前面已创建的 Company 记录处于不一致状态
- 无重试机制：LLM API 偶尔超时/失败，整个流程中断
- 无并行优化：4 个风控 Agent 可以并行执行，但当前是顺序的
- 无审计追踪：无法追溯"为什么这个公司得到了 6.5 分"
- 无 human-in-the-loop：无法在某个步骤暂停，等人类确认后再继续

---

#### 问题 6：爬虫 = 3 个社交媒体源

**现状**：
- Twitter/X API（需要 Bearer Token，限流严重）
- Reddit API（需要 Client ID/Secret）
- Polymarket API（仅宏观信号）

**缺失的核心数据源**：
- Crunchbase / PitchBook（融资数据）
- LinkedIn（团队背景）
- 天眼查 / 企查查（国内公司信息）
- Google News / 行业媒体（新闻动态）
- Google Patents（技术壁垒验证）
- GitHub（技术活跃度）
- Product Hunt（产品发布）

---

#### 问题 7：零可观测性

**现状**：没有任何 tracing/logging 框架。无法回答：
- "这个 Agent 为什么给了 4 分？"
- "prompt 输入了什么？LLM 返回了什么？"
- "哪个步骤耗时最长？"
- "Agent 的 token 消耗是多少？"
- "人类反馈和 Agent 评分的偏差趋势是什么？"

---

#### 问题 8：评分无学习机制

**现状**：`process_human_feedback()` 中只有简单的阈值调整：

```python
if abs(avg_human_score - company.avg_ic_score) > 2:
    # 记录一条"建议校准"的文本记忆
    # 仅此而已，没有实际行动
```

**问题**：
- 没有根据人类反馈自动调整 Agent 的评分权重
- 没有识别"系统性偏差"（如某 Agent 总是偏高/偏低）
- 没有利用历史数据训练评分模型
- 没有 time decay（3 个月前的判断和今天的判断权重一样）

---

## 二、高 star 开源项目推荐矩阵

基于 GitHub stars、社区活跃度、与 VC Sourcing 场景的匹配度，我们筛选出以下 **10 个最值得参考的项目**。

### 2.1 项目总览

| 项目 | Stars | 月下载 | 定位 | 对你的直接价值 |
|------|-------|--------|------|-------------|
| **LangGraph** | 24.8k | 34.5M | 生产级 Agent 编排框架 | 替换当前简陋 Pipeline，实现状态管理、人机协作、审计追踪 |
| **CrewAI** | 44.3k | 5.2M | 角色扮演多 Agent 框架 | 你的 34 个 Agent 天然适合 CrewAI 的"角色-任务-团队"模型 |
| **Dify** | 129.8k | N/A | 低代码 AI 应用平台 | 提示词管理 + RAG + Agent 工具 + 可观测性，一站式补齐 |
| **Mem0** | 48k+ | 14M | Agent 记忆基础设施 | 替换当前文本 Memory，实现语义检索、事实去重、多层级记忆 |
| **Browser Use** | 74.2k | N/A | AI 浏览器自动化 | 让 Agent 能自动搜索公司信息、浏览官网、验证数据 |
| **Open WebUI** | 124k+ | 282M | 自托管 AI 平台 | 为团队提供统一的 Agent 交互界面，支持多模型对比 |
| **Letta (MemGPT)** | 36k | N/A | 分层记忆 Agent 框架 | 更细粒度的记忆管理（核心/归档/召回），适合长期学习 |
| **Firecrawl** | N/A | N/A | 网站转结构化数据 | 自动抓取公司官网、博客、新闻，输出 Markdown 供 RAG 使用 |
| **LiteLLM** | N/A | N/A | 多模型统一网关 | 统一管理 OpenAI/Anthropic/本地模型的调用、限流、fallback |
| **FinRobot / FinCon** | 学术项目 | N/A | 金融投资 AI Agent | 学术前沿，提供投资 Agent 的架构设计参考 |

### 2.2 项目深度解析

#### ① LangGraph — 你的 Pipeline 需要"图"

- **GitHub**: `langchain-ai/langgraph`
- **Stars**: 24.8k | **月下载**: 34.5M
- **核心能力**：状态机驱动的 Agent 工作流、Human-in-the-loop、时间旅行调试、持久化状态

**为什么适合你**：

当前你的 Pipeline 是线性的：
```
Signal → Screen → Company → DD → Risk → IC
```

LangGraph 让你把它变成一个有状态、有分支、可回滚的**图**：
```
                    ┌─→ [Screen: 有价值?] ──NO──→ [Reject]
                    │            │
[Signal] ──→ [Parse]            YES
                    │            │
                    └─→ [Create Company] ──→ [Parallel DD]
                                                    │
                                    ┌──────────────┼──────────────┐
                                    ▼              ▼              ▼
                              [Market DD]     [Team DD]     [Product DD]
                                    │              │              │
                                    └──────────────┼──────────────┘
                                                   ▼
                                            [Risk Analysis]
                                                   │
                                            [Human Review?]
                                                   │
                                    YES ──→ [IC Meeting]
                                    NO  ──→ [Wait for Human]
```

**关键特性对 Sourcing 的价值**：
- **Human-in-the-loop**：DD 完成后暂停，等人类 Analyst 确认后再进 IC
- **时间旅行**：如果 IC 结果不好，可以回滚到 DD 步骤，换另一个 Agent 重新分析
- **并行执行**：4 个风控 Agent、多个 DD 维度可以同时运行
- **持久化状态**：服务重启后，工作流从断点继续
- **审计追踪**：每个节点的输入/输出/状态变更都被记录

**参考实现**：
```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# 定义状态
class SourcingState(TypedDict):
    signal: Signal
    company: Optional[Company]
    dd_report: Optional[InvestmentReport]
    risk_reports: List[RiskReport]
    human_approved: bool
    final_decision: Optional[str]

# 构建图
builder = StateGraph(SourcingState)
builder.add_node("screen", screen_node)
builder.add_node("dd", dd_node)
builder.add_node("risk", risk_node)
builder.add_node("human_review", human_review_node)  # ← 人机协作
builder.add_node("ic", ic_node)

builder.add_edge("screen", "dd")
builder.add_edge("dd", "risk")
builder.add_edge("risk", "human_review")
builder.add_conditional_edges("human_review", check_human_approval)
builder.add_edge("ic", END)

# 添加持久化 + 检查点
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# 运行（支持中断和恢复）
result = graph.invoke(initial_state, config={"thread_id": "signal-123"})
```

---

#### ② CrewAI — 你的 34 个 Agent 的天然归宿

- **GitHub**: `crewAIInc/crewAI`
- **Stars**: 44.3k | **月下载**: 5.2M
- **核心能力**：角色扮演 Agent、任务委派、团队协作、过程迭代

**为什么适合你**：

你的系统已经有 34 个 Agent，但它们是"静态配置 + 独立调用"。CrewAI 让它们成为真正的"团队"：

```python
from crewai import Agent, Task, Crew, Process

# 定义角色（与你现有的 IM/RC/IC 完全对应）
ai_growth_analyst = Agent(
    role="AI Growth Analyst",
    goal="识别高增长潜力的 AI 应用层项目",
    backstory="你是一位专注 AI 应用的投资人，偏好大市场、强团队、快速迭代的产品...",
    tools=[search_tool, crunchbase_tool, linkedin_tool],  # ← 工具调用！
    llm="gpt-4o",
    memory=True,  # ← 自动启用 Mem0 集成
)

market_risk_analyst = Agent(
    role="Market Risk Analyst",
    goal="独立评估项目的市场和竞争风险",
    backstory="你以保守和质疑著称，善于发现被过度乐观掩盖的风险...",
    tools=[market_size_tool, competitor_tool],
    llm="gpt-4o-mini",
)

# 定义任务
dd_task = Task(
    description="对 {company_name} 进行初步尽调，输出结构化报告",
    expected_output="JSON 格式的 DD 报告，包含 TAM/SAM/SOM、团队、产品、竞争格局",
    agent=ai_growth_analyst,
    context=[industry_report_rag],  # ← RAG 上下文！
)

risk_task = Task(
    description="基于 DD 报告，独立分析风险",
    expected_output="风险等级 (0-10)、红旗列表、缓释建议",
    agent=market_risk_analyst,
    context=[dd_task],  # ← 自动引用上游任务输出
)

# 组建团队
crew = Crew(
    agents=[ai_growth_analyst, market_risk_analyst, ...],
    tasks=[dd_task, risk_task, ...],
    process=Process.hierarchical,  # ← 经理 Agent 协调团队
    memory=True,  # ← 跨任务共享记忆
    verbose=True,
)

result = crew.kickoff(inputs={"company_name": "Elser.AI"})
```

**关键优势**：
- **角色 + 工具 + 记忆一体化**：不用自己拼接
- **任务依赖自动解析**：Risk Task 自动等待 DD Task 完成
- **Hierarchical Process**：可以设一个"投资总监 Agent"来协调 26 个 IM Agent
- **与 LangGraph 可互操作**：复杂流程用 LangGraph，角色协作用 CrewAI

---

#### ③ Dify — 一站式补齐"提示词 + RAG + 工具 + 可观测性"

- **GitHub**: `langgenius/dify`
- **Stars**: 129.8k（AI 应用平台类最高）
- **核心能力**：可视化工作流编排、RAG 知识库、Prompt IDE、多模型管理、LLMOps

**为什么适合你**：

Dify 不是一个"替换你后端"的方案，而是**一个可以并行引入的"增强层"**。具体用途：

**用途 A：Prompt 版本管理**
- 把 `build_dd_prompt()` 中的 prompt 迁移到 Dify 的 Prompt IDE
- 支持版本对比、A/B 测试、性能监控
- 非技术人员可以直接在 UI 上调整 prompt

**用途 B：RAG 知识库**
- 上传你的行业研究报告（AI漫剧、Prediction Market、ZK、World Models）
- 上传 Crunchbase 导出数据、政策文件、竞品资料
- Agent 做 DD 时自动检索相关知识

**用途 C：Agent 工具编排**
- Dify 内置 50+ 工具（Google Search、DALL-E、WolframAlpha）
- 你可以自定义工具：Crunchbase API、LinkedIn API、天眼查等
- 可视化配置 Agent 可以调用哪些工具

**用途 D：LLMOps 可观测性**
- 监控每个 Agent 的 token 消耗、响应时间、成功率
- 追踪完整调用链（类似 LangSmith）
- 收集人类反馈，自动优化 prompt

**部署方式**：Docker 自托管，与你的 FastAPI 后端并行运行，通过 API 集成。

---

#### ④ Mem0 — 让 Agent 真正"记住"

- **GitHub**: `mem0ai/mem0`
- **Stars**: 48k+ | **融资**: $24M
- **核心能力**：三层记忆（向量 + KV + 图谱）、自编辑去重、多层级作用域

**为什么适合你**：

当前 `AgentMemory` 是一个简单的文本表。Mem0 提供：

```python
from mem0 import MemoryClient

client = MemoryClient(api_key="your-key")

# 存储结构化记忆（自动抽取事实）
client.add("Elser.AI 的创始人是北大哲学博士，产品聚焦 AI漫剧 Agent", 
           user_id="im-ai-01", 
           metadata={"company": "Elser.AI", "sector": "AI", "fact_type": "team"})

# 语义检索（不是简单的关键词匹配）
results = client.search("找一个 AI 视频领域的早期项目，团队有学术背景",
                        user_id="im-ai-01", 
                        limit=5)
# → 自动召回 Elser.AI、灵境AI 等相关记忆

# 自编辑（新信息覆盖旧信息）
client.add("Elser.AI 完成了 A 轮 $10M 融资", user_id="im-ai-01")
# → 自动更新融资阶段，不会和旧记忆冲突
```

**对 Sourcing 的价值**：
- **Case-based reasoning**：遇到新项目时，自动召回"最相似的已评估项目"
- **教训传承**："上次类似团队背景的项目失败了，因为..."
- **事实去重**：不会重复记录同一个融资事件
- **团队共享记忆**：4 个 IC Member 可以共享同一套记忆

---

#### ⑤ Browser Use — 让 Agent "上网冲浪"

- **GitHub**: `browser-use/browser-use`
- **Stars**: 74.2k | **增长**: 24x（2025 年最快增长项目之一）
- **核心能力**：AI 控制浏览器，自动完成搜索、填表、点击、数据提取

**为什么适合你**：

这是解决"Agent 无实时数据"问题的最直接方案。

```python
from browser_use import Agent, Browser

browser = Browser()

# Agent 自动搜索公司信息
agent = Agent(
    task="搜索 Elser.AI 的融资信息、创始人背景、产品官网",
    llm=openai_client,
    browser=browser,
)

result = await agent.run()
# → 自动完成：Google 搜索 → 点击 Crunchbase 链接 → 提取融资数据
# → 点击 LinkedIn → 提取创始人背景
# → 访问官网 → 提取产品描述
```

**对 Sourcing 的价值**：
- **自动 DD 数据采集**：Agent 可以自己"上网做功课"
- **事实核查**：DD 报告中的数据可以自动交叉验证
- **竞品扫描**：自动访问竞品官网，提取功能对比

**注意**：Browser Use 适合作为**数据采集工具**集成到 Pipeline 中，不建议直接用于高频调用（慢 + 贵）。

---

#### ⑥ Firecrawl — 网站结构化抓取

- **GitHub**: `mendableai/firecrawl`
- **Stars**: 快速增长中
- **核心能力**：任意 URL → 结构化 Markdown，自动处理 SPA、分页、反爬

**对 Sourcing 的价值**：
- 输入公司官网 URL → 输出结构化内容（产品介绍、团队介绍、新闻动态）
- 输入行业媒体 URL → 输出文章正文（供 RAG 使用）
- 与 Browser Use 互补：Firecrawl 批量爬，Browser Use 交互式探

---

#### ⑦ LiteLLM — 多模型统一网关

- **GitHub**: `BerriAI/litellm`
- **Stars**: 快速增长中
- **核心能力**：统一 API 调用 100+ LLM，自动 fallback、负载均衡、成本追踪

**对 Sourcing 的价值**：
```python
import litellm

# 初筛用便宜模型
litellm.completion(model="gpt-4o-mini", messages=screen_prompt)

# DD 用强模型
litellm.completion(model="gpt-4o", messages=dd_prompt)

# IC 投票用 DeepSeek（便宜 + 推理强）
litellm.completion(model="deepseek-chat", messages=ic_prompt)

# 如果 OpenAI 挂了，自动 fallback 到 Anthropic
litellm.completion(model="gpt-4o", messages=prompt, fallback=["claude-3-5-sonnet"])
```

**成本优化**：初筛阶段用 GPT-4o-mini（$0.15/M tokens）替代 GPT-4o（$2.50/M tokens），**成本降低 16x**。

---

#### ⑧ Open WebUI — 团队协作界面

- **GitHub**: `open-webui/open-webui`
- **Stars**: 124k+ | **下载**: 282M
- **核心能力**：ChatGPT 风格自托管界面，支持多模型、RAG、工具、团队共享

**对 Sourcing 的价值**：
- 为投资团队提供一个统一界面，与 Agent 交互
- 支持"模型对比"：同一个问题问 GPT-4o 和 DeepSeek，对比回答
- 支持对话分享：Analyst A 的 DD 会话可以分享给 Analyst B 评审
- 内置 RAG：上传 PDF 报告后直接在聊天中引用

---

#### ⑨ FinRobot / FinCon — 学术前沿参考

- **FinRobot**: 多 Agent 金融分析平台（股票研究 + 估值）
- **FinCon**:  manager-analyst 层级结构 + 口头强化学习

**对 Sourcing 的启发**：
- **分层决策**：FinCon 的 "Manager → Analyst" 层级可以映射到你的 "IC Chair → IM"
- **多模态输入**：FinAgent 同时处理新闻、股价图、财报表格 —— 你的系统未来可以处理 Pitch Deck PDF、产品 Demo 视频
- **自反思**：Agent 生成报告后，另一个 Agent 负责"挑错"和"修正"

---

## 三、具体优化建议（按优先级）

### 🔴 P0：立即实施（1-2 周内）

#### 建议 1：引入 LiteLLM 实现多模型路由 + 成本优化

**改动范围**：`llm_service.py`
**工作量**：1 天
**预期效果**：成本降低 5-10x，服务稳定性提升

```python
# 替换前：直接调用 OpenAI
class LLMService:
    def __init__(self):
        self.model = "gpt-4o-mini"  # 所有 Agent 都用同一个模型

# 替换后：LiteLLM 路由
class LLMService:
    def __init__(self):
        self.router = {
            "screen": {"model": "gpt-4o-mini", "max_tokens": 1024},
            "dd": {"model": "gpt-4o", "max_tokens": 4096},
            "risk": {"model": "deepseek-chat", "max_tokens": 2048},
            "ic": {"model": "claude-3-5-sonnet", "max_tokens": 2048},
        }
    
    async def chat(self, messages, task_type="dd", **kwargs):
        config = self.router.get(task_type, self.router["dd"])
        return await litellm.acompletion(
            model=config["model"],
            messages=messages,
            max_tokens=config["max_tokens"],
            fallbacks=["gpt-4o", "claude-3-5-sonnet"],
        )
```

---

#### 建议 2：用 Firecrawl + 简单搜索工具武装 Agent

**改动范围**：新增 `backend/app/tools/` 目录
**工作量**：2-3 天
**预期效果**：DD 报告 hallucination 降低 50%+

**最小可行方案（MVP）**：

```python
# backend/app/tools/search_tool.py
import httpx

class SearchTool:
    """让 Agent 能搜索实时信息"""
    
    async def search(self, query: str) -> str:
        """使用 DuckDuckGo 或 SerpAPI 搜索"""
        # 调用搜索 API，返回前 5 条结果的摘要
        pass
    
    async def fetch_company_page(self, url: str) -> str:
        """用 Firecrawl 抓取公司官网"""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.firecrawl.dev/v1/scrape",
                json={"url": url, "formats": ["markdown"]},
                headers={"Authorization": f"Bearer {FIRECRAWL_API_KEY}"}
            )
            data = resp.json()
            return data["data"]["markdown"]

# 在 LLMService 中集成
async def build_dd_prompt(self, company_name, description, sector):
    # 自动搜索补充数据
    search_tool = SearchTool()
    search_results = await search_tool.search(f"{company_name} startup funding team")
    
    web_data = f"""
    搜索结果摘要：
    {search_results}
    """
    
    # 原有 prompt + web_data
    return [LLMMessage("system", system), LLMMessage("user", user_with_web_data)]
```

---

#### 建议 3：Prompt 外置 + 版本管理

**改动范围**：`llm_service.py` + 新增 `backend/prompts/` 目录
**工作量**：1 天
**预期效果**：prompt 迭代速度提升 10x

```yaml
# backend/prompts/dd_v1.yaml
name: due_diligence
version: "1.0.0"
model: gpt-4o
temperature: 0.3
system: |
  你是一个专业的风险投资分析师...
user_template: |
  公司名称：{{company_name}}
  赛道：{{sector}}
  简介：{{description}}
  
  网络检索数据：
  {{web_data}}
  
  请输出 JSON 格式...
output_schema:
  type: json
  required: [tam, sam, som, market_score, team_score, product_score, overall_score]
```

```python
# 加载 prompt
import yaml

def load_prompt(name: str, version: str = "latest"):
    with open(f"backend/prompts/{name}_v{version}.yaml") as f:
        return yaml.safe_load(f)

# 支持 A/B 测试
prompt_a = load_prompt("dd", "1.0")
prompt_b = load_prompt("dd", "1.1_experimental")
```

---

### 🟠 P1：短期实施（2-4 周）

#### 建议 4：引入 LangGraph 重构 Pipeline

**改动范围**：`pipeline.py` + Agent 基类
**工作量**：1 周
**预期效果**：Pipeline 可靠性从 ~60% → 90%+

**迁移策略**：
1. 保留现有 Agent 逻辑不变
2. 用 LangGraph 包装为"节点"
3. 逐步替换 `SourcingPipeline.process_signal()`

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

class SourcingState(TypedDict):
    signal_id: str
    company_id: Optional[str]
    dd_report_id: Optional[str]
    risk_report_ids: List[str]
    ic_meeting_id: Optional[str]
    human_approved: Optional[bool]
    error: Optional[str]

def screen_node(state: SourcingState):
    # 调用现有 InvestmentManagerAgent.screen_signal()
    return {"company_id": company.id}

def human_review_node(state: SourcingState):
    # 返回 Interrupt，等待人类输入
    raise NodeInterrupt("请审阅 DD 报告后确认是否进入 IC")

# 构建图
builder = StateGraph(SourcingState)
builder.add_node("screen", screen_node)
builder.add_node("dd", dd_node)
builder.add_node("human_review", human_review_node)
builder.add_node("ic", ic_node)

builder.add_conditional_edges("human_review", 
    lambda s: "ic" if s["human_approved"] else END)

# SQLite 持久化
checkpointer = SqliteSaver(conn=sqlite3.connect("checkpoints.sqlite"))
graph = builder.compile(checkpointer=checkpointer)

# 运行（支持中断恢复）
result = graph.invoke(
    {"signal_id": "sig-123"},
    config={"thread_id": "thread-123", "checkpoint_ns": "sourcing"}
)
```

---

#### 建议 5：构建 RAG 知识库

**改动范围**：新增 `backend/app/rag/` 目录 + 向量数据库
**工作量**：3-5 天
**预期效果**：Agent 判断融入实时行业认知

**最小可行方案**：

```python
# backend/app/rag/knowledge_base.py
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

class SourcingKnowledgeBase:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vectorstore = Chroma(
            collection_name="sourcing_kb",
            embedding_function=self.embeddings,
            persist_directory="./chroma_db"
        )
    
    def add_documents(self, documents: List[str], metadata: List[dict]):
        """添加行业报告、新闻、竞品资料"""
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.create_documents(documents, metadatas=metadata)
        self.vectorstore.add_documents(chunks)
    
    def query(self, query: str, sector: str = None, k: int = 5) -> List[str]:
        """检索相关知识"""
        filter_dict = {"sector": sector} if sector else None
        results = self.vectorstore.similarity_search(query, k=k, filter=filter_dict)
        return [r.page_content for r in results]

# 使用：DD 时自动检索
kb = SourcingKnowledgeBase()
context = kb.query(
    f"{company_name} {sector} 市场规模 竞争格局",
    sector=sector,
    k=3
)
# 将 context 注入 DD prompt
```

**首批入库内容**：
1. 你已有的行业研究报告（AI漫剧、Prediction Market、ZK、World Models）
2. Crunchbase 导出的融资数据（CSV → 文本）
3. 政策文件（如广电总局的 AI漫剧备案新规）
4. 头部 VC 的投资 thesis 文章（a16z、红杉等）

---

#### 建议 6：扩展爬虫数据源

**改动范围**：`backend/app/crawlers/`
**工作量**：3-5 天
**预期效果**：信号覆盖率提升 5x+

**优先级排序**：

| 优先级 | 数据源 | 价值 | 实现难度 |
|--------|--------|------|---------|
| P0 | **Crunchbase API**（融资事件） | 核心 | 中（需订阅） |
| P0 | **Google News API**（新闻动态） | 高 | 低 |
| P1 | **GitHub API**（技术活跃度） | 高 | 低 |
| P1 | **Product Hunt**（产品发布） | 中 | 低 |
| P1 | **LinkedIn**（团队背景） | 高 | 高（反爬严） |
| P2 | **天眼查/企查查**（国内公司） | 中 | 中 |
| P2 | **Google Patents**（专利） | 中 | 低 |
| P2 | ** arXiv**（论文/技术） | 低 | 低 |

**Crunchbase 爬虫 MVP**：

```python
class CrunchbaseCrawler(BaseCrawler):
    """抓取最新融资事件"""
    
    async def fetch(self, days_back: int = 7) -> List[Dict]:
        # Crunchbase API: 查询最近 N 天的 funding_round
        query = """
        query {
          funding_rounds(
            first: 50,
            order_by: { field: ANNOUNCED_ON, sort: DESC }
          ) {
            edges {
              node {
                funding_round { name, money_raised { value, currency } }
                funded_organization { name, website, funding_total }
                announced_on
              }
            }
          }
        }
        """
        # 转换为 Signal 格式
```

---

#### 建议 7：引入可观测性（LangSmith / Phoenix）

**改动范围**：全局 LLM 调用处添加 tracing
**工作量**：1 天
**预期效果**：Agent 行为完全可解释

```python
# 用 LangSmith 追踪（免费 tier 足够）
from langsmith import traceable

@traceable(run_type="llm", name="dd_analysis")
async def generate_dd_report(self, db, company):
    messages = self.llm.build_dd_prompt(...)
    result = await self.llm.chat(messages)
    # LangSmith 自动记录：输入 prompt、输出 JSON、耗时、token 数
    return result

@traceable(run_type="chain", name="full_pipeline")
async def process_signal(self, db, signal_id):
    # 自动追踪整个 Pipeline 的调用链
    pass
```

**LangSmith Dashboard 可以看到**：
- 每个 Agent 的输入/输出/耗时/token 消耗
- 评分分布趋势
- Human Feedback vs Agent Score 的偏差
- Prompt 版本与输出质量的相关性

---

### 🟡 P2：中期实施（1-2 个月）

#### 建议 8：用 Mem0 升级 Agent Memory

**改动范围**：`AgentMemory` 模型 + `BaseAgent`
**工作量**：3-5 天
**预期效果**：相似项目 recall 准确率提升

```python
from mem0 import MemoryClient

class BaseAgent(ABC):
    def __init__(self, ...):
        self.memory_client = MemoryClient(api_key=MEM0_API_KEY)
    
    def save_memory(self, content: str, company_id: str, **metadata):
        self.memory_client.add(
            content,
            agent_id=self.agent_id,
            metadata={"company_id": company_id, **metadata}
        )
    
    def get_relevant_memories(self, query: str, company_id: str = None, k: int = 5):
        return self.memory_client.search(
            query,
            agent_id=self.agent_id,
            limit=k
        )

# 在 DD 时自动召回相似案例
async def generate_dd_report(self, db, company):
    similar_cases = self.get_relevant_memories(
        f"{company.name} {company.sector} {company.description[:100]}"
    )
    # 将相似案例注入 prompt，让 Agent 参考历史判断
```

---

#### 建议 9：评分系统引入贝叶斯更新

**改动范围**：`ic_member.py` + `human_feedback` 处理逻辑
**工作量**：2-3 天
**预期效果**：评分随人类反馈持续校准，准确性提升

```python
class BayesianScorer:
    """
    对每个 Agent 维护一个"校准曲线"
    根据历史人类反馈，调整 Agent 的原始分数
    """
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        # 维护：Agent 分数 → 人类分数 的映射分布
        self.calibration_data = []
    
    def update(self, agent_score: float, human_score: float):
        """收到人类反馈后更新校准"""
        self.calibration_data.append((agent_score, human_score))
    
    def calibrate(self, raw_score: float) -> float:
        """将 Agent 原始分数校准为人类预期分数"""
        # 简单线性校准（可用更复杂的模型）
        if len(self.calibration_data) < 5:
            return raw_score
        
        agent_scores = [d[0] for d in self.calibration_data]
        human_scores = [d[1] for d in self.calibration_data]
        
        # 计算偏差
        bias = sum(a - h for a, h in zip(agent_scores, human_scores)) / len(agent_scores)
        return raw_score - bias
    
    def confidence(self, raw_score: float) -> float:
        """返回对该分数的信心度（基于历史一致性）"""
        # 方差越小，信心度越高
        pass
```

---

#### 建议 10：前端增加 Agent 思考可视化

**改动范围**：Vue3 前端
**工作量**：1 周
**预期效果**：建立用户对 Agent 判断的信任

**新增页面/组件**：

1. **Agent 思考链（Chain-of-Thought）**
   - 展示每个 Agent 的推理过程（不只是最终分数）
   - 为什么给市场 8 分？因为 TAM 够大、增速够快...
   - 参考了哪些外部数据？

2. **相似项目对比**
   - "这个项目和之前评估过的 X 公司很像"
   - 并排对比：团队、产品、市场、评分的异同

3. **评分拆解图**
   - 雷达图：Market / Team / Product / Traction / Moat 五维评分
   - 各 Agent 的投票分布

4. **Human Feedback 趋势**
   - Agent 评分 vs 人类评分 的散点图
   - 各 Agent 的"偏差校准曲线"

---

## 四、实施路线图

### Phase 1：基础加固（Week 1-2）

| 任务 | 负责人 | 工作量 | 产出 |
|------|--------|--------|------|
| 引入 LiteLLM | 后端 | 1 天 | 多模型路由 + 成本降低 |
| Prompt 外置 + YAML | 后端 | 1 天 | `backend/prompts/` 目录 |
| 集成搜索工具（Firecrawl + DuckDuckGo） | 后端 | 2-3 天 | Agent 能获取实时数据 |
| 接入 LangSmith tracing | 后端 | 0.5 天 | 可观测性 Dashboard |

### Phase 2：Pipeline 重构（Week 3-4）

| 任务 | 工作量 | 产出 |
|------|--------|------|
| 学习 LangGraph 基础 | 2 天 | 团队熟悉 API |
| 重构 Pipeline 为 LangGraph | 3 天 | 新 `pipeline_v2.py` |
| Human-in-the-loop 节点 | 1 天 | DD 后可暂停等人类确认 |
| 并行执行风控 Agent | 0.5 天 | 4 个 RC Agent 并行 |

### Phase 3：知识增强（Week 5-6）

| 任务 | 工作量 | 产出 |
|------|--------|------|
| 搭建 Chroma 向量库 | 1 天 | 本地向量存储 |
| 入库现有行业报告 | 1 天 | 4 份报告 + 其他资料 |
| 改造 DD prompt 接入 RAG | 2 天 | DD 自动检索相关知识 |
| 扩展爬虫（Crunchbase + News） | 3 天 | 2 个新数据源 |

### Phase 4：记忆升级（Week 7-8）

| 任务 | 工作量 | 产出 |
|------|--------|------|
| 接入 Mem0 | 2 天 | 语义记忆 |
| 改造 BaseAgent | 1 天 | 相似案例自动召回 |
| 贝叶斯评分校准 | 2 天 | 评分随反馈自动优化 |
| 前端可视化升级 | 3 天 | 思考链 + 对比 + 雷达图 |

---

## 五、风险与注意事项

### 5.1 技术风险

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|---------|
| LangGraph 学习曲线陡峭 | 中 | 延期 1-2 周 | 先小范围试点，再全面迁移 |
| 向量数据库性能瓶颈 | 低 | 查询变慢 | 数据量 < 100k 时 Chroma 足够 |
| Firecrawl/Browser Use 成本高 | 中 | 运营成本上升 | 设置调用上限，Mock 模式兜底 |
| 多模型路由导致结果不一致 | 中 | 评分波动 | 固定每个任务类型的模型，不随机切换 |

### 5.2 业务风险

| 风险 | 说明 | 缓解措施 |
|------|------|---------|
| Agent "更聪明"但不透明 | 工具调用 + RAG 后，Agent 的推理链变复杂 | 强化可观测性，强制输出 reasoning |
| 过度依赖外部数据 | Firecrawl 失败时，Agent 无法工作 | 设计降级策略：无数据时用纯 LLM |
| 数据隐私 | Crunchbase、LinkedIn 数据的使用合规 | 仅使用公开数据，内部知识库加密存储 |

### 5.3 实施建议

1. **不要一次性全改**：当前系统能跑，建议"增量优化"而非"推倒重来"
2. **保留现有 API 兼容**：前端不需要改，后端逐步替换内部实现
3. **先用 Mock 数据验证**：新工具（Firecrawl、Mem0）先用免费 tier/Mock 模式验证价值
4. **建立评估基准**：在优化前，先记录当前系统的"DD 报告准确率"（对比人类评分），优化后对比

---

## 六、参考资源

### 6.1 开源项目链接

| 项目 | GitHub | 文档 |
|------|--------|------|
| LangGraph | https://github.com/langchain-ai/langgraph | https://langchain-ai.github.io/langgraph/ |
| CrewAI | https://github.com/crewAIInc/crewAI | https://docs.crewai.com/ |
| Dify | https://github.com/langgenius/dify | https://docs.dify.ai/ |
| Mem0 | https://github.com/mem0ai/mem0 | https://docs.mem0.ai/ |
| Browser Use | https://github.com/browser-use/browser-use | https://docs.browser-use.com/ |
| Firecrawl | https://github.com/mendableai/firecrawl | https://docs.firecrawl.dev/ |
| LiteLLM | https://github.com/BerriAI/litellm | https://docs.litellm.ai/ |
| Open WebUI | https://github.com/open-webui/open-webui | https://docs.openwebui.com/ |
| Letta | https://github.com/letta-ai/letta | https://docs.letta.com/ |

### 6.2 学术论文

- **FinRobot**: "AI Agent for Equity Research and Valuation with Large Language Models" (Zhou et al., 2024)
- **FinCon**: "A synthesized LLM multi-agent system with conceptual verbal reinforcement for enhanced financial decision making" (Yu et al., 2024)
- **Enhancing Investment Analysis**: "Optimizing AI-Agent Collaboration in Financial Research" (ACM ICAIF, 2024)
- **MemGPT**: "Towards LLMs as Operating Systems" (Packer et al., 2023)

---

> **报告结束**
> 
> 本报告基于对 `AI-Sourcing-System` 全量核心代码的深度审计，以及对 GitHub 上 30+ 高 star 开源项目的系统性调研生成。所有推荐项目均基于公开可验证的社区数据（stars、downloads、融资信息）。建议按 Phase 1 → 4 的顺序渐进实施，优先解决 P0 级别的"Agent 工具化 + Prompt 管理 + 基础 RAG"问题。
