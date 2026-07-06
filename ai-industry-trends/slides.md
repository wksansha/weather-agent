# AI 产业发展趋势
## 从算力到互联的硬科技革命

<!-- layout: title -->

📅 2026 年 6 月 | 👤 AI 产业研究团队 | ⏱ 约 30 min

---

<!-- layout: section -->

## AGENDA · 内容路线图

---

<!-- layout: content -->

## 今天的内容路线图

- **01 CPU：算力基石** — x86 与 ARM 两强争霸，AI 加速单元成标配 (~3min)
- **02 GPU：训练与推理引擎** — Blackwell 领跑，ASIC 双线追击 (~3min)
- **03 光模块：数据洪流通道** — 800G → 1.6T → 3.2T，光电互联革命 (~3min)
- **04 PCB：高速信号载体** — M8→M9 材料升级，高端产能紧缺 (~2min)
- **05 存储：大模型的记忆基石** — HBM4 即将登场，存内计算从概念走向量产 (~3min)
- **06 互联与网络** — NVLink 5 + InfiniBand + Ultra Ethernet (~2min)
- **07 散热与能效** — 单机柜 132kW，液冷从可选项变必选项 (~2min)
- **08 市场格局与展望** — 五大确定性趋势，把握投资脉络 (~4min)

---

<!-- layout: section -->

## CHAPTER 01
### CPU：算力基石

从通用计算到 AI 专用 —— 服务器 CPU 的新战场

---

<!-- layout: content -->

## x86 与 ARM 两强争霸，AI 专用加速单元成为标配

<!-- layout: two_column -->

:::left

### 🔵 Intel Xeon 6

- Granite Rapids · 最多 128 核
- 内置 AMX 矩阵引擎，BF16/INT8 推理加速
- 单路 12 通道 DDR5，PCIe 5.0 × 88 lane
- **AMX · 2048-bit**

### 🔴 AMD EPYC 9005

- Turin · Zen 5 架构
- 最多 192 核 384 线程
- AVX-512 全吞吐，12 通道 DDR5-6000
- CXL 2.0 内存扩展
- **192 Cores · 500W TDP**

:::right

### 🟢 ARM Neoverse V3 / N3

- AWS Graviton4 · NVIDIA Grace
- 每瓦性能领先 x86 约 30-50%
- AmpereOne 192 核云原生 CPU 已量产
- **ARM v9.2 · SVE2**

### 💡 关键趋势

CPU 不再是"通用计算"的代名词。内置 AI 加速器（AMX、SVE、NPU）正让 CPU 在推理侧重新夺回话语权。ARM 阵营凭借每瓦性能优势在云原生场景加速渗透，x86 以生态和单核峰值守住基本盘。

---

<!-- layout: section -->

## CHAPTER 02
### GPU：训练与推理的算力引擎

从 Blackwell 到 ASIC —— 算力军备竞赛的核心战场

---

<!-- layout: content -->

## Blackwell 领跑，AMD + 自研 ASIC 双线追击

| 指标 | NVIDIA B200 | AMD MI450X | Google TPU v6 | 华为 Ascend 910C |
|------|------------|------------|---------------|------------------|
| 制程 | TSMC 4NP | TSMC N3 | TSMC N3 | SMIC N+2 |
| FP16 TFLOPS | 4,500 | 2,300 | 1,800 | 800 |
| 显存 | 192 GB HBM3e | 288 GB HBM3e | 96 GB HBM3 | 128 GB HBM2e |
| TDP | 1,000W | 750W | 600W | 550W |

- **关键数据:** B200 FP4 算力 20K+ TFLOPS | 192 GB HBM3e 显存 | 8 TB/s 带宽

### 💡 关键趋势

NVIDIA 以 Blackwell 架构 + NVLink 5 + 液冷整机柜方案建立系统级壁垒。AMD 以更大显存和开放生态（ROCm 6.0）追赶。Google / AWS / Meta 自研 ASIC 推理芯片加速部署，训练侧 2026 仍是 GPU 天下。

---

<!-- layout: section -->

## CHAPTER 03
### 光模块：数据洪流的"光速"通道

800G → 1.6T → 3.2T，光电互联的速度革命

---

<!-- layout: content -->

## 800G 大规模出货，1.6T 即将商用，硅光技术拐点已至

<!-- layout: two_column -->

:::left

### 🔷 800G OSFP / QSFP-DD800

- 2026 年 AI 训练集群标配
- DR8 / FR4 / SR8 多模方案齐全
- 单模块功耗 ~14W，硅光版本降至 ~10W
- 主要供应商：中际旭创、Coherent、Finisar
- **8×100G PAM4**

### 🔶 1.6T / 3.2T 下一代

- 1.6T OSFP-XD 预计 2026H2 量产
- 200G/lane × 8，CPO 功耗降低 40%+
- **200G/lane · CPO**

:::right

### LPO（线性驱动）

- 去掉 DSP 芯片，功耗降低 50%
- 延迟 < 5ns
- 2026 年 800G LPO 开始小批量部署

### 硅光（SiPh）

- CMOS 工艺兼容，低成本大规模制造
- Intel / Ayar Labs / 曦智科技领跑
- 2027 渗透率预计 > 30%

### 薄膜铌酸锂（TFLN）

- 超高带宽调制器
- 200G+ 单波速率关键使能技术
- HyperLight / 光库科技布局

### 💡 关键趋势

光模块速率每 2 年翻一番。LPO + 硅光两条技术路线并行演进，产业链话语权向模块厂商和硅光代工厂集中。

---

<!-- layout: section -->

## CHAPTER 04
### PCB：高速信号的高密度载体

从 M8 到 M9 材料，AI 服务器 PCB 的价值重构

---

<!-- layout: content -->

## AI 服务器 PCB 四大升级方向

- **📐 层数升级：从 20L → 30L+** — GPU 模组板（UBB）普遍 26-30 层，Switch 背板 34 层+。高层数带来更高的布线密度和更复杂的 PDN 设计。**30L+ · UBB**

- **🔧 材料升级：M7 → M8 → M9** — 超低损耗 CCL 需求爆发。M8 级 Df < 0.002 @ 10GHz，M9 级 Df < 0.0015。松下 Megtron 8、台耀 TU-983 为主流方案。**Df < 0.0015 · M9**

- **📏 HDI + Any-Layer 工艺** — NVIDIA GB300 NVL72 采用超大尺寸 HDI 板，单板 700×600mm+。Any-Layer 技术从手机走向数据中心。**700×600mm · Any-Layer**

- **💪 供需格局：高端产能紧缺** — 全球高端 PCB 产能集中在臻鼎、欣兴、Ibiden、三星电机。AI 拉动高端 PCB 市场 CAGR 25%+（2024-2030），2026 年仍供不应求。**CAGR 25% · 供不应求**

---

<!-- layout: section -->

## CHAPTER 05
### 存储：大模型的"记忆"基石

HBM 堆叠竞赛 + NAND 闪存的大容量时代

---

<!-- layout: content -->

## HBM4 即将登场，存内计算从概念走向量产

| 指标 | HBM3 | HBM3e | HBM4 | LPDDR5x (边缘) |
|------|------|-------|------|----------------|
| 单堆容量 | 24 GB | 36 GB | 48-64 GB | 16-32 GB |
| 带宽 | 819 GB/s | 1.2 TB/s | 1.6-2.0 TB/s | 68 GB/s |
| 堆叠层数 | 12-Hi | 12-Hi | 16-Hi | — |
| IO 位宽 | 1024-bit | 1024-bit | 2048-bit | 64-bit |
| 主要供应商 | SK海力士/三星 | SK海力士/三星/美光 | SK海力士(先行) | 三星/美光 |

### 🔺 HBM 市场格局

SK 海力士 53% 份额领先（HBM3e 独家供货 NVIDIA），三星 38%，美光 9%。2026 全球 HBM 市场规模预计突破 400 亿美元。

### 💡 关键趋势

HBM 是 GPU 性能释放的最大瓶颈。HBM4 通过 2048-bit 位宽和 16-Hi 堆叠将带宽翻倍。PIM（存内计算）让 HBM 不只是"存储"还能执行矩阵运算。边缘侧 LPDDR + 片上 SRAM 围绕能效做取舍。

---

<!-- layout: content -->

## 单机柜 132kW+ 时代，液冷从"可选项"变成"必选项"

### 🌡️ 功耗持续攀升

GB300 NVL72 单机柜功耗高达 132kW。B200 单芯片 TDP 1000W，下一代 Rubin 预计 1500W+。传统风冷极限 ~30kW/机柜已被远远超越。**132kW/rack**

### 💧 液冷三大路线

- **冷板式：** 成熟方案，PUE ~1.1，NVL72 标配。Vertiv / CoolIT / Boyd 为主要供应商
- **浸没式：** 单相/两相，PUE < 1.05，氟化液成本仍高。阿里 / 微软部分 AI 集群已部署
- **芯片级：** 微通道直触，台积电 / Cooltera 研发中

### 📊 市场规模

2026 全球液冷市场 ~120 亿美元（CAGR 35%+）。CDU 单台 1.5MW 散热能力。2028 年 80%+ 新建 AI DC 将采用液冷，PUE 从 1.4 降至 1.05。

---

<!-- layout: content -->

## 2026 年 AI 基础设施市场规模

### 核心市场数据

- **芯片总市场: $420B** | GPU/AI 加速器: $180B | HBM 存储: $85B | 光模块: $28B

### 🏆 芯片四强格局

NVIDIA 以 ~80% AI GPU 份额绝对领先。AMD 追赶至 ~12%。自研 ASIC（Google TPU / AWS Trainium / Meta MTIA）合计 ~5%。华为 Ascend 在中国市场份额领先。

### 🌏 国产替代加速

华为 Ascend 910C 量产，寒武纪思元 690 进入数据中心。海光 DCU 兼容 ROCm 生态。中国 AI 芯片自给率 2026 年约 15-20%，加速追赶中。

### 📈 Capex 竞赛

微软/谷歌/亚马逊/Meta 2026 AI Capex 合计超 $300B。xAI Colossus 10 万 GPU 集群已投产，全球 AI 超算竞赛白热化。

**重点标的：** NVIDIA (NVDA) · AMD (AMD) · Broadcom (AVGO) · SK海力士 · 中际旭创 · 华为昇腾 · Marvell · Arista

---

<!-- layout: content -->

## 2026-2028：六个确定性趋势

1. **算力持续翻倍** — GPU 每 2 年算力翻倍（Blackwell → Rubin → Vera）。ASIC 推理芯片将占推理市场 30%+，训练仍以 GPU 为主

2. **互联速率倍增** — Scale-Up：NVLink 6→7，UBB 2.0。Scale-Out：800G → 1.6T → 3.2T。CPO 将光引擎集成至交换机芯片

3. **存储带宽破墙** — HBM4 → HBM4e，PIM 存内计算普及。CXL 3.0 内存池化打破"内存墙"。QLC NAND 256TB SSD 成为推理缓存标配

4. **液冷全面渗透** — 2028 年 80%+ 新建 AI DC 采用液冷。PUE 从 1.4 → 1.05。液冷产业链 CAGR 35%+

5. **端侧 AI 崛起** — AI PC（NPU > 40 TOPS）、AI 手机（SoC 内置 LLM 引擎）、具身智能（机器人芯片）将创造新增长极

6. **地缘重塑供应链** — 出口管制推动国产替代。东南亚封装测试产能扩建。Chiplet + 先进封装（CoWoS / EMIB）成为"新摩尔定律"

---

<!-- layout: section -->

## 感谢聆听 · 欢迎交流

AI 基础设施正经历百年一遇的架构变革，每一个环节都值得深入跟踪。

📧 ai-research@example.com | 🔗 github.com/ai-trends | 📊 数据截止 2026.Q2

Thank You · Questions & Discussion
