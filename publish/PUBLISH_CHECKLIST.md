# SkillHub 发布清单

两个独立 Skill：**素材整理**（一次归档）与 **定向改写**（按岗交付）。分开发布，便于计费与能力边界划分。

| | 简历素材库 | 定向简历改写 |
|--|-----------|-------------|
| 能力 | 经历归档与指标管理 | 按招聘要求改写并导出 PDF |
| 输出 | `简历数据库.md` | 投递简历 + 一页 PDF |
| Slug | `resume-database-generic` | `resume-tailor-generic` |
| 定价 | 0.10 元/次 | 0.50 元/次 |

---

## Skill 1 · 简历素材库

| 显示名称 | 简历素材库 |
| 标签 | 内容创作 · 求职工具 |
| 版本 | v1.0.0 |
| 包 | `publish/resume-database-generic.zip` |

**描述：**

> 基于原始简历与用户确认信息，建立结构化经历素材库，归档项目贡献、量化结果及待确认项，供多岗位投递复用。仅维护素材，不输出定向简历与 PDF。

**变更说明：** v1.0.0 首发，支持新建、增量更新与多项目结构化整理。

---

## Skill 2 · 定向简历改写

| 显示名称 | 定向简历改写 |
| 标签 | 内容创作 · 求职工具 |
| 版本 | v1.0.0 |
| 包 | `publish/resume-tailor-generic.zip` |

**描述：**

> 依据目标岗位招聘要求，筛选匹配经历、改写投递内容并完成版式校验，输出一页 PDF。内容须可溯源，不编造事实。不含面试辅导、岗位搜索；建议配合「简历素材库」使用。

**变更说明：** v1.0.0 首发，支持岗位定向改写、一页 PDF 导出与版式检查。

---

## 发布前

- [ ] 企业认证与商户入驻
- [ ] 上传两个 ZIP（根目录含 `SKILL.md`）
- [ ] 各补 3 条案例（见 `CASES.md`）

```powershell
cd e:\resume-skills-generic\resume-skills-generic\publish
Compress-Archive -Path "resume-database-generic\*" -DestinationPath "resume-database-generic.zip" -Force
Compress-Archive -Path "resume-tailor-generic\*" -DestinationPath "resume-tailor-generic.zip" -Force
```
