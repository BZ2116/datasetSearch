# 2026-08-18 日总结：合成数据与增强类型

## 一、今日完成

完成 Self-Instruct、Natural Instructions、LLM 数据增强综述、Evol-Instruct/WizardLM 和 FLAN Collection 的研读，并建立 GSM8K 可验证增强实验 Exp03。

新增论文卡片：

- `01_self_instruct/reading_card.md`
- `02_natural_instructions/reading_card.md`
- `03_llm_augmentation/reading_card.md`
- `04_evol_instruct/reading_card.md`
- `05_flan/reading_card.md`

新增实验材料：

- `benchmarks/augmentation_taxonomy.md`
- `experiments/exp03_synthetic_augmentation/README.md`
- `experiments/exp03_synthetic_augmentation/AGENT_TASK.md`
- `experiments/exp03_synthetic_augmentation/config.json`

## 二、核心结论

数据增强至少要区分：

1. 语言表达多样性；
2. 实体、数值和场景覆盖；
3. 新任务和任务族生成；
4. 约束和难度提升；
5. 反事实条件变化；
6. 多步结构组合；
7. reasoning 与 verifier 联合增强。

Self-Instruct 说明模型可以从少量 seed 自举生成 instruction，但必须过滤无效和相似样本；Natural Instructions 说明任务定义和任务族划分对跨任务泛化很重要；Evol-Instruct 说明增加复杂度可能提升能力，也可能造成不可解任务和标签失效；FLAN 说明任务模板和混合比例会影响泛化。

## 三、Exp03 实验逻辑

```text
A 原始样本重复
B 语言改写
C 实体/数值替换
D 增加约束
E 反事实变体
F 多步组合
G reasoning + verifier
```

固定 GSM8K seed、最终样本数、模型、训练 token 和随机种子。所有增强样本保存 parent ID、生成信息和 verifier 结果；无法通过答案验证的样本进入失败集，不能静默用于训练。

## 四、下一步

由执行 Agent 下载 GSM8K，生成 6 类增强，完成 verifier、去重、等规模训练和未见表达/数字/组合评测。最终重点判断增强是否在固定样本数下提升未见分布，而不是只增加数据量。
