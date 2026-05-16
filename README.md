# secure-aggregation-mini

`secure-aggregation-mini` is a lightweight teaching project for understanding the core idea of secure aggregation in federated learning. It uses small numeric vectors to simulate client updates, pairwise masks, masked upload, and server-side aggregation.

The project is designed for classroom demonstrations and hands-on experiments. It does not implement a production-grade cryptographic protocol, network communication, or dropout recovery.

## 1. 项目简介

在联邦学习中，多个客户端会向服务端上传模型更新或梯度。如果服务端直接接收每个客户端的明文更新，就可能观察到单个客户端的局部训练信息。安全聚合的目标是让服务端只能看到多个客户端更新的总和，而不能直接获得任意单个客户端的真实更新。

本项目通过一个极简的两两掩码机制演示安全聚合的基本思想：

- 每个客户端生成自己的本地更新向量；
- 客户端之间构造可相互抵消的随机掩码；
- 每个客户端上传被掩码保护后的更新；
- 服务端只对上传结果求和；
- 所有两两掩码在求和过程中抵消，服务端得到全体更新总和。

## 2. 教学目标

完成本项目后，学生应能够理解：

1. 为什么联邦学习中的客户端更新可能暴露隐私；
2. 安全聚合试图保护的对象是什么；
3. 两两随机掩码如何在聚合时相互抵消；
4. 服务端为什么可以得到总和，但难以直接观察单个客户端更新；
5. 教学模拟协议与真实安全聚合协议之间的差异。

## 3. 工程结构

```text
secure-aggregation-mini/
├── README.md
├── requirements.txt
├── config.py
├── mask_utils.py
├── client.py
├── server.py
├── run_demo.py
├── compare_plain_and_secure.py
├── examples/
│   └── sample_updates.json
├── results/
│   └── .gitkeep
└── .gitignore
```

主要文件说明：

| 文件 | 作用 |
|---|---|
| `config.py` | 实验参数配置，包括客户端数量、向量维度、随机种子等 |
| `mask_utils.py` | 生成两两掩码、检查掩码抵消效果 |
| `client.py` | 定义客户端对象，生成本地更新与掩码更新 |
| `server.py` | 定义服务端对象，接收并聚合上传更新 |
| `run_demo.py` | 运行完整安全聚合演示 |
| `compare_plain_and_secure.py` | 对比明文聚合与安全聚合的结果 |
| `examples/sample_updates.json` | 一组固定样例更新，便于课堂讲解 |
| `results/` | 保存实验输出 |

## 4. 快速开始

### 4.1 安装依赖

```bash
pip install -r requirements.txt
```

### 4.2 运行安全聚合演示

```bash
python run_demo.py
```

运行后，程序会输出：

- 每个客户端的真实更新；
- 每个客户端上传给服务端的掩码更新；
- 服务端聚合后的结果；
- 明文求和结果；
- 两者之间的误差。

默认结果会保存到：

```text
results/secure_aggregation_result.json
```

### 4.3 对比明文聚合与安全聚合

```bash
python compare_plain_and_secure.py
```

该脚本会展示：

- 明文聚合时，服务端可以看到每个客户端的真实更新；
- 安全聚合时，服务端只能看到每个客户端的掩码更新；
- 聚合总和与明文求和保持一致。

## 5. 核心原理

假设有三个客户端，它们的真实更新分别为：

```text
u1, u2, u3
```

客户端之间生成两两随机掩码：

```text
m12, m13, m23
```

上传前，每个客户端构造掩码更新：

```text
client 1: u1 + m12 + m13
client 2: u2 - m12 + m23
client 3: u3 - m13 - m23
```

服务端求和：

```text
(u1 + m12 + m13) + (u2 - m12 + m23) + (u3 - m13 - m23)
= u1 + u2 + u3
```

所有掩码项在聚合过程中抵消，服务端获得全体更新之和，但无法直接从单个上传值中恢复对应客户端的真实更新。

## 6. 实验内容

本项目建议作为一次 30 到 60 分钟的课堂实验使用。可以安排以下任务：

1. 修改 `config.py` 中的 `NUM_CLIENTS`，观察不同客户端数量下的聚合结果；
2. 修改 `VECTOR_DIM`，观察高维更新向量中的掩码抵消；
3. 在 `client.py` 中打印本地掩码，理解每个客户端上传值的构成；
4. 在 `server.py` 中尝试读取单个客户端上传值，分析其与真实更新之间的差异；
5. 删除某一个客户端上传结果，观察两两掩码无法完全抵消的问题。

## 7. 适用范围与限制

本项目适用于联邦学习、隐私计算和数据安全课程中的原理演示。它只实现安全聚合的最小教学流程，重点在于帮助学生理解“可聚合、不可单独观察”的基本思想。

本项目不包含以下能力：

- 真实网络通信；
- 生产级密码协议；
- 客户端掉线恢复；
- 恶意客户端防护；
- 密钥协商与身份认证；
- 与真实联邦学习框架的集成。

因此，本项目不能直接用于生产环境或真实隐私保护任务。

## 8. 项目声明

**Project Name:** secure-aggregation-mini  
**Project Authors:** Zhi Li, Tianxin Liu, Bingbin Ye  
**Affiliation:** College of Cyber Security, Jinan University  
**作者单位：** 暨南大学网络空间安全学院

This project is developed as a lightweight teaching and hands-on learning tool for understanding the basic workflow of secure aggregation in federated learning and privacy computing. It is intended for undergraduate and graduate students to conduct simple verification experiments on privacy-preserving aggregation principles.
