# Polymarket BTC 5分钟涨跌策略 — GitHub 竞品深度调研报告

> **调研日期**: 2026-04-28  
> **目标市场**: https://polymarket.com/event/btc-updown-5m-1777373400  
> **调研范围**: GitHub 上所有 Polymarket 5分钟 BTC Up/Down 交易策略

---

## 一、最相关的 6 个项目

### 1. TheOneWhoBurns/btc-updown-bot ⭐ 最实战（有真实交易记录）

| 属性 | 内容 |
|------|------|
| **GitHub** | https://github.com/TheOneWhoBurns/btc-updown-bot |
| **定位** | Polymarket BTC 5分钟 Up/Down 全自动交易机器人 |
| **语言** | Python |
| **核心模型** | GBM 波动率模型 + Kelly Criterion 仓位管理 |

**v1 真实交易结果（血的教训）**:
- 本金: $130 USDC
- 交易次数: 159 个市场
- 胜率: 65.4%
- **最终盈亏: -$96.64 ❌**
- 原因分析:
  1. **Ghost fills**: GTC 限价单显示 MATCHED 但实际 0 shares
  2. **Adverse selection**: 赢的限价单不成交，输的必成交
  3. **Silent redemption failures**: redeem_positions() 返回 True 但到账 $0
  4. **Paper WR (77%) ≠ Real WR (65.4%)**

**v2 改进（基于 162 笔真实交易的过滤器）**:

| 过滤器 | 值 | 原因 |
|--------|-----|------|
| `P_ENTRY` | >= 0.84 | 最低模型置信度 |
| `MIN_BUY_PRICE` | >= $0.70 | $0.65-0.70 区间胜率 41%，亏损 $43 |
| `MAX_BUY_PRICE` | <= $0.90 | 避免过高价格 |
| `MIN_EDGE` | >= 0.00 | 负 edge 交易亏损 $20.75 |
| `MAX_TAU` | <= 250s | 早期入场(280s+)反转率高 |
| `MIN_TAU` | >= 30s | 太接近到期无法成交 |
| `VOL_KILL` | 0.05-0.30% | 跳过极端波动 |

**核心公式**:
```python
P_up = Phi(ln(S_t / S_0) / (sigma * sqrt(tau)) * 0.95)
# S_0 = BTC 窗口起始价格
# S_t = 当前 BTC 价格 (Binance websocket)
# tau = 窗口剩余秒数
# sigma = EWMA 每秒波动率 (10分钟回望)
# 0.95 = 均值回归阻尼因子
```

**仓位管理**: Scaled Kelly fraction (0.05-0.75)，基于内部 bankroll

---

### 2. wincXDSolana/polymarket-bot ⭐ 3 (MoonDev 风格)

| 属性 | 内容 |
|------|------|
| **GitHub** | https://github.com/wincXDSolana/polymarket-bot |
| **定位** | 5分钟 BTC/ETH/SOL Up/Down 均值回归机器人 |
| **策略** | 均值回归 + MACD 确认 |

**核心逻辑**:
```python
def mean_reversion_signal(df):
    df["sma"] = df["close"].rolling(10).mean()
    df["dev"] = (df["close"] - df["sma"]) / df["sma"]
    
    # MACD 确认
    macd = ta.trend.MACD(df["close"])
    df["macd"] = macd.macd()
    df["signal"] = macd.macd_signal()
    
    latest = df.iloc[-1]
    if latest["dev"] > 0.015 and latest["macd"] < latest["signal"]:
        return "NO", 0.60   # 超买 + 看跌 MACD → 押 NO
    elif latest["dev"] < -0.015 and latest["macd"] > latest["signal"]:
        return "YES", 0.60  # 超卖 + 看涨 MACD → 押 YES
    return None, 0
```

**特点**:
- 扫描所有活跃 5分钟加密市场
- Gasless limit orders（避免手续费）
- 检查重复持仓
- 每 30 秒扫描一次

---

### 3. ciliaai/polymarket-gooning ⭐ 4（最数学化）

| 属性 | 内容 |
|------|------|
| **GitHub** | https://github.com/ciliaai/polymarket-gooning |
| **定位** | 实时信号扫描 + 多因子量化模型 |
| **策略** | Kelly + Black-Scholes + VPIN + OU 均值回归 |

**五大数学模型**:

1. **Kelly Criterion 仓位优化**:
   ```
   f* = (bp - q) / b
   ```

2. **Black-Scholes 二进制期权定价**:
   ```
   C = e^(-rT) × N(d₂)
   d₂ = [ln(P/K) + (r - σ²/2)T] / (σ√T)
   ```

3. **VPIN (订单流毒性检测)**:
   ```
   VPIN = Σ|V_buy - V_sell| / (n × V_bucket)
   当 VPIN > 0.4 时检测到有毒流
   ```

4. **Ornstein-Uhlenbeck 均值回归**:
   ```
   dP = θ(μ - P)dt + σdW
   半衰期 = ln(2) / θ
   入场信号: |P - μ| > 2σ
   ```

5. **综合风险评分**:
   ```
   risk_score = w₁×liquidity_risk + w₂×time_decay + w₃×correlation_risk
   ```

---

### 4. chrisgillam/polymarket_gambot ⭐ 24（体育套利标杆）

| 属性 | 内容 |
|------|------|
| **GitHub** | https://github.com/chrisgillam/polymarket_gambot |
| **定位** | Polymarket 体育套利机器人 |
| **策略** | Pinnacle  Sharp 赔率对比 + Kelly Criterion |

**核心逻辑**:
1. 从 Pinnacle（最 Sharp 的体育博彩）获取真实赔率
2. 移除庄家抽水后得到"真实概率"
3. 与 Polymarket 价格对比，发现定价偏差
4. 使用 Kelly Criterion 计算最优仓位
5. 使用 FOK (Fill-or-Kill) 订单避免滑点

**关键参数**:
- `kelly_multiplier`: 0-1，控制 Kelly 激进程度
- `target_buy_ev`: 3-8% 是最佳区间
- `MAX_PERCENTAGE_BET`: 单注最大资金占比
- `MAX_DOLLAR_BET`: 单注最大金额

---

### 5. alteregoeth-ai/weatherbot ⭐ 240（最完整）

| 属性 | 内容 |
|------|------|
| **GitHub** | https://github.com/alteregoeth-ai/weatherbot |
| **定位** | Polymarket 天气交易机器人 |
| **策略** | 外部数据 + EV 计算 + Kelly + 止损 |

**v1 → v2 升级**:

| 功能 | v1 | v2 |
|------|-----|-----|
| 城市覆盖 | 6 个美国城市 | 20 个城市，4 大洲 |
| 数据源 | NWS | ECMWF + HRRR/GFS + METAR |
| EV 计算 | ❌ | ✅ |
| Kelly Criterion | ❌ | ✅ (fractional) |
| 止损 | ❌ | ✅ (20% stop, 移动止损) |
| 滑点过滤 | ❌ | ✅ (max spread $0.03) |
| 自校准 | ❌ | ✅ |

**配置参数**:
```json
{
  "balance": 10000.0,
  "max_bet": 20.0,
  "min_ev": 0.05,
  "max_price": 0.45,
  "kelly_fraction": 0.25,
  "max_slippage": 0.03
}
```

---

### 6. sterlingcrispin/nothing-ever-happens ⭐ 918（买 No 策略）

| 属性 | 内容 |
|------|------|
| **GitHub** | https://github.com/sterlingcrispin/nothing-ever-happens |
| **定位** | 在独立非体育市场买 "No" |
| **策略** | 扫描市场 → 找低于价格上限的 No → 买入 |

**配置参数**:
```json
{
  "max_entry_price": 0.65,      // 最高买入价格
  "cash_pct_per_trade": 0.02,   // 每次交易使用 2% 现金
  "min_trade_amount": 5,        // 最小交易金额
  "allowed_slippage": 0.3,      // 允许滑点
  "buy_retry_count": 3,         // 买入重试次数
  "max_new_positions": -1       // 最大新仓位 (-1=无限制)
}
```

**安全模型**: 需要同时设置 `BOT_MODE=live` + `LIVE_TRADING_ENABLED=true` + `DRY_RUN=false` 才会真实下单

---

## 二、关键教训汇总

### 2.1 用户策略（价格 < 0.50 买入）的问题

| 问题 | 证据 | 来源 |
|------|------|------|
| **数学期望为负** | E = -price²，恒小于 0 | 基础概率论 |
| **$0.65-0.70 区间胜率仅 41%** | 162 笔真实交易统计 | TheOneWhoBurns |
| **低价区间亏损 $43** | 实际交易记录 | TheOneWhoBurns |
| **Ghost fills 严重** | 显示 MATCHED 但 0 shares | TheOneWhoBurns |
| **Adverse selection** | 赢的不成交，输的必成交 | TheOneWhoBurns |
| **Paper 胜率 ≠ Real 胜率** | 77% vs 65.4% | TheOneWhoBurns |

### 2.2 成功策略的共同特征

| 特征 | 说明 | 代表项目 |
|------|------|---------|
| **有外部信息源** | 不只看 Polymarket 价格 | weatherbot (NWS), gambot (Pinnacle) |
| **正 EV 过滤** | 只交易期望收益 > 0 的机会 | weatherbot, gambot, gooning |
| **Kelly 仓位管理** | 根据 edge 大小调整仓位 | weatherbot, gambot, TheOneWhoBurns |
| **严格入场过滤** | 不满足条件绝不入场 | TheOneWhoBurns v2 |
| **止损机制** | 亏损超过阈值立即退出 | weatherbot (20% stop) |
| **验证成交** | 下单后验证实际成交数量 | TheOneWhoBurns |
| **Paper 先行** | 实盘前充分模拟测试 | 所有成功项目 |

### 2.3 推荐改进方向

基于竞品分析，建议将用户策略从"无脑低价买入"升级为：

```
1. 获取 Binance BTC 实时价格 (websocket)
        ↓
2. GBM 模型计算真实概率 P_up
        ↓
3. 与 Polymarket 价格对比，计算 edge = P_up - market_price
        ↓
4. 仅当 edge > 0 且满足所有过滤器时才入场
        ↓
5. Kelly Criterion 计算仓位大小
        ↓
6. 下 GTC limit order
        ↓
7. 3秒后验证成交，未成交则取消
        ↓
8. 窗口到期后验证赎回
```

---

## 三、代码参考来源

1. TheOneWhoBurns/btc-updown-bot — GBM 模型 + Kelly + 真实交易数据
2. wincXDSolana/polymarket-bot — 均值回归 + MACD + 5分钟扫描
3. ciliaai/polymarket-gooning — Kelly + Black-Scholes + VPIN + OU
4. chrisgillam/polymarket_gambot — Pinnacle 套利 + Kelly + FOK
5. alteregoeth-ai/weatherbot — 外部数据 + EV + Kelly + 止损
6. sterlingcrispin/nothing-ever-happens — 买 No 策略 + 安全模式
7. warproxxx/poly-maker — 做市机器人 + WebSocket + 仓位合并
8. HKUDS-AI/polymarket-ai-trading — 均值回归 + AI 评分 + 三模型并行
