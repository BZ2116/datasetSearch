# Exp01：过滤与去重的收益验证

## 目的

区分过滤、exact dedup 与 near dedup 的独立收益，不把“清洗后数据更好”作为未经验证的前提。本实验使用 1,000–10,000 条 Dolma 或 FineWeb 小规模文本，不复现完整大规模预训练。

## 四组对照

| 组别 | 处理 | 目的 |
|---|---|---|
| A | 原始数据 | 基线 |
| B | 语言、长度、格式、安全过滤 | 测量过滤收益 |
| C | B + exact dedup | 测量完全重复删除收益 |
| D | C + near dedup | 测量近重复删除的额外收益和覆盖损失 |

四组必须使用同一候选池、同一数据划分规则和随机种子。模型比较时固定模型、训练步数、batch size、token 预算和评测集；如果各组数据量不同，额外报告自然规模和等 token 预算两种结果。

## 处理规则

### 过滤

- 记录目标语言、语言识别器和版本；
- 删除空文档和明显过短文档，超长文档记录截断策略；
- 规范化 Unicode、空白和换行，记录 HTML 残留和控制字符；
- 使用可复现的安全/PII 规则，保存每条删除原因；
- 过滤阈值见 [`configs/filter.yaml`](configs/filter.yaml)。

### Exact dedup

在规范化文本上计算 SHA-256，重复文本归入同一 `dedup_group_id`，默认保留最长文档，并记录被删除文档的来源和 ID。

### Near dedup

使用 MinHash/LSH 或固定 n-gram Jaccard 相似度。必须记录 n-gram 设置、hash 参数、相似度阈值、随机种子、簇大小和保留规则。近重复簇需要人工抽检，防止误删有效变体。参数见 [`configs/dedup.yaml`](configs/dedup.yaml)。

## 指标

### 数据层

- 文档数和保留率；
- exact/near 重复率；
- 平均长度和长度分位数；
- 来源、语言、主题或任务分布；
- 过滤原因计数；
- train/dev/test n-gram overlap；
- 去重簇大小分布；
- 被删样本抽检中的误删率和漏删率。

### 模型层

- 小型语言模型 validation loss / perplexity；
- WikiText-103 或 LAMBADA 轻量评测；
- 训练 token、步数、时间和不同随机种子的均值/标准差。

## 运行流程

```text
固定原始数据和 split
→ 生成 A/B/C/D 四个版本
→ 统计保留、重复、覆盖和污染
→ 抽检过滤与去重失败样本
→ 检查 train/dev/test overlap
→ 固定预算训练小模型
→ 报告验证 loss 和轻量下游指标
→ 分析收益与覆盖损失
```

先完成数据层统计，再决定是否训练模型；如果规则明显误删，应先改配置。

## 结果解释

- B 优于 A：只说明当前过滤配置有效；
- C 优于 B：说明 exact dedup 可能减少重复或污染，需检查 token 和覆盖变化；
- D 低于 C：可能 near dedup 过强或误删有效变体；
- D 高于 C：需排除数据量、采样和训练预算差异；
- loss 下降但下游变差：检查过拟合、污染和覆盖损失。

## Agent 执行包

将本目录整体交给执行 Agent。Agent 读取 [`AGENT_TASK.md`](AGENT_TASK.md)，自主申请 GPU、安装依赖、下载 FineWeb 和 TinyStories-33M，运行数据处理与训练，并将完整结果写入 `results/run/`。具体固定参数见 [`config.json`](config.json)，单入口处理程序是 [`run_experiment.py`](run_experiment.py)。

本机只验证代码语法和核心函数，不填写虚构的保留率或模型分数；真实结果必须由执行 Agent 产生。
