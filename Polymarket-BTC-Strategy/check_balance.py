#!/usr/bin/env python3
"""检查 Polymarket 钱包余额"""

import os
from dotenv import load_dotenv
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import BalanceAllowanceParams, AssetType

load_dotenv()

PRIVATE_KEY = os.getenv("POLYMARKET_PRIVATE_KEY", "")
FUNDER_ADDRESS = os.getenv("POLYMARKET_FUNDER_ADDRESS", "")
CHAIN_ID = int(os.getenv("POLYMARKET_CHAIN_ID", "137"))
SIGNATURE_TYPE = int(os.getenv("SIGNATURE_TYPE", "2"))
CLOB_API = "https://clob.polymarket.com"


def main():
    if not PRIVATE_KEY or not FUNDER_ADDRESS:
        print("❌ 缺少环境变量，请检查 .env 文件")
        return
    
    print("🔌 正在连接 Polymarket...")
    client = ClobClient(
        CLOB_API,
        key=PRIVATE_KEY,
        chain_id=CHAIN_ID,
        signature_type=SIGNATURE_TYPE,
        funder=FUNDER_ADDRESS,
    )
    
    creds = client.create_or_derive_api_creds()
    client.set_api_creds(creds)
    
    print("✅ 认证成功！")
    print(f"\n钱包地址: {FUNDER_ADDRESS}")
    
    # 获取 USDC 余额
    balance = client.get_balance_allowance(
        BalanceAllowanceParams(asset_type=AssetType.COLLATERAL)
    )
    print(f"USDC 余额: {balance}")
    
    # 获取 API Key 信息
    api_key = client.get_api_key_details()
    print(f"\nAPI Key 详情: {api_key}")


if __name__ == "__main__":
    main()
