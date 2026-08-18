# 论文阅读卡片：DataDignity

## 基本信息

- **论文：** DataDignity: Training Data Attribution for Large Language Models
- **状态：** 2026 前沿/待确认
- **链接：** https://arxiv.org/abs/2605.05687
- **类型：** provenance benchmark / 来源归因

## 归因对象

给定 prompt、模型回答和候选语料，找出真正支持回答的来源文档。

## Benchmark 设计

FakeWiki 使用来源保持改写、相似但缺少关键事实的 anti-document，以及 jailbreak-style query，避免 lexical retrieval 假装完成来源归因。

## 主要启发

来源归因必须区分“主题相似”与“事实支持”；评测应包含 hard negatives、改写和查询变换。

## 边界

这是回答到来源的 provenance 任务，不等同于训练样本 influence；本轮 Exp04 不直接复现 FakeWiki。
