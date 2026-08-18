# 2026-08-19 日总结：验证合成数据是否真正有效

## 一、今日完成

完成 WebArena、OSWorld、SWE-bench、FLAMES、Diverse Synthetic Coding Tasks 和 ToolMind 的研读，并将“可执行 verifier、环境反馈、逐步验证和失败归因”映射到 Exp03。

新增阅读卡片：

- `01_webarena/reading_card.md`
- `02_osworld/reading_card.md`
- `03_swebench/reading_card.md`
- `04_flames/reading_card.md`
- `05_diverse_coding/reading_card.md`
- `06_toolmind/reading_card.md`

新增判定材料：

- `benchmarks/synthetic_data_validity_criteria.md`
- `benchmarks/synthetic_failure_taxonomy.md`

已有 `experiments/exp03_synthetic_augmentation/evaluation.md` 定义了 GSM8K 的四类评测 split、污染门禁、verifier 指标和 bootstrap CI；本日没有修改执行代码。

## 二、核心结论

WebArena、OSWorld 和 SWE-bench 的共同原则是：最终成功必须由环境状态、功能 evaluator 或测试集验证，不能只看自然语言输出是否“像正确答案”。FLAMES 和 ToolMind 进一步说明，合成 reasoning/trajectory 数据要检查每一步过程、反馈和失败，而不是只检查最终结果。

因此，“合成数据有效”必须同时满足：

```text
固定训练预算
→ 数据质量/标签一致
→ verifier 通过
→ 无评测污染
→ 未见分布性能提升
→ 多随机种子结果稳定
```

只有训练域提升，不能称为有效泛化；只有数据覆盖增加但模型不提升，也只能称为数据层新增，不能直接称为能力收益。

## 三、Exp03 结论口径

Exp03 的 A 组原始样本重复是“只增加数据量”的 baseline。B–G 组只有在固定最终样本数下改善未见表达、数字/实体或组合 split，并通过 GSM8K verifier、去重和污染检查，才可以支持“增强有效”的结论。

## 四、下一步

执行 Agent 运行 Exp03，返回生成失败、验证失败、近重复、污染、训练指标、分 split 评测和最终报告。结果返回前不得把任何增强类型写成已被实验证明有效。
