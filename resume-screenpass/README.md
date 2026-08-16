# 过筛选改简历 · ScreenPass Resume

# 六秒定生死 — JD 证据链匹配与一页 PDF 交付引擎

# Six Seconds Decide — JD Evidence-Chain Matching & Single-Page PDF Delivery Engine

> **Cursor Agent Skill · 匹配改写层 · 解析 JD、驱动证据链映射、执行 STAR 改写与版式校验，输出恰好一页 PDF。**  
> **Cursor Agent Skill · Matching & Render Layer · Parses JD, drives evidence-chain mapping, executes STAR rewriting and layout validation, delivers exactly one page PDF.**

[![Version](https://img.shields.io/badge/version-v1.0.0-blue)](SKILL.md)
[![Cursor Skill](https://img.shields.io/badge/platform-Cursor%20Agent%20Skill-000000)](https://cursor.com)
[![Language](https://img.shields.io/badge/language-中文%20%7C%20Chinese-orange)](#)

---

## 产品定位 · Product Positioning

**ScreenPass Resume** 是简历投递流水线的 **匹配改写层（Matching & Render Layer）**。Agent 解析目标岗位 JD，从 `简历数据库.md` 或原始简历中驱动匹配引擎选取可验证证据，执行 STAR 改写、首屏关键词对齐与版式校验，最终通过脚本导出 **恰好一页** 的投递 PDF。全流程坚持 **不编造事实** — 缺指标标注 `[待补充：指标]`，交付前须经人工审阅确认。

**ScreenPass Resume** is the **Matching & Render Layer** of the resume delivery pipeline. The Agent parses the target JD, drives the matching engine to select verified evidence from `简历数据库.md` or source resumes, executes STAR rewriting, above-the-fold keyword alignment, and layout validation, then exports an **exactly one-page** PDF via script. **No fabrication** — missing metrics are flagged; human review is required before delivery.

---

## 核心能力 · Core Capabilities

| 能力 Capability | 说明 Description |
|-----------------|------------------|
| **JD 解析** | 提取岗位关键词、核心能力要求与优先级 |
| **证据链映射** | 从素材库匹配可验证经历，建立 JD ↔ 证据对应关系 |
| **匹配引擎** | 强匹配前置、弱相关压缩、结果量化加粗 |
| **首屏优化** | 上 1/3 区域对齐岗位关键词与核心成果 |
| **版式校验** | 脚本预检条目密度、页数与排版规范 |
| **一页 PDF** | 经 `check_resume_skill.py` 验证后导出终稿 |

---

## 问题与方案 · Problem → Solution

**问题：** 招聘方与 ATS 在 **6–10 秒** 内完成初筛。JD 关键词未出现在首屏、证据密度失衡、或 AI 润色后面试无法举证 — 简历往往在细读之前即被过滤。投完第 8 个岗仍用同一份通用简历，本质上是在赌关键词碰运气。

**Problem:** Recruiters and ATS complete first-pass screening in **6–10 seconds**. Missing above-the-fold keywords, imbalanced evidence density, or AI-polished bullets you cannot defend in interviews — most resumes are filtered before detailed review. Sending the same generic resume to every role is a keyword lottery.

**方案：** `resume-screenpass` 将按 JD 改写封装为可重复的 Agent 工作流：JD 解析 → 证据链映射 → STAR 改写 → 版式校验 → 一页 PDF。每个岗位产出独立定向稿，每条表述可回溯至素材来源。过筛选，再谈面试。

**Solution:** `resume-screenpass` packages JD tailoring as a repeatable Agent workflow: JD parsing → evidence-chain mapping → STAR rewriting → layout validation → single-page PDF. Each role gets a dedicated draft; every claim traces to source material. Pass the screen first — then earn the interview.

---

## 工作流 · Workflow

```text
JD + 原始简历（或 简历数据库.md）
        ↓
  JD 解析 → 证据链映射 → 匹配排序
        ↓
  STAR 改写 → Markdown 模板填充
        ↓
  人工审阅确认
        ↓
  check_resume_skill.py → markdown_resume_to_pdf.py
        ↓
  交付：公司+姓名+岗位.pdf（恰好 1 页）
```

**推荐搭配：** [简历弹药库 · Resume Vault](../resume-vault/) — 先完成经历结构化入库，再进入本模块执行证据链匹配。无素材库时，每次改写均从零考古。

---

## 适用对象 · Who It's For

- **多岗并行投递者** — 校招、实习、跳槽等需按 JD 快速产出定向版本
- **素材库持有者** — 已有 `简历数据库.md`，要求改写不丢细节、不编造
- **版式质量要求者** — 需脚本校验页数与排版，拒绝超页或空疏 PDF
- **证据链意识者** — 要求每条投递表述可回溯、面试可举证

---

## 快速开始 · Quick Start

### 1. 安装 Agent Skill

复制本目录至 Cursor 技能路径：

| 范围 Scope | 路径 Path |
|------------|-----------|
| 项目级 Project | `<your-project>/.cursor/skills/resume-screenpass/` |
| 个人级 User | `~/.cursor/skills/resume-screenpass/`（Windows: `%USERPROFILE%\.cursor\skills\`） |

确认 `SKILL.md` 存在后，在对话中输入：**「用 resume-screenpass 按这份 JD 执行证据链匹配改写，导出一页 PDF。」**

### 2. 准备输入

- **目标 JD** — 文本 / 链接 / 截图
- **原始简历** 或 **`简历数据库.md`**（来自 [Resume Vault](../resume-vault/)）
- **可选** — 岗位名称、城市、证件照路径

### 3. 命令行脚本 · CLI Scripts

在工作区简历目录下运行：

```bash
# 版式预检（仅 Markdown）
python path/to/resume-screenpass/scripts/check_resume_skill.py 示例公司+张三+示例岗位.md --markdown-only

# 导出一页 PDF（--preset tight | fill）
python path/to/resume-screenpass/scripts/markdown_resume_to_pdf.py 示例公司+张三+示例岗位.md --preset fill

# 证件照裁剪（默认 540×790）
python path/to/resume-screenpass/scripts/crop_profile_photo.py photo.jpg -o profile-photo-cropped.png
```

依赖：**Pillow**（裁剪）；**Playwright** 等（PDF 导出 — 见脚本头部说明）。

---

## 包内文件 · Package Contents

| 文件 File | 用途 Purpose |
|-----------|--------------|
| [SKILL.md](SKILL.md) | **主入口** — 工作流、硬门槛、快速开始 |
| [reference.md](reference.md) | 步骤细则、版式标准、证据规则、PDF 规范 |
| [examples.md](examples.md) | 表头、编号条目、技能行示例（虚构占位） |
| [resume-template.md](resume-template.md) | Markdown 简历模板 |
| [resume-database-template.md](resume-database-template.md) | 知识库空白模板 |
| [scripts/](scripts/) | 版式检查、PDF 导出、证件照裁剪 |
| [CASES.md](CASES.md) | 典型使用场景 |

---

## 典型指令 · Example Prompts

- 「请根据附件招聘要求执行证据链匹配改写，经历分条、结果加粗，导出一页 PDF。」
- 「素材库已就绪，按目标岗位 JD 输出定向版本，弱相关经历予以压缩。」
- 「内容已确认，请执行版式校验并导出 PDF，要求恰好一页。」

更多场景见 [CASES.md](CASES.md)。

---

## 模块分工 · Division of Labor

| resume-vault（上游） | resume-screenpass（本模块） |
|----------------------|-----------------------------|
| 沉淀全部可验证事实与 STAR | 按 JD 驱动匹配引擎筛选证据 |
| 记录层级规则与按岗映射 | 执行 STAR 改写与版式校验 |
| 管理指标来源与待确认项 | 输出 Markdown + 一页 PDF |

---

## 隐私 · Privacy

示例使用虚构占位信息。请替换为经确认的真实材料，勿将他人隐私提交至公开仓库。

---

**v1.0.0** · Cursor Agent Skill · 匹配改写层 · Matching & Render Layer
