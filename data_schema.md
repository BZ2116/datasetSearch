# 项目统一数据 Schema

## 设计原则

1. 原始内容与处理结果分离，避免覆盖证据；
2. 每个样本可追溯到来源、版本和处理运行；
3. 质量分数必须带评估方法和版本，不能只保存一个无来源的数字；
4. schema 同时支持文本样本、指令样本和 Agent 轨迹；
5. 缺失字段使用 `null` 或空数组，不用伪造默认值。

## 最小记录

```json
{
  "id": "stable_sample_id",
  "schema_version": "1.0",
  "content_type": "document|instruction|qa|trajectory",
  "source": {
    "source_type": "web|paper|code|human|synthetic|benchmark",
    "source_name": "fineweb|dolma|longtaskbench",
    "source_id": "original_document_or_task_id",
    "source_url": null,
    "snapshot": "crawl_or_release_version",
    "license": null,
    "retrieved_at": null
  },
  "content": {
    "input": "...",
    "output": "...",
    "reasoning": null
  },
  "task": {
    "task_family": "...",
    "capability_tags": ["planning", "tool_use"],
    "difficulty": null,
    "language": "zh"
  },
  "processing": {
    "pipeline_version": "v1",
    "filter_decisions": [],
    "dedup_group_id": null,
    "augmentation_type": "none",
    "parent_ids": []
  },
  "quality": {
    "correctness": null,
    "completeness": null,
    "clarity": null,
    "diversity": null,
    "safety": null,
    "verifier_type": "none|program|model|human",
    "verifier_result": null,
    "scorer_version": null
  },
  "split": "train|dev|test|holdout",
  "contamination_risk": "unknown|low|medium|high",
  "created_at": "..."
}
```

## Agent 轨迹扩展字段

```json
{
  "trajectory": {
    "initial_state": "...",
    "goal_state": "...",
    "observations": [],
    "actions": [],
    "tool_calls": [],
    "step_errors": [],
    "recovery_actions": [],
    "trajectory_success": null,
    "total_steps": null
  }
}
```

## Provenance 必填字段

对本项目而言，以下字段不能省略：`source_type`、`source_name`、`source_id`、`snapshot`、`pipeline_version`、`filter_decisions`、`dedup_group_id`、`split`。如果来源或处理信息未知，明确记为 `unknown`，不能默认为可信。
