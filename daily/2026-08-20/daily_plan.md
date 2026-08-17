# 2026-08-20 日计划：数据归因与模型能力支撑

## 对应研究问题

模型的回答和能力究竟由哪些数据支撑？

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
- 归因方法分类表。
- 归因排名与删除后性能变化图。
- 归因可靠性和适用边界说明。

## 对调研的作用

把“归因分数”转化为可验证证据，判断归因方法能否支持数据选择、删除有害数据和解释模型能力来源。
