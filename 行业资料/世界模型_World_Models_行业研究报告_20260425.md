# 世界模型（World Models）深度行业研究报告

> 报告日期：2026年4月25日
> 研究范围：全球世界模型技术生态，涵盖视频生成世界模型、潜在世界模型、交互式3D世界模型、物理仿真及具身智能应用
> 核心观点：世界模型正从"更好的视频生成"进化为"可交互的物理仿真引擎"，成为通向AGI和Physical AI的核心路径。2026年Q1已有约$60亿流入6-7家头部公司，但技术路线之争远未结束。当前最确定的投资机会在"世界模型基础设施层"（仿真平台、数据工具链）和"垂直场景落地"（自动驾驶、机器人），而非押注单一路线的Foundation Model公司。

---

## 摘要（Executive Summary）

### 核心结论
- **技术成熟度**：世界模型处于"GPT-2.5时刻"——能力真实存在，但实验室到实际部署的gap仍然很大。三大路线（视频生成、潜在模型、交互式3D）各有优劣，最终架构仍是开放问题
- **市场规模**：世界模型作为AI子集，处于$500B+全球AI市场（2026年）和$136B生成式AI市场之内。专门的世界模型市场尚无明确定义，但Physical AI相关市场（机器人、自动驾驶、仿真）合计超$300B
- **关键趋势**：(1) 从"观看世界"到"与世界交互"的范式转移；(2) 仿真到现实（Sim-to-Real）成为机器人训练的核心路径；(3) 物理AI开发者工具链（"物理AI的Cursor"）涌现
- **投资主题**：基础设施层（仿真平台、数据工具）> 垂直应用（自动驾驶、机器人）> Foundation Model（路线不确定性高）
- **风险因素**：技术路线不确定性极高；训练成本惊人（NVIDIA Cosmos需10,000 H100训练3个月）；物理世界的复杂性远超语言；监管对自主系统的安全要求

### 投资评级矩阵
| 维度 | 评分 (1-5) | 说明 |
|------|-----------|------|
| 技术成熟度 | ★★☆☆☆ | 概念验证大量存在，但可泛化的通用世界模型仍未出现 |
| 市场吸引力 | ★★★★★ | Physical AI（机器人+自动驾驶）是万亿级市场，世界模型可能是关键使能技术 |
| 竞争格局 | ★★☆☆☆ | 极度早期，大厂和初创公司同场竞技，赢家远未确定 |
| 监管风险 | ★★★☆☆ | 自主系统安全法规趋严，但当前影响有限 |
| 时机窗口 | ★★★☆☆ | Foundation Model层估值已极高（$3-8B pre-product）；基础设施层仍有合理估值 |

---

## 一、技术演进（Technology Evolution）

### 1.1 技术定义与核心原理

世界模型（World Models）是AI系统对世界运作方式的内部表示——学习物体如何移动、相互作用、对行动做出反应，从而能够预测未来状态。

**与视频生成模型的本质区别**：
- **视频模型**：P(x_{t+1} | x_t) —— 基于当前帧预测下一帧，被动观看
- **世界模型**：P(s_{t+1} | s_t, a_t) —— 基于当前状态和行动预测下一状态，主动交互

那个 **a_t**（action，行动）是关键。世界模型必须理解：如果我做了X，世界会如何响应。

用投资语言理解：**视频生成是"更好的好莱坞"；世界模型是"更好的现实模拟器"**。

**为什么世界模型可能是通向AGI的必要路径？**
- Yann LeCun的核心论点：人类大部分推理根植于物理世界，而非语言。儿童通过观察物体掉落就内化了重力概念，无需牛顿定律教学
- 当前LLM（GPT、Claude等）是" linguistic world model"（语言世界模型），但缺乏对物理因果关系的理解
- 世界模型提供了一种学习范式：通过观察+交互，而非仅通过文本，来构建对世界的理解

### 1.2 发展历程时间线

| 时间 | 里程碑 | 意义 |
|------|--------|------|
| 1990 | Schmidhuber提出"世界模型"概念 | 理论起源 |
| 2018 | Ha & Schmidhuber: "World Models"论文 | 首次用神经网络构建可训练的世界模型，在虚拟环境中训练智能体 |
| 2020 | Dreamer (Danijar Hafner, DeepMind) | 潜在世界模型（Latent World Model）的突破：智能体在想象中训练 |
| 2021 | MuZero (DeepMind) | 结合世界模型与蒙特卡洛树搜索，在围棋、象棋、Atari中取得SOTA |
| 2022 | Interactive World Models探索 | 研究者开始探索可交互的生成式世界模型 |
| 2023 | Genie (DeepMind), V-JEPA (Meta/LeCun) | Google发布Genie（可交互2D世界）；LeCun发布I-JEPA/V-JEPA |
| 2024 | Sora (OpenAI), Veo (Google), Genie 2 | 视频生成世界模型爆发；Genie 2支持3D可交互环境 |
| 2025 | Genie 3, Cosmos, Marble, AMI Labs成立 | 实时交互式3D世界模型成熟；NVIDIA发布Cosmos；LeCun离开Meta创办AMI |
| 2026 | AMI $1B融资, World Labs $1B融资, Wayve $1.2B | 世界模型成为AI融资最大主题之一；物理AI应用加速 |

### 1.3 技术路线对比

当前世界模型领域存在**五大竞争路线**：

| 路线 | 代表方案 | 核心原理 | 优势 | 劣势 | 适用场景 |
|------|----------|----------|------|------|----------|
| **视频生成模型** | Sora, Veo 3, Runway GWM-1 | 基于Transformer预测像素序列 | 视觉质量极高；可利用海量互联网视频训练 | 非交互式；不理解物理因果；幻觉严重 | 内容创作、影视制作 |
| **生成式交互世界模型** | Genie 3, World Labs Marble | 生成可交互的3D环境，支持实时操作 | 真正的交互性；支持训练embodied agents | 计算成本极高；物理一致性仍有限 | 游戏、机器人训练、虚拟世界 |
| **潜在世界模型** | Dreamer, V-JEPA 2, AMI VL-JEPA | 在压缩的潜在空间中建模世界动态 | 计算效率高；适合agent训练 | 抽象表示可能丢失关键物理细节 | 机器人控制、连续控制任务 |
| **混合方法** | General Intuition, Moonlake | 生成式世界用于数据收集+潜在空间用于agent学习 | 兼顾视觉质量和训练效率 | 架构复杂；需要协调两个子系统 | 通用embodied AI |
| **神经符号世界模型** | Verses.ai AXIOM | 对象级表示+主动推理 | 可解释性强；符合人类认知结构 | 工程化程度最低；扩展性未验证 | 科学模拟、可解释AI |

**关键争论：哪条路线会赢？**

当前共识：**没有单一赢家，最终方案可能是多种方法的组合**。

- Google DeepMind采取多路线并进：Genie（生成式）、SIMA（LLM-based agent）、Veo（视频生成）
- LeCun的AMI押注潜在世界模型（JEPA架构）
- Fei-Fei Li的World Labs押注生成式3D世界
- OpenAI的Sora团队虽关停toC产品，但明确表示继续专注世界模拟研究

**投资者的框架性认知**：
1. **视频生成路线**（Sora/Veo）更像"更好的工具"，而非AGI路径
2. **交互式生成路线**（Genie/Marble）最有潜力成为通用训练平台
3. **潜在模型路线**（JEPA/Dreamer）在机器人控制上效率最高
4. **混合路线**可能是长期最优解，但技术复杂度也最高

### 1.4 关键技术瓶颈与突破方向

**瓶颈1：物理一致性（Physical Consistency）**
- 当前世界模型在长时间交互后会出现物理规律违背（物体穿墙、重力异常等）
- **突破方向**：
 - 物理引擎耦合（将神经世界模型与传统物理仿真结合）
 - 更长的上下文窗口和一致性机制
 - 物理约束嵌入训练目标

**瓶颈2：Sim-to-Real Gap**
- 在模拟中训练的agent在真实世界表现下降
- Meta的V-JEPA 2在100万小时互联网视频训练后，仅用62小时机器人数据就达到80%零样本抓取成功率——这是鼓舞人心的，但仅限于"容易模拟的任务"
- **突破方向**：
 - Domain Randomization（域随机化）
 - 真实世界数据闭环（Tesla FSD、Waymo的做法）
 - 自适应世界模型（根据真实世界反馈持续更新）

**瓶颈3：训练成本**
- NVIDIA Cosmos训练需10,000 H100 GPU运行3个月
- 这种资本密集度意味着只有少数公司能训练基础世界模型
- **突破方向**：
 - 更高效的架构（Mamba、State Space Models替代Transformer）
 - 蒸馏和压缩技术
 - 开放模型权重降低重复训练需求

**瓶颈4：数据稀缺**
- 全球机器人操作数据仅约30万小时，而互联网文本约300万亿token、视频约10亿小时
- **突破方向**：
 - 合成数据生成（世界模型本身就是解决方案）
 - 遥操作数据收集（Physical Intelligence、Tesla的做法）
 - 互联网视频的无监督学习（V-JEPA路线）

---

## 二、市场现状（Market Landscape）

### 2.1 市场规模与增长预测

世界模型本身尚无独立的市场规模统计，但其支撑的核心市场包括：

```
世界模型相关市场总规模（单位：十亿美元）

数据来源：Grand View Research, Noizz.io, Statista, BVP

┌─────────────────────────────────────────────────────────────┐
│ 全球AI市场（2026年）                    $539B                │
│ ├─ 生成式AI                            $136B                │
│ ├─ AI基础设施                          $176B                │
│ └─ 世界模型相关子市场                                          │
│    ├─ 自动驾驶软件/仿真                 $45B (est.)          │
│    ├─ 机器人软件/仿真                   $32B (est.)          │
│    ├─ 游戏引擎/3D内容生成               $28B (est.)          │
│    ├─ 工业仿真/Digital Twin             $38B (est.)          │
│    └─ 世界模型基础设施/工具链             $5B (est.,  nascent)│
└─────────────────────────────────────────────────────────────┘

世界模型直接相关市场（基础设施+平台）：
2024: ████░░░░░░░░░░░░░░░░  ~$1.0B
2025: ███████░░░░░░░░░░░░░  ~$2.0B
2026: ██████████░░░░░░░░░░  ~$5.0B (est.)
2028: ████████████████░░░░  ~$15B (est.)
2030: ████████████████████  ~$40B (est.)

驱动假设：
- 自动驾驶仿真渗透率从5%提升至30%
- 机器人训练从物理为主转向仿真为主（60%+）
- 游戏/3D内容生成中AI辅助比例从10%提升至50%
```

**关键数据点**：
- 2025年全球AI创业公司VC投资约$980亿，其中约45%投向AI基础设施和应用
- Q1 2026单季度约$60亿流入6-7家世界模型公司
- NVIDIA Cosmos平台下载量突破200万次

### 2.2 市场细分（Segmentation）

| 细分领域 | 当前规模(est.) | 增长率 | 代表应用 | 关键玩家 |
|----------|---------------|--------|----------|----------|
| **自动驾驶仿真** | $12B | 35% | 虚拟测试里程、场景生成、传感器仿真 | Wayve, Waymo, NVIDIA (Cosmos), Antioch |
| **机器人训练/仿真** | $8B | 45% | 操作训练、sim-to-real、策略验证 | Physical Intelligence, General Intuition, Ai2 |
| **游戏/3D内容生成** | $15B | 40% | 程序化世界生成、AI辅助关卡设计 | World Labs (Marble), DeepMind (Genie), Runway |
| **工业仿真/Digital Twin** | $22B | 25% | 工厂仿真、供应链优化、预测维护 | NVIDIA (Omniverse), Siemens, Ansys |
| **世界模型基础设施** | $1B | 80% | 仿真平台、数据工具链、评估基准 | Antioch, Foxglove, Voxel51 |

**增长最快**：世界模型基础设施（80% CAGR），因为整个Physical AI生态需要工具链支撑。

### 2.3 价值链分析

```
上游（基础模型/算力）        中游（平台/工具链）           下游（应用/终端）
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ 世界模型Foundation│       │ 仿真平台/引擎    │       │ 自动驾驶系统     │
│ (AMI, World Labs)│◄─────►│ (Genie, Marble) │◄─────►│ (Wayve, Waymo)  │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ 云计算/算力      │       │ 开发者工具链     │       │ 机器人系统       │
│ (NVIDIA, AWS)   │◄─────►│ (Antioch,Cursor)│◄─────►│ (Figure, Tesla) │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ 训练数据         │       │ 数据基础设施     │       │ 游戏/娱乐       │
│ (合成/真实)      │◄─────►│ (Foxglove,Scale)│◄─────►│ (Ubisoft, EA)   │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ 芯片/硬件        │       │ 评估/测试平台    │       │ 工业/制造       │
│ (NVIDIA H100)   │◄─────►│ (Voxel51, Argus)│◄─────►│ (Siemens, Bosch)│
└─────────────────┘       └─────────────────┘       └─────────────────┘

价值捕获分析：
- 上游Foundation Model：高资本壁垒，赢家通吃风险，当前估值已极高
- 中游平台/工具链："卖铲子"逻辑，风险较低，增长确定性高
- 下游应用：需垂直领域know-how，但市场规模最大

Bessemer Ventures判断："Near-term value will accrue to full-stack, vertically 
integrated players, not pure-play foundation model companies."
（近期价值将归属于全栈垂直整合玩家，而非纯Foundation Model公司）
```

### 2.4 区域市场分布

| 区域 | 市场份额 | 增长驱动力 | 代表公司/项目 |
|------|---------|-----------|--------------|
| **北美** | 45% | VC资本密集、顶级研究人才、自动驾驶领先 | AMI Labs, World Labs, OpenAI, NVIDIA, Google DeepMind |
| **欧洲** | 25% | 自动驾驶监管友好（英国、德国）、学术基础强 | Wayve (英国), AXELERA AI (荷兰), Oxa (英国) |
| **亚太** | 25% | 制造业基础、机器人需求、政府AI投资 | 中国：商汤、百度Apollo；日本：丰田、索尼 |
| **其他** | 5% | 中东主权基金、以色列技术 | Mobileye (以色列) |

---

## 三、竞争格局与主要玩家（Competitive Landscape）

### 3.1 市场集中度分析

世界模型市场呈现"**大厂主导基础研发、初创公司探索应用**"的格局：
- **Foundation Model层**：Google DeepMind、OpenAI、Meta、AMI Labs、World Labs 5家占据95%+的研发投入
- **基础设施/工具链层**：高度分散，20+初创公司竞争
- **应用层**：自动驾驶（Waymo、Wayve、Tesla）、机器人（Physical Intelligence、Figure）相对集中

### 3.2 主要玩家画像

#### AMI Labs (Advanced Machine Intelligence)
- **公司**：AMI Labs
- **定位**：Yann LeCun的世界模型商业化尝试，押注JEPA架构
- **核心产品/技术**：
  - VL-JEPA（Vision-Language JEPA）：结合视觉和语言的联合嵌入预测架构
  - 目标：构建理解物理世界、拥有持久记忆、能够推理和规划的AI系统
- **融资情况**：$10.3亿（2026年3月），估值$35亿——欧洲史上最大种子轮
- **投资者**：Bezos Expeditions, Cathay Innovation, Greycroft, Hiro Capital, HV Capital, Mark Cuban, Eric Schmidt
- **团队**：
  - Yann LeCun（Executive Chairman）：图灵奖得主，Meta FAIR创始人
  - Alex LeBrun（CEO）：前Nabla（医疗AI）CEO
- **竞争优势**：
  - LeCun的学术权威和人才号召力
  - JEPA架构在自监督学习中的理论基础扎实
  - 全球布局（巴黎、蒙特利尔、新加坡、纽约）
- **风险点**：
  - $35亿 pre-product估值极高，已price in大量预期
  - JEPA路线尚未在规模上证明优于生成式路线
  - 与Meta的竞业/知识产权关系

#### World Labs
- **公司**：World Labs
- **定位**：Fei-Fei Li的3D生成式世界模型公司
- **核心产品/技术**：
  - Marble：首个商业化的世界模型产品，从文本/照片/视频生成可下载的3D环境
  - 支持VR（Vision Pro, Quest 3）
  - 导出格式兼容Unreal Engine和Unity
- **融资情况**：累计超$10亿，估值$54亿（2026年2月）
- **投资者**：a16z, NEA, Radical Ventures等
- **团队**：
  - Fei-Fei Li（创始人）：斯坦福AI实验室主任，ImageNet创始人
  - Justin Johnson（联合创始人）：密歇根大学教授，生成模型专家
- **商业模式**：Freemium（Free $0/4次 → Max $95/月/75次）
- **竞争优势**：
  - Fei-Fei Li的学术声誉和人才网络
  - Marble是首个商业化世界模型产品，有真实收入
  - 3D内容生成市场（游戏、影视、VR）明确
- **风险点**：
  - 当前Marble更偏向内容创作工具，而非通用世界模型
  - $54亿估值对当前收入而言极高
  - 与Sora/Veo/Runway在内容生成市场的直接竞争

#### Google DeepMind
- **公司**：Google DeepMind
- **定位**：多路线并进的世界模型研究领导者
- **核心产品/技术**：
  - Genie 3：首个实时交互式3D世界模型（24fps, 720p），支持键盘/控制器操作
  - SIMA 2：基于Gemini的通用游戏/3D环境Agent
  - Veo 3：视频生成世界模型
  - "Video Thinking"团队：将世界模型能力整合进Gemini
- **资源投入**：DeepMind拥有"科技史上最强的印钞机"（Google搜索广告）作为后盾
- **竞争优势**：
  - 无限算力和数据资源
  - Demis Hassabis的AGI愿景与资源执行力
  - Waymo已使用DeepMind世界模型测试驾驶模型
- **风险点**：
  - Google的大公司病——多线并行可能导致资源分散
  - 商业化节奏可能慢于初创公司

#### NVIDIA
- **公司**：NVIDIA
- **定位**：世界模型基础设施的"卖铲人"
- **核心产品/技术**：
  - Cosmos World Foundation Model：开源世界模型平台，面向Physical AI
  - Omniverse：工业仿真和数字孪生平台
  - 200万+下载量
- **商业模式**：不卖模型，卖GPU+平台生态
- **竞争优势**：
  - 控制算力基础设施（H100/B200/GB200）
  - Cosmos开源策略建立生态粘性
  - Omniverse在企业工业仿真中的先发优势
- **投资含义**：NVIDIA是世界模型浪潮中最确定的受益者，但非早期VC机会

#### Wayve
- **公司**：Wayve
- **定位**：自动驾驶+世界模型的垂直整合者
- **核心产品/技术**：
  - GAIA-1 / GAIA-2：自动驾驶世界模型
  - 端到端自动驾驶系统，在车辆中运行
- **融资情况**：$12亿（2026年2月Series D+），估值$86亿
- **投资者**：SoftBank, NVIDIA, Microsoft, Uber, Baillie Gifford
- **竞争优势**：
  - 英国监管对自动驾驶测试最友好
  - 端到端AI驾驶的技术路线与Tesla一致但更加纯粹
  - 与Uber的合作提供真实部署场景
- **风险点**：
  - $86亿估值对pre-revenue公司而言极高
  - 自动驾驶商业化时间线持续推迟的行业风险

#### Physical Intelligence (Pi)
- **公司**：Physical Intelligence
- **定位**：机器人Foundation Model
- **核心产品/技术**：
  - π0：通用机器人策略模型
  - 通过遥操作收集数据训练通用机器人技能
- **融资情况**：$6亿（2025年11月），估值$56亿
- **投资者**：Amazon, OpenAI, Sequoia, Thrive Capital等
- **团队**：
  - Karol Hausman（CEO）：前Google DeepMind机器人研究主管
  - Sergey Levine（联合创始人）：UC Berkeley机器人学习顶级学者
  - Chelsea Finn（联合创始人）：斯坦福助理教授，机器人学习专家
- **竞争优势**：
  - 可能是全球最强的机器人学习团队
  - 先发优势：最早提出并实践"机器人Foundation Model"概念
- **风险点**：
  - 机器人数据获取成本极高（遥操作$100+/小时）
  - 技术路线（纯数据驱动 vs 世界模型增强）存在不确定性

### 3.3 竞争态势矩阵

**技术路线 vs 商业化进度矩阵**：

| | 高商业化（产品/收入） | 中商业化（试点/合作） | 早期阶段（研究/pre-product） |
|--|---------------------|---------------------|---------------------------|
| **生成式交互** | World Labs (Marble) | Genie 3, Runway | Decart, Moonlake |
| **潜在模型** | - | V-JEPA 2 (Meta) | AMI Labs, Embo (Hafner) |
| **混合方法** | - | General Intuition | - |
| **LLM-based** | - | SIMA 2, Physical Intelligence | - |

**关键观察**：
- 唯一有明确产品收入的是World Labs（Marble订阅），但$54亿估值已极高
- 大部分"头部"世界模型公司（AMI、Wayve、Physical Intelligence）都是pre-product/pre-revenue
- **基础设施层（仿真工具、数据平台）可能是风险收益比更好的投资区域**

---

## 四、未来方向与趋势（Future Trends）

### 4.1 技术趋势

**趋势1：从"通用世界模型"到"领域专用世界模型"**
- 通用世界模型（理解所有物理规律）可能需要10年+才能实现
- 短期更现实的路径：自动驾驶专用世界模型、厨房专用世界模型、工厂专用世界模型
- **投资含义**：垂直领域世界模型公司可能比通用公司更快商业化

**趋势2：世界模型与LLM的融合**
- Google将世界模型能力整合进Gemini（Video Thinking团队）
- 物理推理+语言理解的多模态模型是中期最可能成功的架构
- **投资含义**：纯世界模型公司可能面临大厂的"功能整合"竞争

**趋势3：开源生态的加速**
- NVIDIA Cosmos开源下载200万+
- Ai2开源MolmoBot（纯仿真训练的机器人策略）
- 开源可能 commoditize 基础世界模型，但数据和部署平台仍有壁垒
- **投资含义**：类似于LLM领域的Llama效应——开源模型降低门槛，但垂直应用和数据飞轮创造赢家

**趋势4：仿真到现实的闭环**
- 未来机器人训练的标准流程：仿真预训练 → 真实世界微调 → 真实世界数据回流更新世界模型
- 这个闭环是世界模型商业化的核心飞轮
- **投资含义**：具备数据闭环能力的公司（Tesla、Waymo、Physical Intelligence）有结构性优势

### 4.2 应用趋势

**趋势1：自动驾驶是世界模型最先落地的场景**
- Waymo已使用DeepMind世界模型评估驾驶模型
- 虚拟测试里程可以替代数十亿真实路测里程
- 监管接受度：仿真测试数据在部分司法管辖区可被纳入安全认证

**趋势2：机器人训练从"物理优先"转向"仿真优先"**
- Bessemer估计：行业机器人数据成本未来两年将超过$30亿
- 世界模型可以将仿真训练比例从当前的<20%提升至>60%
- 这是10倍级的成本降低

**趋势3：游戏和娱乐是toC最先爆发的场景**
- Marble、Genie等产品的直接应用
- 用户生成内容（UGC）+ AI生成世界（AIGW）= 新的内容范式
- 但商业模式尚不明确（订阅？按生成量付费？）

**趋势4：科学和工业仿真**
- 药物发现：分子动力学世界模型
- 气候模拟：地球系统世界模型
- 材料科学：新材料发现的世界模型
- 这些领域的世界模型可能产生巨大的社会价值和商业价值

### 4.3 产业整合趋势

- **Big Tech全面布局**：Google（DeepMind）、Meta（FAIR/JEPA）、Microsoft（投资Wayve/Physical Intelligence）、NVIDIA（Cosmos/Omniverse）
- **垂直整合**：自动驾驶公司（Wayve、Tesla、Waymo）自建世界模型；机器人公司（Physical Intelligence、Figure）同理
- **工具链独立化**：仿真和数据工具正在从"大厂内部工具"变为"独立平台公司"（Antioch、Foxglove）

### 4.4 监管与伦理趋势

| 法规/议题 | 影响 | 方向 |
|----------|------|------|
| 自动驾驶安全法规 | 要求仿真测试+真实测试双重验证 | 正面（增加仿真需求） |
| AI系统可解释性要求 | 世界模型是"黑盒"，interpretability是刚需 | 中性/负面（增加合规成本） |
| 机器人安全标准 | 工业/服务机器人部署前的仿真验证要求 | 正面 |
| 生成内容版权 | AI生成3D世界的知识产权归属 | 不确定 |
| 深度伪造/虚假信息 | 世界模型生成的逼真内容可能被滥用 | 负面（潜在监管限制） |

---

## 五、创业公司推荐（Startup Recommendations）

### 5.1 推荐清单

#### 公司 1: Antioch
| 属性 | 详情 |
|------|------|
| **公司名** | Antioch |
| **成立时间** | 2024年5月 |
| **总部** | 美国纽约 |
| **融资阶段** | Seed |
| **累计融资** | $850万 |
| **估值** | $6,000万（2026年4月） |
| **核心产品** | 物理AI仿真平台——"物理AI的Cursor"；支持机器人开发者在虚拟环境中测试和训练 |
| **技术差异化** | 多模态仿真（支持NVIDIA Cosmos、World Labs、自有物理引擎）；聚焦缩小sim-to-real gap |
| **团队背景** | Harry Mellsop（CEO，前Chainalysis）；Alex Langshur（联合创始人，前Transpose/Chainalysis）；Michael Calvey（联合创始人）；Collin Schlager（前Meta Reality Labs）；Colton Swingle（前Google DeepMind） |
| **LinkedIn** | [linkedin.com/company/antioch-ai](https://linkedin.com/company/antioch-ai) |
| **X/Twitter** | [@antioch_ai](https://x.com/antioch_ai) |
| **官网** | [antioch.ai](https://antioch.ai) |
| **投资亮点** | A*和Category Ventures领投；团队有安全/DeepMind/Meta背景；物理AI工具链是确定性的"卖铲子"机会 |
| **风险提示** | 客户以早期初创公司为主；大厂（NVIDIA Omniverse）竞争 |

#### 公司 2: General Intuition
| 属性 | 详情 |
|------|------|
| **公司名** | General Intuition |
| **成立时间** | 2024年 |
| **总部** | 美国 |
| **融资阶段** | Seed |
| **累计融资** | $1.337亿（2025年10月）——超大种子轮 |
| **估值** | 未公开 |
| **核心产品** | 混合世界模型：生成式世界用于数据收集 + 潜在空间用于agent训练 |
| **技术差异化** | 结合两种路线的优势；声称在General Intuition实验室"几乎每天都有突破" |
| **团队背景** | 未公开详细团队信息 |
| **LinkedIn** | 需手动查找 |
| **X/Twitter** | [@generalintuition](https://x.com/generalintuition)（假设） |
| **官网** | [generalintuition.com](https://generalintuition.com)（假设） |
| **投资亮点** | $133M+超大种子轮表明顶级VC conviction；混合路线可能是长期最优解 |
| **风险提示** | 团队信息不透明；技术路线复杂度高；与AMI/World Labs的直接竞争 |

#### 公司 3: Embo
| 属性 | 详情 |
|------|------|
| **公司名** | Embo |
| **成立时间** | 2026年（筹备中） |
| **总部** | 美国（推测） |
| **融资阶段** | 融资中（目标$1亿） |
| **累计融资** | 未关闭 |
| **估值** | 未公开 |
| **核心产品** | 基于Dreamer路线的潜在世界模型，专注embodied systems |
| **技术差异化** | Danijar Hafner的Dreamer技术商业化；纯潜在空间agent训练，计算效率极高 |
| **团队背景** | Danijar Hafner（CEO，Dreamer论文作者，现Google DeepMind）；Wilson Yan（联合创始人） |
| **LinkedIn** | 需手动查找 |
| **X/Twitter** | 需手动查找 |
| **官网** | 未上线 |
| **投资亮点** | Dreamer是潜在世界模型的canonical example；Hafner是世界模型领域最顶级的研究者之一 |
| **风险提示** | 公司尚未正式成立；潜在世界模型的泛化能力仍有争议；与Google DeepMind的竞业关系 |

#### 公司 4: Decart
| 属性 | 详情 |
|------|------|
| **公司名** | Decart |
| **成立时间** | 2023年 |
| **总部** | 以色列 |
| **融资阶段** | Series B |
| **累计融资** | $1亿+（2025年夏，估值$31亿） |
| **估值** | $31亿 |
| **核心产品** | 世界模型基础设施；为AI agents提供仿真训练环境 |
| **技术差异化** | 以色列强大的AI/安全人才基础；专注agent训练的基础设施 |
| **团队背景** | 以色列顶尖技术团队（具体信息需进一步研究） |
| **LinkedIn** | [linkedin.com/company/decart](https://linkedin.com/company/decart) |
| **X/Twitter** | [@decart_ai](https://x.com/decart_ai) |
| **官网** | [decart.ai](https://decart.ai) |
| **投资亮点** | $31亿估值表明 strong VC traction；以色列AI生态系统质量高 |
| **风险提示** | 估值已较高（pre-product?）；与General Intuition/AMI的功能重叠 |

#### 公司 5: Foxglove
| 属性 | 详情 |
|------|------|
| **公司名** | Foxglove |
| **成立时间** | 2021年 |
| **总部** | 美国旧金山 |
| **融资阶段** | Series B |
| **累计融资** | $4,000万+（多轮） |
| **估值** | 未公开 |
| **核心产品** | 物理AI数据基础设施——数据管道、可视化、调试工具 |
| **技术差异化** | "Physical AI的Datadog"；解决机器人/自动驾驶的数据管理痛点 |
| **团队背景** | Adrian Macneil（CEO，前Cruise数据基础设施负责人） |
| **LinkedIn** | [linkedin.com/company/foxglove](https://linkedin.com/company/foxglove) |
| **X/Twitter** | [@foxglove](https://x.com/foxglove) |
| **官网** | [foxglove.dev](https://foxglove.dev) |
| **投资亮点** | Adrian Macneil是Cruise数据基础设施的 builder；数据工具链是Physical AI的刚需；已被Antioch等采用 |
| **风险提示** | 工具链市场可能面临大厂（NVIDIA、AWS）的竞争 |

#### 公司 6: Voxel51
| 属性 | 详情 |
|------|------|
| **公司名** | Voxel51 |
| **成立时间** | 2018年 |
| **总部** | 美国密歇根 |
| **融资阶段** | Series B |
| **累计融资** | $3,000万+ |
| **估值** | 未公开 |
| **核心产品** | FiftyOne：开源计算机视觉数据和模型评估平台 |
| **技术差异化** | CV/机器人数据的评估和调试；开源社区驱动 |
| **团队背景** | Brian Moore（CEO，密歇根大学计算机视觉博士） |
| **LinkedIn** | [linkedin.com/company/voxel51](https://linkedin.com/company/voxel51) |
| **X/Twitter** | [@voxel51](https://x.com/voxel51) |
| **官网** | [voxel51.com](https://voxel51.com) |
| **投资亮点** | 开源策略建立开发者粘性；计算机视觉数据评估是世界模型训练的刚需 |
| **风险提示** | 从CV评估扩展到世界模型评估的路径需验证 |

#### 公司 7: Argus Systems
| 属性 | 详情 |
|------|------|
| **公司名** | Argus Systems |
| **成立时间** | 2024年 |
| **总部** | 美国 |
| **融资阶段** | 早期 |
| **累计融资** | 未公开 |
| **估值** | 未公开 |
| **核心产品** | 自主系统安全/评估平台 |
| **技术差异化** | 世界模型和自主系统的interpretability、安全评估 |
| **团队背景** | Lisa Yan（创始人） |
| **LinkedIn** | 需手动查找 |
| **X/Twitter** | 需手动查找 |
| **官网** | 需查找 |
| **投资亮点** | Bessemer提到interpretability是"non-negotiable"；安全评估是监管合规的刚需 |
| **风险提示** | 极早期；市场和产品形态不明确 |

### 5.2 创业公司竞争雷达

| 公司 | 技术壁垒 | 团队背景 | 商业化进度 | 融资能力 | 生态位 |
|------|----------|----------|-----------|----------|--------|
| **Antioch** | ★★★☆☆ | ★★★★☆ | ★★☆☆☆ | ★★★☆☆ | 仿真平台 |
| **Foxglove** | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | 数据基础设施 |
| **Voxel51** | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | CV/数据评估 |
| **Embo** | ★★★★★ | ★★★★★ | ☆☆☆☆☆ | ★★★★☆ | 潜在世界模型 |
| **Decart** | ★★★★☆ | ★★★★☆ | ★★☆☆☆ | ★★★★★ | 世界模型infra |
| **General Intuition** | ★★★★☆ | ★★★☆☆ | ★☆☆☆☆ | ★★★★★ | 混合世界模型 |
| **Argus** | ★★★☆☆ | ★★★☆☆ | ★☆☆☆☆ | ★★☆☆☆ | 安全/评估 |

---

## 六、投资判断与风险提示（Investment Thesis & Risks）

### 6.1 投资主题

**主题1：Physical AI的基础设施层是确定性最高的机会**
- 类比：淘金热中"卖铲子"的商人最稳定赚钱
- 无论哪条世界模型路线获胜，都需要仿真平台、数据工具链、评估基础设施
- **代表机会**：Antioch（仿真）、Foxglove（数据）、Voxel51（评估）

**主题2：垂直整合的全栈公司比纯Foundation Model公司更有价值**
- Bessemer判断："Near-term value will accrue to full-stack, vertically integrated players"
- 理由：世界模型必须与实际物理系统（车、机器人）结合才能产生价值
- **代表机会**：Wayve（自动驾驶）、Physical Intelligence（机器人）
- **注意**：这些公司估值已极高（$5-8B），需谨慎评估entry point

**主题3：世界模型+机器人是最具颠覆性的交叉点**
- 机器人数据稀缺是世界模型的完美应用场景
- 世界模型可以将机器人训练成本降低10-100倍
- **代表机会**：Physical Intelligence（已高估值）、Embo（早期）、General Intuition（混合路线）

**主题4：国防/双用机器人将产生第一个$50B+ IPO**
- Bessemer预测：国防机器人将产生机器人领域首个$50B+ IPO
- Anduril已达$600亿估值（2026年3月）；Saronic $1.75B Series D
- 世界模型在国防仿真（战场模拟、无人系统训练）中有直接应用
- **投资含义**：关注具备双用能力（commercial + defense）的世界模型/机器人公司

**主题5：开源世界模型创造生态系统机会**
- NVIDIA Cosmos开源下载200万+，类似Llama效应
- 基础模型 commoditized → 垂直应用和数据飞轮创造价值
- **代表机会**：基于Cosmos/OSS世界模型构建垂直应用的公司

### 6.2 时机判断

| 阶段 | 判断 | 说明 |
|------|------|------|
| **技术成熟度** | 极早期 | 通用世界模型尚未出现；领域专用模型刚起步 |
| **市场时机** | 基础设施层适合进入；Foundation Model层已过热 | 工具链和平台公司估值仍合理（$50-200M）；Foundation Model公司估值$3-8B pre-product |
| **估值水平** | 严重分化 | 头部（AMI $3.5B, World Labs $5.4B, Wayve $8.6B）极高；基础设施层仍合理 |
| **流动性预期** | 3-7年 | Foundation Model公司可能2027-2028年IPO；基础设施层公司可能被战略收购 |

### 6.3 核心风险

| 风险类型 | 风险描述 | 发生概率 | 影响程度 | 缓解因素 |
|----------|----------|----------|----------|----------|
| **技术风险** | 世界模型可能永远无法达到物理一致性要求，sim-to-real gap持续存在 | 中 | 极高 | 领域专用模型降低泛化要求；物理引擎耦合增强一致性 |
| **路线风险** | 当前投资的某条技术路线（JEPA/生成式/混合）被证明是死胡同 | 高 | 高 | 分散投资多条路线；关注基础设施层（路线无关） |
| **资本效率风险** | 训练成本过高，资本密集度导致只有少数玩家能存活 | 中 | 中 | 开源模型降低门槛；蒸馏和压缩技术 |
| **大厂碾压风险** | Google/OpenAI/NVIDIA通过资源整合推出更优方案 | 高 | 中 | 垂直领域know-how和部署能力是初创公司护城河 |
| **监管风险** | 自主系统（自动驾驶、机器人）安全法规趋严 | 中 | 中 | 仿真测试降低真实世界风险；安全评估工具需求增加 |
| **估值风险** | Pre-product公司$3-8B估值已price in完美执行 | 高 | 高 | 避免追高；关注收入/产品驱动的entry point |

### 6.4 建议关注信号

**未来6-12个月关键跟踪指标**：

1. **Genie 3/Marble用户数据**：实际用户活跃度、留存率、使用场景分布
2. **Cosmos生态增长**：基于Cosmos构建的应用数量；企业客户签约情况
3. **AMI Labs技术发布**：首个公开演示或产品预览的时间和质量
4. **机器人sim-to-real里程碑**：Physical Intelligence或Figure的sim-to-real成功率数据
5. **Wayve商业化进展**：与Uber合作的具体部署城市和里程数据
6. **硬件成本曲线**：H100/B200供应和价格变化对世界模型训练成本的影响
7. **中国竞争者动态**：Qwen3等多模态模型是否加入世界模型竞赛

---

*本报告基于公开市场信息整理，仅供内部研究参考，不构成投资建议。*

**数据来源**：
- Not Boring: "World Models: Computing the Uncomputable", 2026
- Introl Blog: "World Models Race 2026", 2026
- Themis: "World Models: Five Competing Approaches", 2026
- Crunchbase News: "AMI Raises $1B", 2026
- Wired: "Yann LeCun Raises $1 Billion", 2026
- TechCrunch: "Antioch Simulation Startup", 2026
- Bessemer Venture Partners: "Predictions: Robotics and Physical AI", 2026
- 36氪: "Sora关停与世界模型赛道", 2026
- NVIDIA: Cosmos Platform官方数据
- Google DeepMind: Genie 3, SIMA 2官方发布
- Noizz.io: AI Market Size 2026
- Grand View Research: AI Market Report 2033

**报告撰写日期**：2026年4月25日
**下次更新建议**：2026年7月（跟踪Genie 3/Marble用户数据、AMI首次产品发布、Q2融资数据）
