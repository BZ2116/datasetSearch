# 2026-08-15 日计划：明确高质量数据集的定义与构建框架

## 对应研究问题

数据集怎么构建才算高质量？

## 复现对象与材料

- Dolma：数据来源、统一 schema、provenance、过滤和版本化。
- FineWeb：Common Crawl 清洗、质量过滤和去重思路。
- DataComp：固定模型和评测集，只比较数据构建策略。

## 具体工作

- [x] 为三篇工作建立阅读卡，记录数据来源、处理步骤、保留率、质量指标和评测方式。
- [x] 对比“数据文件”和“可复现数据构建流程”的区别。
- [x] 明确质量维度：正确性、完整性、多样性、覆盖度、可追溯性、安全性、污染风险。
- [x] 确定本项目统一数据 schema 和 provenance 字段。

## 产出

- `benchmarks/data_construction_matrix.md`
- `data_schema.md`
- `benchmarks/high_quality_data_checklist.md`
- `benchmarks/data_construction_matrix.md` 中的数据生命周期图

## 对调研的作用

为后续过滤、选择、混合和增强实验建立统一评价标准，避免只用模型分数定义数据质量。
