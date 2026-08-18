# 2026-08-20 日计划：数据归因与模型能力支撑

## 对应研究问题

模型的回答和能力究竟由哪些数据支撑？

## 论文研读

- `[正式录用] TRAK: Attributing Model Behavior at Scale`（ICML 2023）：回顾随机投影和可扩展归因假设。
- `[正式录用] Helpful or Harmful Data? FreeShap`（ICML 2024）：阅读 helpful/harmful 样本识别、删除和选择实验。
- `[正式录用] Source-Aware Training Enables Knowledge Attribution in Language Models`（COLM 2024）：区分影响归因与知识来源归因。
- `[前沿/待确认] Data Shapley in One Training Run`：理解单次训练估计数据价值的思路。
- `[前沿/待确认] DataDignity`：补充 provenance benchmark 和来源保持改写的验证方法。

阅读产出：更新归因方法分类表，明确每篇工作归因的对象、需要的模型信息、验证方式和适用边界；再决定本日复现哪些方法。

对应阅读卡片位于 `daily/2026-08-20/01_trak/` 至 `05_datadignity/`。

## 复现对象与具体数据集

先做低成本、可控复现：

- TRAK + CIFAR-10：复现视觉分类数据归因。
- TRAK + QNLI：复现语言分类数据归因。
- FreeShap + QNLI 或 SST-2：复现 helpful/harmful data 选择或删除。

不在本日尝试大模型逐条归因。

## 复现对照

- attribution 方法。
- embedding similarity baseline。
- loss/gradient baseline。
- 随机排序 baseline。

## counterfactual 验证

- 删除 top-k 高影响样本。
- 删除 bottom-k 样本。
- 随机删除同样数量样本。
- 重新训练或继续训练。
- 比较目标验证集 loss 和 accuracy 变化。

## 产出

- `experiments/exp04_attribution/README.md`
- `experiments/exp04_attribution/AGENT_TASK.md`
- `experiments/exp04_attribution/config.json`
- `benchmarks/attribution_method_matrix.md`
- `daily/2026-08-20/daily_summary.md`
- 归因排名与删除后性能变化图。
- 归因可靠性和适用边界说明。

## 对调研的作用

把“归因分数”转化为可验证证据，判断归因方法能否支持数据选择、删除有害数据和解释模型能力来源。
