# 2026-08-17 日总结：数据选择与混合策略

## 一、今日完成

围绕“数据选择和数据混合分别带来什么收益”，完成了 DataComp-LM、DS²、Data Mixture Optimization、D3、Large-Scale Data Selection 和 Rethinking Data Selection 六项工作的整理，并据此修订 `benchmarks/data_selection_matrix.md` 和 `experiments/exp02_selection_mixture/` 实验任务包。

新增：

- `01_datacomp_lm/reading_card.md`
- `02_ds2/reading_card.md`
- `03_mixture_optimization/reading_card.md`
- `04_d3/reading_card.md`
- `05_large_scale_selection/reading_card.md`
- `06_coverage_over_difficulty/reading_card.md`
- `experiments/exp02_selection_mixture/README.md`
- `experiments/exp02_selection_mixture/AGENT_TASK.md`
- `experiments/exp02_selection_mixture/config.json`
- `benchmarks/data_selection_matrix.md`

矩阵和 6 张阅读卡片现在逐篇记录了数据池、选择信号、baseline、固定预算、主要指标、结论以及 Exp02 能否验证的范围。

## 二、核心研究结论

DataComp-LM 的关键不是某个具体筛选器，而是固定模型、训练代码、计算预算和下游评测，把数据选择变成受控变量。其官方 testbed 使用 Common Crawl 候选池和 53 个下游评测，说明数据构建应当按照统一协议比较。

数据选择不能简化为“选择最高质量”或“选择最难样本”：

- quality 主要处理可靠性和噪声；
- difficulty 反映模型相关的学习难度，但可能选出不可学或错误样本；
- coverage 处理任务、表达、实体和能力的覆盖；
- quality + coverage 试图在可靠性和多样性之间平衡；
- mixture 研究不同任务族/来源比例对能力结构的影响。

DS² 和 D3 共同说明：质量/可靠性需要和多样性联合考虑；Data Mixture Optimization 说明配比搜索应考虑训练成本、不确定性和多保真实验；Large-Scale Data Selection 提醒复杂方法在大池子上未必超过随机；Rethinking Data Selection 则直接提出生成任务中 coverage 可能优于 difficulty。因此 Exp02 必须保留随机基线、固定选择预算，并按任务族拆分报告。

## 三、Exp02 实验设计

```text
A random
B quality
C difficulty/perplexity
D embedding coverage
E quality + coverage
F1/F2/F3 task-family mixtures
```

固定 10,000 条候选池、2,000 条选中数据、TinyStories-33M、三个随机种子和四类未见分布评测。Agent 可以申请 GPU 和安装依赖，但不能改变实验变量。该实验是方向性复现，不声称复现论文的大规模绝对分数。

## 四、下一步

由另一台电脑上的执行 Agent 拉取 `exp02_selection_mixture`，完成数据下载、分数计算、子集构建、模型训练和分层评测。结果需要返回选择分数、选中 ID、覆盖统计、模型指标、环境信息和最终报告。
