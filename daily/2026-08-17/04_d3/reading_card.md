# 论文阅读卡片：D3

## 基本信息

- **论文：** D3: Diversity, Difficulty, and Dependability-Aware Data Selection for Sample-Efficient LLM Instruction Tuning
- **作者 / 年份：** Jia Zhang 等 / 2025
- **状态：** IJCAI 2025
- **链接：** https://www.ijcai.org/proceedings/2025/928
- **类型：** 指令数据选择

## 一句话理解

> 有价值的 instruction 数据需要同时考虑多样性、难度和可靠性，而不是只按单一分数排序。

## 数据池与处理

在多个公开 instruction 数据集和 Taobao Live 实际数据上进行选择实验。

## 方法与 baseline

用 diversity、uncertainty-based difficulty 和外部 LLM dependability 评分，构造 weighted coreset，并进行多轮迭代选择；与单指标或其他选择方法比较。

## 主要结论

论文报告使用少于全量 10% 的数据也能获得有竞争力或更好的 instruction tuning 表现。

## 对本项目的启发

Exp02 的 E 组对应质量+coverage 的简化版本，C/D 分别对应 difficulty/coverage。dependability 暂用规则或已有标签代理，不能假装等同于 D3 的外部 LLM 评分。
