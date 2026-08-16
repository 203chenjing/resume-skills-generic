# 六秒过筛选 · Agent 原生简历投递流水线

# Pass the 6-Second Screen · Agent-Native Resume Delivery Pipeline

> **面向 Cursor Agent 的双模块简历工作流：经历结构化入库 → JD 证据链匹配 → 版式校验 → 一页 PDF 交付。**  
> **A dual-module Cursor Agent workflow — structured experience vaulting → JD evidence-chain matching → layout validation → single-page PDF delivery.**

[![Cursor](https://img.shields.io/badge/platform-Cursor%20Agent%20Skills-000000)](https://cursor.com)
[![Language](https://img.shields.io/badge/language-中文%20%7C%20English-orange)](#)

---

## 产品定义 · Product Definition

**Resume Skills Generic** 是一套面向求职场景的 Cursor Agent Skill 组合，将简历投递从「反复翻改旧 PDF」升级为可复用的 Agent 工作流。上游模块沉淀可验证经历档案，下游模块执行 JD 驱动的证据链匹配与版式校验，最终输出恰好一页、可溯源的投递 PDF。

**Resume Skills Generic** is a Cursor Agent Skill suite for job applications. It replaces ad-hoc PDF editing with a repeatable agent workflow: an upstream module archives verified experience, a downstream module runs JD-driven evidence-chain matching and layout validation, and delivers a traceable, exactly-one-page PDF.

---

## 问题与方案 · Problem → Solution

**问题：** 招聘方与 ATS 通常在 **6–10 秒** 内完成初筛，判定依据并非履历全貌，而是关键词可见度、首屏证据密度与岗位叙事一致性。缺乏单一事实来源时，每次定向改写都需重新考古原始材料，细节在压缩与合并中持续流失；通用 AI 润色虽能美化措辞，却无法建立可回溯的证据链，筛选过关后往往在面试环节失守。

**Problem:** Recruiters and ATS systems typically complete first-pass screening in **6–10 seconds**, judging keyword visibility, above-the-fold evidence density, and role narrative alignment — not your full career history. Without a single source of truth, every tailoring session re-excavates source material and loses detail through compression. Generic AI polish improves wording but cannot establish a traceable evidence chain — screening gains collapse in interviews.

**方案：** 本套件以 **Ingest → Vault → Match → Render → PDF** 五步流水线组织投递流程。`resume-vault` 将原始简历与用户确认事实结构化归档为 `简历数据库.md`；`resume-screenpass` 解析目标 JD、驱动匹配引擎选取证据、执行 STAR 改写与版式校验，导出经脚本验证的单页 PDF。全流程坚持不编造、人工审阅、证据可溯源。

**Solution:** This suite organizes delivery as a five-stage pipeline — **Ingest → Vault → Match → Render → PDF**. `resume-vault` archives verified facts into `简历数据库.md`; `resume-screenpass` parses the target JD, drives the matching engine to select evidence, executes STAR rewriting and layout validation, and exports a script-verified single-page PDF. The full workflow enforces no fabrication, human-in-the-loop review, and traceable evidence.

---

## 产品模块 · Product Modules

| 模块 Module | 定位 Positioning | 能力标签 Capability Tags |
|-------------|------------------|--------------------------|
| [**简历弹药库 · Resume Vault**](resume-vault/) | 经历结构化入库 · Experience Ingestion Layer | `证据归档` `STAR 结构化` `指标台账` `待确认管理` `多岗复用` |
| [**过筛选改简历 · ScreenPass Resume**](resume-screenpass/) | JD 匹配改写引擎 · JD Matching & Render Engine | `证据链映射` `匹配引擎` `STAR 改写` `版式校验` `一页 PDF` |

---

## 架构与工作流 · Architecture & Workflow

```mermaid
flowchart LR
    A[Ingest<br/>原始简历 + 确认事实] --> B[Vault<br/>简历数据库.md]
    B --> C[Match<br/>JD 证据链映射]
    C --> D[Render<br/>STAR 改写 + 模板]
    D --> E[PDF<br/>版式校验 + 交付]
```

```text
Ingest    原始简历 / 复盘文档 / 用户确认事实
   ↓
Vault     resume-vault  →  简历数据库.md（结构化证据档案）
   ↓
Match     resume-screenpass  →  JD 解析 + 证据链映射 + 匹配排序
   ↓
Render    STAR 改写 + Markdown 模板填充
   ↓
PDF       版式预检 → 脚本导出 → 公司+姓名+岗位.pdf（恰好 1 页）
```

---

## 快速安装 · Quick Install

### 1. Clone

```bash
git clone https://github.com/203chenjing/resume-skills-generic.git
cd resume-skills-generic
```

### 2. 部署 Agent Skills · Deploy to Cursor

将 `resume-vault/` 与 `resume-screenpass/` 复制至 Cursor 技能目录：

| 范围 Scope | 路径 Path |
|------------|-----------|
| 项目级 Project | `<your-project>/.cursor/skills/` |
| 个人级 Global | `~/.cursor/skills/`（Windows: `%USERPROFILE%\.cursor\skills\`） |

### 3. 启动工作流 · Invoke

- **建库：**「用 resume-vault 根据这份简历建立结构化素材库。」  
  *"Use resume-vault to build a structured experience database from this resume."*
- **改写：**「用 resume-screenpass 按这份 JD 执行证据链匹配改写，导出一页 PDF。」  
  *"Use resume-screenpass to match evidence to this JD and export a one-page PDF."*

各模块详细文档见 [`resume-vault/README.md`](resume-vault/README.md) 与 [`resume-screenpass/README.md`](resume-screenpass/README.md)。

---

## 适用对象 · Who It's For

| 人群 Segment | 典型场景 Typical Use Case |
|--------------|---------------------------|
| **多岗投递者** | 校招、实习、跳槽等需面向多个 JD 快速产出定向版本 |
| **复杂经历持有者** | 同一雇主下并列项目或多条工作线，需按岗切换叙事主线 |
| **质量优先者** | 要求证据可溯源、拒绝 AI 编造，需脚本校验版式与页数 |
| **Agent 工作流用户** | 已在 Cursor 中使用 Agent Skill，希望将简历投递纳入可复用流水线 |

---

## 信任与合规 · Trust & Compliance

- **不编造事实** — 缺指标标注 `[待补充：指标]` 或 `[待确认]`，禁止凭空生成经历
- **人工审阅闭环** — Agent 产出内容须经用户确认后方可导出终稿
- **证据可溯源** — 每条投递表述可回溯至 `简历数据库.md` 或原始材料
- **隐私保护** — 示例与文档使用虚构占位信息；请替换为经确认的真实材料，勿将他人隐私提交至公开仓库

- **No fabrication** — missing metrics flagged as `[待补充：指标]` or `[待确认]`; no invented experience
- **Human-in-the-loop** — agent output requires user confirmation before final export
- **Traceable evidence** — every claim maps back to `简历数据库.md` or source material
- **Privacy** — samples use fictional placeholders; replace with verified information only

---

**v1.0.0** · Cursor Agent Skills · 求职工具 · Agent Workflow
