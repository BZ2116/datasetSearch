# 论文阅读卡片：FLAN Collection

## 基本信息

- **论文：** The Flan Collection: Designing Data and Methods for Effective Instruction Tuning
- **年份：** 2023
- **链接：** https://arxiv.org/abs/2301.13688
- **类型：** 任务混合 / 指令模板 / 泛化

## 一句话理解

> 将多个数据集转换为统一 instruction 格式，使用 zero-shot、few-shot、chain-of-thought 等模板并按配方混合训练。

## 核心贡献

FLAN 说明任务数量、模板多样性、任务配比和推理格式都会影响 instruction tuning 的泛化，不能把多任务数据简单拼接。

## 风险

任务混合比例可能导致强势任务压制小任务；chain-of-thought 数据可能包含错误过程或评测污染；不同模板之间也可能重复。

## 对本项目的启发

Exp03 保留固定总样本数，用原始样本复制组作为“只增加数量”的 baseline，并单独比较语言改写、难度增强和可验证 reasoning。
