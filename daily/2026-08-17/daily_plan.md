# 2026-08-17 日计划：数据选择与混合策略

## 对应研究问题

数据选择和数据混合分别带来什么收益？

## 论文研读

重点阅读以下工作，先明确方法和实验结论，再设计复现实验。正式录用论文为主，前沿工作单独标注：

- `[正式录用] DataComp-LM`（NeurIPS 2024）：固定模型、训练预算和评测协议。
- `[正式录用] DS²`（ICLR 2025）：了解 rating-based 数据筛选和数据效率评测。
- `[正式录用] Data Mixture Optimization`（NeurIPS 2025）：理解数据配比优化的实验设置。
- `[正式录用] D3`（IJCAI 2025）：了解 diversity、difficulty、dependability 的组合。
- `[前沿/待确认] Large-Scale Data Selection for Instruction Tuning`：补充 instruction 数据选择方法。
- `[前沿/待确认] Rethinking Data Selection: The Importance of Coverage over Difficulty`：核对 coverage 与 difficulty 的比较。

阅读产出：更新 `benchmarks/data_selection_matrix.md`，记录每篇论文的数据池、选择信号、baseline、固定预算和主要指标，并明确哪些结论可以由本实验验证。

## 具体数据与 benchmark

参考 DataComp-LM 的固定模型/训练/评测思想；由于本实验要直接比较 instruction 数据选择，使用带有来源和任务族标签的 instruction 数据池作为可执行替代。

DataComp 的固定模型和下游测试集用于控制变量；重点记录其数据筛选策略，而不是复现完整数据规模。

## 复现对照组

- A：随机选择。
- B：质量分数选择。
- C：难度/perplexity 选择。
- D：embedding coverage 选择。
- E：质量 + coverage 联合选择。
- F：不同来源/任务族混合比例。

## 具体指标

- 训练域性能。
- 未见表达、未见实体和未见任务族性能。
- 数据来源覆盖度和任务族覆盖度。
- 数据重复率与样本数量。

## 产出

- `experiments/exp02_selection_mixture/README.md`
- `experiments/exp02_selection_mixture/AGENT_TASK.md`
- `experiments/exp02_selection_mixture/config.json`
- `benchmarks/data_selection_matrix.md`
- `daily/2026-08-17/daily_summary.md`

## 对调研的作用

验证“难度最高的数据不一定最有用”，并区分选择策略提升的是模型质量、覆盖范围还是跨域泛化。
