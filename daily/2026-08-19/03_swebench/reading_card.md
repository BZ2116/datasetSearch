# 论文阅读卡片：SWE-bench

## 基本信息

- **论文：** SWE-bench: Can Language Models Resolve Real-World GitHub Issues?
- **状态：** ICLR 2024
- **链接：** https://proceedings.iclr.cc/paper_files/paper/2024/file/edac78c3e300629acfe6cbe9ca88fb84-Paper-Conference.pdf
- **类型：** 可执行代码 benchmark

## 核心贡献

从真实 GitHub issue 和对应 pull request 构造软件工程任务，要求模型修改代码，并用仓库测试判断是否解决问题。

## 对合成数据验证的启发

verifier 必须独立于生成过程，并能区分“输出像正确答案”和“实际通过测试”。Exp03 的 GSM8K 数值 verifier、答案一致率和失败分类遵循同一原则。

## 局限

代码测试可能存在环境依赖和测试覆盖不足；因此执行结果仍需记录测试版本、环境和未覆盖错误。
