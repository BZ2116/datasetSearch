# 论文阅读卡片：FreeShap

## 基本信息

- **论文：** Helpful or Harmful Data? Fine-tuning-free Shapley Attribution for Explaining Language Model Predictions
- **状态：** ICML 2024
- **链接：** https://proceedings.mlr.press/v235/wang24aq.html
- **类型：** helpful/harmful 数据归因

## 归因对象

训练样本对语言模型预测的 Shapley-style 贡献，重点识别有帮助、有害和错误标签样本。

## 方法与用途

不需要对目标模型进行 fine-tuning，利用模型预测/表示估计样本贡献，并用于数据删除、选择和错误标签检测。

## 验证方式

比较归因排名和删除/选择后的任务性能，考察 helpful/harmful 数据是否能改善数据子集。

## 边界

近似 Shapley 依赖模型输出和候选集合；分数是目标任务相关的，不是数据的绝对价值。

## Exp04 迁移

在 QNLI 或 SST-2 进行低成本 helpful/harmful 排名和 counterfactual 删除，避免与 TRAK 的梯度要求混淆。
