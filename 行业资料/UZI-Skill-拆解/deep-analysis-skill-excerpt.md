# Deep-Analysis Skill · 51人评审团关键片段

> 摘自 `skills/deep-analysis/SKILL.md` 中关于 Stage 3、评分公式、硬门控的核心内容

---

## Stage 3 · 51评委量化裁决

Task 3 产物：`.cache/{ticker}/panel.json`

角色：🤖 规则引擎（骨架分）+ 🧠 Agent role-play 覆盖

---

## 核心评分公式（v2.11 校准版）

```
overall = fund_score × 0.6 + consensus × 0.4

consensus = (bullish_count + 0.6 × neutral_count) / active_count
```

**v2.11 校准改动**：

| 改动 | 旧(v2.9.1) | 新(v2.11) | 影响 |
|------|-----------|-----------|------|
| verdict阈值 | 85/70/55/40 | **80/65/50/35** | 从未有股能≥85，下调5分让白马/真强股进"可以蹲一蹲"档 |
| consensus neutral权重 | 0.5（半权） | **0.6** | 51评委里价值派+游资35人偏保守，0.5让白马consensus仅37，0.6更贴近"不坑但不是心头好"的真实语义 |

公式（未变）：`overall = fund_score × 0.6 + consensus × 0.4`

典型白马（如茅台）预期：
- v2.9.1：`fund=62 consensus=45 → overall 55 → 观望优先`
- v2.11：`fund=62 consensus=50 → overall 57 → 观望优先`（但更接近"可以蹲一蹲"边界，白马行情启动时容易进65）

两档合计影响 ~5-8分。**真正的坑仍会 <35 → 回避**，分数辨识度不降反升。

---

## 风格动态加权（v2.7 · 自动）

stage2 自动识别股票 style（白马/高成长/周期/小盘投机/分红防御/困境反转/量化因子/中性兜底），按 style 调整：
- 51评委组级权重（A-G × style矩阵）+ 8个个体 override
- 22维 fundamental dim multiplier
- neutral 半权计入 consensus（修正旧公式0%权重的问题）

报告 hero 区会显示 style chip + 加权前后分数对比。

**Agent 可在 `agent_analysis.json` 显式覆盖 style**（若你认为脚本误判）：
```json
{
  "agent_reviewed": true,
  "detected_style_override": "growth_tech",
  "style_override_reason": "市值虽大但属于科技成长轨道，不是传统白马"
}
```

**量化因子型 detection（用户特别要求）**：
- `lib/quant_signal.detect_quant_signal` 用结构性特征：基金 top-1 持仓 < 2% → 疑似量化（无需名字含"量化"）
- 持有目标股票的基金里 ≥3家量化基金且把目标股放进 top-10 → quant_factor

---

## HARD-GATE-PERSONA-ROLEPLAY · 51评委 role-play 必须读 YAML persona（v2.15）

从 v2.15.0 起，`skills/deep-analysis/personas/*.yaml` 有全51位投资者的 persona 定义——
**12个 flagship 手写**（巴菲特/芒格/格雷厄姆/费雪/林奇/木头姐/索罗斯/达里奥/段永平/张坤/赵老哥/章盟主）
· **39个 stub 自动生成**（auto_generated_stub · 仅作基础身份提示，主要还是靠 Rules 引擎）。

**当你进入 stage1 后的 role-play 阶段时，必须**：

1. **读 `skills/deep-analysis/personas/{investor_id}.yaml`**（id 跟 panel.json 里一致，如 `buffett.yaml` / `zhao_lg.yaml`）
2. 对 **flagship persona**（12个）· YAML 优先级 > Rules headline：
   - 每条 headline 必须引用 `key_metrics` 里的具体条目（如巴菲特说"ROE 连续10年>15%"，段永平说"PE 40红线"，林奇说"PEG<1"，赵老哥说"封板时间+市值1000亿上限"）
   - 每条 reasoning 必须带 `voice` 字段的风格词（巴菲特的"Mr. Market"、林奇的"tenbagger"、木头姐的"Wright's Law / exponential disruption"、赵老哥的"龙头战法"）
   - **signal 必须与 persona 历史立场对齐**：巴菲特不会对 PE 882 的股票说买入；木头姐不会对白酒说"五大平台之一"；赵老哥不会对 9000 亿市值说"打板"
3. 对 **stub persona**（39个 · _meta.status=auto_generated_stub）· Rules 引擎输出优先：
   - YAML 仅补充身份信息（school / group）
   - 不要假装比 Rules 知道更多
   - 可以按 group 风格模板补充简短 voice，但不得编造具体历史言论
4. **prefix-stable system message**（如果走 `lib.personas.build_system_message`）：
   - 同一 SNAPSHOT JSON 只拼一次
   - 51 persona 调用时 system message 字节级一致（prompt cache 命中）

**绝不能**：
- ❌ 给某个投资者写他历史上不可能持的立场（林奇对 EPS 0 的股票说 PEG 可算 · 木头姐对 OEM 代工说"必须重仓"）—— Rules 引擎历史上有4个此类硬伤，v2.15 就是为修这个
- ❌ 用千篇一律的模板话术（"基本面良好"、"值得关注"、"估值合理"）—— 每个 persona 必须有自己 voice 字段里的特色语言
- ❌ 绕过 YAML 直接编 persona 历史立场（尤其是有 flagship 档案的12位 · 必须读档案）

---

## Agent 介入环节（Stage 1 之后、Stage 2 之前）

核心要求：**Do NOT run stage2() until ALL of the following are complete**:

1. You have READ `.cache/{ticker}/panel.json` and reviewed the 51 skeleton scores
2. You have SPAWNED sub-agents (or personally analyzed) each investor group
3. You have MERGED agent results back into panel.json with updated headline/reasoning/score
4. You have WRITTEN `agent_analysis.json` with dim_commentary (≥5 dimensions) + panel_insights
5. You have SET `agent_reviewed: true` in agent_analysis.json

Skipping this step produces a report with mechanical rule-engine output instead of genuine investment analysis. The whole point of this plugin is agent-driven judgment.

### agent_analysis.json 格式

```json
{
  "agent_reviewed": true,
  "dim_commentary": {
    "0_basic": "建筑央企，主营市政/房建。市值偏小，营收稳但利润率极薄（1.2%），典型低毛利基建股。",
    "1_financials": "ROE 不到8%，连续3年下滑。现金流波动大，应收账款占营收比偏高，回款风险明显。",
    "2_kline": "均线空头排列，MACD死叉，量能萎缩。典型下跌趋势，不满足Stage 2条件。"
  },
  "panel_insights": "51评委中，价值派集体看空（ROE太低+无护城河），游资中性（有地方城投概念但板块热度不够），只有少数逆向投资者给出中性偏多。整体共识32%，偏弱。",
  "great_divide_override": {
    "punchline": "DCF说高估23%，但城投重组预期让LBO视角的IRR仍有18% — 这个冲突值得关注。",
    "bull_say_rounds": [
      "宁波城投整合预期 + 地方债化解受益，估值有弹性",
      "PB仅0.9x，历史底部区间，安全边际够",
      "综合看62分，城投故事讲通了就是翻倍"
    ],
    "bear_say_rounds": [
      "ROE连降3年，基建毛利率8%是天花板",
      "应收账款/营收>60%，回款是生死线",
      "综合看35分，低质量资产不值得冒险"
    ]
  },
  "narrative_override": {
    "core_conclusion": "宁波建工 · 48分 · 谨慎。典型地方基建股，ROE不到8%、毛利率8%，靠城投整合讲故事。51位大佬12人看多，29人看空。DCF高估23%，但LBO压力测试IRR 18% — 博弈价值存在但风险更大。",
    "risks": [
      "ROE持续下滑，连续3年低于8%",
      "应收账款占比过高，回款周期拉长",
      "地方财政压力传导至工程款支付"
    ],
    "buy_zones": {
      "value": {"price": 3.85, "rationale": "PB 0.8x · 历史底部 + 净资产折价"},
      "growth": {"price": 4.10, "rationale": "城投整合落地前的博弈价"},
      "technical": {"price": 4.25, "rationale": "MA120支撑位 · 需放量确认"},
      "youzi": {"price": 4.50, "rationale": "城投板块联动时的短线切入点"}
    }
  }
}
```

**stage2() 会自动读取 agent_analysis.json，合并到 synthesis 中。** Agent 写入的字段优先级高于脚本生成的 stub。

---

## 多空大分歧 · The Great Divide

当51评委出现极端分歧时，系统生成"多空大辩论"：

费雪 100分 vs 卡拉曼 96分，三轮互喷，每轮引用具体数字。

**设计意图**：矛盾必须呈现，不准和稀泥。DCF 与 Comps 结论冲突时，**把冲突写进报告**；51评委分歧大时，**强调分歧本身是信息**。

---

## 自查 Gate（v2.9 机械强制）

`assemble_report.py::assemble()` 自动跑 `lib/self_review.py` 检查 ~13 条规则；有 critical 就 raise RuntimeError **拒绝生成 HTML**。

**自查覆盖的规则**（对应每次 BUG 经验）：

| severity | check | 背后 BUG |
|----------|-------|---------|
| 🔴 | `check_industry_mapping_sanity` | BUG#R10 行业碰撞（工业金属→农副食品加工） |
| 🔴 | `check_all_dims_exist` | wave2 timeout 导致 12_capital_flow 缺失 |
| 🔴 | `check_empty_dims` | crash / timeout 产生的空维度 |
| 🔴 | `check_panel_non_empty` | panel 全 skip / avg_score 异常 |
| 🔴 | `check_coverage_threshold` | `_integrity.coverage_pct < 60` |
| 🔴 | `check_placeholder_strings` | synthesis 含 "[脚本占位]" |
| 🔴 | `check_agent_analysis_exists` | agent_analysis.json 缺失 / agent_reviewed!=True |
| 🟡 | `check_valuation_sanity` | DCF/Comps 全0 |
| 🟡 | `check_industry_data_coverage` | 7_industry 定性字段需 web_search 补 |
| 🟡 | `check_factcheck_redflags` | 编造"苹果产业链"无 raw_data 证据 |

**迭代流程**：
```
loop:
  1. python review_stage_output.py <ticker>
  2. 读 _review_issues.json
  3. if critical_count > 0: 修 → 重跑 review
  4. if warning_count > 0: 修或 ack
  5. 若 critical_count == 0: 进入 HTML 生成
```
