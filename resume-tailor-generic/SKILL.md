---
name: resume-tailor-generic
description: 定向简历改写。依据目标岗位招聘要求，筛选匹配经历、改写投递内容并完成版式校验，输出一页 PDF。在用户需按岗改简历、多岗位适配或 PDF 终稿导出时使用。素材归档请用 resume-database-generic。不编造事实。
tags: [内容创作, 求职工具, 简历]
version: 1.0.0
capability: text_generation
pricing:
  model: per_call
  amount_fen: 50
---

# 定向简历改写

## 快速开始

1. 确认 **JD + 原始简历**（可选已确认的 `简历数据库.md`）。
2. 按 [工作流程](#工作流程) 提取事实 → 分析 JD → 映射证据 → STAR 改写 → 套模板。
3. **人工内容审阅**（对照 [reference.md](reference.md) 完整清单）。
4. `python scripts/check_resume_skill.py input.md --markdown-only`
5. `python scripts/markdown_resume_to_pdf.py input.md` → 须 `Page check: 1 page.` 且 `Skill check: passed.`
6. 请用户确认事实/指标后交付；有修改则从步骤 3 重来。

缺 JD 或原始简历时先索取。禁止编造事实；缺指标写 `[待补充：指标]`。

## 必备输入

| 输入 | 说明 |
|------|------|
| 目标 JD | 文本 / 链接 / 截图 / 文件 |
| 原始简历 | PDF / Markdown / DOCX 文本 / 粘贴 |
| 简历数据库（可选） | `简历数据库.md`，仅合并用户已确认内容 |
| 偏好（可选） | 岗位名、城市、文件名、证件照 |

知识库缺失时，按 **resume-database-generic** 技能判断是否先建库。

## 工作流程

```
任务进度：
- [ ] 1. 提取事实（含知识库；禁止编造）
- [ ] 2. 分析 JD（核心 / 可强化 / 弱相关）
- [ ] 3. 证据映射（删无关、定层级与压缩策略）
- [ ] 4. STAR + 指标改写编号条目
- [ ] 5. 按模板写 Markdown（版式硬规则见 reference）
- [ ] 6. 审阅 → 预检 → 导出 PDF → 调节直至通过
```

各步细则、层级规则、版式与 PDF 循环见 **[reference.md](reference.md)**。条目示例见 **[examples.md](examples.md)**。

### 硬门槛（不可省略）

- 交付 PDF 时：**恰好 1 页**，且已跑导出与检查脚本（若存在）。
- **项目简介仅 1 行（1 句）**：紧挨 `**项目一/二：…**` 下一行；约 25–45 字，只点明场景 + 职责边界；细节、指标、流程一律放编号条目。禁止写成 2 句及以上长段。
- **正文行要写满（强制）**：编号条目与 `相关技能` 每条都要信息密度够高，PDF 两端对齐后**不要出现「一整行只剩半截字」的空疏感**；单条经历宜约 **80–140 字**（2–4 个完整分句：场景→动作→协同/规则→结果），技能四行每行写到接近行末。禁止短句堆砌、标题很长正文却半句就结束。细则见 [reference.md](reference.md)「行宽与信息密度」。
- `check_resume_skill.py` **只查版式**，不查真实性与 JD 匹配；内容审阅必须人工完成。
- 内容审阅未通过 → 只改 Markdown，不交付 PDF。
- 每次改 Markdown 后，导出前须重新内容审阅。

## 输出

- **Markdown** 简历（基于 [resume-template.md](resume-template.md)）。
- **PDF**（若需要）：文件名 `公司+姓名+岗位.pdf`，无 `_脚本版` 等后缀。
- 对话中简述：JD 优化点、待确认指标、导出命令。

## 核心检查（终稿前）

完整清单见 [reference.md#质量检查清单](reference.md)。至少核对：

- [ ] 事实有据，无编造
- [ ] 上三分之一体现 JD 匹配
- [ ] 实习经历：单项目用 `1.`；多项目用 `**项目一：**` + **仅 1 行简介** + 顶格 `1）2）`（见 [reference.md](reference.md)）
- [ ] 项目简介为 **1 行 1 句**（灰色斜体）；章节标题为**灰色底栏**；职责标题与量化结果 **加粗**
- [ ] 量化结果已加粗；经历正文讲人话，避免中英混杂；`AI技能` 写泛化能力
- [ ] 编号条目与技能行**行宽写满**：无大片半行空白、无「标题长正文短」；技能四行均接近行末
- [ ] `相关技能` 恰为 4 行（工作 / 数据 / AI / 语言）
- [ ] `---` 在 `实习经历`、`相关技能` 前各一行且无空行
- [ ] PDF 为 1 页且 `Skill check: passed.`（若用脚本）

## 配套资源

| 文件 | 用途 |
|------|------|
| [reference.md](reference.md) | 步骤细则、版式、证据规则、完整质检、PDF 标准 |
| [examples.md](examples.md) | 表头、编号条目、技能行、文件名示例 |
| [resume-template.md](resume-template.md) | Markdown 简历模板 |
| [resume-database-template.md](resume-database-template.md) | 知识库空白模板 |
| [scripts/markdown_resume_to_pdf.py](scripts/markdown_resume_to_pdf.py) | 导出 PDF |
| [scripts/check_resume_skill.py](scripts/check_resume_skill.py) | 版式检查 |
| [scripts/crop_profile_photo.py](scripts/crop_profile_photo.py) | 证件照裁剪 |
