# 论文阅读卡片：DataComp-LM

## 基本信息

- **论文：** DataComp-LM: In Search of the Next Generation of Training Sets for Language Models
- **年份 / 状态：** 2024 / NeurIPS 2024
- **链接：** https://arxiv.org/abs/2406.11794
- **类型：** Benchmark / 数据选择 / 预训练数据

## 一句话理解

> 固定语言模型训练流程和评测协议，只改变训练数据，把数据构建变成可控 benchmark。

## 数据池与处理

使用 Common Crawl 构建约 240T tokens 的候选池，支持 filtering、dedup、数据来源构建和 mixing 等策略。

## Baseline 与控制变量

固定 OpenLM 训练 recipe、模型规模、计算预算和评测协议；使用 53 个下游评测比较数据构建策略。

## 主要结论

数据设计会影响模型性能和计算效率，DCLM-Baseline 说明经过处理的数据可以用较少训练 token 获得有竞争力的结果。

## 对本项目的启发

Exp02 应固定模型、样本数、训练 token 和评测集，只改变选择方法；但不能把小规模 instruction 实验的结果外推为 DCLM 的大规模结论。
