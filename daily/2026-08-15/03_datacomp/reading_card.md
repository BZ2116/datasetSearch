# 论文阅读卡片

## 基本信息

- **论文：** DataComp: In Search of the Next Generation of Multimodal Datasets
- **作者 / 年份：** Samir Yitzhak Gadre 等 / NeurIPS 2023
- **链接：** https://arxiv.org/abs/2304.14108
- **论文类型：** Benchmark / 数据选择
- **阅读范围：** 摘要、benchmark 设计、数据池、baseline 与评测

## 一句话理解

> DataComp 固定模型训练流程和评测协议，只让研究者改变数据集，从而把数据构建从隐含工程工作变成可比较的实验对象。

## 1. 它解决的问题

传统 benchmark 通常固定数据、比较模型，导致数据筛选和数据来源的贡献难以单独衡量。DataComp 反过来固定模型和训练代码，鼓励研究者设计更好的数据集。

## 2. 数据来源

提供来自 Common Crawl 的 CommonPool，包含约 12.8B image-text pairs；同时区分只使用候选池的 filtering track 和允许外部数据的 BYOD track。

## 3. 核心处理

```text
fixed candidate pool / external sources
    ↓
filtering, scoring, deduplication or source curation
    ↓
fixed training code and compute budget
    ↓
38 downstream evaluation datasets
    ↓
compare data curation strategies
```

**论文真正创新：**

将数据集设计建立为 benchmark：固定模型架构、训练代码、规模和评测集，使不同数据处理策略之间具备可比性。

## 4. 是否合成

- [x] 完全不是合成数据
- [ ] 部分合成
- [ ] 主要是合成数据

说明：候选数据主要来自网页图文对，研究重点是筛选和构建，不是生成训练样本。

## 5. 如何评测

在多个数据规模和固定计算预算下训练 CLIP，并在 38 个下游数据集上评测。论文报告的代表性 baseline DataComp-1B 在 ImageNet zero-shot 上达到 79.2%，说明数据构建策略可以在固定训练流程下产生显著差异。

## 6. 最大局限

- 原始 DataComp 面向图文对和 CLIP，不是语言模型或 Agent benchmark；
- 下游分数仍是间接指标，不能自动解释具体数据为何有效；
- 固定训练配方提高可比性，但可能限制某些数据类型的最佳训练方式；
- 评测集污染、来源偏差和多任务权衡仍需要额外分析。

## 7. 对 LongTaskBench 的启发

### 可直接迁移

固定模型、训练预算、评测集和随机种子，只比较任务来源、清洗策略、增强方法或混合比例。

### 需要修改

将图文数据集的样本筛选扩展为任务级、轨迹级和能力覆盖级选择。

### 准备验证

构造随机、质量、难度、coverage 和质量+coverage 五种选择策略，在相同样本数和 token 预算下训练 Agent。

### 预期收益

避免把模型差异、训练预算差异误判为数据集差异。

### 潜在风险

单一总分可能掩盖某些任务族退化，因此必须报告分能力、分任务族和未见分布指标。

## 一句话结论

> DataComp 提供了研究数据价值的实验控制方法：先固定模型和评测，再把数据构建策略作为唯一主要变量。
