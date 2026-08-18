# Exp03 执行 Agent 任务书

你是执行者，不是实验设计者。先读取本目录的 `README.md`、`config.json`、`evaluation.md` 和固定 prompt 文件。不得自行更换模型、prompt、数据划分、评测集或训练参数。

## 固定约束

使用 `openai/gsm8k` train split 固定抽取 100 条 seed，生成 6 类增强和 1 个重复 baseline。可以申请 GPU、安装依赖，但生成模型、版本、prompt、temperature、重试上限、组定义、seed 数量、最终样本数、验证规则和训练预算均已固定，不得更改。

## 执行步骤

1. 创建环境，记录 Git commit、Python、CUDA、GPU 和依赖版本。入口命令为 `python exp03_runner.py --stage init --results-dir results`；依赖安装使用 `pip install -r requirements.txt`。
2. 下载 GSM8K，按题型/答案格式分层抽取 100 条，保存 `seed.jsonl` 和 hash。
3. 为每条 seed 生成 rewrite、entity_numeric、constraint、counterfactual、composition、verified_reasoning 六类候选；每类先生成 2–3 倍目标数量。
4. 对所有候选运行 GSM8K 数值答案 verifier；记录通过、失败和无法解析的原因。
5. 去除 parent 内重复、跨 parent 近重复和与 eval 的污染；生成每组恰好 1,000 条训练样本。若不足，报告不足，不使用未经验证样本补齐。
6. 用同一 TinyStories-33M、同一 tokenizer、三个 seed 和相同 token budget 训练 A–G。
7. 按四类评测 split 汇报 accuracy、verifier pass rate、任务覆盖、重复率和错误类型。
8. 生成 `augmentation_report.md`，分别回答语言、实例、难度、反事实、结构和 verifier 是否带来未见分布收益。

## 必须返回

```text
results/exp03/seed.jsonl
results/exp03/augmented_candidates.jsonl
results/exp03/failed_generation.jsonl
results/exp03/accepted_train.jsonl
results/exp03/failed_verification.jsonl
results/exp03/augmentation_statistics.csv
results/exp03/model_metrics.csv
results/exp03/evaluation_by_split.csv
results/exp03/augmentation_report.md
results/exp03/environment.txt
results/exp03/run.log
```

不能通过 verifier 的样本必须留在失败文件中；不能只返回成功样本而丢失失败记录。

统一入口负责初始化协议、写入 resolved config 和 hash，并在 validate 阶段执行失败门禁。完整运行命令为 `python exp03_runner.py --stage all --results-dir results`；所有数据生成、验证、训练和评测模块都已接入该入口，不能绕过配置快照和 hash 检查。

## 失败条件

有效样本不足 1,000、评测集未冻结 hash、训练 token 或模型 revision 漂移、缺少任一训练 seed、评测污染、缺少失败记录，均不得生成“成功”报告；对应阶段必须标记 `FAILED` 并停止后续比较。
