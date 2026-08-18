# 论文阅读卡片：WebArena

## 基本信息

- **论文：** WebArena: A Realistic Web Environment for Building Autonomous Agents
- **状态：** ICLR 2024
- **链接：** https://proceedings.iclr.cc/paper_files/paper/2024/hash/4410c0711e9154a7a2d26f9b3816d1ef-Abstract-Conference.html
- **类型：** 可执行 Agent benchmark

## 核心贡献

提供包含电商、论坛、协作开发和内容管理网站的可复现环境，并用功能正确性 evaluator 判断长任务是否成功。

## 对合成数据验证的启发

最终成功状态比“回答看起来合理”更可靠；长任务应记录 end-to-end success、步骤错误和恢复情况。Exp03 当前是 GSM8K，迁移原则是用程序 verifier 验证最终状态，而不是只用文本相似度。

## 局限

WebArena 的环境搭建成本高，不适合直接作为本轮数学增强实验；本轮只迁移执行式 evaluator 的思想。
