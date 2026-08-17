# 2026-08-16 日总结：过滤与去重实验设计

## 一、今日完成

围绕“过滤和去重分别带来什么收益”，建立了 `experiments/exp01_filter_dedup/` 实验骨架：

- 明确原始、过滤、过滤+exact dedup、过滤+near dedup 四组对照；
- 定义语言、长度、格式和安全过滤记录要求；
- 定义 exact/near dedup 的参数、簇信息和抽检要求；
- 建立数据统计表、模型指标表和失败样本抽检表；
- 明确固定数据池、split、随机种子和训练预算的控制原则。

## 二、实验逻辑

```text
A 原始数据
  ↓ 过滤
B 过滤数据
  ↓ exact dedup
C 完全去重数据
  ↓ near dedup
D 近重复去重数据
```

只比较原始数据和最终清洗数据，无法知道收益来自过滤还是去重，也无法发现 near dedup 是否误删了有效变体。因此本实验将每一步单独作为对照。

## 三、当前边界

今日完成的是实验设计、配置和结果模板，尚未运行数据处理或模型训练，因此没有虚构保留率、重复率、验证 loss 或下游分数。运行结果将写入 `experiments/exp01_filter_dedup/results/`。

## 四、执行方式升级

实验目录现已改造成可直接交给执行 Agent 的自包含任务包，包含：

- `AGENT_TASK.md`：执行步骤、不可改变的变量和验收标准；
- `config.json`：固定 FineWeb、TinyStories-33M、训练预算、seed 和评测集；
- `run_experiment.py`：数据处理单入口；
- `requirements.txt`：依赖清单；
- `tests/`：核心规范化、过滤和 exact dedup 测试；
- `results/run/`：执行 Agent 必须返回的完整结果目录。

本机只完成代码语法和核心函数验证，没有虚构实验结果。下一步由另一台电脑上的 Agent 申请 GPU、下载数据和模型并运行完整实验。
