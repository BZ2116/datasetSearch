# 论文阅读卡片：DS²

## 基本信息

- **论文：** Improving Data Efficiency via Curating LLM-Driven Rating Systems
- **作者 / 年份：** Jinlong Pang 等 / 2025
- **状态：** ICLR 2025
- **链接：** https://proceedings.iclr.cc/paper_files/paper/2025/hash/faa6144674bce872365874c576b4f56f-Abstract-Conference.html
- **类型：** 指令数据选择

## 一句话理解

> LLM 评分并非无偏标签，需要建模评分错误，并在选择时同时考虑分数和多样性。

## 数据池与处理

面向 instruction tuning 数据，论文比较大规模数据与小规模 curated subset，并使用 LLM 对样本进行质量评分。

## 方法与控制

通过 score transition matrix 校正 LLM rating，再使用 diversity-aware selection 选择子集；与全量数据、原始评分选择和人工整理数据比较。

## 主要结论

论文报告约 3.3% 的 curated subset 可以超过 300k 样本的全量数据，说明低质量和冗余数据可能抵消规模收益。

## 局限与迁移

评分校正依赖评分模型和校准数据。Exp02 只实现 quality proxy + coverage，不声称复现完整 transition matrix；必须把 proxy 误差单独记录。
