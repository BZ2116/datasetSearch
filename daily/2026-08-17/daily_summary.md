# 2026-08-17 日总结：数据选择与混合策略

## 一、今日完成

围绕“数据选择和数据混合分别带来什么收益”，完成了 DataComp-LM、instruction data selection 和 coverage/difficulty 方向的整理，并建立 `experiments/exp02_selection_mixture/` 实验任务包。

新增：

- `experiments/exp02_selection_mixture/README.md`
- `experiments/exp02_selection_mixture/AGENT_TASK.md`
- `experiments/exp02_selection_mixture/config.json`
- `benchmarks/data_selection_matrix.md`

## 二、核心研究结论

DataComp-LM 的关键不是某个具体筛选器，而是固定模型、训练代码、计算预算和下游评测，把数据选择变成受控变量。其官方 testbed 使用 Common Crawl 候选池和 53 个下游评测，说明数据构建应当按照统一协议比较。

数据选择不能简化为“选择最高质量”或“选择最难样本”：

- quality 主要处理可靠性和噪声；
- difficulty 反映模型相关的学习难度，但可能选出不可学或错误样本；
- coverage 处理任务、表达、实体和能力的覆盖；
- quality + coverage 试图在可靠性和多样性之间平衡；
- mixture 研究不同任务族/来源比例对能力结构的影响。

近期大规模 instruction selection 结果也提醒：复杂选择方法在大池子上未必超过随机，representation-based 方法可能更稳定。因此 Exp02 必须保留随机基线、固定选择预算，并按任务族拆分报告。

## 三、Exp02 实验设计

```text
A random
B quality
C difficulty/perplexity
D embedding coverage
E quality + coverage
F1/F2/F3 task-family mixtures
```

固定 10,000 条候选池、2,000 条选中数据、TinyStories-33M、三个随机种子和四类未见分布评测。Agent 可以申请 GPU 和安装依赖，但不能改变实验变量。

## 四、下一步

由另一台电脑上的执行 Agent 拉取 `exp02_selection_mixture`，完成数据下载、分数计算、子集构建、模型训练和分层评测。结果需要返回选择分数、选中 ID、覆盖统计、模型指标、环境信息和最终报告。
