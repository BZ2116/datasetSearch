# 数据归因方法矩阵

| 工作 | 归因对象 | 模型信息 | 主要验证 | 可支持的结论 | 本轮边界 |
|---|---|---|---|---|---|
| TRAK | 样本对预测/验证目标的影响 | 梯度、checkpoint | LDS、删除/重训 | 归因排序是否预测反事实性能变化 | 只做 QNLI 小模型 |
| FreeShap | helpful/harmful 样本贡献 | 模型输出/表示，不要求 fine-tuning | 删除、选择、错标检测 | 哪些样本对目标预测有益/有害 | 先做 QNLI/SST-2 |
| Source-Aware Training | 知识支持来源 | 训练时 source ID 和模型 | citation faithfulness、perplexity | 回答应引用哪个来源 | 不与 influence 混合 |
| In-Run Data Shapley | 单次训练中数据累计价值 | 训练过程更新和效用函数 | 与重训/目标效用比较 | 特定训练运行中的数据价值 | 本轮不实现 |
| DataDignity | 回答支持文档的 provenance | 候选文档和回答，支持开放模型 | Recall@k、hard negatives、改写/jailbreak | 是否找到真实支持来源 | 本轮只记录方法边界 |

## 统一验证原则

归因分数本身不是证据。必须进行 counterfactual：

```text
归因排序
→ 删除 top-k / bottom-k / random
→ 重新训练或继续训练
→ 比较目标 loss / accuracy
```

如果 top-k 删除没有造成预期变化，或 bottom-k 删除反而提升目标性能，说明归因排序需要重新校准，不能直接用于数据选择。
