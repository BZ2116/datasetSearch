# Exp04 执行 Agent 任务书

## 固定约束

先读取本目录 README 和 config。可以申请 GPU、安装依赖，但不得更换 QNLI、BERT、删除比例、seed、目标指标或 baseline。任何方法失败都要保留日志并标记失败。

## 步骤

1. 下载 GLUE QNLI，记录 revision、字段映射和 hash。
2. 训练 Full baseline，保存 checkpoint、dev loss 和 accuracy。
3. 运行 TRAK；若失败，运行 embedding similarity、per-example loss/gradient、random，并明确记录 TRAK failure。
4. 对每种排序生成 top-k、bottom-k 和 random 删除集合，保存样本 ID。
5. 对 Full、各删除组和 Top-k select 重新训练 3 个 seed；训练预算完全一致。
6. 计算目标 dev 指标、置信区间、归因排序相关性和删除后性能变化。
7. 输出 `attribution_report.md`，区分 influence attribution、source attribution 和实验实际覆盖范围。

## 必须返回

```text
results/exp04/config_resolved.json
results/exp04/environment.txt
results/exp04/attribution_scores.parquet
results/exp04/selected_or_removed_ids.json
results/exp04/model_metrics.csv
results/exp04/counterfactual_metrics.csv
results/exp04/attribution_report.md
results/exp04/run.log
```

没有 counterfactual 重训结果时，不得生成“归因有效”结论。
