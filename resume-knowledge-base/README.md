# 简历知识库 · Resume Knowledge Base

# 写一次，百岗可调 — 你的经历证据档案

> **Cursor Agent Skill · 上游入库层**  
> 把可验证事实归档成 `简历数据库.md`，供下游匹配引擎跨岗位复用。

[![Version](https://img.shields.io/badge/version-v1.0.0-blue)](SKILL.md)
[![Cursor Skill](https://img.shields.io/badge/platform-Cursor%20Agent%20Skill-000000)](https://cursor.com)

---

## 上游模块：事实底座

改简历最难的不是「写」，是「找」——指标散落在 PDF、聊天记录和脑子里，每次按 JD 改稿都要重新考古。知识库解决这个问题：**把经历沉淀为单一事实来源**，下游只在已确认内容里选材组合。

AI 编造的根源，往往是手里没有真相。知识库是第一道闸：只搬运、不润色，不确定的统一标 `[待确认]`。

*Resume Knowledge Base is the upstream evidence layer. Ingest once; every downstream rewrite pulls from the same source of truth.*

---

## 核心能力

| 能力 | 说明 |
|------|------|
| **事实搬运** | 从原始材料导入，只归档、不润色 |
| **STAR 结构化** | 按雇主 / 项目分层，补全情境→任务→行动→结果 |
| **指标台账** | 量化结果、关键词标签、数据来源集中管理 |
| **待确认管理** | 未核实数据统一标 `[待确认]`，不误写入投递稿 |
| **回写机制** | 改写环节被压缩的细节回写库内，防止证据流失 |

**本模块不做：** 定向改写、JD 匹配、PDF 导出——那是 [简历优化 · Resume Optimizer](../resume-optimizer/) 的职责。

---

## 在流水线中的位置

```text
原始简历 + 用户确认信息
        ↓
  事实导入（只搬运，不润色）
        ↓
  雇主 / 项目分层 → STAR 补全 → 指标 / 关键词 / 待确认区
        ↓
  输出 / 更新 简历数据库.md
        ↓
  下游：resume-optimizer 证据链匹配改写
```

**推荐搭配：** [简历优化 · Resume Optimizer](../resume-optimizer/) — 知识库持有全量真相，优化模块打定向稿。

---

## 怎么用

### 1. 安装

复制本目录至 Cursor 技能路径：

| 范围 | 路径 |
|------|------|
| 项目级 | `<your-project>/.cursor/skills/resume-knowledge-base/` |
| 个人级 | `~/.cursor/skills/resume-knowledge-base/` |

### 2. 准备输入

- **原始简历** — PDF / Markdown / DOCX / 粘贴文本
- **可选** — 已有 `简历数据库.md`、实习复盘、项目文档
- **空白模板** — [resume-database-template.md](resume-database-template.md)

### 3. 开聊

**「用 resume-knowledge-base 根据这份简历建立结构化素材库。」**

你会得到：创建或更新的 `简历数据库.md`，以及新增区块、待确认项、是否建议进入简历优化的汇报。

---

## 适合谁

- **多岗投递规划者** — 首次接入先建库，再进改写流水线
- **并列项目持有者** — 同雇主多条工作线，记录按岗切换规则
- **指标管理需求者** — 量化结果散落各处，要集中台账
- **新经历归档者** — 实习 / 项目刚结束，趁细节完整一次性入库

---

## 典型指令

- 「请根据这份 PDF 建立结构化简历素材库，未核实数据标注待确认。」
- 「请将近期实习经历增量写入素材库，整理可量化成果。」
- 「同一家公司有两个并列项目，请在素材库中分层归档并标注按岗映射规则。」

更多场景 → [CASES.md](CASES.md)

---

## 包内文件

| 文件 | 用途 |
|------|------|
| [SKILL.md](SKILL.md) | **主入口** — 触发条件、工作流、质量清单 |
| [reference.md](reference.md) | 逐步细则、层级规则与 STAR 标准 |
| [examples.md](examples.md) | 素材库条目示例（虚构占位） |
| [CASES.md](CASES.md) | 典型使用场景 |

---

## 模块分工

| resume-knowledge-base（本模块） | resume-optimizer（配套） |
|--------------------------------|--------------------------|
| 沉淀全部可验证事实与 STAR | 按 JD 驱动匹配引擎筛选证据 |
| 记录层级规则与按岗映射 | 执行 STAR 改写与版式校验 |
| 管理指标来源与待确认项 | 输出 Markdown + 一页 PDF |

---

示例使用虚构占位信息。真实材料请自行替换，勿将他人隐私提交至公开仓库。

`v1.0.0` · Experience Ingestion Layer
