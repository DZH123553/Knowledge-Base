"""Identify market (A / H / U) from a ticker or stock name and normalize the code.

v2.9.2 · 扩展 `_a_share_suffix` 覆盖 ETF / LOF / 可转债 等非个股 6 位码
        + 增加 `classify_security_type` 识别标的类型（stock/etf/lof/cb）
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

Market = Literal["A", "H", "U"]
SecurityType = Literal["stock", "etf", "lof", "convertible_bond", "unknown"]


@dataclass
class TickerInfo:
    raw: str            # original user input
    code: str           # numeric/letter code without exchange suffix
    full: str           # canonical: 002273.SZ / 00700.HK / AAPL
    market: Market      # A / H / U


_RE_A_NUMERIC = re.compile(r"^\d{6}$")
_RE_A_FULL = re.compile(r"^(\d{6})\.(SZ|SH|BJ)$", re.I)
_RE_HK = re.compile(r"^(\d{4,5})(?:\.HK)?$", re.I)
_RE_US = re.compile(r"^[A-Z][A-Z\.\-]{0,5}$")


# ═══════════════════════════════════════════════════════════════
# v2.9.2 · 完整的 6 位码分类（之前只看前 2 位，漏了一大片）
# ═══════════════════════════════════════════════════════════════
# 沪市 (SH)：
#   600xxx / 601xxx / 603xxx / 605xxx · 主板股票
#   688xxx · 科创板股票
#   900xxx · B 股
#   50xxxx / 51xxxx / 52xxxx / 56xxxx / 58xxxx · ETF
#   501xxx / 502xxx / 506xxx · LOF（部分重叠 ETF 范围，逻辑上同属 SH 基金）
#   10xxxx / 11xxxx · 可转债
#
# 深市 (SZ)：
#   000xxx / 001xxx / 002xxx / 003xxx · 主板 / 中小板股票
#   300xxx · 创业板股票
#   159xxx · ETF
#   160xxx / 161xxx / 162xxx / 163xxx / 164xxx / 165xxx / 166xxx / 167xxx / 168xxx · LOF
#   12xxxx / 127xxx / 128xxx · 可转债
#
# 北交所 (BJ)：
#   83xxxx / 87xxxx / 88xxxx / 92xxxx

_SH_PREFIXES_2 = ("60", "68", "90")       # 688 涉及在 _SH_3 里单独覆盖
_SH_STOCK_PREFIXES_3 = ("688",)
_SH_B_SHARE = ("900",)
_SH_FUND_PREFIXES_2 = ("50", "51", "52", "56", "58")
_SH_BOND_PREFIXES_2 = ("10", "11")

_SZ_STOCK_PREFIXES_3 = ("000", "001", "002", "003", "300", "301")
_SZ_FUND_PREFIXES_3 = ("159",)
_SZ_LOF_PREFIXES_2 = ("16",)  # 160xxx-168xxx
_SZ_BOND_PREFIXES_2 = ("12",)

_BJ_PREFIXES_2 = ("83", "87", "88", "92")


def _a_share_suffix(code6: str) -> str:
    """Decide SZ/SH/BJ for a 6-digit A-share code.

    v2.9.2 修复：之前只看前 2 位 (60/688/900 → SH, 其他 → SZ)，导致：
      - 512400 (SH ETF) 被错判 SZ
      - 10xxxx / 11xxxx (SH 可转债) 被错判 SZ
      - 159xxx (SZ ETF) 虽然默认 SZ 对了但巧合
    现在按完整规则走，任何 6 位码都能归对交易所。
    """
    # 北交所
    if code6.startswith(_BJ_PREFIXES_2):
        return "BJ"
    # 沪市（按优先级：股票 → ETF/LOF/可转债）
    if code6.startswith(_SH_STOCK_PREFIXES_3):    # 688xxx 科创板
        return "SH"
    if code6.startswith(_SH_B_SHARE):              # 900xxx B 股
        return "SH"
    if code6.startswith(("60",)):                  # 600/601/603/605/606...
        return "SH"
    if code6.startswith(_SH_FUND_PREFIXES_2):      # 50/51/52/56/58 · SH ETF/LOF
        return "SH"
    if code6.startswith(_SH_BOND_PREFIXES_2):      # 10/11 · SH 可转债
        return "SH"
    # 深市（包含其他所有剩余 6 位码）
    return "SZ"


def classify_security_type(code6: str) -> SecurityType:
    """v2.9.2 新增：识别标的类型（stock / etf / lof / convertible_bond）.

    用于 fetch_basic 早期拒绝非个股标的（插件设计为个股分析，ETF/可转债
    没有 ROE / 护城河 / 管理层等字段，不适合跑 51 评委流程）。
    """
    if not code6 or not code6.isdigit() or len(code6) != 6:
        return "unknown"
    # ETF
    if code6.startswith(_SZ_FUND_PREFIXES_3) or \
       code6.startswith(_SH_FUND_PREFIXES_2):
        # SH 50/51/52/56/58 中，501/502/506 部分是 LOF，其他是 ETF
        if code6.startswith(("501", "502", "506")):
            return "lof"
        return "etf"
    # SZ LOF (160xxx-168xxx)
    if code6.startswith(_SZ_LOF_PREFIXES_2):
        return "lof"
    # 可转债
    if code6.startswith(_SH_BOND_PREFIXES_2) or \
       code6.startswith(_SZ_BOND_PREFIXES_2):
        return "convertible_bond"
    # 股票
    if code6.startswith(_SH_STOCK_PREFIXES_3) or \
       code6.startswith(_SH_B_SHARE) or \
       code6.startswith(("60",)) or \
       code6.startswith(_SZ_STOCK_PREFIXES_3) or \
       code6.startswith(_BJ_PREFIXES_2):
        return "stock"
    return "unknown"


def parse_ticker(raw: str) -> TickerInfo:
    """Best-effort parse. For Chinese names (e.g. '水晶光电'), caller must resolve via fetch_basic first."""
    s = raw.strip().upper().replace(" ", "")

    m = _RE_A_FULL.match(s)
    if m:
        return TickerInfo(raw=raw, code=m.group(1), full=f"{m.group(1)}.{m.group(2).upper()}", market="A")

    if _RE_A_NUMERIC.match(s):
        suffix = _a_share_suffix(s)
        return TickerInfo(raw=raw, code=s, full=f"{s}.{suffix}", market="A")

    if s.endswith(".HK"):
        code = s.removesuffix(".HK").lstrip("0") or "0"
        return TickerInfo(raw=raw, code=code, full=f"{code.zfill(5)}.HK", market="H")

    # v2.10.2 · 3-位数纯数字（如 "700"/"981"）A 股不存在，走 HK
    # 原逻辑：_RE_A_NUMERIC 要求 6 位，_RE_HK 匹配 4-5 位 → "700" 3 位都不匹配
    # 落到最后 A 股兜底 → 错判为 A 股 code=700
    if s.isdigit() and 3 <= len(s) <= 5:
        padded = s.zfill(5)
        return TickerInfo(raw=raw, code=s.lstrip("0") or "0", full=f"{padded}.HK", market="H")

    if _RE_HK.match(s) and not _RE_US.match(s):
        return TickerInfo(raw=raw, code=s.lstrip("0") or "0", full=f"{s.zfill(5)}.HK", market="H")

    if _RE_US.match(s):
        return TickerInfo(raw=raw, code=s, full=s, market="U")

    # Unrecognized — likely a Chinese name. Caller must resolve.
    return TickerInfo(raw=raw, code=raw, full=raw, market="A")


def is_chinese_name(raw: str) -> bool:
    """True if input contains CJK chars (needs name→code resolution)."""
    return any("\u4e00" <= ch <= "\u9fff" for ch in raw)


if __name__ == "__main__":
    for t in ["002273", "002273.SZ", "600519", "00700.HK", "00700", "AAPL", "BRK.B", "水晶光电"]:
        print(t, "->", parse_ticker(t))
