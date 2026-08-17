# Exp02 执行 Agent 任务书

## 固定约束

你可以申请 GPU、安装依赖和下载数据，但不得改变 `config.json` 中的数据集、候选池大小、选中数量、模型、seed、embedding model、聚类数和混合比例。数据集不可访问时，先记录失败；只有替代数据集也具备任务族/来源标签时才可替换。

## 执行步骤

1. 创建隔离环境，保存 Git commit、Python、CUDA、GPU 和依赖版本。
2. 下载 `allenai/tulu-3-sft-mixture`，抽取候选池 10,000 条，统一为 `id/instruction/input/output/source/task_family` 字段。
3. 按 seed=1701 固定 train/dev/test；所有选择分数只在 train 候选池上计算。
4. 计算 quality proxy、base model difficulty 和 embedding coverage；保存每条样本的原始分数。
5. 生成 A/B/C/D/E 五个 2,000 条子集和 F1/F2/F3 三个混合子集。
6. 计算选择后的来源、任务族、质量、难度、coverage、重复率和 token 统计。
7. 用 TinyStories-33M 对各子集做相同预算的 instruction tuning，使用 seed=1701/1702/1703。
8. 在四类固定评测 split 上评测，并按任务族单独汇报。
9. 生成结果文件和 `selection_report.md`，严格区分数据层和模型层结论。

## 验收条件

- 每个组恰好 2,000 条，除非记录了数据不足原因；
- 所有组使用相同训练预算；
- 分数计算没有使用 test 标签；
- 选择后保留了原始 ID，可追溯回候选池；
- 报告同时包含 random baseline；
- 报告包含均值、标准差、任务族分数和覆盖统计；
- 不得因为某种方法暂时落后而临时调参；
- 不得把 proxy quality 当成人工真实质量。

## 最终返回文件

```text
results/exp02/selection_scores.parquet
results/exp02/selected_ids.json
results/exp02/mixture_assignments.json
results/exp02/data_coverage.csv
results/exp02/model_metrics.csv
results/exp02/evaluation_by_split.csv
results/exp02/selection_report.md
results/exp02/environment.txt
results/exp02/run.log
```
