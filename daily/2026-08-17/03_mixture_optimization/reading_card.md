# 论文阅读卡片：Data Mixture Optimization

## 基本信息

- **论文：** Data Mixture Optimization: A Multi-fidelity Multi-scale Bayesian Framework
- **作者 / 年份：** Thomson Yen 等 / 2025
- **状态：** NeurIPS 2025
- **链接：** https://papers.nips.cc/paper_files/paper/2025/hash/8e49d32f4668a41b013fbc1ed929c007-Abstract-Conference.html
- **类型：** 数据混合 / 优化

## 一句话理解

> 数据配比搜索应利用低成本实验和不确定性建模，而不是只靠人工试错或刚性的 scaling 外推。

## 数据池与实验

基于 SlimPajama 配比构建 472 次预训练运行的模拟器，改变数据组成、模型规模和训练步数。

## 方法与 baseline

将数据 mixture、model scale 和 training steps 作为决策变量，使用多保真、多尺度 Bayesian optimization；与 random search 和 multi-fidelity BO 比较。

## 主要结论

简单 kernel 和 acquisition function 也能利用低成本实验指导高成本实验，论文报告相对基线的搜索加速。

## 对本项目的启发

Exp02 只验证三个离散任务族配方，不复现 Bayesian optimization；后续若有多轮实验，可用前一轮结果缩小配比搜索空间。
