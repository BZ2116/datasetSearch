# 过滤与去重失败样本抽检

## 抽检协议

- 每个处理组至少抽检 20 个被删除样本；
- 过滤删除按原因分层抽样；
- exact dedup 抽检重复簇；
- near dedup 抽检最高、中位数和接近阈值的相似样本对；
- 标记“应删除 / 不应删除 / 无法判断”和理由。

| sample_id | group | operation | reason | judgement | evidence | reviewer |
|---|---|---|---|---|---|---|
| pending | B/C/D | pending | pending | pending | pending | pending |

| operation | sampled | should_delete | should_keep | uncertain | estimated_error_rate | notes |
|---|---:|---:|---:|---:|---:|---|
| language | 0 | 0 | 0 | 0 | pending | pending |
| length | 0 | 0 | 0 | 0 | pending | pending |
| format | 0 | 0 | 0 | 0 | pending | pending |
| security | 0 | 0 | 0 | 0 | pending | pending |
| exact_dedup | 0 | 0 | 0 | 0 | pending | pending |
| near_dedup | 0 | 0 | 0 | 0 | pending | pending |
