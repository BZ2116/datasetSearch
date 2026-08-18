# Exp03：合成数据与增强类型收益验证

## 目的

区分“增加文本数量”和“增加有效能力覆盖”：比较语言改写、实体/数值替换、约束增强、反事实、多步组合和可验证 reasoning 对 GSM8K 泛化的影响。执行者只运行固定协议，不得自行选择模型、prompt、评测集或训练超参。

## 固定下载地址

- 数据集：[openai/gsm8k](https://huggingface.co/datasets/openai/gsm8k)
- 生成模型：[Qwen/Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct)
- 训练模型：[roneneldan/TinyStories-33M](https://huggingface.co/roneneldan/TinyStories-33M)

通过 Hugging Face `datasets` 和 `transformers` 下载；执行时必须记录实际 revision 和缓存文件 hash。

## 固定实验对象

- Seed 数据：GSM8K train 中固定抽取 100 条；
- 训练/评测：由 Agent 按 task/题型分层，避免同题或近题泄漏；
- 模型：`roneneldan/TinyStories-33M`，使用同一 tokenizer；
- 每组最终训练样本数：1,000；
- 随机种子：1801、1802、1803；
- 任务 verifier：答案数值抽取 + exact/normalized match；
- 预算：每组固定 10M training tokens、batch size=8、gradient accumulation=4、AdamW、learning rate=3e-4、weight decay=0.1、warmup ratio=0.03、max length=512；只对 solution 部分计算 loss。

100 个 parent 按答案类型、操作签名和源索引分层抽取，再固定切分 80 个 `parent_train` 与 20 个 `parent_holdout`。所有增强只允许使用 `parent_train`；评测集严格按 [`evaluation.md`](evaluation.md) 从 GSM8K 官方 test split 筛选并冻结 hash。

## 对照组

| 组 | 数据组成 | 目的 |
|---|---|---|
| A | 原始 seed 重复采样至 1,000 | 只增加数量 baseline |
| B | 语言改写 | 测量表达多样性 |
| C | 实体/数值替换 | 测量实例覆盖 |
| D | 增加约束/难度 | 测量难度提升 |
| E | 反事实变体 | 测量条件鲁棒性 |
| F | 多步组合 | 测量结构组合 |
| G | reasoning + verifier | 测量可验证过程 |

六类增强的验收不是只看最终数字：B 要求语义保持，C 要求操作签名保持，D 要求新增约束可满足，E 要求反事实答案重新计算，F 要求中间步骤可复算，G 要求每一步算术关系可解析。无法证明的候选进入失败集。

## 质量门禁

所有增强样本必须保存 `parent_id`、`augmentation_type`、生成 prompt、模型版本、答案、verifier 结果和失败原因。生成异常进入 `failed_generation.jsonl`，无法通过 verifier 的样本进入失败集，不得静默加入训练集。

## 评测

- train-domain：GSM8K 同题型未见题目；
- unseen expression：同一数学结构的新表述；
- unseen numbers/entities：数值和实体替换；
- unseen composition：未出现在 seed 中的多步组合；
- verifier pass rate、answer accuracy、平均推理步数和错误类型。
- 每个 split 200 题，greedy decoding；报告 accuracy、verifier pass rate、重复率、错误类型以及相对 A 的 95% bootstrap CI。

若某组通过全部门禁的样本不足 1,000 条，该组标记失败，不得用未验证样本或复制增强样本补齐。若评测污染率大于 0、缺少训练 seed、配置 hash 漂移或缺失失败记录，整次实验标记失败。

重点比较：在最终训练样本数相同的情况下，增强组是否超过 A；如果只在训练域提升而未见分布不提升，不能称为有效增强。

## 运行

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python exp03_runner.py --stage init --results-dir results
python exp03_runner.py --stage all --results-dir results
python exp03_runner.py --stage validate --results-dir results
```

`all` 依次执行 `prepare → generate → verify → train → evaluate → report`；任一阶段失败都会停止。
