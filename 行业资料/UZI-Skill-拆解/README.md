# UZI-Skill 拆解 · 51人投资评审团

> 来源: [wbh604/UZI-Skill](https://github.com/wbh604/UZI-Skill)  
> 定位: A股/港股/美股 个股深度分析引擎  
> 核心亮点: **51位投资大佬各自按自己的方法论打分，最终加权产出综合评分**

---

## 目录

| 文件 | 内容 |
|------|------|
| [51人评审团实现原理.md](./51人评审团实现原理.md) | **核心分析文档** — 从架构到公式到Persona设计的完整拆解 |
| [investor-panel-agent.md](./investor-panel-agent.md) | Agent定义 — 7组投资者的role-play规则 |
| [investor-panel-skill.md](./investor-panel-skill.md) | Skill定义 — 50贤评审团的完整调用流程 |
| [deep-analysis-skill-excerpt.md](./deep-analysis-skill-excerpt.md) | 深度分析Skill中关于评审团的关键片段（Stage 3 / 评分公式 / 硬门控） |
| [personas/](./personas/) | **51个投资者Persona YAML档案** — 每个人有独立的投资哲学、关键指标、语言风格、历史持仓 |

---

## 一句话总结

UZI-Skill 的 51 人评审团 = **Prompt Engineering + YAML Persona + Rules 引擎 + LLM Role-play**

不是写死的代码打分，而是给每个投资者定义了一套"人格档案"（philosophy + key_metrics + voice），让 LLM 扮演他们去思考。脚本负责算骨架分，Agent 负责做真正的角色扮演覆盖。

---

## 7大流派 · 51人一览

| 组 | 流派 | 人数 | 代表 |
|----|------|------|------|
| A | 经典价值 | 6 | 巴菲特 · 格雷厄姆 · 费雪 · 芒格 · 邓普顿 · 卡拉曼 |
| B | 成长投资 | 4 | 林奇 · 欧奈尔 · 蒂尔 · 木头姐 |
| C | 宏观对冲 | 5 | 索罗斯 · 达里奥 · 马克斯 · 德鲁肯米勒 · 罗伯逊 |
| D | 技术趋势 | 4 | 利弗莫尔 · 米内尔维尼 · 达瓦斯 · 江恩 |
| E | 中国价投 | 6 | 段永平 · 张坤 · 朱少醒 · 谢治宇 · 冯柳 · 邓晓峰 |
| F | A股游资 | 23 | 章盟主 · 赵老哥 · 炒股养家 · 佛山无影脚 · 北京炒家 … |
| G | 量化系统 | 3 | 西蒙斯 · 索普 · 大卫·肖 |

---

## 核心评分公式

```
overall = fund_score × 0.6 + consensus × 0.4

consensus = (bullish + 0.6 × neutral) / active

verdict阈值（v2.11校准）:
  ≥80  强烈买入
  ≥65  买入
  ≥50  关注
  ≥35  观望
  <35  回避
```

---

## 可借鉴到自己的系统

1. **Persona 档案化**: 把投资人的方法论写成结构化 YAML（philosophy / key_metrics / avoids / voice），比纯 prompt 更稳定
2. **分组并行**: 7组风格差异大，可以并行 spawn sub-agent，每组独立 role-play
3. **骨架分 + Agent覆盖**: 先用规则引擎跑骨架分，再用 LLM 做真正的角色扮演覆盖 headline/reasoning/score
4. **射程预过滤**: 游资只评A股、木头姐只看颠覆式创新 —— 不在射程内直接 skip，避免噪音
5. **风格动态加权**: 按股票类型（白马/高成长/周期/小盘投机）动态调整各组权重
6. ** consensus 中性权重**: neutral 不是0分，而是0.6权重 —— 避免保守派拉低 consensus
