# Exp01 执行 Agent 任务书

你是本实验的唯一执行者。可以申请 GPU、安装依赖、下载公开数据集和模型，但不得改变 `config.json` 中的实验组、阈值、数据划分、模型名称、训练 token 预算或评测集。若资源不足，记录失败并停止，不要静默替换变量。

## 执行步骤

1. 读取本文件、`README.md`、`config.json` 和 `requirements.txt`。
2. 创建隔离环境，记录 Python、CUDA、GPU、Git commit 和依赖版本到 `results/run/environment.txt`。
3. 下载 `HuggingFaceFW/fineweb` 的 `sample-10BT`，streaming 抽取 5,000 条；保存原始 JSONL、数据集版本、URL 和 hash。
4. 固定 seed=1601，先划分 80/10/10，再生成 A/B/C/D 四个版本。处理实现调用 `run_experiment.py`。
5. 运行数据统计、污染检查和抽检。每个处理步骤抽检至少 20 条删除样本；near dedup 额外检查最高、中位数和接近 0.85 阈值的样本对。
6. 使用 `roneneldan/TinyStories-33M` 和同一 tokenizer，在四组上进行等 token 训练；总训练 token=10M，seed=1601/1602/1603。记录 validation loss、perplexity、训练时间和显存。
7. 使用固定的 WikiText-2 raw test split 评测，每组使用同一评测代码和参数。
8. 生成完整报告并运行验收检查。

## 运行命令

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r experiments/exp01_filter_dedup/requirements.txt
python experiments/exp01_filter_dedup/run_experiment.py --input results/run/raw.jsonl --output results/run/processed
```

如果使用 streaming 数据下载，需要先将数据保存为 `results/run/raw.jsonl`，字段至少包含 `id` 和 `text`。Agent 可编写下载适配器，但必须保存源码或命令及下载日志。

## 必须返回的文件

```text
results/run/final_report.md
results/run/environment.txt
results/run/raw.jsonl.sha256
results/run/processed/A.jsonl
results/run/processed/B.jsonl
results/run/processed/C.jsonl
results/run/processed/D.jsonl
results/run/processed/data_statistics.csv
results/run/processed/filter_decisions.jsonl
results/run/processed/exact_groups.jsonl
results/run/processed/near_groups.jsonl
results/run/model_metrics.csv
results/run/inspection_samples.md
results/run/run.log
```

报告必须分别回答过滤、exact dedup、near dedup 的收益和代价，并明确哪些结论是数据层证据、哪些结论是模型层证据。没有完成的阶段必须写明失败原因，不能用估计值补齐。
