# 论文阅读卡片：Self-Instruct

## 基本信息

- **论文：** Self-Instruct: Aligning Language Models with Self-Generated Instructions
- **作者 / 年份：** Yizhong Wang 等 / ACL 2023
- **链接：** https://aclanthology.org/2023.acl-long.754/
- **类型：** 指令合成 / 自训练

## 一句话理解

> 用少量 seed instructions 引导模型生成 instruction、input 和 output，再过滤无效与相似样本，用生成数据进行指令微调。

## 核心流程

```text
seed instructions
→ generate new instruction/input/output
→ remove invalid or similar samples
→ fine-tune base model
→ evaluate on seen/unseen tasks
```

## 主要结论

论文报告 Self-Instruct 能显著提升 GPT-3 的 instruction following，并改善 Super-NaturalInstructions 和专家新任务上的表现。

## 风险

生成模型可能复制 seed 模板、生成错误答案、偏向常见任务，且过滤“相似”不能证明真正新增了能力。

## 对本项目的启发

只统计生成数量不够，必须记录有效率、重复率、标签一致率和未见任务泛化。Exp03 将把 Self-Instruct 作为任务生成/改写基线。
