# 2026-08-20 日总结：数据归因与模型能力支撑

## 一、今日完成

完成 TRAK、FreeShap、Source-Aware Training、In-Run Data Shapley 和 DataDignity 的研读，并建立 Exp04 归因实验包。

新增阅读卡片：

- `01_trak/reading_card.md`
- `02_freeshap/reading_card.md`
- `03_source_aware/reading_card.md`
- `04_in_run_shapley/reading_card.md`
- `05_datadignity/reading_card.md`

新增材料：

- `benchmarks/attribution_method_matrix.md`
- `experiments/exp04_attribution/README.md`
- `experiments/exp04_attribution/AGENT_TASK.md`
- `experiments/exp04_attribution/config.json`

## 二、关键区分

归因问题分为两类：

1. **影响归因：** 哪些训练样本改变了模型预测或验证集表现？TRAK、FreeShap、In-Run Data Shapley 属于这一类。
2. **来源归因：** 模型回答中的知识由哪个文档支持？Source-Aware Training 和 DataDignity 属于这一类。

来源归因不能替代影响归因，回答引用了某文档，也不等于该文档对模型参数有最大因果影响。

## 三、Exp04 实验逻辑

```text
归因排序
→ 删除 top-k / bottom-k / random
→ 重新训练同一模型
→ 比较目标 dev loss / accuracy
```

固定 QNLI、BERT、训练预算和三个随机种子。优先运行 TRAK；如果环境不稳定，先完成 embedding、loss/gradient 和 random baseline，并保留 TRAK 失败记录。

## 四、结论口径

归因分数本身不是证据。只有归因排序能够预测 counterfactual 删除后的稳定性能变化，才支持“该方法可用于数据选择或有害数据识别”。

## 五、下一步

由执行 Agent 拉取 Exp04，完成 QNLI 训练、归因排序、删除/重训和报告；本日只完成设计和文档，没有虚构归因结果。
