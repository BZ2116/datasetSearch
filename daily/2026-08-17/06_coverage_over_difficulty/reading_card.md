# 论文阅读卡片：Coverage over Difficulty

## 基本信息

- **论文：** Rethinking Data Selection: The Importance of Coverage over Difficulty in Generative Fine-Tuning
- **作者 / 年份：** Lalchand Pandia 等 / 2026
- **状态：** ICLR 2026 workshop，前沿/待确认，不按正式录用论文处理
- **链接：** https://openreview.net/forum?id=qImiy98UhN
- **类型：** 数据选择 / coverage vs difficulty

## 一句话理解

> 对生成式微调，单纯选择高难样本可能覆盖不足；聚类式 coverage 选择在多个任务上可以超过 difficulty 选择并达到或超过随机。

## 数据与实验

以 Llama-3-8B 和 OLMo2-7B 为案例，在生成式任务上比较 difficulty、random 和 clustering-based coverage。

## 主要结论

论文报告 difficulty selection 在生成任务中可能落后 random，原因是它聚焦困难样本而忽略输入空间覆盖；coverage 方法表现更好。

## 局限与本项目关系

这是 workshop 前沿工作，结论需要更多模型、数据和任务验证。Exp02 的 C/D 组可以做低成本方向性复现，但不能据此宣称 coverage 普遍优于 difficulty。
