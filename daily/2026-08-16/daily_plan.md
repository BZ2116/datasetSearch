# 2026-08-16 日计划：过滤与去重的收益验证

## 对应研究问题

数据过滤和去重分别带来什么收益？

## 具体数据

已确定使用 Dolma 或 FineWeb 的可下载小规模文本子集，控制在 1,000–10,000 条；不尝试复现完整大规模预训练。具体来源、版本和抽样规则待运行时记录。

## 复现对照组

- A：原始数据。
- B：语言、长度、格式和安全过滤。
- C：B + exact dedup。
- D：C + near dedup。

## 具体指标

- 保留率、重复率、平均长度。
- 来源和主题分布变化。
- 训练/验证 n-gram overlap。
- 小型语言模型验证 loss。
- 一个轻量下游评测集，如 WikiText-103 或 LAMBADA。

## 产出

- `experiments/exp01_filter_dedup/README.md`
- `experiments/exp01_filter_dedup/configs/filter.yaml`
- `experiments/exp01_filter_dedup/configs/dedup.yaml`
- `experiments/exp01_filter_dedup/results/` 中的统计表和失败样本抽检表模板。
- `daily/2026-08-16/daily_summary.md`

## 对调研的作用

把“清洗后数据更好”拆成可验证结论：过滤减少噪声，去重减少重复和污染，二者的收益不能混为一谈。
