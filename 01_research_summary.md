# 整合调研执行记录

更新时间：2026-08-15

## 当前总进展

已完成第一天的三项阅读：数据增强/合成综述、Dolma、TRAK。当前形成的主线是：

```text
数据研究地图 → 数据构建与处理 → 数据归因 → 数据选择 → 合成增强 → 可执行 benchmark → 实验验证
```

详细记录位于：`daily/2026-08-14/`。

8 月 15 日进一步完成了高质量数据集的构建框架，补充 FineWeb 和 DataComp，并将 Dolma、FineWeb、DataComp 统一到“来源—处理—版本—评测”的比较框架中。新增：

- `daily/2026-08-15/02_fineweb/reading_card.md`
- `daily/2026-08-15/03_datacomp/reading_card.md`
- `benchmarks/data_construction_matrix.md`
- `benchmarks/high_quality_data_checklist.md`
- `data_schema.md`

## 已完成

| 阶段 | 材料 | 状态 | 产出 |
|---|---|---|---|
| 数据生命周期总览 | A Survey on Data Synthesis and Augmentation for LLMs | 已完成 | `daily/2026-08-14/01_survey/reading_card.md` |
| 候选数据池与数据处理 | Dolma | 已完成 | `daily/2026-08-14/02_dolma/reading_card.md` |
| 数据归因基础 | TRAK | 已完成 | `daily/2026-08-14/03_trak/reading_card.md` |

## 当前执行顺序

接下来不再按原来的论文清单顺序，而按新计划的研究问题推进：

1. 数据归因基础：TRAK（已完成）
2. 数据价值/有害数据：Data Shapley、FreeShap
3. 数据来源归因：Source-Aware Training、DataDignity
4. 数据选择与配方：数据选择、混合比例和 coverage vs. difficulty
5. 合成数据与增强：Self-Instruct、Evol-Instruct、reasoning/tool trajectory 数据
6. 可执行 benchmark：WebArena、OSWorld、τ-bench、SWE-bench 等
7. 设计并运行至少两个小实验

## 下一篇

### TRAK: Attributing Model Behavior at Scale

核心问题：如何在不重训成千上万个模型的情况下，估计某个训练样本对模型预测的影响？

需要重点记录：

- 归因对象是单个预测、验证集表现，还是整体能力；
- TRAK 如何用少量模型和随机投影近似数据影响；
- 它的验证实验如何证明排名有效；
- 归因结果能否用于数据选择、删除有害数据和解释错误；
- 对 LongTaskBench 是否可先做 group-level attribution，而不是逐条样本归因。

原文：[PMLR 页面](https://proceedings.mlr.press/v202/park23c.html)

## 当前核心问题

> 对 LongTaskBench 来说，哪些任务、任务族或增强方式，真正对目标能力和具体回答产生了可验证的贡献？

## 2026-08-15 新结论

高质量数据集不是一个静态数据文件，而是可追溯、可复现、可评测的数据构建流程。至少需要同时记录：原始来源与快照、schema、过滤和去重决策、版本、任务/能力覆盖、污染风险以及固定预算下的模型收益。

FineWeb 提供了“逐项 ablation 数据处理决策”的范式；DataComp 提供了“固定模型和评测、只比较数据策略”的实验控制范式。后续过滤、去重和选择实验将沿用这两个原则。

## 2026-08-16 新增进展

已建立 `experiments/exp01_filter_dedup/` 实验骨架，将过滤与去重拆成四个对照组：原始数据、过滤、过滤+exact dedup、过滤+near dedup。当前完成的是可复现实验设计、配置和结果模板，尚未运行数据处理或模型训练，因此暂无实际收益结论。

## 2026-08-17 新增进展

已建立 `experiments/exp02_selection_mixture/`，将数据选择拆为 random、quality、difficulty、embedding coverage、quality+coverage，并加入任务族混合比例对照。今日的研究判断是：difficulty 是模型相关信号，不能直接等价为数据价值；coverage 和任务族分布必须单独报告；复杂选择方法必须和随机基线、固定预算及未见任务族评测比较。

## 2026-08-18 新增进展

已完成 Self-Instruct、Natural Instructions、LLM 数据增强综述、Evol-Instruct 和 FLAN Collection 的阅读卡片，并建立 `benchmarks/augmentation_taxonomy.md` 与 `experiments/exp03_synthetic_augmentation/`。当前将增强收益拆为语言表达、实例覆盖、任务多样性、难度提升、反事实、结构组合和可验证 reasoning 七类；后续使用 GSM8K verifier 区分“增加数据量”和“增加有效能力覆盖”。

## 2026-08-19 新增进展

已完成 WebArena、OSWorld、SWE-bench、FLAMES、Diverse Synthetic Coding Tasks 和 ToolMind 的研读，补充 `benchmarks/synthetic_data_validity_criteria.md` 与 `benchmarks/synthetic_failure_taxonomy.md`。当前有效性标准是：固定训练预算、质量/标签一致、verifier 通过、无评测污染，并在未见分布上稳定提升；只有训练域提升不能称为真正有效增强。

## 2026-08-20 新增进展

已完成 TRAK、FreeShap、Source-Aware Training、In-Run Data Shapley 和 DataDignity 的研读，并建立 `experiments/exp04_attribution/`。当前将影响归因与来源归因分开：前者必须通过 top/bottom/random 删除后的 counterfactual 重训验证，后者关注回答与支持文档之间的 provenance，不直接等同于训练样本因果影响。
