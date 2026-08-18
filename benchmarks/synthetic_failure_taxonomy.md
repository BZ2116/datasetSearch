# 合成数据失败样本分类

| 类别 | 判定条件 | 处理 | 是否统计为增强失败 |
|---|---|---|---|
| generation_failure | 模型无输出、格式损坏、超时 | 保存原始错误和 prompt，排除训练 | 是 |
| semantic_drift | 改写后任务含义变化 | 保存 parent/child 对照，排除训练 | 是 |
| answer_mismatch | 最终答案与正确答案不一致 | 进入 failed_verification | 是 |
| reasoning_error | 中间步骤错误但最终答案偶然正确 | 排除 reasoning 组，单独统计 | 是 |
| constraint_violation | 新增约束未满足或互相冲突 | 排除训练 | 是 |
| invalid_counterfactual | 反事实条件不成立或无法重新计算 | 排除训练 | 是 |
| composition_error | 多步组合中间状态不一致 | 排除训练 | 是 |
| exact_duplicate | 与 parent 或组内样本完全重复 | 去重并记录 | 是 |
| near_duplicate | 5-gram MinHash Jaccard ≥ 0.85 | 去重并记录簇信息 | 是 |
| contamination | 与 eval 有 exact/near overlap | 整次实验失败门禁 | 是 |
| unsupported_answer | 无法解析数字答案或 verifier 不支持 | 进入失败集 | 是 |
