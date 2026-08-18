# 论文阅读卡片：FLAMES

## 基本信息

- **论文：** FLAMES: Improving LLM Math Reasoning via a Fine-Grained Analysis of the Data Synthesis Pipeline
- **状态：** 前沿/待确认
- **链接：** https://arxiv.org/abs/2508.16514
- **类型：** 数学 reasoning 合成数据分析

## 核心贡献

系统分析数学 reasoning 数据合成流程中的多个策略和质量因素，强调生成问题、推理过程、最终答案和训练收益之间不能混为一谈。

## 对 Exp03 的启发

合成样本需要逐层检查：问题是否有效、推理是否成立、答案是否一致、verifier 是否通过，以及最终是否改善未见分布表现。

## 主要风险

只验证最终答案可能漏掉错误 reasoning；只看 verifier 通过率也不能证明模型学到了新能力，因此必须同时报告过程质量和模型泛化。
