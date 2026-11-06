# 规范库索引

按“写的是什么”路由到对应规范。**先在这里判定归属，再进对应文件**；判定不了就按 `grill-intake.md` 追问。

| 规范 | 关键词 / 触发语 | 规范文件 | 状态 |
|---|---|---|---|
| 大一年度项目（立项 / 中期检查 / 结题） | 大一年度项目、立项报告、中期检查、结题报告、基础学部 | [`annual-project.md`](annual-project.md)（写作）+ [`../../hit-standard-word-type/references/annual-project-format.md`](../../hit-standard-word-type/references/annual-project-format.md)（排版） | 已收录 |
| 课程报告六类 | 实验报告、调研报告、文献综述、课程设计、读书报告、小论文 | [`assignment-types.md`](assignment-types.md) | 已收录 |
| 校级大学生创新创业训练计划（大创） | 大创、国创、省创、创新创业训练计划、创新训练/创业训练/创业实践、申请书、进展报告、验收书、中期检查、结题验收 | [`dachuang.md`](dachuang.md)（写作）+ [`../../hit-standard-word-type/references/dachuang-format.md`](../../hit-standard-word-type/references/dachuang-format.md)（排版） | 已收录 |
| 本科毕业设计（论文）开题 / 中期 / 结题 | 毕设、毕业论文、开题报告、开题检查、中期检查、结题、任务书、外文翻译、答辩、理工类、人文社科类 | [`undergrad-thesis.md`](undergrad-thesis.md)（写作）+ [`../../hit-standard-word-type/references/undergrad-thesis-format.md`](../../hit-standard-word-type/references/undergrad-thesis-format.md)（排版） | 已收录 |
| 研究生学位论文 / 实践成果（硕士 / 博士） | 学位论文、硕士论文、博士论文、实践成果、案例研究、调研报告、盲审、答辩、学术学位、专业学位、理工类、人文社科类 | [`graduate-thesis.md`](graduate-thesis.md)（写作）+ [`../../hit-standard-word-type/references/graduate-thesis-format.md`](../../hit-standard-word-type/references/graduate-thesis-format.md)（排版） | 已收录 |
| 研究生开题 / 中期检查 / 预答辩 | 开题报告、中期检查、预答辩、开题答辩 | — | 待收录（范例未覆盖，要学院模板） |
| 官方原件（模板）清单 | 模板、原件、制式表格、封面、签字栏、在原件上填 | 仓库根 `templates/README.md`（安装后为 `~/.workbuddy/skills/hit-standard-word-type/templates/README.md`）+ [`../../hit-standard-word-type/references/template-fill.md`](../../hit-standard-word-type/references/template-fill.md) | 已收录 |

## 判定规则

1. 用户明说活动名称 → 直接对应上表。
2. 只说“报告”“作业”→ 问一句：“这是课程作业，还是学校/学院统一组织的项目报告（大一年度项目、大创、毕设）？”
3. 提到“基础学部”→ 大一年度项目。
4. 提到“指导教师意见 / 专家组意见 / 批准经费 / 中期检查”等表格字段 → 多半是校级项目表格，继续追问具体是哪个项目。
5. 状态为“待收录”的规范：**如实告诉用户规范还没内置**，请对方提供学院下发的模板文件或要求原文；拿到后按下面的流程补进来，不要凭通用经验硬写。
6. **同一活动有多个分支的，必须先问分支再动笔**：大创要先问赛道（创新训练/创业训练/创业实践）与阶段（申请书/中期/进展报告/验收书）；大一年度项目要先问校区与阶段；本科毕设要先问阶段（开题/中期/结题）与学科门类；研究生学位论文要先问学位层次（硕/博）、学位类型（学术/专业）与学科门类（理工/人文社科）。分支问错，模板、字数、封面字段、层次编号全错。
7. **本科毕设与研究生学位论文是两套规范，不要混用**：本科图表单语题注、无英文内封、页眉不分奇偶页；研究生双语题注、中英内封、页眉奇偶页不同。用户说“写论文”时先问一句“本科毕设还是研究生学位论文”。
8. **同一活动的不同阶段可能有的收录、有的没收录**：本科毕设三个环节都已收录；研究生学位论文本体已收录，但开题/中期/预答辩没有——用户说“研究生论文”时先问是哪一种，别默认按学位论文写。
9. **先查原件再动手**：`templates/` 里有这份文档的学校原件，一律复制原件填内容（`template-fill.md`），不新建封面、不重绘表格。原件缺失才自建，并在交付说明里写明。

## 新增一份规范时怎么做

用户提供了新的模板/要求（.doc/.docx/.pdf/截图）后：

1. **抽结构**：页面设置（纸型、页边距、网格、行距）、封面字段、表格列名、章节标题与顺序、各部分字数要求。
2. **抽格式**：各级标题字体字号、正文字体字号、图表题位置与字号、参考文献著录格式、页脚页码。
3. **写两份文件**：
   - 写作侧 → `hit-assignment-report/references/<规范名>.md`：差异点、章节骨架与字数配比、评审关注点、交付清单。开头写清触发词与“先问什么”。
   - 排版侧 → `hit-standard-word-type/references/<规范名>-format.md`：可逐条执行的格式值 + 自检清单。与 `formatting-spec.md` 冲突时声明优先级。
4. **挂路由**：上面表格加一行（状态改“已收录”）；`hit-assignment-report/SKILL.md` 的 description 补触发词；`hit-standard-word-type/SKILL.md` 的“先判断用哪套规范”表加一行。
5. **标注不确定项**：模板本身没写、只能从版式反推的值（如页边距实测 2cm），必须写明“实测/推定”，不要伪装成硬性规定。

## 多校区 / 多版本的通用处理

同一活动有多个版本（如本部 vs 深圳校区）时：

- 写作侧用**差异对照表**，逐项列“字段 / 章节 / 字数 / 表名”的差别，不写两份几乎相同的全文。
- 排版侧只写**一份**通用规则 + 差异小表，冲突值在表里单独列。
- 判定顺序永远先问“哪个校区/哪个版本”，再往下走。
