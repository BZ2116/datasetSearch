# Exp03 固定评测协议

评测集共四个 split，每个 200 题，共 800 题。统一使用 `openai/gsm8k/main` 的官方 `test` split；不得使用 `parent_train`、候选池或生成结果。筛选后保存 JSONL、来源 index 和 SHA-256，训练前冻结。

| Split | 固定构造规则 | 目的 |
|---|---|---|
| `in_domain` | test 中操作签名出现在 `parent_train` 的题 | 同分布泛化 |
| `unseen_expression` | 操作签名出现在训练集且题面不少于 20 词的 test 题 | 表达泛化代理 |
| `unseen_numbers` | 操作签名出现在训练集，但数字元组未出现在 `parent_train` 的 test 题 | 数值实例泛化 |
| `unseen_composition` | test 题包含至少 4 个数字，且操作签名未出现在 `parent_train` | 结构组合泛化 |

每个 split 只取 test 原题前 200 个符合条件的样本；不足 200 题时整次评测失败，不允许重复补齐。每题必须保存 `eval_id`、`eval_source_index`、`split`、`operation_signature`、`numbers`、`answer` 和 `source_hash`。

## 指标和门禁

- `answer_accuracy`：normalized exact match；
- `verifier_pass_rate`：答案解析成功且通过 GSM8K verifier 的比例；
- `exact_duplicate_rate`、`near_duplicate_rate`：评测内部及与全部训练文本比较；
- `error_type`：`parse_failure`、`arithmetic_error`、`constraint_error`、`composition_error`、`unsupported_answer`；
- 相对 A 的百分点差和 95% bootstrap CI，bootstrap seed=1901、重采样 10,000 次。

训练文本与评测文本 exact match 或 5-gram MinHash Jaccard ≥ 0.85 均视为污染。污染率大于 0 时整次实验失败。只有未见 split 的提升才支持“有效增强”结论；仅训练域提升只能报告为训练域收益。
