# 2026-08-19 日计划：验证合成数据是否真的有用

## 对应研究问题

如何验证合成数据不是只增加数据量？

## 论文研读

- `[正式录用] WebArena`（ICLR 2024）：参考可执行任务和最终成功率评测。
- `[正式录用] OSWorld`（NeurIPS 2024）：参考多步骤计算机操作和环境反馈评测。
- `[正式录用] SWE-bench`（ICLR 2024）：参考代码任务的可执行 verifier 和测试集设计。
- `[前沿/待确认] FLAMES`：重点查看过程、答案和验证器一致性的要求。
- `[前沿/待确认] Increasing LLM Coding Capabilities through Diverse Synthetic Coding Tasks`：关注合成代码任务的多样性。
- `[前沿/待确认] ToolMind`：了解工具调用/轨迹数据中的逐步验证和失败风险。
- 回看 `Self-Instruct` 与 `Evol-Instruct` 的质量控制部分，整理可迁移的过滤和人工抽检方法。

阅读产出：形成“数据量增加”与“能力覆盖增加”的判定表，并把论文中的验证指标映射到下面的对照实验。

对应阅读卡片位于 `daily/2026-08-19/01_webarena/` 至 `06_toolmind/`。

## 具体评测

根据前一天的数据类型选择：

- GSM8K：准确率、未见题型、数值变体、程序/计算器验证。
- MBPP：pass@1、单元测试通过率、未见函数描述。
- Super-NaturalInstructions：未见任务模板和任务族泛化。

## 训练/评测对照

- A：原始数据，固定样本数。
- B：加入语言改写，固定总样本数。
- C：加入难度增强，固定总样本数。
- D：加入可验证 reasoning，固定总样本数。
- E：单纯复制原始样本，固定总样本数。

必须保持模型、训练步数、token 预算、batch size 和评测集一致。

## 必须记录

- 训练域性能。
- 未见表达、实体、模板和任务族性能。
- 语义保持率、标签一致率、重复率。
- 自动 verifier 通过率和人工抽检结果。

## 产出

- `experiments/exp03_synthetic_augmentation/evaluation.md`
- `benchmarks/synthetic_data_validity_criteria.md`
- `benchmarks/synthetic_failure_taxonomy.md`
- `daily/2026-08-19/daily_summary.md`
- “增加数据量”与“增加能力覆盖”的对照结果。

## 对调研的作用

形成判断合成数据有效性的标准：只有在固定预算下提升未见分布表现，并且通过质量/一致性验证，才算真正有用。
