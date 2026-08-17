# AI 数据集构建与数据增强：整合调研方案

日期：2026-08-14

## 0. 调研目标

本调研不以“读完很多论文”为目标，而是回答下面五个问题：

1. 什么样的数据对模型能力真正有帮助？
2. 如何从原始数据构建高质量数据集？
3. 如何选择、混合和增强数据，而不是盲目扩大规模？
4. 如何验证合成数据没有引入噪声、重复和错误？
5. 如何用 benchmark 反向指导数据集设计？

最终要得到一套可复用的数据研究 pipeline，以及至少 2 个可以自己跑的实验。

## 1. 所有论文串起来后的总体脉络

这些工作实际上可以串成一条完整的数据生命周期：

```text
候选数据池
   ↓
来源选择与数据说明
   ↓
清洗、语言识别、质量过滤、隐私过滤
   ↓
文档/样本去重与污染控制
   ↓
能力覆盖分析与数据选择
   ↓
数据混合比例优化
   ↓
合成、改写、难度演化和反事实增强
   ↓
程序验证、模型验证、人工抽检
   ↓
训练或构造 benchmark
   ↓
下游评测、轨迹分析、失败归因
   ↓
动态重加权与下一轮数据改进
```

## 2. 数据归因与模型回答来源

这条线称为 **training data attribution / data influence / data provenance**。它与数据构建的关系非常直接：如果我们能知道哪些训练样本影响了某个回答，就能反过来判断哪些数据有用、哪些数据造成错误、哪些数据被重复学习，以及某种数据增强是否真的改变了目标能力。

需要区分三个问题：

1. **影响归因**：删除某条训练数据，模型回答会怎么变？
2. **来源归因**：模型回答中的知识最可能来自哪篇文档？
3. **机制归因**：哪些训练样本促成了某个内部 head、feature 或能力的形成？

### 经典和基础方法

- [TRAK: Attributing Model Behavior at Scale（ICML 2023）](https://proceedings.mlr.press/v202/park23c.html)：使用随机投影近似数据归因，目标是把模型预测追溯到训练样本；适合先理解 scalable influence 的基本思想。
- [Data Shapley in One Training Run（2024）](https://arxiv.org/abs/2406.11011)：尝试在一次训练中估计数据价值，减少反复重训成本。
- [Helpful or Harmful Data? FreeShap（ICML 2024）](https://arxiv.org/abs/2406.04606)：用近似 Shapley 方法判断样本对语言模型预测是有益还是有害，并用于数据选择、错误标签检测和数据删除。
- [Training Data Attribution via Approximate Unrolling / Source（NeurIPS 2024）](https://proceedings.neurips.cc/paper_files/paper/2024/hash/7af60ccb99c7a434a0d9d9c1fb00ca94-Abstract-Conference.html)：处理多阶段、尚未收敛训练中的归因问题，弥补简单 influence function 的不足。

### 回答到来源的归因

- [Source-Aware Training Enables Knowledge Attribution in Language Models（COLM 2024）](https://arxiv.org/abs/2404.01019)：训练模型学习文档 ID，使模型回答时能够引用支持知识的预训练来源；这是把“归因分析”变成“模型可输出的来源证明”。
- [DataDignity: Training Data Attribution for Large Language Models（2026）](https://arxiv.org/abs/2605.05687)：构造 FakeWiki benchmark，用来源保持的改写、相似但缺少关键事实的 anti-document 和 jailbreak-style query 测试真正的 provenance，而不是简单 lexical retrieval。
- [Daunce: Data Attribution through Uncertainty Estimation（ICLR 2026 submission）](https://openreview.net/forum?id=IKB9uhMVH9)：通过多个扰动模型的不确定性协方差做数据归因，并尝试支持黑盒模型；应关注其黑盒归因结论的验证强度。

### 从数据到模型内部机制

- [Analyzing Memorization in Large Language Models through the Lens of Model Attribution（2025）](https://arxiv.org/abs/2501.05078)：从模型归因角度分析记忆和训练数据复现。
- [Which Data Attributes Stimulate Math and Code Reasoning?（Infra）](https://openreview.net/forum?id=MAJVBIZa6I)：用 influence function 把数学、代码推理能力归因到样本、序列甚至 token，并研究跨领域影响。
- [Mechanistic Data Attribution（2026）](https://arxiv.org/abs/2601.21996)：尝试把训练样本归因到可解释的内部单位，进一步通过删除或复制高影响样本验证 induction head 等机制的形成。

这一环节的核心结论是：

> 数据集构建不应该只问“这条数据质量高不高”，还应该问“它是否对目标回答、目标能力或目标机制产生了可验证的贡献”。

### 最值得跑的归因实验

从 1,000–10,000 条可控 SFT 数据开始，训练一个小模型并保存 checkpoint，然后选一个目标验证集：

1. 用 embedding 相似度找最相关训练样本；
2. 用 TRAK 或 FreeShap 找高影响样本；
3. 随机抽取同样数量的样本作为 baseline；
4. 删除高影响样本，重新训练或继续训练；
5. 比较目标问题的 loss、答案概率和能力分数变化；
6. 检查归因排名是否能预测删除后的性能变化。

如果计算资源有限，先做 leave-one-group-out：把数据按来源、任务族或增强类型分组，每次删除一组，而不是逐条删除。这样可以直接回答：

- 哪个数据源帮助了哪个能力？
- 哪类增强样本真正有用？
- 哪类数据只增加了相似表达，没有增加新能力？
- 哪类样本对某个回答有害？

## 3. 数据生命周期与研究阶段

加入归因后，完整闭环变成：

```text
数据构建
  ↓
训练模型
  ↓
对目标问题/能力做评测
  ↓
归因到训练样本、数据源或内部机制
  ↓
删除、重采样、增强高价值数据
  ↓
重新训练和验证
```

这比传统的“清洗一次、训练一次、看总分”更接近 2026 年数据研究的前沿。

### 3.1 第一阶段：建立候选数据池

代表工作：Dolma、FineWeb、DataComp、DataComp-LM。

核心问题：数据从哪里来，如何保证来源多样、合法、可复现、可分析？

- **Dolma** 强调开放、可复现的多来源语料和数据处理工具；
- **FineWeb** 强调 Common Crawl 的系统清洗、去重和质量过滤；
- **DataComp** 把数据集设计本身变成标准化实验；
- **DataComp-LM** 将这种思路扩展到语言模型预训练数据。

这一阶段的核心结论是：

> 数据集不是一个下载下来的文件，而是候选池、处理规则、版本、采样比例和评测协议的集合。

### 3.2 第二阶段：质量过滤与去重

代表工作：FineWeb、Dolma、Data Filtering Networks、Data Selection for Language Models via Importance Resampling。

常见方法包括：

- 规则过滤：长度、特殊字符、语言、格式、毒性、PII；
- 模型过滤：质量分类器、教育性评分、困惑度、reward model；
- 去重：文档级、段落级、n-gram、MinHash、embedding；
- 重要性筛选：根据目标任务或模型影响估计样本价值。

关键结论不是“过滤越多越好”，而是：

> 过滤需要在质量、覆盖、多样性和规模之间做权衡；过度去重和过度过滤都可能损失泛化能力。

### 3.3 第三阶段：数据选择与数据配方

代表工作：FLAN、Large-Scale Data Selection for Instruction Tuning、ROSE、DS²、Task-Specific Data Selection、Data Mixture Optimization、Decouple Searching from Training、Why Less is More。

这一阶段出现了两个变化。

第一，数据选择从“挑好样本”转向“挑对目标有用的样本”：

- representation-based selection；
- reward-oriented selection；
- holdout-loss-based selection；
- activation-based selection；
- coverage-aware selection。

第二，数据配比从人工经验转向优化问题：

- 网页、代码、数学、科学、对话数据各占多少；
- 不同模型规模是否需要不同配比；
- 小规模实验能否预测大规模配方；
- 是否应该训练过程中动态调整权重。

2026 年的一个重要趋势是：

> “难度最高的数据”不一定最有用；覆盖度、目标相关性和数据多样性可能更加重要。

### 3.4 第四阶段：合成数据和数据增强

代表工作：Self-Instruct、WizardLM/Evol-Instruct、FLAN、数据增强综述、FLAMES、代码 reasoning synthetic data、ToolMind。

可以把增强分成五类：

| 增强类型 | 主要改变 | 典型方法 | 主要风险 |
|---|---|---|---|
| 语言增强 | 表达方式 | 改写、翻译、风格变化 | 语义漂移 |
| 实例增强 | 实体和数值 | 替换实体、扰动输入 | 标签失效 |
| 难度增强 | 约束和推理 | Evol-Instruct、反事实 | 任务不可解 |
| 结构增强 | 任务组合 | 多步组合、任务图扩展 | 逻辑不一致 |
| 轨迹增强 | 状态、动作、反馈 | 工具调用、失败恢复 | 错误轨迹放大 |

Self-Instruct 解决“没有足够 instruction 数据”的问题；Evol-Instruct 解决“指令太简单”的问题；FLAMES 和代码 reasoning 数据进一步要求过程、答案和验证器一致；ToolMind 则把验证细化到每一轮工具调用。

因此，现代合成数据的质量标准已经从：

```text
问题 → 答案
```

发展到：

```text
任务 → 推理/动作 → 结果 → 可执行验证 → 失败归因
```

### 3.5 第五阶段：可执行数据与 benchmark

代表工作：Natural Instructions、WebArena、OSWorld、τ-bench、SWE-bench、TRAJECT-Bench、NaturalGAIA、TRACE/Self-Evolving Agent Benchmarks、Sci-Reasoning。

这些工作说明 benchmark 数据至少有三种形态：

1. **静态样本**：输入、输出、标签；
2. **可执行任务**：环境状态、动作空间、目标状态、evaluator；
3. **轨迹数据**：观察、动作、工具调用、反馈、修正和最终结果。

评测也从最终答案正确率扩展为：

- 最终成功率；
- 步骤级正确率；
- 约束违规率；
- 工具调用成功率；
- 首次失败位置；
- 恢复成功率；
- 轨迹效率；
- 多次运行稳定性 `pass^k`；
- 能力维度分数。

## 4. 最值得自己跑的案例

下面按“价值/成本比”排序。

### 案例 A：质量过滤与去重对比

目标：验证数据质量处理是否比简单扩大数据量更重要。

数据：选 1,000–10,000 条公开文本、instruction 或 QA 数据。

构造四个版本：

1. 原始数据；
2. 规则过滤；
3. 规则过滤 + exact/near dedup；
4. 质量评分 + dedup + 分层采样。

记录指标：

- 保留率；
- 重复率；
- 平均长度；
- 语言/主题分布；
- 人工质量评分；
- 下游模型效果。

推荐参考：Dolma、FineWeb、DataComp-LM。

价值：最高，成本最低，是所有后续实验的基础。

### 案例 B：随机选择 vs 难度选择 vs 覆盖选择

目标：验证 2026 年“coverage 可能比 difficulty 更重要”的观点。

从同一个大数据池中选取相同数量的样本：

1. 随机选择；
2. 按长度或 perplexity 选择；
3. 按模型评分选择；
4. 按 embedding 聚类覆盖选择；
5. 难度和覆盖联合选择。

保持以下条件不变：

- 模型；
- 训练步数；
- 学习率；
- token 数；
- batch size；
- 评测集。

比较：

- in-domain 性能；
- out-of-domain 性能；
- 任务族泛化；
- 数据重复和覆盖指标。

推荐参考：Large-Scale Data Selection、Why Less is More、Rethinking Data Selection、DS²。

价值：非常高，能够直接形成数据选择研究结果。

### 案例 C：同一任务的多种增强方式

目标：区分“语言多样性”“任务多样性”和“难度提升”的作用。

选 50–100 个 seed 样本，生成：

- 语言改写；
- 实体替换；
- 约束增加；
- 反事实变体；
- 多步组合；
- 失败案例。

保持原始标签或目标可验证，并统计：

- 语义保持率；
- 标签一致率；
- 重复率；
- 人工可解率；
- 增强后模型在未见表达上的表现。

推荐参考：Self-Instruct、WizardLM、Evol-Instruct、FLAN、数据增强综述。

价值：适合快速验证合成数据是否真的带来泛化，而不是只增加训练量。

### 案例 D：可验证 reasoning 数据

目标：比较普通答案数据和“答案 + 过程 + verifier”数据的差异。

可以使用数学、代码或结构化推理任务。

构造三种数据：

1. 只有问题和答案；
2. 问题、解释和答案；
3. 问题、过程、答案和程序验证器。

对数学使用计算器或形式检查；对代码使用单元测试；对结构化任务使用规则 evaluator。

推荐参考：FLAMES、代码 synthetic reasoning data、Self-Instruct、ToolMind。

价值：如果资源允许，研究价值最高，因为它能验证“可验证过程”是否比自然语言解释更有效。

### 案例 E：静态 benchmark vs 轨迹 benchmark

目标：验证只看最终结果会不会遗漏关键失败信息。

将一个任务设计成：

- 初始状态；
- 若干允许动作；
- 中间反馈；
- 最终目标状态；
- evaluator。

记录完整轨迹并标注：

- 第一次错误动作；
- 错误类型；
- 是否修正；
- 最终是否成功；
- 是否存在更短路径。

推荐参考：τ-bench、WebArena、OSWorld、TRAJECT-Bench、NaturalGAIA。

价值：最适合 LongTaskBench，但环境开发成本高，建议作为第二阶段实验。

## 5. 推荐 benchmark 组合

### 如果研究普通语言模型数据

- MMLU：知识和学科覆盖；
- ARC / OpenBookQA：知识与推理；
- GSM8K / MATH：数学推理；
- HumanEval / MBPP：代码生成；
- AlpacaEval / MT-Bench：指令跟随和对话；
- BBH：复杂推理。

### 如果研究数据选择和泛化

不要只用训练域内测试集，至少分成：

```text
训练域内
未见表达
未见实体
未见任务模板
未见任务族
跨领域测试
```

重点看数据增强是否提升了真正的泛化。

### 如果研究 agent / 可执行任务

- WebArena：网页任务；
- OSWorld：桌面和跨应用任务；
- τ-bench：用户—工具—agent 交互；
- SWE-bench：真实代码问题；
- TRAJECT-Bench：轨迹级工具使用；
- NaturalGAIA：GUI 任务和高质量轨迹。

注意：这些 benchmark 的环境配置、版本和数据污染风险必须记录，不能只比较一个总分。

## 6. 一套完整的数据实验 pipeline

```text
1. 定义目标能力
2. 建立候选数据池
3. 记录 provenance 和版本
4. 做基础清洗与安全过滤
5. 做 exact / near dedup
6. 分析质量、主题、长度和能力覆盖
7. 设计多个数据选择策略
8. 设计增强策略
9. 做自动验证和人工抽检
10. 固定模型、训练预算和评测集
11. 训练多个数据版本
12. 做 in-domain / out-of-domain / unseen split 评测
13. 分析失败样本和数据贡献
14. 更新数据配方或动态权重
```

## 7. 推荐的最小数据 schema

```json
{
  "id": "sample_id",
  "source": "human/synthetic/web/benchmark",
  "source_id": "original_id",
  "version": "v1",
  "input": "...",
  "output": "...",
  "reasoning": "optional",
  "task_family": "...",
  "capability_tags": ["coverage", "reasoning"],
  "difficulty": 3,
  "quality_scores": {
    "correctness": 0,
    "clarity": 0,
    "diversity": 0
  },
  "augmentation_type": "none/rewrite/counterfactual/evolution",
  "verifier": "none/programmatic/model/human",
  "contamination_risk": "low",
  "split": "train/dev/test"
}
```

如果是 agent 数据，再增加：

```json
{
  "initial_state": "...",
  "actions": [],
  "observations": [],
  "tool_calls": [],
  "goal_state": "...",
  "step_errors": [],
  "recovery_actions": [],
  "trajectory_success": true
}
```

## 8. 五周完整调研方案

### 第 1 周：建立文献和数据流程认识

阅读：Dolma、FineWeb、DataComp、DataComp-LM、FLAN、Self-Instruct。

产出：

- 论文矩阵；
- 数据生命周期图；
- 数据处理决策表；
- 500–1,000 条数据的清洗/去重小实验。

### 第 2 周：研究数据选择、覆盖和配比

阅读：Large-Scale Data Selection、ROSE、DS²、Why Less is More、Rethinking Data Selection、Data Mixture Optimization。

产出：

- 随机/难度/覆盖选择对比；
- 数据覆盖指标；
- 数据配比实验；
- in-domain 与 out-of-domain 评测。

### 第 3 周：研究合成数据和增强

阅读：WizardLM、Evol-Instruct、FLAMES、ToolMind、reasoning synthetic data 和数据增强综述。

产出：

- 50–100 个 seed 样本；
- 4–6 种增强版本；
- 自动验证器；
- 语义保持率、有效率、重复率和泛化结果。

### 第 4 周：研究 benchmark 和可验证任务

阅读：WebArena、OSWorld、τ-bench、SWE-bench、TRAJECT-Bench、NaturalGAIA、TRACE、Sci-Reasoning。

产出：

- 一个最小可执行任务环境；
- 一个 evaluator；
- 至少 20 个任务；
- 成功/失败/恢复轨迹；
- trajectory-level 指标。

### 第 5 周：研究数据归因与数据 provenance

阅读顺序：

1. TRAK；
2. FreeShap；
3. Source / Approximate Unrolling；
4. Source-Aware Training；
5. DataDignity；
6. Daunce；
7. Infra 或 Mechanistic Data Attribution。

产出：

- 一张归因方法分类表；
- 一个小模型和可控训练数据池；
- 一个 leave-one-group-out 或 TRAK 归因实验；
- 一张“训练数据 → 目标回答/能力”的影响图；
- 对归因可靠性的 counterfactual 验证。

## 9. 最终报告结构

```text
1. 研究问题与范围
2. 文献分类与发展脉络
3. 数据生命周期
4. 数据质量、去重和过滤
5. 数据选择与混合
6. 合成数据与增强
7. 可验证 reasoning 和 agent trajectory
8. Benchmark 与评测设计
9. 小规模实验及结果
10. 失败案例与风险
11. 推荐的数据 schema 和 pipeline
12. 最值得继续研究的三个问题
```

## 10. 最值得继续研究的四个问题

### 问题一：Coverage 还是 Difficulty？

在相同数据预算下，覆盖更多任务分布是否比选择更难样本更有效？

### 问题二：合成数据的增益来自哪里？

是语言多样性、任务覆盖、难度提升，还是教师模型的答案风格？

### 问题三：可验证轨迹是否优于静态答案？

在工具使用、代码和复杂任务中，加入过程和 evaluator 是否能带来更好的泛化与恢复能力？

### 问题四：模型回答中的知识和能力来自哪些数据？

数据归因方法能否可靠地识别支持某个回答的训练样本？被归因的样本是否真的具有因果作用？删除、复制或增强这些样本后，模型行为是否按预测方向变化？

## 11. 推荐的第一批实验顺序

如果按优先级安排第一批实验，顺序如下：

1. **质量过滤 + 去重对比**：成本最低，建立数据处理基础；
2. **随机 vs 难度 vs 覆盖选择**：最能体现 2026 年数据研究前沿；
3. **静态答案 vs 可验证过程/轨迹**：最接近 LongTaskBench 的潜在差异化；
4. **数据归因 + 反事实删除**：验证哪些训练数据真正影响模型回答。

最终不要只报告“哪个分数更高”，还要报告：

- 数据保留率；
- 训练和生成成本；
- 覆盖度；
- 重复率；
- 未见分布泛化；
- 失败类型；
- evaluator 的可靠性。

## 12. 统一论文索引

下面按数据生命周期汇总本方案中提到的论文和资源。

### 数据来源、清洗、过滤和预训练数据

- [Dolma: an Open Corpus of Three Trillion Tokens](https://arxiv.org/abs/2402.00159)
- [FineWeb: Decanting the Web for the Finest Text Data at Scale](https://proceedings.neurips.cc/paper_files/paper/2024/file/370df50ccfdf8bde18f8f9c2d9151bda-Paper-Datasets_and_Benchmarks_Track.pdf)
- [DataComp](https://papers.neurips.cc/paper_files/paper/2023/hash/56332d41d55ad7ad8024aac625881be7-Abstract-Datasets_and_Benchmarks.html)
- [DataComp-LM](https://proceedings.neurips.cc/paper_files/paper/2024/file/19e4ea30dded58259665db375885e412-Paper-Datasets_and_Benchmarks_Track.pdf)
- [Data Filtering Networks](https://neurips.cc/virtual/2023/80515)
- [Data Selection for Language Models via Importance Resampling](https://proceedings.neurips.cc/paper_files/paper/2023/hash/6b9aa8f418bde2840d5f4ab7a02f663b-Abstract-Conference.html)

### 指令数据、合成数据和数据增强

- [The Flan Collection](https://arxiv.org/abs/2301.13688)
- [Natural Instructions](https://github.com/allenai/natural-instructions)
- [Self-Instruct（ACL 2023）](https://aclanthology.org/2023.acl-long.754/)
- [WizardLM / Evol-Instruct](https://www.microsoft.com/en-us/research/publication/wizardlm-empowering-large-language-models-to-follow-complex-instructions/)
- [A Survey on Data Synthesis and Augmentation for Large Language Models](https://arxiv.org/abs/2410.12896)
- [Data Augmentation using Large Language Models](https://aclanthology.org/2024.findings-acl.97/)
- [FLAMES](https://arxiv.org/abs/2508.16514)
- [Increasing LLM Coding Capabilities through Diverse Synthetic Coding Tasks](https://arxiv.org/abs/2510.23208)
- [ToolMind](https://arxiv.org/abs/2511.15718)

### 数据选择、数据配比和数据效率

- [Large-Scale Data Selection for Instruction Tuning](https://arxiv.org/abs/2503.01807)
- [ROSE](https://aclanthology.org/2025.findings-emnlp.710/)
- [DS²: Improving Data Efficiency via Curating LLM-Driven Rating Systems](https://proceedings.iclr.cc/paper_files/paper/2025/file/faa6144674bce872365874c576b4f56f-Paper-Conference.pdf)
- [Task-Specific Data Selection via Monosemantic Neuronal Activations](https://huggingface.co/papers/2503.15573)
- [Data Mixture Optimization](https://papers.nips.cc/paper_files/paper/2025/hash/8e49d32f4668a41b013fbc1ed929c007-Abstract-Conference.html)
- [Decouple Searching from Training](https://arxiv.org/abs/2602.00747)
- [Why Less is More (Sometimes): A Theory of Data Curation](https://iclr.cc/virtual/2026/poster/10011214)
- [Rethinking Data Selection: The Importance of Coverage over Difficulty](https://openreview.net/forum?id=qImiy98UhN)
- [Holdout-Loss-Based Data Selection](https://www.microsoft.com/en-us/research/publication/holdout-loss-based-data-selection-for-llm-finetuning-via-in-context-learning/)
- [Rethinking Data Curation: Online Reweighting](https://arxiv.org/abs/2605.05227)

### 数据归因、影响分析、记忆和来源追踪

- [TRAK: Attributing Model Behavior at Scale](https://proceedings.mlr.press/v202/park23c.html)
- [Data Shapley in One Training Run](https://arxiv.org/abs/2406.11011)
- [Helpful or Harmful Data? FreeShap](https://arxiv.org/abs/2406.04606)
- [Training Data Attribution via Approximate Unrolling / Source](https://proceedings.neurips.cc/paper_files/paper/2024/hash/7af60ccb99c7a434a0d9d9c1fb00ca94-Abstract-Conference.html)
- [NeurIPS 2024 Final-Model-Only Data Attribution](https://neurips.cc/virtual/2024/105337)
- [Source-Aware Training Enables Knowledge Attribution](https://arxiv.org/abs/2404.01019)
- [Analyzing Memorization through Model Attribution](https://arxiv.org/abs/2501.05078)
- [Which Data Attributes Stimulate Math and Code Reasoning?](https://openreview.net/forum?id=MAJVBIZa6I)
- [Daunce: Data Attribution through Uncertainty Estimation](https://openreview.net/forum?id=IKB9uhMVH9)
- [DataDignity](https://arxiv.org/abs/2605.05687)
- [Mechanistic Data Attribution](https://arxiv.org/abs/2601.21996)
- [Training Data Influence Analysis and Estimation: A Survey](https://doi.org/10.1007/S10994-023-06495-7)

### Benchmark、可执行任务和轨迹数据

- [Natural Instructions](https://github.com/allenai/natural-instructions)
- [WebArena](https://proceedings.iclr.cc/paper_files/paper/2024/hash/4410c0711e9154a7a2d26f9b3816d1ef-Abstract-Conference.html)
- [OSWorld](https://papers.nips.cc/paper_files/paper/2024/hash/5d413e48f84dc61244b6be550f1cd8f5-Abstract-Datasets_and_Benchmarks_Track.html)
- [τ-bench](https://arxiv.org/abs/2406.12045)
- [SWE-bench](https://proceedings.iclr.cc/paper_files/paper/2024/file/edac78c3e300629acfe6cbe9ca88fb84-Paper-Conference.pdf)
- [TRAJECT-Bench](https://www.amazon.science/publications/traject-bench-a-trajectory-aware-benchmark-for-evaluating-agentic-tool-use)
- [NaturalGAIA](https://openreview.net/forum?id=bNDVJ9omfk)
- [TRACE / Self-Evolving Agent Benchmarks](https://researchportal.hkust.edu.hk/en/publications/towards-self-evolving-agent-benchmarks-validatable-agent-trajecto/)
- [Sci-Reasoning](https://arxiv.org/abs/2601.04577)
- [What Matters in Data Curation for Multimodal Reasoning?](https://arxiv.org/abs/2601.10922)

### 评测与污染控制补充

- [Does Question Really Matter? The Attribution of Answer Bias in LLM Evaluation](https://ojs.aaai.org/index.php/AAAI/article/view/40262)
- [VisualWebArena](https://aclanthology.org/2024.acl-long.50/)
- [Windows Agent Arena](https://neurips.cc/virtual/2024/100964)

## 13. 总结

从 Dolma、FineWeb 到 DataComp，解决的是“如何获得和处理数据”；从 FLAN、Self-Instruct、WizardLM 到 FLAMES，解决的是“如何扩展任务和推理数据”；从数据选择、数据混合优化到 online reweighting，解决的是“如何让有限数据更有效”；从 TRAK、FreeShap、Source、DataDignity 到 Mechanistic Data Attribution，解决的是“模型行为和回答究竟由哪些数据支撑”；从 WebArena、OSWorld、τ-bench 到 TRAJECT-Bench，解决的是“如何让数据和评测接近真实行为”。

最清晰的研究主线是：

> 从静态数据集走向可分析、可选择、可增强、可验证、可反馈的数据系统。

这也是最值得你自己跑实验的方向：先建立一个小数据池，再比较不同过滤、选择、增强和验证策略，最后用 benchmark 的未见分布结果判断数据是否真的有效。
