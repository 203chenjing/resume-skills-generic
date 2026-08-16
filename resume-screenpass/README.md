# 过筛选改简历 · ScreenPass Resume

> **过筛选，再谈面试 — 把 JD 关键词、上 1/3 证据和一页密度，收成能活过简历筛选的定向 PDF。**  
> **Pass the screen first — map JD keywords, top-third evidence, and one-page density into a tailored PDF built to survive recruiter first-pass filtering.**

[![Version](https://img.shields.io/badge/version-v1.0.0-blue)](SKILL.md)
[![Cursor Skill](https://img.shields.io/badge/platform-Cursor%20Agent%20Skill-000000)](https://cursor.com)
[![Language](https://img.shields.io/badge/language-中文%20%7C%20Chinese-orange)](#)

面向 **Cursor Agent** 的通用中文简历改写技能：读取招聘要求（JD），从可验证经历中筛选证据，按 STAR 重写，套模板输出 Markdown，并通过脚本校验版式、导出一页 PDF。**不编造事实** — 缺指标标注 `[待补充：指标]`，交付前需人工审阅。

A **Cursor Agent Skill** for Chinese resume tailoring: ingest a JD, map **verified** experience, rewrite with STAR, output Markdown from templates, and export a **single-page PDF** with layout checks. **No fabrication** — missing metrics are flagged; human review before you send.

---

## 故事 · The moment you need this

你投完第 8 个岗，手机还亮着。JD 里写着「用户增长」「A/B 测试」「SQL」，你的简历上还是「参与项目、协助推进」——关键词对不上，ATS 和 HR 的第一遍筛选就直接把你划掉了。招聘方平均只在一份简历上停留 **6–10 秒**；他们看的不是你有没有经历，而是 **上 1/3 是否像这个岗的人**。

你试过让 AI 一键润色：措辞变漂亮了，面试一问细节却答不上来——因为那些数字和成果，根本没在你的素材里。或者 PDF 终于写满一页，导出却变成两页，版式空一块；再改一版，又错过投递窗口。

这个技能干的事很具体：**从 JD 反推证据链，把通用简历收成「这一岗」的一页定向稿** — 关键词可见、结构可扫、事实可溯源。不是替你编造亮点，而是让你在筛选关面前，看起来像对的人。

You've applied to eight roles and it's past midnight. The JD asks for *user growth*, *A/B testing*, *SQL* — your resume still says *participated in projects* and *assisted with initiatives*. Keywords don't match; ATS and recruiter **first-pass screening** move on. Recruiters spend roughly **6–10 seconds** per resume. They're not asking whether you have experience — they're asking whether the **top third looks like this role**.

Maybe you tried AI polish: prettier words, but the interview falls apart when they ask for details — because those metrics were never in your source material. Or the PDF spills to two pages, or looks hollow on one. Another edit, another missed window.

This skill does one thing clearly: **work backward from the JD, map verified evidence, and compress a generic resume into a one-page, role-aligned draft** — keywords visible, layout scannable, every claim traceable. Not invented highlights. A resume that can **pass the screen**.

---

## 为什么是它 · Why this skill

### 问题 · The problem

简历筛选（HR 人工扫读 + ATS 关键词匹配）是一道 **先过滤、后细读** 的关。大多数简历死在第一遍：JD 关键词没出现在显眼位置、经历和岗位叙事对不上、一页纸信息密度失衡，或者 AI 润色后面试无法举证 — 还没聊到能力，就已经出局。

Screening — human skim plus ATS keyword matching — is **filter first, read later**. Most resumes die on the first pass: JD terms missing from the visible zone, experience that doesn't read like this role, one-page density that's off, or AI-polished bullets you can't defend in an interview. You're out before the conversation starts.

### 洞察 · The insight

过筛选靠的不是「更华丽的形容词」，而是三件事同时成立：**关键词对上 JD**、**最强证据出现在上 1/3**、**一页内可快速扫读**。任何一条做不到，6–10 秒的初筛窗口就关上了。改写必须基于可验证事实；否则过了筛选，也会在面试里崩盘。

Passing the screen isn't about fancier adjectives. Three things must hold at once: **keywords match the JD**, **strongest evidence sits in the top third**, **one page that scans fast**. Miss any one, the 6–10 second window closes. Tailoring must trace to verified facts — otherwise screening success becomes interview failure.

### 方案 · The solution

`resume-screenpass` 把「按 JD 改写」做成可重复流程：

- 解析 JD → 映射你素材库/原始简历里的 **可验证证据**（不凭空加料）
- STAR 重写：弱相关压缩，强匹配前置，结果量化加粗
- 上 1/3 优先对齐岗位关键词与核心成果
- 套模板输出 Markdown → 人工审阅 → 版式预检 → 导出 **恰好一页** PDF

`resume-screenpass` turns JD tailoring into a repeatable pipeline:

- Parse the JD → map **verified evidence** from your database or source resume (no invented facts)
- STAR rewrite: compress weak matches, front-load strong ones, bold quantified outcomes
- Top third aligned to role keywords and headline wins
- Template Markdown → human review → layout preflight → export **exactly one page** PDF

### 结果 · The outcome

**之前：** 同一份通用简历四处投，关键词靠碰运气，HR 已读不回，面试被问「这数据哪来的」。  
**之后：** 每个 JD 一版定向稿 — 筛选能扫到匹配点，一页 PDF 可直接投递，每条经历能回溯到素材来源。诚实，但 **能打**。

**Before:** One generic resume everywhere, keywords a coin flip, *read no reply*, interview questions about numbers you can't source.  
**After:** One tailored draft per JD — screening can see the fit, one-page PDF ready to send, every bullet traceable to your source material. Honest, and **built to pass the screen**.

---

## 适合谁 · Who it's for

- 同时投多个岗位、需要 **按 JD 快速改一版** 的求职者（校招 / 实习 / 跳槽）
- 已有或正在建 `简历数据库.md`、希望改写 **不丢细节、不瞎编** 的人
- 受够了 PDF 超页、版式空疏，想要 **可脚本校验的一页终稿** 的人

Job seekers applying to **multiple roles** who need a fast, JD-specific version; anyone with (or building) `简历数据库.md` who wants tailoring **without losing nuance or fabricating**; anyone tired of two-page PDFs or sparse one-pagers who wants a **script-checkable single-page deliverable**.

---

## 工作流 · Workflow

```text
JD + 原始简历（或 简历数据库.md）
        ↓
  分析 JD → 映射证据 → STAR 改写
        ↓
  套模板写 Markdown → 人工审阅
        ↓
  check_resume_skill.py → markdown_resume_to_pdf.py
        ↓
  交付：公司+姓名+岗位.pdf（恰好 1 页）
```

**推荐搭配 · Best paired with:** [简历弹药库 · Resume Vault](../resume-vault/) — 先归档全部事实与 STAR，再按岗定向改写。没有素材库，每次改写都在重新翻 PDF；有库，筛选关用的是 **对的弹药**。  
Build your experience vault first, then tailor per application — the screen only sees what you can surface fast.

---

## 快速开始 · Quick start

### 1. 安装到 Cursor · Install in Cursor

复制本目录到 Cursor 技能路径之一：

Copy this folder into one of your Cursor skills paths:

| 范围 Scope | 路径 Path |
|------------|-----------|
| 项目级 Project | `<your-project>/.cursor/skills/resume-screenpass/` |
| 个人级 User | `~/.cursor/skills/resume-screenpass/`（Windows: `%USERPROFILE%\.cursor\skills\`） |

确认存在 `SKILL.md`，在对话中说：**「用 resume-screenpass 根据这份 JD 改简历并导出一页 PDF。」**  
Ensure `SKILL.md` exists, then prompt: **"Use resume-screenpass to tailor my resume to this JD and export a one-page PDF."**

### 2. 准备输入 · Prepare inputs

- **目标 JD** — 文本 / 链接 / 截图
- **原始简历** 或 **`简历数据库.md`**（来自 [Resume Vault](../resume-vault/)）
- **可选** — 岗位名、城市、证件照路径

### 3. 命令行脚本 · CLI scripts

在工作区简历目录下运行（将路径替换为你的 clone 路径）：

Run from your resume workspace (adjust paths to your clone):

```bash
# 版式预检 · Layout preflight (Markdown only)
python path/to/resume-screenpass/scripts/check_resume_skill.py 示例公司+张三+示例岗位.md --markdown-only

# 导出一页 PDF · Export one-page PDF (--preset tight | fill)
python path/to/resume-screenpass/scripts/markdown_resume_to_pdf.py 示例公司+张三+示例岗位.md --preset fill

# 证件照裁剪 · Crop profile photo (default 540×790)
python path/to/resume-screenpass/scripts/crop_profile_photo.py photo.jpg -o profile-photo-cropped.png
```

依赖 · Dependencies: **Pillow**（裁剪）; **Playwright** 等（PDF / 完整检查 — 见脚本头部说明）。

---

## 包内文件 · What's inside

| 文件 File | 用途 Purpose |
|-----------|--------------|
| [SKILL.md](SKILL.md) | **主入口** — 流程、硬门槛、快速开始 |
| [reference.md](reference.md) | 步骤细则、版式、证据规则、PDF 标准 |
| [examples.md](examples.md) | 表头、编号条目、技能行示例（虚构占位） |
| [resume-template.md](resume-template.md) | Markdown 简历模板 |
| [resume-database-template.md](resume-database-template.md) | 知识库空白模板 |
| [scripts/](scripts/) | 导出、检查、证件照裁剪 |
| [CASES.md](CASES.md) | 3 个典型使用场景 |

---

## 典型场景 · Example prompts

- 「请根据附件招聘要求改写简历，经历分条、结果加粗，导出一页 PDF。」  
  *"Tailor my resume to the attached JD, bold quantified results, export a one-page PDF."*
- 「素材库已就绪，按目标岗位 JD 改一版，弱相关经历压缩。」  
  *"My experience database is ready — create a user-ops intern version and compress weak matches."*
- 「内容已确认，请版式检查并导出，要求恰好一页。」  
  *"Content is final — run layout checks and export exactly one page."*

更多见 [CASES.md](CASES.md) · See [CASES.md](CASES.md) for full scenarios.

---

## 隐私 · Privacy

示例使用虚构信息（张三、示例公司等）。请替换为你**经确认**的真实材料，勿将他人隐私提交到公开仓库。  
Samples use fictional placeholders. Replace with **your verified** information; never commit others' private data.

---

**v1.0.0** · 内容创作 · 求职工具 · Cursor Agent Skill
