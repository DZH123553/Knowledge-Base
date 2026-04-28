# Polymarket BTC 自动交易策略

> ⚠️ **高风险警告**：此策略数学期望为负，仅供教育研究使用

## 快速开始

```bash
# 1. 克隆并进入目录
git clone https://github.com/DZH123553/Knowledge-Base.git
cd Knowledge-Base/Polymarket-BTC-Strategy

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的钱包信息

# 4. 检查余额
python check_balance.py

# 5. 查看可用市场
python polymarket_btc_bot.py --list-markets

# 6. 模拟运行（推荐先测试）
python polymarket_btc_bot.py --mode paper

# 7. 实盘运行（⚠️ 使用真实资金）
python polymarket_btc_bot.py --mode live
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `polymarket_btc_bot.py` | 主策略代码 |
| `polymarket_strategy_design.md` | 策略设计文档（含风险分析） |
| `check_balance.py` | 钱包余额检查工具 |
| `.env.example` | 环境变量模板 |
| `requirements.txt` | Python 依赖 |

## 策略参数（通过 .env 配置）

```
MAX_BUDGET=10.0          # 总预算上限（USDC）
PRICE_THRESHOLD=0.50     # 触发买入的价格阈值
CHECK_INTERVAL=30        # 检查间隔（秒）
```
