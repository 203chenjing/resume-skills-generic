# 简历优化 · Resume Optimizer

# 六秒定生死 — JD 证据链匹配 + 一页 PDF 交付

> **Cursor Agent Skill · 下游匹配改写层**  
> 解析 JD → 证据链映射 → STAR 改写 → 版式校验 → 恰好一页 PDF。

[![Version](https://img.shields.io/badge/version-v1.0.0-blue)](SKILL.md)
[![Cursor Skill](https://img.shields.io/badge/platform-Cursor%20Agent%20Skill-000000)](https://cursor.com)

---

## 下游模块：按岗选材与出稿

招聘方只给你六秒。JD 关键词不在首屏、叙事与岗位不对路，简历直接 pass——这不是润色能救的，是**选材与排序**的问题。

简历优化把改简历从「创作」变成「选择」：解析岗位描述作为压缩方向，从知识库召回可验证证据，强匹配前置、弱相关压缩，STAR 改写后经你审阅，脚本校验版式，交付**恰好一页 PDF**。

*Resume Optimizer is the downstream matching and render engine. The JD sets the compression direction; you keep final approval on every line.*

---

## 核心能力

| 能力 | 说明 |
|------|------|
| **JD 解析** | 提取岗位关键词、核心能力、优先级 |
| **证据链映射** | 从素材库匹配可验证经历，建立 JD ↔ 证据对应 |
| **匹配引擎** | 强匹配前置、弱相关压缩、结果量化加粗 |
| **首屏优化** | 上 1/3 区域对齐岗位关键词与核心成果 |
| **版式校验** | 脚本预检条目密度、页数与排版规范 |
| **一页 PDF** | 经 `check_resume_skill.py` 验证后导出终稿 |

---

## 在流水线中的位置

```text
JD + 原始简历（或 简历数据库.md）
        ↓
  JD 解析 → 证据链映射 → 匹配排序
        ↓
  STAR 改写 → Markdown 模板填充
        ↓
  人工审阅确认（Human-in-the-loop）
        ↓
  check_resume_skill.py → markdown_resume_to_pdf.py
        ↓
  交付：公司+姓名+岗位.pdf（恰好 1 页）
```

**推荐搭配：** [简历知识库 · Resume Knowledge Base](../resume-knowledge-base/) — 先入库再匹配，效果拉满；没有知识库也能跑，但每次从零考古。

---

## 怎么用

### 1. 安装

复制本目录至 Cursor 技能路径：

| 范围 | 路径 |
|------|------|
| 项目级 | `<your-project>/.cursor/skills/resume-optimizer/` |
| 个人级 | `~/.cursor/skills/resume-optimizer/` |

### 2. 准备输入

- **目标 JD** — 文本 / 链接 / 截图
- **原始简历** 或 **`简历数据库.md`**（来自 [Resume Knowledge Base](../resume-knowledge-base/)）
- **可选** — 岗位名称、城市、证件照路径

### 3. 开聊

**「用 resume-optimizer 按这份 JD 执行证据链匹配改写，导出一页 PDF。」**

### 4. CLI 脚本（可选）

```bash
# 版式预检（仅 Markdown）
python path/to/resume-optimizer/scripts/check_resume_skill.py 示例公司+张三+示例岗位.md --markdown-only

# 导出一页 PDF
python path/to/resume-optimizer/scripts/markdown_resume_to_pdf.py 示例公司+张三+示例岗位.md --preset fill
```

依赖：**Pillow**（裁剪）；**Playwright** 等（PDF 导出 — 见脚本头部说明）。

---

## 适合谁

- **多岗并行投递者** — 校招 / 实习 / 跳槽，按 JD 快速出定向版本
- **知识库持有者** — 已有 `简历数据库.md`，改写不丢细节、不编造
- **版式质量控** — 脚本校验页数排版，拒绝超页或空疏 PDF
- **证据链意识者** — 每条表述可回溯，面试敢举证

---

## 典型指令

- 「请根据附件招聘要求执行证据链匹配改写，经历分条、结果加粗，导出一页 PDF。」
- 「素材库已就绪，按目标岗位 JD 输出定向版本，弱相关经历予以压缩。」
- 「内容已确认，请执行版式校验并导出 PDF，要求恰好一页。」

更多场景 → [CASES.md](CASES.md)

---

## 包内文件

| 文件 | 用途 |
|------|------|
| [SKILL.md](SKILL.md) | **主入口** — 工作流、硬门槛、快速开始 |
| [reference.md](reference.md) | 步骤细则、版式标准、证据规则、PDF 规范 |
| [scripts/](scripts/) | 版式检查、PDF 导出、证件照裁剪 |
| [CASES.md](CASES.md) | 典型使用场景 |

---

## 模块分工

| resume-knowledge-base（上游） | resume-optimizer（本模块） |
|-------------------------------|----------------------------|
| 沉淀全部可验证事实与 STAR | 按 JD 驱动匹配引擎筛选证据 |
| 记录层级规则与按岗映射 | 执行 STAR 改写与版式校验 |
| 管理指标来源与待确认项 | 输出 Markdown + 一页 PDF |

---

## 三个原则

- **不编造** — 缺指标标 `[待补充：指标]`，绝不凭空写经历
- **可溯源** — 每条 bullet 能回溯到 `简历数据库.md` 或原始材料
- **人工确认** — 内容审阅通过后才导出 PDF；AI 提案，你裁决

---

示例使用虚构占位信息。真实材料请自行替换，勿将他人隐私提交至公开仓库。

`v1.0.0` · Matching & Render Layer
