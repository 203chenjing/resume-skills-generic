# 简历弹药库 · Resume Vault

# 写一次，百岗可调 — 结构化经历证据档案

# Write Once, Deploy Everywhere — Structured Experience Evidence Archive

> **Cursor Agent Skill · 经历入库层 · 将可验证事实归档为 `简历数据库.md`，供匹配引擎跨岗位复用。**  
> **Cursor Agent Skill · Experience Ingestion Layer · Archives verified facts into `简历数据库.md` for cross-role reuse by the matching engine.**

[![Version](https://img.shields.io/badge/version-v1.0.0-blue)](SKILL.md)
[![Cursor Skill](https://img.shields.io/badge/platform-Cursor%20Agent%20Skill-000000)](https://cursor.com)
[![Language](https://img.shields.io/badge/language-中文%20%7C%20Chinese-orange)](#)

---

## 产品定位 · Product Positioning

**Resume Vault** 是简历投递流水线的 **经历入库层（Ingestion Layer）**。基于原始简历与用户确认信息，Agent 将项目贡献、量化指标、STAR 叙事及 `[待确认]` 项结构化写入 `简历数据库.md`，形成可供下游匹配引擎调用的证据档案。本模块 **仅负责归档，不输出定向简历或 PDF**；按岗改写请使用配套 [**ScreenPass Resume**](../resume-screenpass/)。

**Resume Vault** is the **Experience Ingestion Layer** of the resume delivery pipeline. From source resumes and user-confirmed facts, the Agent structures project contributions, quantified metrics, STAR narratives, and `[待确认]` items into `简历数据库.md` — an evidence archive callable by the downstream matching engine. This module **archives only**; for role-specific tailoring, use [**ScreenPass Resume**](../resume-screenpass/).

---

## 核心能力 · Core Capabilities

| 能力 Capability | 说明 Description |
|-----------------|------------------|
| **事实搬运** | 从原始材料导入可验证信息，只归档、不润色 |
| **STAR 结构化** | 按雇主 / 项目分层，补全情境、任务、行动、结果叙事 |
| **指标台账** | 集中管理量化结果、关键词标签与数据来源 |
| **待确认管理** | 未核实数据统一标注 `[待确认]`，避免误写入投递稿 |
| **回写机制** | 改写环节压缩或合并的细节回写库内，防止证据流失 |

---

## 问题与方案 · Problem → Solution

**问题：** 缺乏结构化证据档案时，每次按 JD 改写简历均需重新翻阅 PDF、检索聊天记录、临时拼凑指标。细节在反复压缩中持续流失，筛选关需要的核心关键词与量化证据往往无法及时调取。

**Problem:** Without a structured evidence archive, every JD tailoring session re-opens PDFs, searches chat logs, and assembles metrics ad hoc. Detail erodes through repeated compression; the keywords and quantified evidence screening requires are rarely available on demand.

**方案：** `resume-vault` 在执行任何定向改写之前，先将全部可验证事实归位至 `简历数据库.md`。下游匹配引擎按 JD 需求从档案中选取证据，而非每次从零考古。一份档案，支撑百次岗位适配。

**Solution:** `resume-vault` consolidates all verified facts into `简历数据库.md` before any tailoring begins. The downstream matching engine selects evidence from the archive per JD requirements — not from scratch each time. One archive, many role adaptations.

---

## 工作流 · Workflow

```text
原始简历 + 用户确认信息
        ↓
  事实导入（只搬运，不润色）
        ↓
  雇主 / 项目分层 → STAR 补全 → 指标 / 关键词 / 待确认区
        ↓
  输出 / 更新 简历数据库.md
        ↓
  下游：resume-screenpass 证据链匹配改写
```

**推荐搭配：** [过筛选改简历 · ScreenPass Resume](../resume-screenpass/) — Vault 持有全量真相档案，ScreenPass 执行单岗证据链匹配与 PDF 交付。

---

## 适用对象 · Who It's For

- **多岗投递规划者** — 首次接入时先建库，再进入改写流水线
- **并列项目持有者** — 同一雇主下多条工作线，需记录按岗切换规则
- **指标管理需求者** — 量化结果散落多处，需集中台账与待确认标注
- **新经历归档者** — 实习或项目结束后趁细节完整，一次性结构化入库

---

## 快速开始 · Quick Start

### 1. 安装 Agent Skill

复制本目录至 Cursor 技能路径：

| 范围 Scope | 路径 Path |
|------------|-----------|
| 项目级 Project | `<your-project>/.cursor/skills/resume-vault/` |
| 个人级 User | `~/.cursor/skills/resume-vault/`（Windows: `%USERPROFILE%\.cursor\skills\`） |

确认 `SKILL.md` 存在后，在对话中输入：**「用 resume-vault 根据这份简历建立结构化素材库。」**

### 2. 准备输入

- **原始简历** — PDF / Markdown / DOCX / 粘贴文本
- **可选补充** — 已有 `简历数据库.md`、实习复盘、项目文档
- **空白模板** — [resume-database-template.md](resume-database-template.md) 或 [resume-database-l012-template.md](resume-database-l012-template.md)

### 3. 预期输出

- 创建或更新 **`简历数据库.md`**
- Agent 汇报：新增区块、待确认项、是否建议进入 ScreenPass 改写流程

---

## 包内文件 · Package Contents

| 文件 File | 用途 Purpose |
|-----------|--------------|
| [SKILL.md](SKILL.md) | **主入口** — 触发条件、工作流、质量清单 |
| [reference.md](reference.md) | 逐步细则、层级规则与 STAR 标准 |
| [examples.md](examples.md) | 素材库条目示例（虚构占位） |
| [resume-database-template.md](resume-database-template.md) | 标准空白模板 |
| [resume-database-l012-template.md](resume-database-l012-template.md) | L0–L2 层级模板 |
| [CASES.md](CASES.md) | 典型使用场景 |

---

## 典型指令 · Example Prompts

- 「请根据这份 PDF 建立结构化简历素材库，未核实数据标注待确认。」
- 「请将近期实习经历增量写入素材库，整理可量化成果。」
- 「同一家公司有两个并列项目，请在素材库中分层归档并标注按岗映射规则。」

更多场景见 [CASES.md](CASES.md)。

---

## 模块分工 · Division of Labor

| resume-vault（本模块） | resume-screenpass（配套） |
|------------------------|---------------------------|
| 沉淀全部可验证事实与 STAR | 按 JD 驱动匹配引擎筛选证据 |
| 记录层级规则与按岗映射 | 执行 STAR 改写与版式校验 |
| 管理指标来源与待确认项 | 输出 Markdown + 一页 PDF |

---

## 隐私 · Privacy

示例使用虚构占位信息。请替换为经确认的真实材料，勿将他人隐私提交至公开仓库。

---

**v1.0.0** · Cursor Agent Skill · 经历入库层 · Experience Ingestion Layer
