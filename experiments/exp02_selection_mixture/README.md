# Exp02：数据选择与混合策略

## 1. 实验目的

在同一个 instruction 数据池中，固定模型、样本预算、训练预算和评测集，只改变样本选择与任务族混合策略，回答：

1. 随机选择是否已经足够强；
2. 质量最高的数据是否一定最有用；
3. 难度最高的数据是否会损害覆盖和泛化；
4. embedding coverage 是否比 difficulty 更能保留任务多样性；
5. quality + coverage 是否能在质量和泛化之间取得平衡；
6. 来源/任务族混合比例如何影响已见和未见任务表现。

## 2. 数据与执行边界

本实验默认使用 `HuggingFaceH4/Bespoke-Stratos-17k` 作为可验证 reasoning 的候选池不合适，因此本实验固定使用带有 task/source 标签的 `allenai/tulu-3-sft-mixture` 的小规模子集；若该数据不可访问，Agent 必须选择一个字段包含 `instruction/input/output` 且能保留来源或任务族标签的公开 instruction 数据集，并在报告中记录替代理由。

目标候选池：10,000 条；每组选择：2,000 条；训练 token、模型和 seed 完全一致。

Agent 必须保存：数据集版本、字段映射、原始 hash、抽样 seed、许可证、来源/任务族字段缺失率。

## 3. 选择方法

| 组别 | 方法 | 具体规则 | 要验证的因素 |
|---|---|---|---|
| A | Random | 固定 seed 随机抽 2,000 条 | 基线 |
| B | Quality | 按 correctness/format/length/answerability 综合分排序，分层取样 | 质量 |
| C | Difficulty | 按固定 base model 的 perplexity 或 loss 取高难样本 | 难度 |
| D | Coverage | embedding 后 k-means/贪心 farthest-first，按簇覆盖取样 | 多样性/覆盖 |
| E | Quality + Coverage | 先保留质量前 70%，再用 coverage 选择 2,000 条 | 质量与覆盖联合 |
| F1/F2/F3 | Mixture | 固定总数，改变任务族比例 | 配方 |

质量、难度和 coverage 分数只能使用候选池的 train 部分计算，不能使用 dev/test 标签或评测答案。

## 4. 固定评分定义

### Quality

默认综合分：

```text
quality = 0.4 * correctness_proxy
        + 0.2 * format_score
        + 0.2 * answer_length_score
        + 0.2 * completeness_score
```

如果没有可靠的 correctness 标签，Agent 不得伪造；应改用可审计的规则代理，并在报告中标为 `proxy`。

### Difficulty

用同一个冻结 base model 对 instruction/output 计算 token-level loss 或 perplexity。选择高难样本时不能改变模型、tokenizer 或 loss 口径。

### Coverage

用同一个冻结 encoder 生成 instruction+output embedding，固定降维/聚类参数，采用簇覆盖或 farthest-first 选择。必须报告：簇数、每簇样本数、选中簇数、平均到最近选中样本距离。

## 5. 混合比例

按任务族标签把候选池分成至少三类：reasoning、knowledge/QA、instruction/dialogue。固定总量 2,000 条，比较：

| 配方 | reasoning | knowledge/QA | instruction/dialogue |
|---|---:|---:|---:|
| F1 balanced | 33% | 33% | 34% |
| F2 reasoning-heavy | 60% | 20% | 20% |
| F3 natural | 按候选池原始比例 | 按原始比例 | 按原始比例 |

若原始数据没有这些标签，Agent 必须使用公开标签或固定规则映射，并报告映射误差和 unknown 比例。

## 6. 模型与训练

- base model：`roneneldan/TinyStories-33M`；
- tokenizer：模型自带 tokenizer；
- 训练方式：监督微调 instruction/output；
- 每组样本数：2,000；
- 最大长度：512；
- 训练 token：每组相同；
- seed：1601、1602、1603；
- 优化器、学习率、batch size、训练步数：全组固定；
- Agent 可申请 GPU，但不得因 GPU 不同改变实验变量。

## 7. 评测分层

评测集必须从候选池之外构造或下载，并按以下维度记录：

- in-domain：与训练任务族相同但样本不同；
- unseen expression：相同能力、不同表达；
- unseen entity：相同任务模板、不同实体/数值；
- unseen task family：训练中没有出现的任务族；
- source/task-family split：按来源或任务族分组报告。

每一层报告准确率或任务适用的自动指标，不能只报告一个平均分。

## 8. 数据层指标

- 选中样本数和 token 数；
- 来源覆盖率；
- 任务族覆盖率；
- embedding 簇覆盖率；
- 平均/分位数质量分数；
- 平均/分位数 difficulty；
- exact/near duplicate rate；
- train/eval overlap；
- unknown label rate；
- 各组与候选池分布的 divergence。

## 9. 结果解释

- B 高于 A：质量代理在当前数据池有效，但不能证明质量分数具有普适性；
- C 高于 A 但 unseen 表现下降：难度选择可能牺牲覆盖；
- D 高于 C：支持 coverage 对泛化的价值，但要排除 embedding 参数影响；
- E 最稳定：说明质量筛选后再做覆盖选择可能优于单排序；
- F2 只提升 reasoning：说明混合比例带来能力专门化，不代表总体配方最优；
- 复杂选择不如随机：保留该结果，不通过调参直到胜出。

## 10. 执行 Agent 必须返回

```text
AGENT_TASK.md
config.json
selection_scores.parquet
selected_ids.json
mixture_assignments.json
data_coverage.csv
model_metrics.csv
evaluation_by_split.csv
selection_report.md
environment.txt
run.log
```

任何替代数据集、替代模型、跳过指标或失败阶段都必须在 `selection_report.md` 中明确记录。
