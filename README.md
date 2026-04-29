# Edu Agent Mimo Demo

一个用于申请 / 演示小米 Mimo 使用资格的多 Agent 教育内容生产系统原型。

本项目模拟一个面向小学语文、数学教辅素材生产的智能 Agent 工作流，支持：

- 教材内容结构化解析
- 拼音、错别字、标题规则、编号规则校验
- X-Y 页码规划
- 多页拆分与版式规划
- 英文图像生成提示词生成
- 生成结果质检
- 根据质检结果自动生成优化建议
- 可扩展为 Mimo / OpenAI / Qwen / Claude 等模型后端

> 当前代码是一个可运行的工程骨架，核心 Agent 逻辑已封装。LLM 调用层默认使用 MockLLM，方便无 Key 启动；接入 Mimo 时只需要实现 `src/llm/mimo_client.py` 中的请求逻辑。

---

## 适合展示给平台的项目说明

本项目不是简单 Prompt 工具，而是一个多 Agent 协作的长链路教育内容生产系统。它将“资料输入 → 结构化解析 → 规则判断 → 知识校验 → 版式规划 → 提示词生成 → 结果质检 → 自动优化”串成闭环，可用于批量生成小学语文、数学等学科的知识图解、背默练习页、看拼音写词语页和复习封面。

系统重点验证模型在以下能力上的表现：

1. 长上下文理解
2. 多步骤任务规划
3. 中文教育内容校验
4. 复杂规则遵循
5. 多 Agent 协同
6. 图片生成提示词工程
7. 自动质检与闭环优化

---

## 项目结构

```bash
edu-agent-mimo-demo/
├── README.md
├── requirements.txt
├── .env.example
├── run_demo.py
├── src/
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── orchestrator.py
│   ├── agents/
│   │   ├── base.py
│   │   ├── content_parser.py
│   │   ├── rule_planner.py
│   │   ├── knowledge_checker.py
│   │   ├── layout_planner.py
│   │   ├── prompt_generator.py
│   │   ├── quality_inspector.py
│   │   └── optimizer.py
│   └── llm/
│       ├── base.py
│       ├── mock_client.py
│       └── mimo_client.py
└── examples/
    └── sample_request.json
```

---

## 快速开始

```bash
pip install -r requirements.txt
python run_demo.py
```

启动 API：

```bash
uvicorn src.app:app --reload --port 8000
```

调用接口：

```bash
curl -X POST http://127.0.0.1:8000/workflow/generate \
  -H "Content-Type: application/json" \
  -d @examples/sample_request.json
```

---

## 接入 Mimo 的位置

在 `.env` 中填写：

```bash
MIMO_API_KEY=your_key_here
MIMO_BASE_URL=https://api.example.com/v1
MIMO_MODEL=mimo-agent-model
LLM_PROVIDER=mimo
```

然后在 `src/llm/mimo_client.py` 中按 Mimo 实际 API 文档补齐请求参数即可。

---

## 示例输出

系统会输出：

- 结构化课文内容
- 规则判断结果
- 校验报告
- 页面拆分方案
- 图像生成提示词
- 质检报告
- 下一轮优化建议

---

## 可评估指标

后续可以接入以下指标：

- 内容结构化准确率
- 拼音校验召回率
- 标题规则命中率
- X-Y 编号正确率
- 图片提示词一次可用率
- 质检问题召回率
- 人工修改时间下降比例
- 单课批量生产耗时
