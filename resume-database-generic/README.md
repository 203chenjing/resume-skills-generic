# 简历素材库 · Your Resume Source of Truth

> **写一次，投百岗 — 在简历筛选开战前，把 STAR、指标和待确认项装进你的弹药库。**  
> **Write once, apply everywhere — stock STAR, metrics, and open items before the battle of resume screening.**

[![Version](https://img.shields.io/badge/version-v1.0.0-blue)](SKILL.md)
[![Cursor Skill](https://img.shields.io/badge/platform-Cursor%20Agent%20Skill-000000)](https://cursor.com)
[![Language](https://img.shields.io/badge/language-中文%20%7C%20Chinese-orange)](#)

面向 **Cursor Agent** 的简历经历素材库技能：从原始简历与你确认的信息出发，维护 `简历数据库.md`，沉淀项目贡献、量化结果、层级规则与 `[待确认]` 项。**只归档、不投递** — 本技能不输出定向简历或 PDF；按岗改写请用配套技能。

A **Cursor Agent Skill** for building and maintaining **`简历数据库.md`** — your structured experience archive with STAR narratives, metrics, hierarchy rules, and flagged open items. **Archive only** — no tailored resume or PDF here; use the companion tailor skill when you're ready to fight the screen.

---

## 故事 · The moment you need this

你又打开那份旧 PDF，准备改第 3 个岗位的简历。上次实习的细节——到底提升了多少留存？那个 A/B 测试的样本量是多少？——散落在聊天记录、复盘文档和记忆碎片里。翻半小时，还是不敢写进简历，怕面试被追问。

更糟的是：上礼拜你为「岗位 A」压缩掉的一段调研经历，这次投「岗位 B」正好是关键词——但 PDF 里已经删没了，细节也记不清了。简历筛选看的不是你有没有做过，而是 **你能不能快速拿出和 THIS 岗位最相关的证据**。没有单一事实来源，每次定向改写都在重新挖坟，细节丢一次就少一次。

`简历数据库.md` 是你的 **弹药库**：开战前把 STAR、数字、并列项目、待核实项全部归位。到了简历筛选这一关，你不是临时拼凑，而是 **精准调取** — 这个岗用增长项目打头，那个岗换数据分析主线，同一份真相，不同的出击角度。

You open that old PDF again — third role this week. Details from your last internship: how much did retention actually improve? What was the A/B sample size? They're scattered across chat logs, retros, and memory. Thirty minutes later, you still won't put them on the resume — afraid of the interview follow-up.

Worse: the user-research bullet you cut for a *product* application was exactly what *user ops* needs — but it's gone from the PDF, and the nuance is fading. Screening isn't asking whether you did the work. It's asking whether you can **surface the right evidence for THIS role, fast**. Without a single source of truth, every tailoring session re-digs the PDF and loses detail.

`简历数据库.md` is your **ammunition closet**: STAR, numbers, parallel projects, and open questions filed before the fight. When screening hits, you don't scramble — you **draw the right round** — growth story for this JD, analytics thread for that one. Same truth, different angle.

---

## 为什么是它 · Why this skill

### 问题 · The problem

没有素材库时，每次按 JD 改简历都是 **从零考古**：翻 PDF、搜聊天记录、猜指标、合并经历时丢掉细节。筛选失败，往往不是因为你不匹配，而是 **这一刻拿不出对的证据** — 关键词对不上、最强项目没排在显眼处、量化结果临时凑不出来。改得越急，丢得越多。

Without a database, every JD tailoring session is **archaeology**: dig the PDF, search chats, guess metrics, lose nuance when you merge bullets. Screening fails not because you're unqualified — because **you can't surface the right evidence in time** — keywords miss, the best project isn't visible, numbers aren't at hand. Rush the edit, lose the detail.

### 洞察 · The insight

简历筛选是一场 **速度战**：HR 和 ATS 在几秒内决定「像不像这个岗」。赢家通常在投之前就完成了分类——哪些经历对哪类 JD 能打、数字是否经核实、并列项目如何切换主线。这些不该在凌晨改简历时现想；应该是一份 **随时可调用的真相档案**。

Screening is a **speed game**: HR and ATS decide *does this look like the role?* in seconds. Winners pre-sort — which experiences fit which JD families, which numbers are verified, how to switch emphasis across parallel projects. That shouldn't happen at midnight during an edit. It should live in a **truth archive you can call on instantly**.

### 方案 · The solution

`resume-database-generic` 维护你的 `简历数据库.md`：

- 从原始材料 **只搬运、不润色** 导入可验证事实
- 按雇主 / 项目分层整理，补全 STAR 叙事
- 集中记录量化指标、关键词标签与 `[待确认]` 区
- 压缩或合并后的细节 **回写库内**，避免下次再丢

`resume-database-generic` maintains your `简历数据库.md`:

- Import **verified facts only** — transport, don't polish
- Layer by employer / project; build STAR narratives
- Central ledger for metrics, keyword tags, and `[待确认]` items
- **Write back** compressed or merged detail so the next round doesn't start from zero

### 结果 · The outcome

**之前：** 每投一岗重新翻 PDF，细节越改越薄，筛选时拿不出最匹配的项目线。  
**之后：** 一份库走百岗 — 定向改写时直接映射证据，筛选关看到的是 **这一岗最值得打的那几枪**。配合 `resume-tailor-generic`，从弹药库到一页 PDF，链路完整。

**Before:** Re-dig the PDF per application, thinner detail each time, wrong project line when screening looks for fit.  
**After:** One library, many roles — tailoring maps evidence instantly; the screen sees **the strongest match for this JD**. Pair with `resume-tailor-generic` for the full path from closet to one-page PDF.

---

## 适合谁 · Who it's for

- **首次接入**、后续要投多个岗位的人 — 先建库，再改写，别在筛选前裸奔
- 同一家公司有 **并列项目 / 多条工作线**，需要按 JD 切换主线
- 指标散落、记不清出处，需要 `[待确认]` 集中管理
- 刚结束实习 / 项目，趁细节还在， **一次性归档**

Anyone **setting up for multiple applications** — build the closet before the screen; candidates with **parallel projects or work lines** at one employer; anyone whose metrics live in fragments and need a `[待确认]` ledger; anyone who just finished an internship or project and should **archive while the detail is fresh**.

---

## 工作流 · Workflow

```text
原始简历 + 用户确认信息
        ↓
  导入事实（只搬运，不润色）
        ↓
  按雇主整理 → 补 STAR → 指标 / 关键词 / 待确认区
        ↓
  输出 / 更新 简历数据库.md
        ↓
  下一步：resume-tailor-generic 按 JD 改写
```

**推荐搭配 · Best paired with:** `resume-tailor-generic` — 素材库是 **全量真相**，改写技能是 **单岗交付**。库不负责过筛选；但没有库，改写技能也无弹可打。  
Database holds the **full truth**; tailor skill delivers **one role at a time**. The closet doesn't pass the screen — but without it, tailoring fires blanks.

---

## 快速开始 · Quick start

### 1. 安装到 Cursor · Install in Cursor

复制本目录到 Cursor 技能路径之一：

Copy this folder into one of your Cursor skills paths:

| 范围 Scope | 路径 Path |
|------------|-----------|
| 项目级 Project | `<your-project>/.cursor/skills/resume-database-generic/` |
| 个人级 User | `~/.cursor/skills/resume-database-generic/`（Windows: `%USERPROFILE%\.cursor\skills\`） |

确认存在 `SKILL.md`，在对话中说：**「用 resume-database-generic 根据这份简历建立素材库。」**  
Ensure `SKILL.md` exists, then prompt: **"Use resume-database-generic to build my experience database from this resume."**

### 2. 准备输入 · Prepare inputs

- **原始简历** — PDF / Markdown / DOCX / 粘贴文本
- **可选** — 已有 `简历数据库.md`、实习复盘、项目文档
- **模板** — [resume-database-template.md](resume-database-template.md) 或 [resume-database-l012-template.md](resume-database-l012-template.md)

### 3. 输出 · Output

- 创建或更新 **`简历数据库.md`**（或你指定的路径）
- 对话中说明：新增区块、仍待确认项、是否建议下一步按 JD 改简历

Creates or updates **`简历数据库.md`** (or your chosen path). The agent summarizes what was added, what's still open, and whether to tailor next.

---

## 包内文件 · What's inside

| 文件 File | 用途 Purpose |
|-----------|--------------|
| [SKILL.md](SKILL.md) | **主入口** — 何时建库、分工、质量清单 |
| [reference.md](reference.md) | 逐步细则、层级与 STAR 规则 |
| [examples.md](examples.md) | 素材库条目示例（虚构占位） |
| [resume-database-template.md](resume-database-template.md) | 标准空白模板 |
| [resume-database-l012-template.md](resume-database-l012-template.md) | L0–L2 层级模板 |
| [CASES.md](CASES.md) | 3 个典型使用场景 |

---

## 典型场景 · Example prompts

- 「请根据这份 PDF 建立简历素材库，未核实数据标注待确认。」  
  *"Build my experience database from this PDF — flag unverified metrics."*
- 「请将近期实习经历补入素材库，整理可量化成果。」  
  *"Add my latest internship to the database with quantified outcomes."*
- 「同一家公司有两个并列项目，请在素材库中分开整理。」  
  *"I had two parallel projects at one company — structure them separately in the DB."*

更多见 [CASES.md](CASES.md) · See [CASES.md](CASES.md) for full scenarios.

---

## 与改写技能的分工 · Division of labor

| 本技能 resume-database-generic | 配套 resume-tailor-generic |
|--------------------------------|----------------------------|
| 沉淀全部可验证事实与 STAR | 按单个 JD 筛选、压缩、排序 |
| 记录层级与映射规则 | 执行合并/拆条与投递版式 |
| 管理指标来源与待确认项 | 输出 Markdown + 一页 PDF |

---

## 隐私 · Privacy

示例使用虚构信息（张三、示例公司等）。请替换为你**经确认**的真实材料，勿将他人隐私提交到公开仓库。  
Samples use fictional placeholders. Replace with **your verified** information; never commit others' private data.

---

**v1.0.0** · 内容创作 · 求职工具 · Cursor Agent Skill
