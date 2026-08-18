# 论文阅读卡片：Natural Instructions

## 基本信息

- **论文：** Cross-Task Generalization via Natural Language Crowdsourcing Instructions
- **作者 / 年份：** Mishra 等 / ACL 2022
- **链接：** https://github.com/allenai/natural-instructions
- **类型：** 多任务 instruction benchmark

## 一句话理解

> 将任务定义、输入输出格式和示例组织成自然语言 instruction，研究模型跨任务族的泛化。

## 核心数据结构

每个任务包含任务说明、输入/输出字段、正例，数据按任务而不是只按样本组织，支持 unseen task 的评测。

## 主要启发

增强数据的任务多样性不能只用样本条数衡量，应记录任务模板、任务族和任务定义是否真正新增。

## 风险

不同任务模板的标签定义可能不一致；随机切分样本会把同一任务泄漏到 train/test，夸大跨任务泛化。

## 对本项目的启发

Exp03 将按 task family 划分评测集，区分未见表达、未见实体和未见任务族，而不是只做随机样本切分。
