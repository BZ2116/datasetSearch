# 2026-08-18 日计划：合成数据与增强类型

## 对应研究问题

数据增强带来什么收益？

## 论文研读

- `[正式录用] Self-Instruct`（ACL 2023）：理解从少量 seed 生成 instruction 数据的流程和过滤方法。
- `[正式录用] Natural Instructions`（ACL 2022）：理解任务模板、任务族和跨任务泛化。
- `[正式录用] Data Augmentation using Large Language Models`（Findings of ACL 2024）：比较不同增强操作及其风险。
- `[前沿/待确认] WizardLM / Evol-Instruct`：重点阅读难度演化的操作类型及质量风险。
- `[前沿/待确认] The Flan Collection`：作为任务混合和指令泛化的补充材料。
- 回看已完成的 `[综述] A Survey on Data Synthesis and Augmentation for Large Language Models`，只提取 taxonomy，不重复精读。

阅读产出：补充增强类型 taxonomy，分别记录语言多样性、任务多样性、难度提升和 reasoning/trajectory 增强的证据与风险。

对应阅读卡片位于 `daily/2026-08-18/01_self_instruct/` 至 `05_flan/`。

## 具体数据集

使用以下任务之一作为可控 seed 数据：

- GSM8K：数学推理。
- MBPP：代码生成。
- Super-NaturalInstructions：多任务指令。

优先选择 GSM8K 或 MBPP，便于自动验证。

## 复现对象

- Self-Instruct：任务/指令生成。
- Evol-Instruct：增加约束和任务难度。
- FLAN：任务混合和指令泛化。

## 增强版本

- 原始样本。
- 语言改写。
- 实体/数值替换。
- 增加约束。
- 反事实变体。
- 多步组合。
- 失败案例或错误答案修正。

## 产出

- `experiments/exp03_synthetic_augmentation/README.md`
- 增强类型 taxonomy。
- 50–100 个 seed 样本及其增强版本。
- 每种增强的生成规则和风险记录。

## 对调研的作用

区分语言多样性、任务多样性和难度提升，避免把“生成了更多文本”误判为“产生了更多有效数据”。
