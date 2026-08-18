# 论文阅读卡片：Evol-Instruct

## 基本信息

- **论文：** WizardLM: Empowering Large Language Models to Follow Complex Instructions
- **作者 / 年份：** Can Xu 等 / ICLR 2024
- **链接：** https://www.microsoft.com/en-us/research/publication/wizardlm-empowering-large-language-models-to-follow-complex-instructions/
- **类型：** 难度演化 / 合成 instruction

## 一句话理解

> 通过逐步重写 instruction，增加约束、推理步骤和问题复杂度，再用生成数据微调模型。

## 典型操作

- 增加约束；
- 增加推理步骤；
- 引入更多概念或领域；
- 将简单任务组合为复杂任务；
- 改变格式或目标要求。

## 主要风险

难度增加可能导致任务不可解、答案失效、约束冲突和错误轨迹放大。复杂度本身不是有效训练信号。

## 对本项目的启发

Exp03 的“增加约束”和“多步组合”必须同时通过 GSM8K 答案验证，并记录可解率和标签一致率。
