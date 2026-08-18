# 论文阅读卡片：OSWorld

## 基本信息

- **论文：** OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments
- **状态：** NeurIPS 2024
- **链接：** https://papers.nips.cc/paper_files/paper/2024/hash/5d413e48f84dc61244b6be550f1cd8f5-Abstract-Datasets_and_Benchmarks_Track.html
- **类型：** 可执行多模态 Agent benchmark

## 核心贡献

构造 369 个跨网页、桌面应用、文件 I/O 和多应用工作流的任务，每个任务包含环境设置和 execution-based evaluation。

## 对合成数据验证的启发

评测应保存环境状态、动作过程和最终状态；多步任务不能只看最后一段自然语言答案。对于 Exp03，reasoning 增强应至少保存每步计算关系和 verifier 结果。

## 局限

OSWorld 面向真实计算机环境，成本和复现复杂度高，本轮只借鉴过程反馈与执行验证。
