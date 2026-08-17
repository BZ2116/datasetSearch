# 2026-08-17 日计划：数据选择与混合策略

## 对应研究问题

数据选择和数据混合分别带来什么收益？

## 具体数据与 benchmark

优先使用 DataComp small/medium filtering track；如果计算资源不足，使用一个带有任务族标签的 instruction 数据池作为替代。

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
- 选择方法矩阵。
- 数据混合配置。
- benchmark 与指标设计。

## 对调研的作用

验证“难度最高的数据不一定最有用”，并区分选择策略提升的是模型质量、覆盖范围还是跨域泛化。
