# Exp04：数据归因与模型能力支撑

## 目的

验证归因分数是否能预测训练数据对目标模型行为的实际贡献，并区分“相关性排序”和“反事实影响”。

## 低成本固定方案

- 主数据集：GLUE QNLI；
- 模型：`bert-base-uncased`，固定 revision；
- 训练：固定 epochs、batch size、learning rate、max length 和 seed；
- 目标：dev 集 accuracy 和 loss；
- 方法：TRAK、embedding similarity、per-example loss/gradient、random；
- 删除比例：top 1%、bottom 1%、random 1%；
- 每个删除版本重新训练 3 个 seed。

如果 TRAK 环境无法稳定运行，Agent 可先完成 `embedding/loss/random` 三个 baseline，并把 TRAK 标记为失败，不得伪造 TRAK 分数。

## 对照与反事实

| 组 | 操作 | 目的 |
|---|---|---|
| Full | 全量训练 | 基线 |
| Top-k remove | 删除归因最高样本 | 检查高影响数据是否真的有帮助 |
| Bottom-k remove | 删除归因最低样本 | 检查低价值/有害数据 |
| Random remove | 随机删除同样数量 | 反事实基线 |
| Top-k select | 只保留高归因子集 | 数据选择应用 |

## 必须记录

- attribution scores 和排序；
- 目标样本/验证集定义；
- 模型和数据版本；
- 删除样本 ID；
- 每个 seed 的 accuracy、loss、训练时间；
- top/bottom/random 的结果均值、标准差和 bootstrap CI；
- 归因排名与删除后性能变化的 Spearman/Pearson 相关；
- 失败原因和梯度/显存问题。

## 结论口径

只有当 top-k、bottom-k、random 删除之间出现稳定且方向合理的性能差异，并能在多个 seed 重复，才能说归因排序具有实验支持。否则只能报告为启发式相关性。
