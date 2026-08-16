# 先过简历筛选 · Pass the Screen First

> **两个 Cursor Agent 技能，把「翻旧 PDF 改简历」变成「弹药库 → 定向稿 → 一页 PDF」。**  
> **Two Cursor Agent Skills — turn "digging through old PDFs" into vault → tailored draft → one-page PDF.**

[![Cursor](https://img.shields.io/badge/platform-Cursor%20Agent%20Skills-000000)](https://cursor.com)
[![Language](https://img.shields.io/badge/language-中文%20%7C%20English-orange)](#)

---

## 故事 · Why this exists

你打开那份旧 PDF，准备改第 3 个岗位的简历。JD 写着「用户增长」「A/B 测试」「SQL」，简历上还是「参与项目、协助推进」——关键词对不上，HR 和 ATS 在 **6–10 秒** 内就把你划掉了。更糟的是：上礼拜为岗位 A 删掉的一段经历，投岗位 B 时正好是核心关键词，但细节已经记不清了。

招聘方看的不是你有没有做过，而是 **这一刻你能不能拿出和 THIS 岗位最相关的证据**。没有单一事实来源，每次定向改写都在重新考古；改得越急，丢得越多。我们做了两个技能：**先把经历装进弹药库，再按 JD 打出能活过筛选的一页定向稿** — 诚实、可溯源、能打。

You open that old PDF again — third role this week. The JD asks for *user growth*, *A/B testing*, *SQL*; your resume still says *participated in projects*. Keywords miss, and HR plus ATS move on in **6–10 seconds**. Worse: the bullet you cut for Role A was exactly what Role B needs — but the nuance is gone.

Screening isn't asking whether you did the work. It's asking whether you can **surface the right evidence for THIS role, fast**. Without a single source of truth, every tailoring session re-digs the PDF and loses detail. We built two skills: **stock your vault first, then ship a one-page draft built to pass the screen** — honest, traceable, ready to send.

---

## 两个技能 · Two skills, one pipeline

| | Skill | One-liner |
|---|-------|-----------|
| **弹药库** | [**简历弹药库 · Resume Vault**](resume-vault/) | 写一次，投百岗 — STAR、指标、`[待确认]` 全部归档，筛选开战前有弹可打。 |
| **过筛选** | [**过筛选改简历 · ScreenPass Resume**](resume-screenpass/) | 从 JD 反推证据链，STAR 重写 + 版式校验，导出 **恰好一页** PDF。 |

```text
原始简历 + 你确认的事实
        ↓
  简历弹药库 · Resume Vault  →  简历数据库.md
        ↓
  过筛选改简历 · ScreenPass   →  Markdown → 一页 PDF
        ↓
  公司+姓名+岗位.pdf（投递）
```

---

## 适合谁 · Who it's for

- **校招 / 实习 / 跳槽**，同时投多个岗位、需要按 JD 快速改一版的人
- 同一家公司有 **并列项目 / 多条工作线**，需要按岗切换主线
- 受够了 AI 润色后面试答不上细节，想要 **可溯源、不编造** 的改写流程
- 想要 **脚本校验版式**、PDF 不再超页或空疏的终稿

Anyone applying to **multiple roles** who needs fast JD-specific versions; candidates with **parallel projects** at one employer; anyone tired of AI polish you can't defend in interviews; anyone who wants **script-checkable, exactly-one-page** PDFs.

---

## 快速安装 · Quick install

### 1. Clone

```bash
git clone https://github.com/203chenjing/resume-skills-generic.git
cd resume-skills-generic
```

### 2. Copy both skills into Cursor

复制 `resume-vault/` 与 `resume-screenpass/` 到 Cursor 技能目录（二选一）：

| Scope | Path |
|-------|------|
| Project | `<your-project>/.cursor/skills/` |
| Global | `~/.cursor/skills/`（Windows: `%USERPROFILE%\.cursor\skills\`） |

### 3. Prompt

- **建库：**「用 resume-vault 根据这份简历建立素材库。」  
  *"Use resume-vault to build my experience database from this resume."*
- **改简历：**「用 resume-screenpass 按这份 JD 改简历并导出一页 PDF。」  
  *"Use resume-screenpass to tailor my resume to this JD and export a one-page PDF."*

各技能详情见 [`resume-vault/README.md`](resume-vault/README.md) 与 [`resume-screenpass/README.md`](resume-screenpass/README.md)。

---

## 隐私 · Privacy

示例与文档中的姓名、公司均为 **虚构占位**（如张三、示例公司）。请替换为你经确认的真实材料，勿将他人隐私提交到公开仓库。

Samples use **fictional placeholders**. Replace with your verified information; never commit others' private data.

---

**v1.0.0** · Cursor Agent Skills · 内容创作 · 求职工具
