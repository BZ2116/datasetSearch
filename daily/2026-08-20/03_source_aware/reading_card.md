# 论文阅读卡片：Source-Aware Training

## 基本信息

- **论文：** Source-Aware Training Enables Knowledge Attribution in Language Models
- **状态：** COLM 2024
- **链接：** https://openreview.net/forum?id=UPyWLwciYz
- **类型：** 知识来源归因 / provenance

## 归因对象

回答中的知识由哪个预训练来源文档支持，不是训练样本对预测 loss 的影响。

## 方法

先让模型学习文档 ID 与知识关联，再通过 instruction tuning 学习在回答中引用支持来源。

## 主要结论

在合成数据上可以实现较忠实的 source citation，同时不显著损害 perplexity；数据增强对来源归因能力有帮助。

## 边界

需要来源 ID 和受控数据构造；来源 citation 不等于证明该样本因果影响了模型参数。

## Exp04 迁移

本日不复现 source-aware training，只在方法矩阵中与 influence attribution 分开记录。
