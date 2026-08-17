# 数据构建方法对比矩阵

## 1. 研究对象对比

| 工作 | 数据形态 | 候选来源 | 主要数据操作 | 评测控制 | 可迁移结论 |
|---|---|---|---|---|---|
| Dolma | 预训练文本 | Common Crawl、GitHub、Reddit、论文、书籍、Wikipedia 等 | parsing、filtering、deduplication、decontamination、mixing | 固定 OLMo 训练设置和下游任务 | 数据集应是来源、规则、版本和配方的集合 |
| FineWeb | 预训练网页文本 | 96 个 Common Crawl snapshots | HTML 抽取、语言/质量过滤、去重、教育性筛选 | 固定模型训练设置，比较处理 ablation | 每个处理决策都应可记录、可复现、可验证 |
| DataComp | 图文对 | Common Crawl CommonPool，另有 BYOD | 过滤、打分、去重、来源构建 | 固定模型、训练代码、预算和下游评测 | 数据构建可以成为受控 benchmark |

## 2. “数据文件”与“可复现构建流程”的区别

| 维度 | 只有数据文件 | 可复现构建流程 |
|---|---|---|
| 来源 | 通常只有最终文件 | 原始来源、抓取版本、许可和来源 ID |
| 处理 | 无法知道删掉了什么 | 规则、阈值、顺序和失败统计均可追踪 |
| 版本 | 文件名或日期 | schema 版本、代码版本、配置 hash、数据版本 |
| 质量 | 只能抽样检查结果 | 可比较不同过滤/去重策略的收益和代价 |
| 复现 | 重新下载后可能不同 | 固定输入快照、配置、随机种子和环境 |
| 评测 | 只报告最终模型分数 | 固定模型、预算、split 和 benchmark，支持 ablation |
| 归因 | 难以追溯样本来源 | 可从样本追溯到文档、处理步骤和数据配方 |

## 3. 数据生命周期图

```mermaid
flowchart LR
    A[定义目标能力] --> B[候选数据池]
    B --> C[记录 provenance]
    C --> D[解析与 schema 统一]
    D --> E[质量/安全/隐私过滤]
    E --> F[Exact 与 near dedup]
    F --> G[污染控制与覆盖分析]
    G --> H[选择与混合]
    H --> I[增强与合成]
    I --> J[自动验证与人工抽检]
    J --> K[固定预算训练与评测]
    K --> L[归因与失败分析]
    L --> H
```

## 4. 本项目的判断

高质量数据集不是“保留率最高”或“模型总分最高”的数据集，而是能够在目标能力上取得可重复收益，同时具备正确性、覆盖度、可追溯性和安全边界的数据构建流程。

后续实验必须至少保留以下对照：原始数据、规则过滤、过滤+exact dedup、过滤+near dedup，以及在固定训练预算下的下游评测。

## 5. 参考来源

- Dolma：`daily/2026-08-14/02_dolma/reading_card.md`
- [FineWeb 论文](https://arxiv.org/abs/2406.17557)
- [DataComp 论文](https://arxiv.org/abs/2304.14108)
- [DataComp-LM 官方页面](https://www.datacomp.ai/dclm/)
