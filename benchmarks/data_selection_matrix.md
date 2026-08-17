# 数据选择与混合策略矩阵

## 一、论文级对比

| 工作 | 状态 | 数据池/规模 | 选择信号或配比方法 | Baseline/控制变量 | 主要指标与结论 | Exp02 可验证内容 |
|---|---|---|---|---|---|---|
| DataComp-LM | NeurIPS 2024 | Common Crawl，DCLM pool 约 240T tokens | filtering、dedup、source curation、mixing | 固定 OpenLM 训练 recipe、模型规模和评测协议；53 个下游任务 | 数据构建本身可作为 benchmark 变量，DCLM-Baseline 在较少训练 token 下取得有竞争力的下游表现 | 固定 TinyStories-33M、样本数、token 和评测，比较选择策略 |
| DS² | ICLR 2025 | instruction tuning 数据；论文报告 300k 全量与约 3.3% 子集 | LLM rating 经 score transition matrix 校正，并加入 diversity-aware selection | 与随机、原始 LLM rating、人工/已有 curated 数据比较；固定微调模型和预算 | 校正评分并加入多样性后，小子集可超过大而冗余的数据集；LLM rating 存在系统偏差 | B 的 quality proxy、D 的 coverage、E 的联合选择；不能复现其完整 score transition matrix |
| Data Mixture Optimization | NeurIPS 2025 | SlimPajama 配比模拟器，基于 472 次预训练运行 | 多保真、多模型规模 Bayesian optimization，联合选择 mixture、model scale、steps | 与 random search 和 multi-fidelity BO 比较；显式建模不确定性 | 在模拟实验中用低成本实验指导高成本配比搜索，报告相对搜索加速 | 只做固定预算下的 3 个离散配方，不验证完整 BO 或跨规模外推 |
| D3 | IJCAI 2025 | 多个公开 instruction 数据集和 Taobao Live 实际数据 | diversity、difficulty、dependability 三维评分，迭代 weighted coreset selection | 与单一质量/难度选择和其他自动选择方法比较 | 少于全量 10% 的数据取得有竞争力或更好的 instruction tuning 效果 | C/D/E 分别近似 difficulty、coverage、quality+coverage；dependability 只做规则代理 |
| Large-Scale Data Selection for Instruction Tuning | 2025，前沿补充 | 最多 5.8M 候选池，最多选择 2.5M 样本，7 个任务 | representation-based、quality/importance 等选择方法 | 大规模池和选择预算下与 random 比较，固定模型和任务 | 部分复杂方法在大规模设置下不如 random；RDS+ 的表示选择更稳定且更省计算 | D 的 representation/coverage 与 A random 的直接比较；不复现其百万级规模 |
| Rethinking Data Selection | ICLR 2026 workshop，前沿/待确认 | generative fine-tuning，Llama-3-8B、OLMo2-7B 案例 | difficulty score 与 clustering-based coverage | 比较 difficulty、random、coverage，固定生成任务和模型 | 生成任务中 difficulty 选择可能落后 random；coverage 选择在多个任务上达到或超过 random | C 与 D 的核心直接复现；只能验证方向性，不能声称普遍规律 |

## 二、方法矩阵

| 方法 | 选择信号 | 优点 | 主要风险 | 本实验对应组 |
|---|---|---|---|---|
| Random | 无 | 低成本、最稳妥的基线 | 可能保留噪声，覆盖有随机波动 | A |
| Quality | 规则或模型质量分 | 降低明显低质样本 | proxy 偏差，可能损失长尾 | B |
| Difficulty | base model loss/perplexity | 关注模型当前不熟悉的样本 | 过难、错误或不可学样本会被高估 | C |
| Coverage | embedding 簇或距离 | 保留任务、表达和实体多样性 | embedding 偏差，聚类参数敏感 | D |
| Quality + Coverage | 质量筛选后做覆盖选择 | 兼顾可靠性和多样性 | 阈值和权重更多 | E |
| Mixture | 来源/任务族配方 | 控制能力结构和专门化 | 总分掩盖局部任务退化 | F |

## 三、对本项目的研究判断

数据价值至少包含两个正交维度：

```text
样本是否值得保留：quality / dependability
样本是否提供新信息：coverage / diversity
```

Difficulty 是模型相关信号，不等于数据价值。高 perplexity 可能意味着真正的推理挑战，也可能意味着标签错误、格式异常或任务不可解。因而 Exp02 必须同时报告 difficulty 分布、质量代理和任务覆盖，不能只报告“选出的样本更难”。

数据混合也不能只看总比例。每个配方必须报告来源、任务族、能力标签和未见任务族表现，否则一个平均分无法说明配方究竟提升了什么能力。

## 四、哪些结论可以由 Exp02 验证

可以验证：

- 在固定样本数和训练预算下，coverage 是否优于 difficulty；
- quality+coverage 是否比单一 quality 或 coverage 更稳定；
- 复杂选择方法是否超过 random；
- 不同任务族混合比例是否造成能力专门化；
- 数据层 coverage 变化是否与未见任务族性能相关。

不能直接验证：

- DataComp-LM 的大规模 scaling law；
- DS² 的完整 rating transition matrix；
- Data Mixture Optimization 的 Bayesian optimization 和跨规模外推；
- D3 的完整 dependability 评分和迭代 coreset 算法；
- 论文在 7B/8B 模型上的绝对分数。

## 五、参考资料

- [DataComp-LM 官方页面](https://www.datacomp.ai/dclm/)
- [DataComp-LM 论文](https://arxiv.org/abs/2406.11794)
- [DS² / Improving Data Efficiency via Curating LLM-Driven Rating Systems](https://proceedings.iclr.cc/paper_files/paper/2025/hash/faa6144674bce872365874c576b4f56f-Abstract-Conference.html)
- [Data Mixture Optimization](https://papers.nips.cc/paper_files/paper/2025/hash/8e49d32f4668a41b013fbc1ed929c007-Abstract-Conference.html)
- [D3](https://www.ijcai.org/proceedings/2025/928)
- [Large-Scale Data Selection for Instruction Tuning](https://arxiv.org/abs/2503.01807)
- [Rethinking Data Selection](https://openreview.net/forum?id=qImiy98UhN)
