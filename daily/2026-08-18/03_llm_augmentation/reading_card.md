# 论文阅读卡片：LLM 数据增强综述

## 基本信息

- **论文：** Data Augmentation using Large Language Models: Data Perspectives, Learning Paradigms and Challenges
- **年份 / 状态：** 2024 / arXiv 综述
- **链接：** https://arxiv.org/abs/2403.02990
- **类型：** Survey

## Taxonomy

本文作为分类参考，将增强抽象为：

- 语言/表述变化；
- 实体、数值和实例变化；
- instruction/task 生成；
- 难度和约束演化；
- 多任务或多步结构组合；
- reasoning、tool-use 和 trajectory 增强；
- 答案、过程和 verifier 联合增强。

## 核心启发

增强操作改变的对象不同，收益和风险也不同。应分别评估表达泛化、任务覆盖、难度提升和过程可验证性。

## 局限

综述汇总的方法实验设置不统一，不能直接推出某种增强一定更好；本项目只使用其 taxonomy，不把综述中的跨论文分数横向比较。
