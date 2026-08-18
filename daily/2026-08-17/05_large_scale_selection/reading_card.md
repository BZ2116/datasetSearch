# 论文阅读卡片：Large-Scale Data Selection

## 基本信息

- **论文：** Large-Scale Data Selection for Instruction Tuning
- **作者 / 年份：** Hamish Ivison 等 / 2025
- **状态：** 前沿补充，计划中标记为待确认
- **链接：** https://arxiv.org/abs/2503.01807
- **类型：** 指令数据选择

## 一句话理解

> 小规模数据池上有效的选择方法，放大到百万级候选池后未必超过随机，表示空间选择反而可能更稳定。

## 数据池与处理

最多从 5.8M 样本中选择 2.5M 样本，并在 7 个任务上评测不同选择方法。

## Baseline 与主要结论

比较 random、复杂自动选择方法和 representation-based RDS+。论文报告若干复杂方法在大规模设置下不如 random，而 RDS+ 在测试设置中更稳定且计算效率更高。

## 对本项目的启发

Exp02 必须保留 random baseline，并报告选择方法的计算成本；小规模实验只能验证趋势，不能证明方法在大池子上仍然成立。
