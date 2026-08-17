# 数据选择与混合策略矩阵

| 方法 | 选择信号 | 优点 | 主要风险 | 本实验对应组 |
|---|---|---|---|---|
| Random | 无 | 最可靠的低成本基线 | 可能保留噪声，覆盖波动 | A |
| Quality | 规则/模型质量分 | 降低明显低质样本 | proxy 偏差，可能牺牲长尾 | B |
| Difficulty | base model loss/perplexity | 关注模型当前不会的样本 | 选出不可学、过难或模板噪声 | C |
| Coverage | embedding 簇/距离 | 保留任务和表达多样性 | embedding 偏差，参数敏感 | D |
| Quality + Coverage | 质量筛选后做覆盖选择 | 兼顾可靠性与多样性 | 组合参数更多 | E |
| Mixture | 来源/任务族配方 | 控制能力结构和专门化 | 总分掩盖任务族退化 | F1/F2/F3 |

## 研究判断

数据选择至少包含两个独立维度：

```text
样本是否值得保留（quality / dependability）
样本是否提供新覆盖（coverage / diversity）
```

Difficulty 是模型相关信号，不应直接当作数据价值。困难可能来自真正的推理挑战，也可能来自标签错误、表达异常或任务不可解。因此 difficulty 组必须配合正确性和可学习性检查。

近期大规模 instruction selection 研究报告，复杂选择方法在大候选池上可能不如随机，而 representation-based selection 更稳定；这说明选择方法必须进行规模、随机基线和任务族分解验证，不能只在小数据集上展示 top-k 分数。

## 参考资料

- [DataComp-LM 官方页面](https://www.datacomp.ai/dclm/)
- [DataComp-LM 论文](https://arxiv.org/abs/2406.11794)
- [Large-Scale Data Selection for Instruction Tuning](https://arxiv.org/abs/2503.01807)
- [Rethinking Data Selection: The Importance of Coverage over Difficulty](https://openreview.net/forum?id=qImiy98UhN)
- [D3: Diversity, Difficulty, and Dependability-Aware Data Selection](https://www.ijcai.org/proceedings/2025/928)
