#!/usr/bin/env python3
"""
Polymarket BTC 自动交易策略
策略：当 Yes/No 价格低于阈值时持续买入，直到预算耗尽或市场结算

⚠️ 高风险警告：此策略数学期望为负，仅供教育研究
"""

import os
import sys
import time
import logging
import argparse
from datetime import datetime, timezone
from typing import Optional, Dict, List, Tuple
from dotenv import load_dotenv

# Polymarket SDK
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import (
    OrderArgs, MarketOrderArgs, OrderType,
    BalanceAllowanceParams, AssetType,
)
from py_clob_client.order_builder.constants import BUY, SELL

# 加载环境变量
load_dotenv()

# ───────────────────────────── 配置 ─────────────────────────────

# API 端点
CLOB_API = "https://clob.polymarket.com"
GAMMA_API = "https://gamma-api.polymarket.com"
DATA_API = "https://data-api.polymarket.com"

# 策略参数
MAX_BUDGET = float(os.getenv("MAX_BUDGET", "10.0"))          # 总预算上限 (USDC)
PRICE_THRESHOLD = float(os.getenv("PRICE_THRESHOLD", "0.50")) # 价格触发阈值
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "30"))       # 检查间隔 (秒)

# 认证参数
PRIVATE_KEY = os.getenv("POLYMARKET_PRIVATE_KEY", "")
FUNDER_ADDRESS = os.getenv("POLYMARKET_FUNDER_ADDRESS", "")
CHAIN_ID = int(os.getenv("POLYMARKET_CHAIN_ID", "137"))
SIGNATURE_TYPE = int(os.getenv("SIGNATURE_TYPE", "2"))

# 目标市场配置（示例：BTC $1M before GTA VI）
# 用户需要根据实际情况修改
TARGET_MARKET = {
    "condition_id": os.getenv("TARGET_CONDITION_ID", "0xbb57ccf5853a85487bc3d83d04d669310d28c6c810758953b9d9b91d1aee89d2"),
    "question": os.getenv("TARGET_QUESTION", "Will bitcoin hit $1m before GTA VI?"),
}

# ───────────────────────────── 日志 ─────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("BTC-BOT")

# ───────────────────────────── 颜色输出 ─────────────────────────────

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def green(s): return f"{Colors.GREEN}{s}{Colors.RESET}"
def red(s): return f"{Colors.RED}{s}{Colors.RESET}"
def yellow(s): return f"{Colors.YELLOW}{s}{Colors.RESET}"
def blue(s): return f"{Colors.BLUE}{s}{Colors.RESET}"

# ───────────────────────────── 核心类 ─────────────────────────────

class PolymarketBTCBot:
    """Polymarket BTC 自动交易机器人"""
    
    def __init__(self, mode: str = "paper"):
        self.mode = mode  # "paper" 或 "live"
        self.client: Optional[ClobClient] = None
        self.total_spent = 0.0
        self.total_bets = 0
        self.positions: Dict[str, Dict] = {}  # token_id -> position info
        self.market_info: Optional[Dict] = None
        self.yes_token_id: Optional[str] = None
        self.no_token_id: Optional[str] = None
        self.min_order_size: float = 5.0  # 默认值，会从市场获取
        
    def connect(self) -> bool:
        """连接 Polymarket API 并派生 API Key"""
        if not PRIVATE_KEY or not FUNDER_ADDRESS:
            logger.error(red("❌ 缺少环境变量：POLYMARKET_PRIVATE_KEY 或 POLYMARKET_FUNDER_ADDRESS"))
            logger.info("请复制 .env.example 为 .env 并填入你的钱包信息")
            return False
        
        try:
            logger.info(blue("🔌 正在连接 Polymarket CLOB API..."))
            self.client = ClobClient(
                CLOB_API,
                key=PRIVATE_KEY,
                chain_id=CHAIN_ID,
                signature_type=SIGNATURE_TYPE,
                funder=FUNDER_ADDRESS,
            )
            
            # 派生 API Key
            creds = self.client.create_or_derive_api_creds()
            self.client.set_api_creds(creds)
            logger.info(green("✅ API 认证成功！"))
            
            return True
            
        except Exception as e:
            logger.error(red(f"❌ 连接失败: {e}"))
            return False
    
    def fetch_market_info(self) -> bool:
        """从 Gamma API 获取市场元数据"""
        import requests
        
        condition_id = TARGET_MARKET["condition_id"]
        url = f"{GAMMA_API}/markets?active=true&conditionIds={condition_id}"
        
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            markets = data if isinstance(data, list) else data.get('markets', [])
            
            if not markets:
                logger.error(red(f"❌ 未找到市场: {condition_id}"))
                return False
            
            market = markets[0]
            self.market_info = market
            
            # 解析 token IDs
            clob_ids = market.get('clobTokenIds', '[]')
            import json
            token_ids = json.loads(clob_ids) if isinstance(clob_ids, str) else clob_ids
            
            if len(token_ids) >= 2:
                self.yes_token_id = token_ids[0]  # Yes token
                self.no_token_id = token_ids[1]   # No token
            else:
                logger.error(red("❌ 无法解析 token IDs"))
                return False
            
            # 获取最小订单量
            self.min_order_size = float(market.get('orderMinSize', 5.0))
            
            # 打印市场信息
            prices = market.get('outcomePrices', '["?", "?"]')
            prices_list = json.loads(prices) if isinstance(prices, str) else prices
            
            logger.info(blue("📊 目标市场信息:"))
            logger.info(f"   问题: {market.get('question', 'N/A')}")
            logger.info(f"   Yes 价格: {prices_list[0] if len(prices_list) > 0 else 'N/A'}")
            logger.info(f"   No 价格:  {prices_list[1] if len(prices_list) > 1 else 'N/A'}")
            logger.info(f"   最小订单: ${self.min_order_size}")
            logger.info(f"   结算时间: {market.get('endDate', 'N/A')}")
            
            # 检查预算是否足够
            if MAX_BUDGET < self.min_order_size:
                logger.warning(yellow(
                    f"⚠️ 预算(${MAX_BUDGET})低于最小订单量(${self.min_order_size})，"
                    f"无法下单！"
                ))
                return False
            
            return True
            
        except Exception as e:
            logger.error(red(f"❌ 获取市场信息失败: {e}"))
            return False
    
    def get_order_book(self, token_id: str) -> Optional[Dict]:
        """获取订单簿"""
        try:
            book = self.client.get_order_book(token_id)
            return {
                'bids': book.bids,
                'asks': book.asks,
                'min_size': float(book.min_order_size),
                'last_trade': book.last_trade_price,
            }
        except Exception as e:
            logger.error(red(f"❌ 获取订单簿失败: {e}"))
            return None
    
    def get_best_prices(self, token_id: str) -> Tuple[float, float]:
        """获取最佳买/卖价
        返回: (best_bid, best_ask)
        """
        book = self.get_order_book(token_id)
        if not book:
            return 0.0, 0.0
        
        bids = book['bids']
        asks = book['asks']
        
        best_bid = float(bids[0].price) if bids else 0.0
        best_ask = float(asks[0].price) if asks else 1.0
        
        return best_bid, best_ask
    
    def place_limit_order(self, token_id: str, side: str, price: float, size: float) -> bool:
        """下限价单
        
        Args:
            token_id: 代币 ID
            side: BUY 或 SELL
            price: 价格 (0.01 - 0.99)
            size: 数量 (USDC)
        """
        if self.mode == "paper":
            logger.info(yellow(
                f"📋 [PAPER] 模拟下单: {side} {size} shares @ ${price:.4f} "
                f"(Token: {token_id[:20]}...)"
            ))
            return True
        
        try:
            # 创建限价单
            order_args = OrderArgs(
                token_id=token_id,
                price=price,
                size=size,
                side=side,
            )
            
            signed_order = self.client.create_order(order_args)
            resp = self.client.post_order(signed_order, OrderType.GTC)
            
            logger.info(green(
                f"✅ 下单成功: {side} {size} shares @ ${price:.4f} | "
                f"OrderID: {resp.get('orderID', 'N/A')[:16]}..."
            ))
            return True
            
        except Exception as e:
            logger.error(red(f"❌ 下单失败: {e}"))
            return False
    
    def execute_strategy(self):
        """执行核心策略"""
        logger.info(blue("=" * 60))
        logger.info(blue(f"🚀 启动策略 | 模式: {self.mode.upper()} | 预算: ${MAX_BUDGET}"))
        logger.info(blue(f"🎯 目标: {TARGET_MARKET['question']}"))
        logger.info(blue(f"📌 触发条件: Yes/No 价格 < ${PRICE_THRESHOLD}"))
        logger.info(blue(f"📌 最小下注: ${self.min_order_size}"))
        logger.info(blue("=" * 60))
        
        if self.mode == "paper":
            logger.info(yellow("⚠️ 当前为模拟模式，不会真实下单"))
        else:
            logger.info(red("🔴 当前为实盘模式，将使用真实资金！"))
            # 实盘延迟 10 秒给用户取消的机会
            logger.info(yellow("10 秒后开始交易，按 Ctrl+C 取消..."))
            time.sleep(10)
        
        try:
            while self.total_spent < MAX_BUDGET:
                now = datetime.now(timezone.utc).strftime('%H:%M:%S')
                
                # 获取当前价格
                yes_bid, yes_ask = self.get_best_prices(self.yes_token_id)
                no_bid, no_ask = self.get_best_prices(self.no_token_id)
                
                logger.info(
                    f"[{now}] Yes: bid={yes_bid:.4f} ask={yes_ask:.4f} | "
                    f"No: bid={no_bid:.4f} ask={no_ask:.4f} | "
                    f"已用: ${self.total_spent:.2f}/${MAX_BUDGET}"
                )
                
                # 计算剩余预算
                remaining = MAX_BUDGET - self.total_spent
                bet_size = min(self.min_order_size, remaining)
                
                if bet_size < self.min_order_size:
                    logger.info(yellow(f"💰 预算不足，停止下注。总花费: ${self.total_spent:.2f}"))
                    break
                
                placed_any = False
                
                # 策略逻辑：Yes 价格 < 阈值 → 买入 Yes
                if yes_ask < PRICE_THRESHOLD:
                    logger.info(
                        green(f"🎯 信号触发: Yes ask={yes_ask:.4f} < {PRICE_THRESHOLD} → 买入 Yes")
                    )
                    if self.place_limit_order(self.yes_token_id, BUY, yes_ask, bet_size):
                        self.total_spent += bet_size
                        self.total_bets += 1
                        placed_any = True
                
                # 策略逻辑：No 价格 < 阈值 → 买入 No
                if no_ask < PRICE_THRESHOLD:
                    logger.info(
                        green(f"🎯 信号触发: No ask={no_ask:.4f} < {PRICE_THRESHOLD} → 买入 No")
                    )
                    if self.place_limit_order(self.no_token_id, BUY, no_ask, bet_size):
                        self.total_spent += bet_size
                        self.total_bets += 1
                        placed_any = True
                
                if not placed_any:
                    logger.info("⏳ 无信号，等待下一轮...")
                
                # 等待下一轮
                time.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info(yellow("\n⛔ 用户中断策略"))
        
        # 策略结束，打印总结
        self.print_summary()
    
    def print_summary(self):
        """打印交易总结"""
        logger.info(blue("=" * 60))
        logger.info(blue("📊 策略结束总结"))
        logger.info(blue("=" * 60))
        logger.info(f"总下注次数: {self.total_bets}")
        logger.info(f"总花费: ${self.total_spent:.2f} / ${MAX_BUDGET}")
        logger.info(f"剩余预算: ${MAX_BUDGET - self.total_spent:.2f}")
        logger.info(blue("=" * 60))
    
    def emergency_stop(self):
        """紧急停止——取消所有未成交订单"""
        if self.mode == "live" and self.client:
            try:
                self.client.cancel_all()
                logger.critical(red("🚨 紧急停止已触发——所有未成交订单已取消"))
            except Exception as e:
                logger.error(red(f"❌ 紧急停止失败: {e}"))


def check_balance():
    """检查钱包余额"""
    if not PRIVATE_KEY or not FUNDER_ADDRESS:
        print(red("❌ 缺少环境变量"))
        return
    
    try:
        client = ClobClient(
            CLOB_API,
            key=PRIVATE_KEY,
            chain_id=CHAIN_ID,
            signature_type=SIGNATURE_TYPE,
            funder=FUNDER_ADDRESS,
        )
        creds = client.create_or_derive_api_creds()
        client.set_api_creds(creds)
        
        # 获取余额
        balance = client.get_balance_allowance(
            BalanceAllowanceParams(asset_type=AssetType.COLLATERAL)
        )
        
        print(green(f"✅ 连接成功！"))
        print(f"钱包地址: {FUNDER_ADDRESS}")
        print(f"USDC 余额: {balance}")
        
    except Exception as e:
        print(red(f"❌ 检查余额失败: {e}"))


def list_btc_markets():
    """列出 Polymarket 上的 BTC 相关市场"""
    import requests
    
    url = f"{GAMMA_API}/markets?active=true&limit=500&offset=0"
    
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        markets = data if isinstance(data, list) else data.get('markets', [])
        
        print(blue("\n📊 Polymarket 上的 BTC 相关市场:\n"))
        print(f"{'Condition ID':<66} | {'Question':<50} | {'Prices':<20} | {'Min':<5}")
        print("-" * 160)
        
        for m in markets:
            title = m.get('question', '').lower()
            if 'bitcoin' in title or 'btc' in title:
                prices = m.get('outcomePrices', '["?", "?"]')
                print(
                    f"{m.get('conditionId', 'N/A'):<66} | "
                    f"{m.get('question', 'N/A')[:48]:<50} | "
                    f"{prices:<20} | "
                    f"{m.get('orderMinSize', 'N/A'):<5}"
                )
        
    except Exception as e:
        print(red(f"❌ 获取市场列表失败: {e}"))


# ───────────────────────────── 主入口 ─────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Polymarket BTC 自动交易策略")
    parser.add_argument("--mode", choices=["paper", "live"], default="paper",
                        help="运行模式: paper(模拟) 或 live(实盘)")
    parser.add_argument("--check-balance", action="store_true",
                        help="检查钱包余额")
    parser.add_argument("--list-markets", action="store_true",
                        help="列出可用的 BTC 市场")
    parser.add_argument("--condition-id", type=str, default=None,
                        help="指定目标市场的 condition ID")
    
    args = parser.parse_args()
    
    if args.check_balance:
        check_balance()
        sys.exit(0)
    
    if args.list_markets:
        list_btc_markets()
        sys.exit(0)
    
    # 如果指定了 condition_id，覆盖默认配置
    if args.condition_id:
        TARGET_MARKET["condition_id"] = args.condition_id
        TARGET_MARKET["question"] = "用户指定市场"
    
    # 初始化机器人
    bot = PolymarketBTCBot(mode=args.mode)
    
    # 连接 API
    if not bot.connect():
        sys.exit(1)
    
    # 获取市场信息
    if not bot.fetch_market_info():
        sys.exit(1)
    
    # 执行策略
    bot.execute_strategy()
