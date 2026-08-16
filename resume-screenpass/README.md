# 过筛选改简历 · ScreenPass Resume

# 六秒定生死 — JD 证据链匹配 + 一页 PDF 交付引擎

> **Cursor Agent Skill · 匹配改写层**  
> 解析 JD → 证据链映射 → STAR 改写 → 版式校验 → 恰好一页 PDF。

[![Version](https://img.shields.io/badge/version-v1.0.0-blue)](SKILL.md)
[![Cursor Skill](https://img.shields.io/badge/platform-Cursor%20Agent%20Skill-000000)](https://cursor.com)

---

## 先说结论

- **JD 驱动匹配引擎** — 强匹配前置、弱相关压缩、结果量化加粗
- **证据链可溯源** — 每条 bullet 能回溯到 `简历数据库.md` 或原始材料
- **脚本校验版式** — 恰好 1 页 PDF，Human-in-the-loop 你点头才交付

---

## 你是不是也…

HR 和 ATS **6–10 秒** 完成初筛。

JD 关键词不在首屏？直接进回收站。

AI 润色看着很美，面试一问细节就穿帮？

投完第 8 个岗还在用同一份通用简历 — **本质上是在赌关键词碰运气。**

**过筛选，再谈面试。**

---

## 核心能力

| 能力 | 一句话 |
|------|--------|
| **JD 解析** | 提取岗位关键词、核心能力、优先级 |
| **证据链映射** | 从素材库匹配可验证经历，建立 JD ↔ 证据对应 |
| **匹配引擎** | 强匹配前置、弱相关压缩、结果量化加粗 |
| **首屏优化** | 上 1/3 区域对齐岗位关键词与核心成果 |
| **版式校验** | 脚本预检条目密度、页数与排版规范 |
| **一页 PDF** | 经 `check_resume_skill.py` 验证后导出终稿 |

---

## Pipeline 位置

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

**推荐搭配：** [简历弹药库 · Resume Vault](../resume-vault/) — 先入库再匹配，效果拉满。

---

## 3 步上手

### 1. 安装

复制本目录至 Cursor 技能路径：

| 范围 | 路径 |
|------|------|
| 项目级 | `<your-project>/.cursor/skills/resume-screenpass/` |
| 个人级 | `~/.cursor/skills/resume-screenpass/` |

开聊：**「用 resume-screenpass 按这份 JD 执行证据链匹配改写，导出一页 PDF。」**

### 2. 准备输入

- **目标 JD** — 文本 / 链接 / 截图
- **原始简历** 或 **`简历数据库.md`**（来自 [Resume Vault](../resume-vault/)）
- **可选** — 岗位名称、城市、证件照路径

### 3. CLI 脚本

```bash
# 版式预检（仅 Markdown）
python path/to/resume-screenpass/scripts/check_resume_skill.py 示例公司+张三+示例岗位.md --markdown-only

# 导出一页 PDF
python path/to/resume-screenpass/scripts/markdown_resume_to_pdf.py 示例公司+张三+示例岗位.md --preset fill
```

依赖：**Pillow**（裁剪）；**Playwright** 等（PDF 导出 — 见脚本头部说明）。

---

## 适合谁

- **多岗并行投递者** — 校招 / 实习 / 跳槽，按 JD 快速出定向版本
- **弹药库持有者** — 已有 `简历数据库.md`，改写不丢细节、不编造
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

| resume-vault（上游） | resume-screenpass（本模块） |
|----------------------|-----------------------------|
| 沉淀全部可验证事实与 STAR | 按 JD 驱动匹配引擎筛选证据 |
| 记录层级规则与按岗映射 | 执行 STAR 改写与版式校验 |
| 管理指标来源与待确认项 | 输出 Markdown + 一页 PDF |

---

示例使用虚构占位信息。真实材料请自行替换，勿将他人隐私提交至公开仓库。

`#Cursor` `#求职` `#过筛选` · v1.0.0 · Matching & Render Layer
