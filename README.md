# 简历投递流水线

# Resume Pipeline

**Agent 原生双模块简历工作流** — 管简历、投简历，不是「写」简历。

*Manage & apply with evidence—not blank-page writing.*

[![Cursor](https://img.shields.io/badge/platform-Cursor%20Agent%20Skills-000000)](https://cursor.com)
[![Language](https://img.shields.io/badge/language-中文%20%7C%20English-orange)](#)

**招聘方只给你 6 秒，你的简历准备好了吗？**

*Recruiters give you about six seconds. Is your resume ready for that scan?*

---

## 你也有过这种时刻

桌面上躺着 `简历_最终版_不改了_真的.pdf`，版本号已经排到 v7。

面试时被问：「你简历上这个指标，具体怎么算的？」——你愣了两秒，因为那个数字是某次改稿时「感觉差不多」写上去的。

**简历不是文学创作，是证据呈现。** 招聘方要的不是文采，是能在六秒内验证、能在面试里追问的事实。

---

## 静态文档 vs 动态博弈

求职是一场动态博弈：每个 JD 强调的能力不同，同一段经历要讲不同的主角。但大多数人手里只有一份静态 Word——

- 投 AI 产品岗，增长数据被埋在第三段；
- 投运营岗，产品方法论占了半页；
- 改到第五版，早期的量化指标找不到了。

**六秒定生死，你却在废墟里考古。** 翻旧 PDF、扒聊天记录、临时凑数字——细节改着改着就丢了，下次还得从零开始。

通用 AI 润色能把句子写漂亮，却解决不了信任：不知道改了什么、为什么改、有没有编造。面试一问细节就穿帮。

---

## 我们需要的是一条流水线，不是一次次手工作坊

按岗改稿是有效求职的前提，但完整走一遍「读懂岗位 → 选材 → 改写 → 检查」往往要 **1–2 小时**。投到第五家，大多数人退回万金油简历——不是不想认真投，是**边际成本太高**。

这套工具把流程拆成可复用的 Agent 流水线：**上游沉淀证据，下游按 JD 匹配改写**。选材不是创作，效率交给 AI，**定稿权留给你**。

*What you need is a pipeline—not a fresh hand-craft job for every application.*

---

## 双模块 Cursor Agent Skill

| 模块 | 角色 |
|------|------|
| [简历知识库 · Resume Knowledge Base](resume-knowledge-base/) | 上游 — 结构化归档可验证事实 |
| [简历优化 · Resume Optimizer](resume-optimizer/) | 下游 — JD 驱动选材、STAR 改写、一页 PDF |

```mermaid
flowchart LR
    A[采集<br/>原始简历 + 确认事实] --> B[归档<br/>简历数据库.md]
    B --> C[匹配<br/>JD 证据链映射]
    C --> D[生成<br/>STAR + 模板]
    D --> E[导出<br/>版式校验 + PDF]
```

---

### 上游：简历知识库 · Resume Knowledge Base

**写一次，百岗可调。**

把原始简历与你确认过的事实，结构化归档成 `简历数据库.md`：STAR、量化指标、`[待确认]` 台账集中管理。只负责入库，不润色、不定向、不出 PDF——下游匹配引擎直接调用全量证据。

→ 详细说明：[resume-knowledge-base/README.md](resume-knowledge-base/README.md)

---

### 下游：简历优化 · Resume Optimizer

**六秒定生死，证据链说话。**

解析目标 JD → 驱动匹配引擎选证据 → 强匹配前置、弱相关压缩 → STAR 改写 → 版式校验 → **恰好一页 PDF**。每条 bullet 能回溯到知识库或原始材料，面试敢讲、敢举证。

有知识库效果拉满；没有也能跑，但每次从零考古。

→ 详细说明：[resume-optimizer/README.md](resume-optimizer/README.md)

---

## 全流程五步

```text
采集    原始简历 / 复盘文档 / 用户确认事实
  ↓
归档    resume-knowledge-base  →  简历数据库.md（结构化证据档案）
  ↓
匹配    resume-optimizer  →  JD 解析 + 证据链映射 + 匹配排序
  ↓
生成    STAR 改写 + Markdown 模板填充（人工审阅确认）
  ↓
导出    版式预检 → 脚本导出 → 公司+姓名+岗位.pdf（恰好 1 页）
```

---

## 谁适合用

| 你是谁 | 为什么需要它 |
|--------|-------------|
| **多岗投递者** | 校招 / 实习 / 跳槽，每个 JD 都要定向版本，拒绝万金油硬投 |
| **经历复杂者** | 同一家公司多个并列项目，按岗切换叙事主线与压缩策略 |
| **质量洁癖者** | 拒绝 AI 编造，要脚本校验 + 证据可溯源 + 人工定稿 |
| **Cursor 重度用户** | 想把简历投递纳入可复用、可审计的 Agent 工作流 |

---

## 三个原则

- **不编造** — 缺指标标 `[待补充：指标]` 或 `[待确认]`，绝不凭空写经历
- **可溯源** — 每条表述能回溯到 `简历数据库.md` 或原始材料
- **人工确认** — Agent 产出须经你逐条确认，才导出终稿；AI 提案，你裁决

---

## 三步开始

### 1. Clone

```bash
git clone https://github.com/203chenjing/resume-pipeline.git
cd resume-pipeline
```

### 2. 安装到 Cursor Skills 目录

| 范围 | 路径 |
|------|------|
| 项目级 | `<your-project>/.cursor/skills/` |
| 个人级 | `~/.cursor/skills/`（Windows: `%USERPROFILE%\.cursor\skills\`） |

将 `resume-knowledge-base/` 与 `resume-optimizer/` 两个文件夹复制进去。

### 3. 开聊

**建知识库：**「用 resume-knowledge-base 根据这份简历建立结构化素材库。」

**按 JD 优化出稿：**「用 resume-optimizer 按这份 JD 执行证据链匹配改写，导出一页 PDF。」

---

## English Overview

**Resume Knowledge Base + Resume Optimizer** is a two-module Cursor Agent Skill pipeline for job-specific resume tailoring—built on a simple premise: tailoring is *selection and compression*, not blank-page writing.

| Module | Role |
|--------|------|
| **Resume Knowledge Base** | Ingest verified facts into `简历数据库.md`—STAR entries, metrics, and `[pending]` flags. Write once, reuse across roles. |
| **Resume Optimizer** | Parse the JD, map evidence, rewrite in STAR format, validate layout, export a **single-page PDF**. Every bullet traces back to your knowledge base. |

**Three principles:** no fabrication · full evidence traceability · human-in-the-loop approval.

**Quick start:** clone the repo → copy both skill folders to `.cursor/skills/` → build your knowledge base → run Optimizer per JD.

---

招聘方的六秒，决定你的简历进不进下一轮。你的简历，值得一条**不丢证据、不编故事**的流水线。

*Every application deserves a version of your story that fits the role—without losing the facts behind it.*

`v1.0.0`
