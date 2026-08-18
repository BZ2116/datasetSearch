# 论文阅读卡片：TRAK

## 基本信息

- **论文：** TRAK: Attributing Model Behavior at Scale
- **状态：** ICML 2023
- **链接：** https://proceedings.mlr.press/v202/park23c.html
- **类型：** 影响归因

## 归因对象

训练样本对某个模型预测或验证目标的影响。

## 方法

利用梯度表示、随机投影和近似 kernel，在少量 checkpoint 下估计训练样本影响，避免训练成千上万个子模型。

## 验证方式

论文使用 LDS 等指标，将归因排序与真实子集重训练后的性能变化比较，并在视觉、语言和多模态任务上验证。

## 边界

需要模型梯度；归因分数不是严格因果证明；对 checkpoint、目标函数和训练状态敏感。

## Exp04 迁移

QNLI 小模型中比较 TRAK、embedding/loss baseline 和随机排序，再用 top/bottom/random 删除重训验证。
