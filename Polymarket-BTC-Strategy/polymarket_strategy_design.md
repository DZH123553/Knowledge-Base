# Polymarket BTC 5分钟涨跌自动交易策略设计文档

> **策略名称**: Reverse-Contrarian BTC Scalper  
> **目标市场**: Polymarket 比特币短期涨跌预测市场  
> **策略版本**: v1.0  
> **生成日期**: 2026-04-28

---

## 一、策略逻辑（Strategy Logic）

### 1.1 核心规则

```
WHILE 市场未结算:
    获取当前 best_bid / best_ask 价格
    
    IF yes_price < 0.50:
        以市价买入 yes（BUY yes at market price）
        下注金额 = min(Polymarket最小限额, 剩余预算)
    
    IF no_price < 0.50:
        以市价买入 no（BUY no at market price）
        下注金额 = min(Polymarket最小限额, 剩余预算)
    
    IF 总下注 >= $10 USDC:
        停止下注
    
    等待 30 秒后重新检查
```

### 1.2 参数配置

| 参数 | 值 | 说明 |
|------|-----|------|
| `MAX_BUDGET` | 10.0 USDC | 单次市场总预算上限 |
| `MIN_BET_SIZE` | 动态获取 | Polymarket 该市场最小订单量（通常为 $5） |
| `PRICE_THRESHOLD` | 0.50 | 触发买入的价格阈值 |
| `CHECK_INTERVAL` | 30 秒 | 价格轮询间隔 |
| `ORDER_TYPE` | LIMIT | 限价单（比市价单更安全） |

---

## 二、⚠️ 策略风险分析（Risk Analysis）

### 2.1 数学期望分析

在预测市场中，**价格 ≈ 市场隐含概率**。当价格 < $0.50 时：

```
期望收益 = P(win) × payoff - 下注金额
         = price × (1 - price) - price
         = price - price² - price
         = -price²  < 0  (恒为负！)
```

**结论**：此策略的数学期望**恒为负**。如果市场定价有效，长期必然亏损。

### 2.2 手续费侵蚀

Polymarket 收取 **2% taker fee**（市价单/吃单）：

| 买入价格 | 需涨到的价格才能回本 | 回本所需涨幅 |
|---------|-------------------|-------------|
| $0.49 | $0.50 | +2.0% |
| $0.40 | $0.408 | +2.0% |
| $0.30 | $0.306 | +2.0% |
| $0.20 | $0.204 | +2.0% |

注意：这里的"回本"仅指覆盖手续费，不包含策略本身的负期望。

### 2.3 流动性风险

- 低价位的订单簿深度可能不足
- 大额市价单会产生显著滑点
- 最小订单量可能为 $5，与 $10 总预算冲突

### 2.4 时间衰减

短期市场（5分钟）价格可能剧烈波动：
- 刚买入后市场立即向不利方向移动
- 来不及在价格回弹前获利了结
- 市场可能在极短时间内结算

---

## 三、所需权限与配置（Requirements）

### 3.1 必需权限

| 权限 | 获取方式 | 安全级别 |
|------|---------|---------|
| **Polygon 钱包私钥** | MetaMask/Polymarket 导出 | 🔴 极高风险——泄露 = 资金被盗 |
| **钱包地址 (Funder)** | 与私钥对应的钱包地址 | 🟡 中风险——仅用于派生 API Key |
| **USDC.e 余额** | Polygon 网络存入 USDC.e | 🟢 低风险 |
| **API Key** | py-clob-client 自动派生 | 🟢 低风险——短期有效 |

### 3.2 Polymarket 认证流程

```
┌─────────────────┐     EIP-712 签名      ┌───────────────┐
│  钱包私钥        │ ──────────────────→  │ Polymarket API │
│  (Polygon链)     │                      │               │
└─────────────────┘                      └───────┬───────┘
                                                  │
                                                  ▼
                                          ┌───────────────┐
                                          │ 派生 API Key   │
                                          │ (Key/Secret/   │
                                          │  Passphrase)   │
                                          └───────────────┘
```

**注意**：Polymarket 不使用"账号密码"，而是使用**钱包签名认证**。

### 3.3 环境变量配置

```bash
# .env 文件
POLYMARKET_PRIVATE_KEY=0x...          # Polygon 钱包私钥（64字符，0x开头）
POLYMARKET_FUNDER_ADDRESS=0x...       # 钱包地址（42字符，0x开头）
POLYMARKET_CHAIN_ID=137               # Polygon Mainnet
SIGNATURE_TYPE=2                      # 0=MetaMask硬件 1=邮箱 2=浏览器代理

# 策略参数
MAX_BUDGET=10.0
PRICE_THRESHOLD=0.50
CHECK_INTERVAL=30
```

---

## 四、技术架构

### 4.1 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    Strategy Bot                              │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │  Price Feed │  │  Signal Gen  │  │  Order Manager   │   │
│  │  (CLOB API) │  │              │  │                  │   │
│  └──────┬──────┘  └──────┬───────┘  └────────┬─────────┘   │
│         │                │                    │             │
│         ▼                ▼                    ▼             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Risk Controller                          │   │
│  │  • 预算检查  • 头寸管理  • 止损触发  • 紧急停止       │   │
│  └────────────────────────┬─────────────────────────────┘   │
│                           │                                  │
└───────────────────────────┼──────────────────────────────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │  Polymarket CLOB │
                   │  https://clob.   │
                   │  polymarket.com  │
                   └─────────────────┘
```

### 4.2 依赖库

```
py-clob-client>=0.29.0    # Polymarket 官方 CLOB SDK
python-dotenv>=1.0.0       # 环境变量管理
requests>=2.31.0           # HTTP 请求（Gamma API）
websockets>=12.0           # WebSocket 实时数据（可选）
```

---

## 五、完整代码实现

见 `polymarket_btc_bot.py`

---

## 六、运行步骤

### Step 1: 安装依赖

```bash
pip install py-clob-client python-dotenv requests
```

### Step 2: 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入你的私钥和地址
```

### Step 3: 检查余额

```bash
python check_balance.py
```

### Step 4: 运行策略（回测/模拟模式）

```bash
python polymarket_btc_bot.py --mode paper
```

### Step 5: 实盘运行

```bash
python polymarket_btc_bot.py --mode live
```

---

## 七、监控与日志

| 指标 | 监控方式 |
|------|---------|
| 当前持仓 | `client.get_positions()` |
| 盈亏 (PnL) | 手动计算：positions × (当前价格 - 成本价) |
| 订单状态 | WebSocket user channel |
| 预算剩余 | 实时累加已下注金额 |

---

## 八、紧急停止机制

```python
# 紧急停止——取消所有未成交订单
def emergency_stop(client):
    client.cancel_all()
    logger.critical("🚨 EMERGENCY STOP TRIGGERED — All orders cancelled")
```

触发条件：
- 键盘 Ctrl+C
- 预算耗尽
- 检测到异常价格行为
- 手动调用 API

---

## 九、Polymarket 上可用的 BTC 市场（截至 2026-04-28）

| 市场 | 当前价格 | 结算日期 | 最小订单 |
|------|---------|---------|---------|
| Will bitcoin hit $1m before GTA VI? | Yes 48.55¢ / No 51.45¢ | 2026-07-31 | $5 |
| Will Bitcoin hit $150k by June 30, 2026? | Yes 1.35¢ / No 98.65¢ | 2026-07-01 | $5 |
| Will Bitcoin hit $150k by December 31, 2026? | Yes 9.5¢ / No 90.5¢ | 2027-01-01 | $5 |

**注意**：Polymarket 上目前没有专门的"5 分钟 BTC 涨跌"市场。如需短期市场，可考虑：
- **Limitless** (Base 链)：有小时/日级别的 BTC 市场
- **Kalshi**：有短期加密市场（需 KYC）

---

## 十、免责声明

> ⚠️ **高风险警告**
> 
> 1. 本策略的数学期望为负，长期运行必然亏损
> 2. Polymarket 收取 2% taker fee，进一步侵蚀利润
> 3. 加密货币预测市场高度波动，可能损失全部资金
> 4. 本代码仅供教育研究，不构成投资建议
> 5. 运行前务必在 paper 模式充分测试
> 6. 永远不要投入无法承受损失的资金
