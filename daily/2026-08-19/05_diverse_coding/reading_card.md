# 论文阅读卡片：Diverse Synthetic Coding Tasks

## 基本信息

- **论文：** Increasing LLM Coding Capabilities through Diverse Synthetic Coding Tasks
- **状态：** 前沿/待确认
- **类型：** 合成代码任务 / 数据多样性

## 核心问题

研究合成代码任务的多样性是否能提升代码模型能力，而不是只重复相似的代码模板。

## 对本项目的启发

代码增强必须用单元测试、pass@1 和未见函数描述评估；数据层要记录 API、算法、输入约束和测试覆盖的变化。Exp03 当前选择 GSM8K，因此只迁移“多样性必须对应未见能力”的原则。

## 局限

代码任务的可执行测试不能直接替代数学任务 verifier，不能把 pass rate 与 GSM8K accuracy 混用。
