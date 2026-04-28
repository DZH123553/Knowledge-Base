# 稳定币基建（Stablecoin Infrastructure）与 Agentic Payment 行业深度研究报告 v2.0

> **报告生成时间**：2026-04-27  
> **研究方法论**：自主网络调研 + 知识库既有内容交叉验证 + 播客/从业者一手观点融合  
> **数据承诺**：本报告所有数据与事实陈述均基于公开可查信息，标注来源与可信度，无编造成分  
> **核心信源**：CryptoSlate, Odaily, CoinShares, BlockEden, AlphaPoint, APIDeck, DeFiPrime, Cobo, Federal Reserve, KPMG, ChainCatcher, 腾讯新闻, OSL Research, Pantera Capital, 支无不言播客, The Block, CoinDesk, Artemis, Foresight News, BlockBeats, 学习区块链

---

## 执行摘要（Executive Summary）

**研究对象**：稳定币基建（发行、分销、托管、支付编排、合规、Agent协议的全栈基础设施）与 Agentic Payment（AI Agent 自主发起、无需人类逐笔授权的支付体系）。这两个赛道正在发生**深层耦合**——稳定币是 Agentic Payment 的天然结算层，Agentic Payment 是稳定币从"投机资产"走向"生产工具"的最强需求驱动力。

### 核心发现

1. **稳定币已成全球支付事实标准**：2026年4月稳定币总市值 **$317B**（Fed 数据），2025年全年链上转账量 **$33万亿**，约为 Visa 年支付量的 **2 倍**。2026年1月单月转账 $10.5万亿，接近 Mastercard 年度总交易额。Citi 预测 2030 年稳定币发行达 **$1.9T**，支持约 **$100万亿** 年交易活动。

2. **传统支付巨头完成战略卡位，并购军备竞赛白热化**：
   - **Stripe** 2024年10月收购 Bridge（$1.1B），2025年稳定币支付量达 **$400B**（60% 为 B2B），已获 OCC 国家信托银行有条件批准；同时孵化 Tempo（$500M 融资，$5B 估值）
   - **Mastercard** 2026年3月收购 BVNK（$1.8B），为其数字资产领域最大收购
   - **Visa** 2025年12月推出 USDC 结算，年化运行率 **$4.6B**，覆盖 50+ 国家、130+ 稳定币卡项目
   - 竞争逻辑一致：传统支付网络 24-72 小时结算 + 多层中间行费用，稳定币轨道秒级结算 + 低成本，与其竞争不如收购

3. **Agentic Payment 从概念进入产品化，但真实需求仍处早期验证**：
   - **x402 协议**（Coinbase，2025年5月）：用 HTTP 402 状态码嵌入稳定币支付，Base 链累计 1.19 亿笔交易、$3,500万成交额；但 2026年3月日均成交额回落至仅 **$2.8万**，平均单笔 $0.20，约半数为测试交易
   - **x402 Foundation**（2026年4月2日并入 Linux Foundation）：22 家创始成员包括 Google、Stripe、AWS、Visa、Mastercard、Microsoft、Shopify、American Express、Ant International，标志着"互联网原生支付层"从企业标准走向行业标准
   - **Agent.market**（2026年4月20日上线）：x402 的 Agent 应用商店，已接入 OpenAI、Venice、Bloomberg、CoinGecko、LinkedIn、X、AWS Lambda 等服务商
   - **AP2 协议**（Google Cloud + Coinbase，2025年9月）：60+ 组织支持，将 x402 集成为链上结算通道之一
   - **Stripe Machine Payments**（2026年2月）：在 Base 链上线，Agent 可直接用 Stripe API 发 USDC
   - **MoonPay Agents**（2026年2月）：非托管 Agent 钱包，支持 7 条链 + x402，覆盖 500+ 企业客户、3000万+ 用户的基础设施
   - **关键矛盾**：协议和基础设施层面热闹非凡，但**日均真实商业交易量仅约 $1.4万**（Odaily 数据），与 $70 亿生态市值严重脱节

4. **产业链已从"单点工具"演进为"七层栈"**：发行层（Circle/Tether）→ 分销层（Coinbase/Wintermute）→ 托管层（Fireblocks）→ 支付编排层（Stripe/Visa/MC）→ 法币桥接层（MoonPay）→ Agent 协议层（x402/AP2/ERC-8004）→ 应用层（AI Agent 市场）。**L1-L4 已被巨头卡位，L5-L7 是创业主战场**。

5. **Agent 银行四层框架揭示终局方向**（基于支无不言播客 Jay Yu/Pantera 观点）：支付只是表象，Agent 银行才是终局。四层架构——Identity（身份）→ Liquidity（流动性/信贷）→ Security Guardrail（安全护栏）→ Discoverability（发现层）——当前仅**支付层最成熟**，其余三层几乎空白。

6. **悬而未决的核心问题**：Agent 法律人格/KYC、机器速度 AML 监控、私钥安全、Solver 中心化风险、跨链流动性碎片化、微支付 Gas 经济学、稳定币发行商利率下行风险。

7. **创业机会集中在"中间件"**：Agent 合规中间件、B2B 跨境支付编排、企业级 Agent 钱包、Agent 身份/信誉系统、微支付聚合器、Agent 安全护栏、Agent 信贷市场。

### 关键数据速览

| 指标 | 数值 | 来源 | 可信度 |
|------|------|------|--------|
| 稳定币总市值 | $317B | Federal Reserve, 2026-04 | 🟢 高 |
| 2025年全年链上转账量 | $33万亿 | DigitalToday/CoinShares | 🟡 中 |
| USDC 2026年1月转账量 | $8.3万亿 | DigitalToday | 🟡 中 |
| Stripe 2025年稳定币支付量 | ~$400B | Stripe 年报 | 🟡 中 |
| Visa 稳定币结算年化运行率 | $4.6B | CryptoSlate | 🟡 中 |
| Mastercard 收购 BVNK | $1.8B | 多家媒体确认 | 🟢 高 |
| Stripe 收购 Bridge | $1.1B | 多家媒体确认 | 🟢 高 |
| x402 Base 链累计交易 | 1.19亿笔 | Artemis | 🟢 高 |
| x402 Base 链累计成交额 | ~$3,500万 | Artemis | 🟢 高 |
| x402 2026年3月日均成交 | ~$2.8万 | Artemis/Odaily | 🟢 高 |
| x402 平均单笔金额 | ~$0.20 | Artemis | 🟢 高 |
| Citi 2030年稳定币预测 | $1.9T 发行，$100T 年交易 | Citi, 2025-09 | 🔴 低（预测） |
| PwC Agent 经济 2030 预测 | $2.6-4.4T 年 GDP | PwC | 🔴 低（预测） |
| Circle 2025年全年收入 | $27.47亿 | Circle 财报 | 🟢 高 |
| Circle USDC 流通量目标 CAGR | 40% | Circle 管理层指引 | 🟡 中 |
| Ralio Pre-Seed 融资 | $2.5M（3倍超额认购） | SVV/多家媒体 | 🟢 高 |

---

## 一、产业链全景：七层栈 + Agent 银行四层框架

### 1.1 七层基础设施栈

稳定币基建 + Agentic Payment 的产业链不再是"发行-交易"的简单二元结构，而是正在分化为一个 **七层垂直栈**。

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              L7: 应用层                                       │
│   AI Agent 市场 / 自主交易 / Agent-to-Agent 商务 / 自动 Treasury 管理         │
│   代表：Virtuals Protocol, Autonolas, 各类 Agent 框架, Agent.market          │
├─────────────────────────────────────────────────────────────────────────────┤
│                              L6: Agent 协议层                                 │
│   Agent 支付标准、身份验证、授权合约（Mandates）、跨 Agent 互操作               │
│   代表：x402 (Coinbase), AP2 (Google+Coinbase), ERC-8004 (BNB Chain), MPP    │
├─────────────────────────────────────────────────────────────────────────────┤
│                              L5: 法币桥接层                                   │
│   法币↔稳定币出入金、KYC/AML、银行连接、多币种兑换                            │
│   代表：MoonPay, Bridge, BVNK, Circle Mint, Coinbase, Paysafe                │
├─────────────────────────────────────────────────────────────────────────────┤
│                              L4: 支付编排层                                   │
│   商户收单、企业 payouts、跨境 B2B、Treasury 管理、卡网络集成                  │
│   代表：Stripe (Bridge), Visa, Mastercard (BVNK), Shopify, Klarna            │
├─────────────────────────────────────────────────────────────────────────────┤
│                              L3: 托管与钱包层                                 │
│   机构托管、MPC 钱包、冷钱包、合规托管、Agent 专用钱包                         │
│   代表：Fireblocks, OKX, Kraken Custody, Cobo, tether.wallet                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                              L2: 分销与流动性层                               │
│   交易所、做市商、OTC、跨链桥、CCTP                                          │
│   代表：Coinbase, Wintermute, Jane Street, Circle CCTP V2                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                              L1: 发行层                                       │
│   稳定币发行、储备管理、合规牌照、1:1 赎回                                    │
│   代表：Circle (USDC), Tether (USDT/OMS), Paxos (PYUSD/USDG)                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                              L0: 结算层（公链/专用链）                         │
│   交易执行、Gas 费、最终性、智能合约平台                                      │
│   代表：Ethereum, Solana, Base, Arbitrum, Tempo, Circle Arc                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 各层价值分配与进入壁垒

| 层级 | 代表玩家 | 毛利率 | 进入壁垒 | 核心能力要求 |
|------|---------|--------|---------|------------|
| L1 发行 | Circle, Tether, Paxos | 极高（国债利息收入） | 极高 | 监管牌照、银行关系、审计合规 |
| L2 分销 | Coinbase, Wintermute | 中高（交易手续费） | 高 | 流动性深度、机构网络、合规 |
| L3 托管 | Fireblocks | 高（托管费） | 高 | 安全基础设施、保险、SOC2 |
| L4 支付编排 | Stripe, Visa, MC | 中（交易抽成 1-3%） | 极高 | 商户网络、品牌信任、合规体系 |
| L5 法币桥接 | MoonPay, Bridge | 中高（兑换差价+手续费） | 中高 | 银行连接、KYC 能力、牌照 |
| L6 Agent 协议 | Coinbase (x402), Google (AP2) | 低（协议免费，生态收益） | 中 | 标准制定能力、开发者生态 |
| L7 应用 | 各类 Agent 框架 | 待验证 | 低 | 产品体验、用户获取 |

**关键洞察**：
- **L1-L4 已被巨头卡位**，新进入者很难在发行、托管、支付编排层与大玩家竞争
- **L5-L7 是创业主战场**，尤其是 Agent 专用的中间件和工具
- **L6（协议层）是兵家必争之地**：谁定义了 Agent 支付的标准，谁就掌握了生态话语权。x402 已经获得 22 家顶级机构背书，MPP（Stripe 自有协议）处于防御姿态，AP2 走企业集成路线

### 1.3 Agent 银行四层框架：超越"支付"的终局视角

基于 Pantera Capital Jay Yu 在支无不言播客中的分析框架，Agent 支付只是表象，Agent 银行才是终局。当前四层架构的成熟度分布极不均匀：

| 层级 | 对应传统银行 | Agent 银行的问题 | 当前成熟度 | 代表玩家/协议 |
|------|-------------|-----------------|-----------|-------------|
| **Identity（身份）** | 存款/KYC | Agent 归属于谁？如何证明"我是谁"？KYC 不适用 | ⭐⭐ 早期 | ERC-8004 (BNB Chain), ZKID, Agent Passport (Kite AI), KYA |
| **Liquidity（流动性）** | 信贷 | Agent 没钱怎么办？副卡模式、信用评分、DeFi 借贷 | ⭐⭐ 非常早期 | Aave/Compound, Ralio, AllScale |
| **Security Guardrail（安全护栏）** | 风控/反洗钱 | Prompt Injection、API Key 泄露、Agent 行为审计 | ⭐⭐ 早期 | Ralio, Capsule Security ($7M), Privy, TEE |
| **Payment（支付）** | 转账/清算 | x402, MPP, AP2 已产品化 | ⭐⭐⭐⭐ 较成熟 | x402, Stripe MPP, AP2, MoonPay Agents |
| **Discoverability（发现层）** | 汇/搜索 | Agent 如何发现需要的服务？"菜谱"式 workflow | ⭐ 概念期 | Agent.market, 8004Scan, Merit Systems |

**投资逻辑**（Jay Yu 观点）：支付层最成熟（已发生），但价值最大的在**信贷层和安全层**（还没人认真做）。Agent 贷款市场"会是一个非常大的机会"，但前提是完善的 Agent 身份体系。

---

## 二、已经实现了什么：现状盘点与真实数据

### 2.1 稳定币基建：从"边缘实验"到"机构级基础设施"

#### ✅ 已实现：发行层高度集中且合规化

| 稳定币 | 发行方 | 市值 | 监管状态 | 关键里程碑 |
|--------|--------|------|---------|-----------|
| USDT | Tether | ~$190B (60% 市占) | 离岸，透明度争议 | 2025年推出 OMS 开源框架；2026年3月推出 tether.wallet 自托管钱包 |
| USDC | Circle | ~$79B (25% 市占) | 美国 GENIUS Act 合规 + MiCA 完全合规 | 2025年6月NYSE上市；CCTP V2 跨17链；OCC 国家信托银行有条件批准（2025年12月） |
| PYUSD | PayPal/Paxos | 较小 | GENIUS Act + MiCA | PayPal 生态内支付 |
| USDG | Global Dollar Network/Paxos | 较小 | GENIUS Act | Mastercard, Robinhood, Kraken, DBS 参与 |
| EURC | Circle | 3亿欧元+ | MiCA 合规（首家） | 欧洲主要合规稳定币 |
| EURI | Société Générale | 较小 | MiCA（首家欧洲银行发行） | 跨境支付 + 智能合约托管 |
| USAT | Tether/Anchorage Digital | 较小 | 美国机构市场 | 被视为 USDC 首个实质性监管竞争对手 |

> **关键数据**：Paxos 通过 5,208 笔发行/赎回交易对外发送了 $89.2B，主要对手方为 Binance、Wintermute、Jane Street、Coinbase（DigitalToday, 2026-04-14）。

> **竞争动态**：MiCA 完全执行后（2026年7月1日），USDT 因无 EU 牌照面临下架。Binance、Kraken、Bitstamp 已开始为欧洲客户下架 USDT。Tether 2026年1-2月销毁 65 亿 USDT，市值从 $186.8B 缩水至 $183.6B，而 USDC 同期增长 16%。这是**监管合规首次直接影响稳定币市场份额**。

#### ✅ 已实现：支付编排层全面拥抱稳定币

**Stripe（通过 Bridge）**：
- 收购 Bridge（$1.1B，2024年10月），2025年2月完成交割
- 2025年稳定币支付量 **~$400B**，Bridge 交易量翻两番
- 商户集成极简：现有 Stripe PaymentIntent 加 `crypto` 支付方式，USDC 自动结算为美元到商户余额
- 手续费 **1.5%**，比标准卡处理费低约 **30%**
- Stablecoin Financial Accounts：覆盖 **101 个国家**，企业可持有稳定币余额并全球发款
- Open Issuance：任何企业可发行品牌稳定币，BlackRock 等机构管理储备；Phantom CASH（1500万+用户）、MetaMask mUSD 均通过此发行
- **两边下注策略**：Stripe 既是 x402 Foundation 创始成员，又推自己的 Machine Payments Protocol（MPP），通过 ChatGPT 集成触达 9 亿周活用户

**Visa**：
- 2025年12月在美国推出 USDC 结算
- 截至2026年3月，年化稳定币结算运行率达 **$4.6B**
- **130+** 稳定币关联卡项目，覆盖 **50+** 国家
- 与 Bridge 合作扩展稳定币关联卡至 **100+** 国家
- Canton Network：面向银行的支付、结算、财资用例
- Rubail Birwadker（Visa 全球增长产品与战略合作主管）："Visa 的目标是确保无论 AI Agent 使用信用卡还是稳定币交易，支付都能安全、无缝地进行"

**Mastercard**：
- 2026年3月宣布收购 BVNK（$1.8B，含 $300M 业绩对价）
- 2025年数字币支付用例已达 **$350B+**
- 2026年3月推出全球加密合作伙伴计划，**85+** 数字资产公司参与（Circle, Binance, Gemini, PayPal, Kraken, MetaMask, Ripple）
- 定位：跨境汇款、 payouts、P2P、B2B 支付、财资管理

**JPMorgan（Kinexys）**：
- 累计处理 **$1万亿** 稳定币等价代币化存款交易
- 可编程跨境 FX 结算扩展至 **25** 个新货币对
- 12 家一级银行对手方接入
- Siemens 报告外汇节省高达 **50%**，结算时间从天级降至秒级

**Shopify**：
- 与 Stripe 和 Coinbase 合作，商户可直接接受 USDC
- 绕过传统支付网络及费用

#### ✅ 已实现：专用稳定币链（Stablechains）

| 链 | 发起方 | 状态 | 核心特性 | 生态合作伙伴 |
|---|--------|------|---------|------------|
| **Tempo** | Stripe + Paradigm | 测试网 live，主网 H1 2026 | 无原生代币，Gas 可用任意稳定币支付，10万+ TPS，0.6秒最终性，内置合规（TIP-403），原生稳定币 DEX | Stripe, Shopify, Nubank, Klarna, DoorDash, Deel, Revolut, Visa, Anthropic, Deutsche Bank |
| **Circle Arc** | Circle | 测试网 100+ 机构参与 | USDC 为原生 Gas 代币，内置 FX 引擎，子秒最终性，50,000+ TPS | BlackRock, Visa, Goldman Sachs, Mastercard, HSBC, AWS, Coinbase, OpenAI |

> **关键洞察**：Stripe 和 Circle 分别推出了自己的 L1，说明稳定币支付已经不满足于在现有公链上运行，而是需要**专门为支付优化的基础设施**。这是从"借用链"到"自建链"的范式转移。

### 2.2 Agentic Payment：协议热闹 vs 真实需求早期

#### ✅ 已实现：三大支付协议 + 一个标准基金会

**1. x402 协议（Coinbase + Cloudflare）**
- 2025年5月推出， revive HTTP 402 "Payment Required" 状态码
- 工作流程：Agent 请求资源 → 服务器返回 402 + 价格 → Agent 用 USDC 支付 → 附上支付证明重试 → 获得资源
- 支持**微支付至亚美分级别**
- **Base 链累计数据**：约 1.19 亿笔交易、$3,500万累计成交额
- **Solana 数据**：2026年以来贡献约 **65%** 的 x402 交易量，结算时间约 400 毫秒（Gas 比 Base 低 20-50 倍）
- **但真实需求回落严重**：2026年2月达峰（380万笔/日，$200万/日），3月日均成交额仅 **$2.8万**，平均单笔 $0.20；Artemis 分析估计约半数为自刷或测试交易
- **Agent.market**（2026年4月20日上线）：x402 的 Agent 应用商店，已接入 OpenAI、Venice（推理）、Bloomberg、CoinGecko（数据）、LinkedIn、X、AgentMail（社交）、AWS Lambda、QuickNode、Alchemy（基础设施）、Bankr、Coinbase RAT（交易）

**2. x402 Foundation（2026年4月2日并入 Linux Foundation）**
- **初始治理主体**：Coinbase、Cloudflare、Stripe
- **22 家创始成员**：AWS、American Express、Base、Circle、Cloudflare、Coinbase、Fiserv、Google、KakaoPay、Mastercard、Microsoft、Polygon Labs、PPRO、Shopify、Sierra、Solana Foundation、Stripe、Visa、Adyen、Anthropic、Vercel、Ant International
- 这四类成员回答了"AI Agent 支付需要谁"：支付金融网络层（Visa/MC/Stripe/AmEx/Adyen/Fiserv/Circle/PPRO/KakaoPay/Ant）、云基础设施层（AWS/Google/Microsoft/Cloudflare）、Web3 层（Coinbase/Base/Solana/Polygon）、商业应用层（Shopify/Sierra/Ampersend.ai/Merit Systems）
- Stripe 两边下注：既是 x402 创始成员，又推 MPP

**3. AP2 协议（Agent Payments Protocol）**
- 2025年9月由 Google Cloud 和 Coinbase 推出
- 开源框架，**60+** 组织支持
- 基于 A2A 和 MCP 协议
- 核心机制：**Mandates**（密码学签名的数字合约），精确定义 Agent 可购买什么、花多少、在什么条件下
- 将 x402 集成为其链上结算通道之一

**4. Stripe Machine Payments（MPP）**
- 2026年2月11日上线
- 开发者通过现有 Stripe API 创建 PaymentIntent
- Stripe 生成存款地址，Agent 发送 USDC
- 通过 Stripe Dashboard/Webhooks/API 追踪交易状态
- 税费、退款、报表复用 Stripe 现有工具
- **分发优势**：通过 ChatGPT 集成触达 9 亿周活用户（含 5000 万付费订阅者）
- **挫折**：ACP 与 Shopify 集成后仅约 12 家商户激活，用户可浏览产品但支付时需跳转零售商网站（The Information, 2026年3月）

#### ✅ 已实现：Agent 钱包基础设施

**MoonPay Agents（2026年2月24日）**：
- 非托管软件层，基于 MoonPay CLI
- 人类一次性完成 KYC 并注资，之后 Agent 可独立交易、兑换、转账
- 支持 Ethereum, Solana, Base, Arbitrum, Optimism, Polygon, Bitcoin
- 原生 x402 支持
- 30+ 预置金融技能（代币发现、风险分析、组合追踪）
- MoonPay 现有 **500+** 企业客户、**3000万+** 用户的基础设施支撑
- 2026年与 Paysafe（年交易量 $1,670亿）集成，将稳定币支付嵌入传统支付平台

**Coinbase Agentic Wallets（2026年2月）**：
- 基于 x402 协议
- Brian Armstrong：AI Agent 无法满足 KYC，因此无法使用传统银行，加密钱包是唯一选择

**BNB Chain Agent 基础设施（2026年2月4日）**：
- **ERC-8004**：创建 Agent 可验证的链上身份
- **BAP-578**：Non-Fungible Agents（NFA），Agent 作为链上资产持有钱包、支配资金

**EIP-7702（以太坊）**：
- 允许标准账户作为单次交易的智能合约
- 人类用户授予 Agent 临时、高度受限的权限
- 支持 session keys（子 Agent 限时高频微交易权限）
- Gas 抽象：可用替代代币支付费用

#### ✅ 已实现：Agent-to-Agent 商务

- **研究 Agent** 付费给 **数据采集 Agent** 获取结构化网页数据
- **数据采集 Agent** 付费给 **计算 Agent** 获取处理能力
- Zyte.com 已构建 x402 集成服务
- Virtuals Protocol 的 Agent Commerce Protocol 处理请求、谈判、交易、评估

#### ✅ 已实现：真实商业集成

| 场景 | 实现状态 | 关键数据 |
|------|---------|---------|
| AI 购物 | Target/Walmart 产品目录接入 ChatGPT | Morgan Stanley：Agent 购物 2030 年达 $190-385B |
| 自动 Treasury | Agent 监控 DeFi 收益并自动再平衡 | 已在 RebelFi 等基础设施上运行 |
| 按次付费 API | CoinGecko x402 端点 $0.01/请求 | 生产环境运行中 |
| 游戏内 Agent 支付 | AEON 在东南亚 4 国上线 | Visa/MC 集成 |
| Adobe AI 浏览器流量 | 2025年7月同比增长 4700% | — |
| AI 代理交易 | 14 周 Beta 项目，1000+ 参与者创建 9500+ Agent，执行 18.7万笔自主交易 | 2025年10月-2026年1月 |

---

## 三、主要公司深度梳理

### 3.1 产业链图谱

```
                         ┌─────────────────┐
                         │   AI Agent 应用   │
                         │ (OpenAI, Anthropic)│
                         └────────┬────────┘
                                  │
      ┌───────────────────────────┼───────────────────────────┐
      ▼                           ▼                           ▼
┌──────────┐              ┌──────────────┐              ┌──────────┐
│ x402     │              │ AP2 Protocol │              │ ERC-8004 │
│ Coinbase │              │ Google+CB    │              │ BNB Chain│
│ (+Agent. │              │ (+Mandates)  │              │ (+NFA)   │
│  market) │              │              │              │          │
└────┬─────┘              └──────┬───────┘              └────┬─────┘
     │                           │                           │
     └───────────────┬───────────┘                           │
                     ▼                                       │
            ┌────────────────┐                               │
            │ 支付编排 + 出入金 │                               │
            │ Stripe(Bridge) │◄──────────┐                   │
            │ Visa           │           │                   │
            │ Mastercard(BVNK)│          │                   │
            │ MoonPay        │           │                   │
            │ Ralio          │           │                   │
            └───────┬────────┘           │                   │
                    │                    │                   │
        ┌───────────┼───────────┐        │                   │
        ▼           ▼           ▼        │                   │
   ┌────────┐  ┌────────┐  ┌────────┐   │                   │
   │发行层   │  │分销层   │  │托管层   │   │                   │
   │Circle   │  │Coinbase│  │Fireblocks│  │                   │
   │Tether   │  │Wintermute│ │OKX      │   │                   │
   │Paxos    │  │Jane St  │  │Kraken   │   │                   │
   └────┬───┘  └────┬───┘  └────┬───┘   │                   │
        │           │           │        │                   │
        └───────────┴───────────┘        │                   │
                    │                    │                   │
                    ▼                    │                   │
            ┌──────────────┐             │                   │
            │ 公链/专用链   │◄────────────┘                   │
            │ Ethereum     │                                 │
            │ Solana       │◄────────────────────────────────┘
            │ Base         │
            │ Tempo        │
            │ Circle Arc   │
            └──────────────┘
```

### 3.2 核心公司数据卡

#### Circle（USDC 发行方）
- **上市**：2025年6月NYSE上市，发行价 $31/股
- **市值**：USDC ~$79B（25% 市占）
- **2025年全年收入**：$27.47亿
- **核心产品**：Circle Mint（机构铸造赎回）、Programmable Wallets、CCTP V2（跨17链，累计 $110B+ 交易量）、Circle Payments Network（SEPA + 印度卢比结算）、StableFX（24/7 机构 FX 交易平台）
- **战略方向**：推动 USDC 向"可编程支付"发展，x402 自支付，机器对机器微支付标准化；与 OpenMind 合作建立机器对机器支付标准
- **管理层指引**：USDC 流通量目标 CAGR 40%；RLDC 利润率维持 38-40%；其他收入（订阅/服务/交易费）$1.5-1.7亿；运营费用 $5.7-5.85亿
- **关键催化剂**：Coinbase 收入分成协议到期（2026年8月）——目前 Circle 与合作伙伴分享约 60% 收入，若重新谈判 RLDC 利润率从 40% 提升至 50-55%，利润将有效增加 25-35%
- **OCC 许可**：2025年12月获有条件批准，完整批准意味着可直接在美联储开设主账户（赚取 IORB 利率，消除对手方风险），绕过商业银行处理年 $4,830亿 铸造/赎回流量
- **投资者/合作伙伴**：BlackRock, Visa, Goldman Sachs, Mastercard, HSBC, AWS, Coinbase, OpenAI
- **CEO Jeremy Allaire**：多次在财报电话会提到 AI Agent 支付需求，"我们即将进入一个可能有数十亿甚至数百亿 AI Agent 在互联网上互动并执行经济功能的世界"

#### Stripe（通过 Bridge）
- **收购**：Bridge（$1.1B，2024年10月）
- **2025年稳定币支付量**：~$400B（60% B2B）
- **商户覆盖**：90% 道琼斯公司、80% 纳斯达克100公司使用 Stripe；几乎所有头部 AI 公司（OpenAI, Anthropic, Cursor, Midjourney）依赖 Stripe
- **关键产品**：Stablecoin Financial Accounts（101国）、Open Issuance、Machine Payments（Base 链）、Tempo（专用链）
- **Tempo**：与 Paradigm 共建的支付 L1，$500M 融资，$5B 估值，OpenAI/Visa/MC/Anthropic/UBS/德意志银行/Shopify 为设计合作伙伴；Klarna 已在测试网发行 KlarnaUSD
- **OCC 许可**：Bridge 获有条件国家信托银行批准（托管、发行、编排、储备管理）
- **两边下注策略**：支持 x402（Base 链）+ 推自有 MPP，通过 ChatGPT 集成触达 9 亿周活用户

#### Tether（USDT 发行方）
- **市值**：~$190B（60% 市占）
- **战略**：2025年推出 Open Monetary System（OMS）开源框架；2026年3月推出 tether.wallet 自托管钱包
- **定位**：帮助新兴市场央行、国家支付系统、私营金融科技部署 USDT 集成支付轨道
- **初始试点**：非洲、亚洲、拉丁美洲 7 国
- **挑战**：MiCA 合规缺失导致欧洲市场份额流失；USAT（通过 Anchorage Digital 发行）被视为 USDC 首个实质性监管竞争对手

#### Coinbase
- **角色**：分销（交易所）+ 协议（x402）+ Agent 钱包
- **x402**：与 Cloudflare 联合创立基金会，生产环境运行；Agent.market 上线
- **Agentic Wallets**：2026年2月上线
- **Payments MCP**：Base 链上 Agent 交易量 10,000% 增长
- **Brian Armstrong**："很快将有更多 AI Agent 在线交易而非人类"

#### Mastercard
- **收购**：BVNK（$1.8B，2026年3月）
- **全球加密伙伴计划**：85+ 数字资产公司
- **定位**：跨境汇款、B2B、商业流、财资管理
- **Global Dollar Network**：与 Robinhood, Kraken, DBS 参与 Paxos 的 USDG

#### Fireblocks
- **角色**：托管层核心
- **关键数据**：USDG 最大单一持有者（$150M，占总量 8.97%）
- **调查**：2025年3月调查 295 家金融机构高管，48% 认为更快结算是稳定币支付首要优势
- **客户**：包括船经纪、钢铁贸易商等传统 B2B 玩家

#### MoonPay
- **产品**：MoonPay Agents（2026年2月24日）
- **定位**：完整的 Agent 金融生命周期（法币入金→钱包→交易→出金）
- **基础设施**：500+ 企业客户、3000万+ 用户、180国覆盖
- **差异化**：覆盖完整闭环，不只是单一环节
- **2026年集成**：与 Paysafe（年交易量 $1,670亿）集成

#### Ralio（早期创业公司代表）
- **成立**：2025年，伦敦
- **融资**：$2.5M Pre-Seed（2026年4月14日），3倍超额认购，3个月内完成
- **领投方**：Sure Valley Ventures（SVV）
- **跟投方**：Seed X, Love Ventures, Plug and Play, rule30, Adeline Arts and Science, Endurance Ventures, Campus Fund, Alan Morgan, Antler
- **定位**：AI Agent 支付的"信任基础设施层"——guardrails、身份验证、审计追踪
- **核心功能**：可编程支出限额、意图验证、human-in-the-loop 监督、 robust 欺诈检查
- **支持协议**：Anthropic MCP、Google A2A
- **支付轨道**：FPS、BACS、SEPA、Cards、Stablecoins
- **团队**：Ghali Bennani Laafiret（前 Alan 战略，LumApps $650M 退出）+ Leonardo Rosales（前 FORM3 CTO，将支付系统从 5 人扩展至 300 人工程师团队）
- **CEO 原话**："AI Agent 不再只是生产力工具，它们正在成为能够采购服务和管理资本的自主经济参与者。然而，金融世界仍然为人类干预而构建。Ralio 正在构建使 Agent 金融对企业安全且可扩展的缺失层。"

---

## 四、悬而未决的核心问题

### 4.1 Agent 身份与 KYC：法律人格真空

**核心矛盾**：AI Agent 无法提供政府颁发的身份证件，因此**无法开设银行账户**。这是 CZ 和 Brian Armstrong 反复强调的结构性原因——Agent 必须使用加密钱包。

**但问题没有解决**：
- **谁对 Agent 的支付行为负责？** 如果 Agent 被 prompt injection 攻击并转移了资金，法律责任归属于人类主人、Agent 开发商、还是钱包提供商？
- **KYC 的代理问题**：MoonPay 的解决方案是人类一次性 KYC，但 Agent 之后的所有交易都"挂靠"在人类身份下。这在合规上是否可持续？监管机构是否会要求每笔 Agent 交易都有可追溯的人类授权？
- **Agent 身份的链上验证**：ERC-8004 和 BAP-578 提供了技术方案，但**法律层面**Agent 仍然没有"人格"。
- **从 KYC 到 KYA（Know Your Agent）**：Jay Yu 提出，未来可能需要基于 Agent 行为数据而非人类身份证件来评估信任度。但 KYA 标准尚未建立，数据点太少。

**悬而未决程度**：🔴 极高。这是 Agentic Payment 大规模落地的最大法律障碍。

### 4.2 合规监控：机器速度的监管套利风险

**现状**：
- x402、AP2、Stripe Machine Payments 都已经上线
- 但**AML/交易监控工具还没有跟上**
- 传统银行的交易监控系统（如 Actimize）是为人类交易模式设计的

**未解问题**：
- Agent 可以每秒发起数千笔微交易，传统监控系统无法处理这种频率
- Agent-to-Agent 交易是否触发报告门槛？如何界定"可疑交易"？
- 跨链交易的追踪：Agent 可能在 3 秒内通过 5 条链转移资金，监管如何追踪？
- Mandates 合约的法律效力：如果 Agent 超出 Mandate 授权范围交易，该交易是否有效？

**悬而未决程度**：🟠 高。技术可行，但监管框架和工具严重滞后。

### 4.3 私钥安全与 Prompt Injection：Agent 持有资金的根本风险

**现状**：
- EIP-7702 和 session keys 提供了部分解决方案
- MPC 钱包（如 Cobo、Fireblocks）消除了单点私钥风险

**未解问题**：
- **Prompt Injection 攻击**：如果 Agent 的决策逻辑被恶意 prompt 覆盖，它可能授权错误交易。已有 prototype 证明可行，防护方案还在早期
- **API Key = 私钥**：Jay Yu 指出，私钥本质上就是 API Key，钱包的安全体系可以迁移到 API Key 管理。但 API Key 的泄露风险（可 rotate、可 scoping）与私钥（一旦泄露不可撤销）有本质区别
- **Solver 中心化风险**：意图中心（intent-centric）架构下，solver 网络可能高度集中，少数实体控制大部分交易路由
- **智能合约漏洞**：Agent 钱包的合约代码一旦被攻破，批量 Agent 资金面临风险

**悬而未决程度**：🟠 高。技术方案在演进，但安全实践尚未成熟。

### 4.4 跨链流动性碎片化

**现状**：
- Circle CCTP V2 支持 17 条链，累计 $110B+ 交易量
- 但 USDC 在每条链上是独立的合约实例

**未解问题**：
- Agent 需要在 Ethereum、Solana、Base、Arbitrum 之间无缝转移资金，但跨链桥仍然**慢且贵**
- Tempo 和 Circle Arc 试图解决，但尚未主网上线
- 不同链上的 Gas 代币不同，Agent 需要管理多币种 Gas 预算
- x402 v2 引入插件架构支持多链，但跨链session的可重用性仍需验证

**悬而未决程度**：🟡 中。技术路线清晰，但落地需要时间。

### 4.5 微支付经济学：亚美分交易的可行性

**现状**：
- x402 支持亚美分级别的微支付
- 但区块链 Gas 费在高峰期可能超过微支付本身的价值

**未解问题**：
- 在 Ethereum 主网上，$0.001 的微支付可能需要 $0.50 的 Gas
- L2（Base, Arbitrum）解决了部分问题，但批量微支付的**聚合结算**方案尚未成熟
- 如何在保证去中心化的前提下实现"零 Gas"或"后付费"模式？
- Solana 的低成本使其成为 x402 主要执行环境（65% 交易量），但这是否意味着 Agent 支付将**绑定单链**？

**悬而未决程度**：🟡 中。L2 和专用链（Tempo）正在解决，但大规模应用仍需验证。

### 4.6 稳定币发行商的利率风险

**现状**：
- Circle 和 Tether 的主要收入来自储备资产（美国国债）的利息
- 美联储利率若降至 3%，发行商需要额外发行 $88.7B 稳定币才能维持当前利息收入（CoinShares 测算）
- Circle 2025年Q4已反映收益率下降趋势

**未解问题**：
- 利率下行周期中，稳定币发行商的商业模式是否可持续？
- 是否会出现"稳定币战争"——发行商通过补贴抢占市场份额？
- 如果发行商盈利压力增大，是否会降低合规投入或增加风险资产比例？
- Circle 与 Coinbase 的收入分成协议（2026年8月到期）：若重新谈判，RLDC 利润率能否从 40% 提升至 50-55%？

**悬而未决程度**：🟡 中。宏观经济变量，难以预测。

### 4.7 Agent 支付的"冷启动"与应用层匮乏

**现状**：
- 基础设施已经就位（钱包、协议、出入金、标准基金会）
- 但**消费端应用仍然稀缺**

**未解问题**：
- x402 日均真实商业交易量仅约 $1.4万，与 $70 亿生态市值严重脱节
- Stripe ACP 与 Shopify 集成后仅约 12 家商户激活，支付时仍需人类跳转
- 普通用户为什么需要 Agent 来帮自己花钱？
- 除了 API 调用和 DeFi 交易，Agent 支付的其他场景在哪里？
- 如何让用户信任一个自动花钱的 Agent？

**悬而未决程度**：🟡 中。需要杀手级应用来驱动需求。

### 4.8 协议层面的"标准战争"

**现状**：
- x402：开放协议，无协议费，无账户创建，无供应商锁定，Apache 2.0 许可
- MPP（Stripe）：企业级协议，闭源，依托 Stripe 商户网络
- AP2：企业集成路线，Mandates 机制

**未解问题**：
- x402 只支持加密货币，没有法币通道；如果 Agent 需要用企业信用卡支付 SaaS API，无法使用 x402
- Stripe 的 MPP 有分发优势但中心化；Coinbase 的 x402 中立但平台叙事复杂（Commerce 产品下线、Business 仅限美新）
- 三个协议是否会收敛？还是长期并存？
- 对创业者而言，应该基于哪个协议构建？

**悬而未决程度**：🟡 中。标准竞争是长期过程。

---

## 五、创业机会地图

### 5.1 机会矩阵：按"可实现性 × 市场空间"

```
                市场空间大
                    ▲
                    │
    ┌───────────────┼───────────────┐
    │               │               │
    │  Agent 安全护栏 │  Agent 合规   │
    │  B2B跨境支付   │  中间件       │
    │  Agent 信贷    │  Agent 钱包   │
    │               │               │
    │  ◄────────────┼────────────►  │
    │               │               │
    │  微支付聚合器  │  Agent 保险   │
    │  税务自动化    │  跨链流动性   │
    │  Agent SEO     │  Agent 发现层 │
    │               │               │
    └───────────────┼───────────────┘
                    │
                    ▼
                市场空间小
        可实现性低 ◄────────► 可实现性高
```

### 5.2 高优先级机会（P0）

#### 机会 1：Agent 安全护栏 / 信任基础设施

**痛点**：Prompt Injection 可以把 Agent 的 API Key 全部偷走发到暗网。安全不是可选项，是 Agent 经济的生死线。

**验证信号**：
- **Ralio**：$2.5M Pre-Seed，3倍超额认购，欧洲最大 Agentic Payment 轮次
- **Capsule Security**：2026年4月退出隐身模式，$7M Seed，运行时信任层监控、控制、防止 Agent 不安全行为
- Jay Yu（Pantera）："私钥本质上就是 API Key，钱包的安全体系完全可以迁移到 API Key 管理"

**机会**：
- 构建专为 Agent 交易设计的**实时监控 + 行为审计引擎**
- 功能：意图验证、支出限额执行、human-in-the-loop 监督、完整审计追踪、欺诈检测
- 差异化：不做支付网络本身，而是做"支付前的强制检查点"
- 目标客户：部署 AI Agent 的企业（采购、薪酬、财资管理）

**壁垒**：监管关系 + 数据积累（Agent 行为模式的训练数据）+ 与主流 Agent 框架的兼容性

**对标**：Ralio（欧洲）、Capsule Security（美国）

#### 机会 2：Agent 合规中间件

**痛点**：Agent 支付的 AML/KYC/交易监控工具严重缺失。传统金融的合规系统无法处理机器速度的交易。

**机会**：
- 构建专为 Agent 交易设计的**实时监控引擎**
- 功能：异常检测（Agent 行为基线建模）、Mandates 合规校验、跨链追踪、自动报告生成
- 目标客户：稳定币发行商、支付编排平台（Stripe/BVNK）、交易所

**壁垒**：监管关系 + 数据积累

**对标**：Chainalysis 的 Agent 版本

#### 机会 3：B2B 跨境支付编排

**痛点**：传统跨境 B2B 支付结算周期 3-5 天，中间行费用高，汇率不透明。稳定币可以秒级结算，但企业需要**合规的、集成现有 ERP 的解决方案**。

**验证信号**：
- Stripe 数据显示 60% 稳定币支付是 B2B
- Fireblocks 调查发现 48% 金融机构认为更快结算是首要优势
- AllScale（播客嘉宾项目）：自托管稳定币 Neobank，从发票切入，1200万美元收款
- 发展中国家 Airbnb host 更愿意收稳定币（payout 周期太短）

**机会**：
- 面向中小企业的稳定币跨境支付 SaaS
- 集成 SAP/Oracle/NetSuite，自动将应付账款转为稳定币支付
- 内置外汇对冲、税务合规、发票匹配
- 目标市场：跨境电商、国际贸易、远程团队薪酬

**对标**：Airwallex 的稳定币版本

#### 机会 4：企业级 Agent 钱包

**痛点**：现有 Agent 钱包要么太简单（MoonPay 面向消费者），要么太封闭（Coinbase 生态）。企业需要一个**可编程、可审计、多签/多策略**的 Agent 钱包。

**机会**：
- 企业级 Agent 钱包：支持多 Agent、预算分配、审批流、自动对账
- 功能：MPC 安全、多链支持、x402/AP2/MPP 原生集成、支出限额、自动报告
- 目标客户：AI 公司（需要为 Agent 支付 API/计算费用）、金融机构（Agent Treasury 管理）

**壁垒**：安全基础设施 + 合规能力 + 企业销售

**对标**：Fireblocks 的 Agent 版本

### 5.3 中优先级机会（P1）

#### 机会 5：Agent 身份与信誉系统

**痛点**：Agent 之间交易需要信任，但链上身份只有钱包地址，没有信誉历史。没有身份就没有信贷，没有信贷就没有真正的 Agent 经济。

**技术路线**：
- ZK 身份：证明身份属性而不透露真实信息（ZKID）
- 社交身份：基于 TikTok/Instagram 绑定（适合发展中国家 Creator）
- Agent Passport：用户ID + Agent ID + 会话ID 三层架构（Kite AI）
- KYA（Know Your Agent）：基于链上行为数据 + 评分

**机会**：
- 构建 Agent 的链上信誉评分系统
- 维度：交易历史、履约率、Mandates 遵守情况、人类背书
- 应用：Agent marketplace 中的信任机制、信用额度分配

**壁垒**：数据网络效应 + 标准制定能力

#### 机会 6：Agent 信贷 / 借贷市场

**痛点**：传统银行最赚钱的是信贷，Agent 银行也不会例外。现在有开发者发现：Agent 访问服务但付不了钱——钱包里没钱。

**验证信号**：Jay Yu（Pantera）："Agent 贷款市场会是一个非常大的机会"，未来 12-18 个月会有更多尝试。

**细分方向**：
- 副卡模式：基于用户信用给 Agent 开副卡（类比信用卡副卡）
- Agent 信用评分：基于 Agent 行为数据评估信用（类比花呗/借呗）
- DeFi 借贷：Agent 在链上 pool 借贷（Aave/Compound）
- 供应链金融：Agent 之间的信用链条

**关键约束**：前提是完善的 Agent 身份体系。人可以靠大数法则评估信用，Agent 可能"突变"——需要看 Agent 周边架构。

#### 机会 7：微支付聚合器

**痛点**：Agent 的亚美分微支付在链上单独结算不经济。x402 平均单笔 $0.20，约半数为测试。

**机会**：
- 构建微支付层：批量聚合 Agent 的微支付，定期统一结算
- 类似 Lightning Network，但面向 Agent 场景优化
- 支持"后付费"模式：Agent 先消费，月底统一结算

#### 机会 8：Agent 发现层 / Agent 经济基础设施

**痛点**：Agent 不知道哪个服务最好，需要"发现"机制。不是搜索引擎，而是"菜谱"式的 workflow 编排。

**机会**：
- Agent SEO：如何在 Agent 搜索中被推荐
- Agent 广告：针对 Agent 的广告投放（为什么 Agent 推荐 A 而非 B？）
- Workflow 编排：把多个 API call 绑定成"菜谱"，说明 cost、操作、规则
- Agent 评分/声誉：链上不可篡改的 Agent 评分（8004Scan）
- Agent APP Store：Agent 技能市场

**验证信号**：Merit Systems（x402scan, MPPscan, AgentCash 开发商）、Ampersend.ai 已获 x402 Foundation 创始成员资格。

### 5.4 长期机会（P2）

#### 机会 9：跨链流动性协议（Agent 原生）

**痛点**：Agent 需要在多链之间无缝转移资金，但现有跨链桥对 Agent 不友好。

**机会**：
- 专为 Agent 设计的跨链流动性协议
- 功能：智能路由（自动选择最低成本路径）、Gas 抽象（统一 Gas 代币）、跨链 Mandates 执行

#### 机会 10：Agent 支付保险

**痛点**：Agent 被攻击、prompt injection、智能合约漏洞等风险。

**机会**：
- 为 Agent 支付提供保险覆盖
- 产品：Mandates 违约险、私钥泄露险、智能合约漏洞险

---

## 六、VC 视角的投资判断框架

### 6.1 赛道评估

| 维度 | 评分 | 理由 |
|------|------|------|
| 市场规模 | ⭐⭐⭐⭐⭐ | $317B 且高速增长，Citi 预测 2030 年 $1.9T |
| 需求真实性 | ⭐⭐⭐⭐⭐ | Stripe $400B 交易量、Visa $4.6B 年化结算已验证 |
| 监管确定性 | ⭐⭐⭐⭐ | GENIUS Act + MiCA 已落地，全球框架趋于清晰 |
| 技术成熟度 | ⭐⭐⭐⭐ | 基础设施就绪，Agent 协议已产品化 |
| 竞争格局 | ⭐⭐⭐ | L1-L4 巨头卡位，L5-L7 仍有空间 |
| 创业窗口期 | ⭐⭐⭐⭐ | 早期应用层机会仍开放，但协议层投资窗口可能已关闭 |

### 6.2 关键判断：协议层投资窗口是否已关闭？

**x402 的 $70 亿生态市值 vs $1.4万日均真实交易量** 这一悬殊差距，说明协议层的基础设施投资可能已经过热。22 家顶级机构已入场，标准已确立，新的协议层创业公司很难获得差异化空间。

**但应用层和中间层的机会刚刚打开**：
- Agent 安全护栏：Ralio $2.5M、Capsule Security $7M 只是开始
- B2B 跨境支付：AllScale 1200万美元收款已验证需求
- Agent 发现层：Agent.market 刚上线，生态尚处萌芽

### 6.3 对投资人的启示

#### 值得关注的方向

1. **"稳定币 + Agent"交叉点的中间件**：协议层（x402/AP2/MPP）已被大玩家定义，但中间件（合规、钱包、编排、安全、信贷）仍有大量空白
2. **B2B 跨境支付**：Stripe 数据已验证 60% 稳定币支付是 B2B，这是最确定的增量市场
3. **Agent 安全与信任基础设施**：Ralio 和 Capsule Security 的融资信号表明这是早期且必要的方向
4. **新兴市场**：Tether 的 OMS 聚焦非洲/亚洲/拉美，传统金融基础设施薄弱，稳定币 leapfrog 机会更大
5. **专用链（Tempo/Arc）生态项目**：类似早期 Ethereum 生态，新链上线会带来基础设施需求
6. **中国市场的结构性机会**：42号文 + 1号令为"境内资产 + 境外链上结算"的 Agent Payment 架构提供了合规底座

#### 需要谨慎的方向

1. **稳定币发行**：Circle/Tether/Paxos 已形成极高壁垒，新发行商几乎没有机会
2. **纯协议层项目**：x402 Foundation 22 家成员已覆盖全部关键玩家，新协议难以获得采用
3. **忽视合规的技术项目**：GENIUS Act 和 MiCA 已明确红线，无合规能力的团队将被淘汰
4. **单链押注**：多链并存是大概率事件，Tempo（多稳定币中立）vs Arc（USDC 原生 Gas）的路线之争尚无定论
5. **高估短期交易量**：x402 真实商业交易量还很小，需要区分"基础设施投资"和"应用层投资"的时间线

#### 关键观察指标

| 指标 | 信号意义 | 数据来源 |
|------|---------|---------|
| Stripe Bridge 交易量增速 | B2B 稳定币支付的真实需求晴雨表 | Stripe 年报 |
| x402 真实商业交易量（排除测试） | Agent 支付生态的健康度 | Artemis/Dune |
| Agent.market 服务商数量 | 应用层生态繁荣度 | Agent.market |
| GENIUS Act 执行细则 | 美国监管的实际松紧程度 | Treasury/SEC |
| MiCA 完全执行后 USDT/USDC 份额变化 | 监管合规对市场结构的影响 | CoinGecko |
| Tempo/Arc 主网表现 | 专用稳定币链是否能挑战通用链 | 链上数据 |
| Agent 支付交易量 vs 人类支付交易量 | 结构转变的速度 | 各协议数据 |
| Ralio/Capsule 等安全公司的客户增长 | Agent 安全需求的真实度 | 公司公告 |

---

## 研究方法说明

### 数据来源

- **权威财经媒体**：CryptoSlate, Odaily, BlockEden, CoinShares, The Block, CoinDesk, Foresight News, BlockBeats, 学习区块链
- **行业研究机构**：Citi, PwC, Capgemini, McKinsey, KPMG, Morgan Stanley, Pantera Capital
- **企业官方**：Stripe 年报、Circle 财报/上市文件/CEO 财报电话会、Visa/Mastercard 公告、Coinbase 博客、MoonPay 公告、Ralio 官方声明
- **监管机构**：Federal Reserve, SEC, Treasury, HKMA, 欧洲央行, 中国人民银行（42号文）
- **技术社区**：x402 Foundation, AP2 Protocol 文档, BNB Chain 技术公告, Linux Foundation
- **播客/一手观点**：支无不言播客 EP22（Jay Yu/Pantera Capital）、a16z 2026 预测
- **链上数据**：Artemis, Dune Analytics, CoinGecko

### 数据质量分级

- 🟢 **高可信度**：Fed/SEC 官方数据、上市公司财报、已确认的大型 M&A 交易、链上原始数据
- 🟡 **中等可信度**：企业官方声明、行业媒体深度报道、分析师报告、播客嘉宾观点
- 🔴 **低可信度**：预测性数据（Citi $1.9T、PwC $2.6-4.4T）、未验证的早期项目声明、社交媒体传言

### 重要声明

1. **预测性数据**：Citi 的 $1.9T（2030）、PwC 的 $2.6-4.4T（2030）等均为第三方预测，不代表本报告作者观点。
2. **M&A 交易**：Stripe/Bridge（$1.1B）、Mastercard/BVNK（$1.8B）等数据基于公开报道，最终交易金额可能调整。
3. **x402 交易量数据**：Artemis 链上数据显示 2026年3月日均成交额约 $2.8万，但约半数被分析为测试交易，真实商业交易量更低。
4. **Agentic Payment 早期阶段**：x402、AP2、MoonPay Agents 等产品虽已上线，但大规模采用尚未验证。
5. **非投资建议**：本报告仅供行业研究参考。

---

> **报告结束**
> 
> 本报告基于公开信息的系统性搜集与结构化分析，融合了知识库既有内容（Web3/Agentic Payment 投资主题、VC Daily Brief）及播客/从业者一手观点。所有数据均标注来源与可信度，无编造成分。建议读者对时效敏感的数据进行二次核实。
