# resume-skills-generic

**Monorepo** for two Cursor Agent Skills — Chinese resume tooling with fictional fixtures only.

| Skill | Purpose |
|-------|---------|
| **resume-database-generic** | Build & maintain `简历数据库.md` — STAR, metrics, open items (archive only) |
| **resume-tailor-generic** | Tailor resume to a JD, STAR rewrite, one-page PDF export, photo crop |

**No real PII** in this repo — names, phones, emails, and employers are placeholders or fictional samples.

## Repository layout

```text
resume-skills-generic/
├── README.md                      ← you are here
├── publish/                       ← release-ready skill packages (install from here)
│   ├── PUBLISH_CHECKLIST.md
│   ├── resume-tailor-generic/
│   └── resume-database-generic/
├── shared/                        ← shared scripts & templates (source for publish sync)
├── fixtures/                      ← fictional samples for regression
└── tests/
    ├── run_regression.py
    └── REGRESSION_REPORT.md
```

Root-level `resume-tailor-generic/` and `resume-database-generic/` may exist locally for development; they are **not** tracked in git — use `publish/` as the canonical copy on GitHub.

## 安装到 Cursor（3–5 步）

1. 克隆或解压本仓库到任意目录。
2. 将 `publish/` 下两个 skill 目录复制到 Cursor 技能目录之一：
   - **项目级**：`<你的项目>/.cursor/skills/`
   - **个人级**：`~/.cursor/skills/`（Windows 常见为 `%USERPROFILE%\.cursor\skills\`）
3. 确认存在：
   - `.cursor/skills/resume-tailor-generic/SKILL.md`
   - `.cursor/skills/resume-database-generic/SKILL.md`
4. 在 Cursor 对话中说明「按 resume-tailor-generic 改简历」或「用 resume-database-generic 建知识库」。
5.（可选）把 `shared/scripts/` 复制到工作区脚本目录，方便命令行直接调用。

## 常用脚本

在 `publish/resume-tailor-generic/scripts/`（或 `shared/scripts/`）下：

```bash
# 版式预检（仅 Markdown）
python check_resume_skill.py path/to/简历.md --markdown-only

# 导出一页 PDF（需本机可运行 Playwright/浏览器依赖）
python markdown_resume_to_pdf.py path/to/简历.md --preset fill

# 证件照裁剪为固定画幅（默认 540x790）
python crop_profile_photo.py photo.jpg -o profile-photo-cropped.png
```

依赖提示：

- `crop_profile_photo.py`：Pillow
- `markdown_resume_to_pdf.py` / 完整 `check_resume_skill.py`：通常需要 Playwright 等（与脚本头部说明一致）

## 推荐工作流

1. 有多次投递需求 → 先用 **resume-database-generic** 建 `简历数据库.md`
2. 拿到 JD → 用 **resume-tailor-generic** 映射证据、STAR 改写、套模板
3. 人工内容审阅 → `check_resume_skill.py --markdown-only` → 导出 PDF
4. 若需证件照 → 先 `crop_profile_photo.py`，再在 Markdown 中引用裁剪后的本地路径

## 回归测试

```bash
python tests/run_regression.py
```

结果写入 `tests/REGRESSION_REPORT.md`。

## 隐私约定

本包示例一律使用虚构信息（如 `张三`、`example@email.com` / `zhangsan@email.com`、`示例大学 A`、`示例科技有限公司`）。  
使用时请替换为**你自己**经确认的真实材料；请勿把他人隐私提交进共享包。
