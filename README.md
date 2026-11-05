# HIT Skills

**给哈工大学生的 AI 报告技能包。** 说清楚要写什么，剩下的交给它：按学院模板搭结构、检索真实知网文献、对账引用、排好版，交出一份能直接提交的 docx。

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](#依赖)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-brightgreen.svg)](https://agentskills.io)
[![Dependencies](https://img.shields.io/badge/deps-stdlib%20only-informational.svg)](#依赖)
[![WorkBuddy](https://img.shields.io/badge/WorkBuddy-%E9%82%80%E8%AF%B7%E6%B3%A8%E5%86%8C-1f8f6f.svg)](https://www.workbuddy.cn/events/invite?inviteCode=08foyuwog)

## 能写什么

| 你要写 | 它会怎么帮你 |
|---|---|
| **大一年度项目**：立项 / 中期检查 / 结题 | 先问清**本部还是深圳**、哪个阶段，再按对应模板落地——封面字段、成员表列名、字数（本部中期 2000 字，深圳 1500 字 + 600 字基本信息）、章节配比、专家组意见栏 |
| **大创**（校级 / 省级 / 国创）：申请书 / 中期检查 / 进展报告 / 验收书 | 三个赛道分开写：**创新训练** 7 节研究、**创业训练** 9 节商业计划、**创业实践** 12 节运营；创业类带 A–H 项目类别与企业指导教师。选错赛道等于重写 |
| **毕业设计（论文）**：开题 / 中期 / 结题 | 三个阶段三份文档分开写：**开题报告 8 节 ≥3000 字**、**中期报告 5 节**、**结题论文 ≥1.5 万字**；理工类与人文社科类两套层次编号，内封要勾“毕业论文/毕业设计”，图表只用中文题注、页眉不分奇偶页 |
| **研究生学位论文 / 实践成果**：硕士 / 博士 | 先分层次：硕士 3~5 万字、图表只用中文、页眉固定；博士 6~10 万字、图表中英双语、页眉奇偶不同、多一页评阅人与答辩委员会名单。再分学科门类：理工 `第1章/1.1/1.1.1`，人文 `第一章/一、/（一）/1.`。专业学位还可在学位论文与实践成果之间选。开题/中期/预答辩不在此范围，需学院模板 |
| **课程报告** | 实验报告、调研报告、文献综述、课程设计、读书报告、小论文六类骨架，按评分点反推章节 |
| **参考文献** | 知网检索 → 批量读摘要 → 你确认 → 下载 PDF/CAJ → md5 校验；正文只写 `[@key]`，编号由脚本渲染 |
| **Word 排版** | [专章说明 ↓](#word-format)：大一年度项目、大创、研究生学位论文、毕设各用各的模板规格；三线表、图表编号、公式、参考文献著录、封面字段全部按规范落地 |

**它不是“帮你写一段话”的写作助手，而是把学校那套规矩做成可执行的流程：**

- **开工先盘问**：校区、阶段、字数、有没有官方模板，问清楚才动笔，不替用户猜
- **文献不许编**：每条参考文献都绑定知网上真实存在的原文文件，对账不过脚本直接拒绝交付
- **格式不用操心**：字体字号、行距、文档网格、图表编号、参考文献著录按规范落到 Word 里

**学校下发的原件也一起放在仓库里**，不用回官网翻附件——克隆下来就能直接复制去填：

| 目录 | 份数 | 里面是什么 |
|---|---|---|
| [`templates/annual-project/`](templates/annual-project/) | 7 | 大一年度项目：本部、深圳各 3 份（立项 / 中期检查 / 结题）+ 管理规范（试行） |
| [`templates/dachuang/`](templates/dachuang/) | 6 | 大创：三赛道申请书 + 项目进展报告 + 项目验收书 + 管理办法（校本〔2024〕61 号） |
| [`templates/undergrad-thesis/`](templates/undergrad-thesis/) | 12 | 本科毕设：写作指南 2、书写范例 2、开题报告、中期报告、过程管理记录表、工作实施细则、撰写规范、原创性声明、封面参考与封面样例 |
| [`templates/graduate-thesis/`](templates/graduate-thesis/) | 6 | 研究生：学位论文写作指南 2、实践成果写作指南 2、书写范例 2 |

逐份清单、官方来源链接与版本日期见 [学校规范原件](#templates)；写作与排版两套规范都是从这些原件里逐条抽出来的，原件看版式，规范看要求。

<a id="word-format"></a>

## Word 排版：格式类返工，一次消掉

写报告真正耗时的往往不是内容，是把格式调成学院要求的样子。这部分直接交给 skill：

- **页面**：A4、页边距、文档网格、行距、页脚页码
- **文字**：各级标题的字体字号与段前段后、正文宋体小四、数字与英文 Times New Roman、首行缩进
- **图表**：三线表（顶线 / 栏目线 / 底线磅值）、表题在上、图题在下、按章编号、正文有“如图 X-X 所示”的提示
- **公式与参考文献**：公式居中、编号右端对齐；参考文献按 GB/T 7714-2005 顺序编码制，正文上角标与条目一一对应
- **标点与引号**：中文全角标点，双引号“”、单引号‘’，禁用英文直引号；书名号《》不混用（见规范 §9）
- **封面**：按报告类型填字段，不留空

| 你在排什么 | 依据 | 关键规格 |
|---|---|---|
| **大一年度项目** 立项 / 中期 / 结题（本部、深圳） | `annual-project-format.md` | A4 + 四边 2cm + 文档网格 46 字×43 行 + 行距 16 磅；封面一号黑体；正文小四宋体；标题层级只用 `一` → `1.` → `（1）`；正文自建表格一律三线表（顶线/底线 1.5 磅、栏目线 0.75 磅、无竖线），模板固定的成员表与成果表保留原框线；结题论文体（题名二号黑体、作者四号楷体、摘要五号） |
| **大创** | `dachuang-format.md` | 封面宋体加粗小二（18pt）、字段小四加粗、表头五号、正文小四宋体、行距保持模板原样；全文连续编号（图 1、表 1） |
| **研究生学位论文 / 实践成果**（硕士 / 博士，理工类、人文社科类） | `graduate-thesis-format.md` | A4 + 上 3.8 / 下 3.0 / 左右 3.0 cm、版心 150×240 mm；封面“□士学位论文”宋体小1号加粗、题目黑体2号、英文题目 Times New Roman 2号加粗、校名楷体小2号加粗；内封 **9 项**（含副导师、行业导师）冒号左黑体4号右宋体4号、行距 1.5；**硕士图表只用中文、博士中英双语**；**博士页眉奇偶不同、硕士单面固定**；章标题段前 1 行段后 0.8 行；页码 `- 1 -`，前置部分罗马数字 |
| **本科毕业设计（论文）**（开题 / 中期 / 结题，理工类、人文社科类） | `undergrad-thesis-format.md` | A4 + 上 3.8 / 下 3.0 / 左右 3.0 cm、版心 150×240 mm、单面；封面题头宋体小1号加粗、题目黑体2号、英文题 TNR 2号加粗、校名楷体小2号加粗；中文内封七行冒号左黑体4号右宋体4号、行距 1.5；章标题黑体小2号**段前 1 行段后 0.8 行**；**图表只用中文题注**（序号与题名空 2 个半角字符）；页眉**不分奇偶页**、粗细双线；含版式截图可对照 |
| **毕业设计、课程论文** | `formatting-spec.md`（HIT 通用规范） | 章标题黑体小二、节标题黑体小三、条标题黑体四号、正文宋体小四、多倍行距 1.25、三线表、图表按章编号、参考文献 GB/T 7714-2005 |
| **手上已有 .docx，只想改格式** | 按报告类型选上面几份之一 | 不动内容，只改样式、标题层级、图表题位置与编号、参考文献格式 |

几份规范的分工是一句话：**学校/学院模板写明的按模板，模板没写清或没提的回落 HIT 通用规范**（三线表线宽、公式编号、插图编排、目录、物理量斜体、装订都在这一档），两边都没写的按通用规范最近条款处理并在交付说明里注明。

<a id="report-map"></a>

## 报告全景：HIT 什么时候要你交什么

先看清全貌，再决定写哪一份——**同一所学校里，这几套文档的模板、字数、封面字段互不通用**。

### 一、大一年度项目（基础学部 · 大一）

| 阶段 | 交什么 | 字数 | 本部 / 深圳差异 |
|---|---|---|---|
| 立项 | 立项报告 + 成员表 + 指导教师/专家组意见栏 | 2000 字以上，六部分 | 封面“专业（类）/专业集群/学院（部）”不同；深圳无辅导员栏 |
| 中期检查 | 中期检查报告 + 专家组意见 | **本部 2000 字左右（五小节）；深圳 1500 字左右（四小节）+ 基本信息表（背景≤200 字、方案≤400 字）** | 差别最大的一份，写错版本等于白写 |
| 结题 | 结题报告 + 项目成果表 | 3000 字左右，六部分 | 深圳多一节“拟依托项目继续开展大创”（选填） |

### 二、大创（本科生院 · 全校本科生，团队 3–5 人）

**先分赛道**——三份申请书正文完全不同：

| 赛道 | 做什么 | 执行时限 | 指导教师 | 申请书正文 |
|---|---|---|---|---|
| 创新训练 | 自主完成创新性研究：设计、实施、研究报告 | 一般 1 年，≤2 年 | 1 位为主 | **7 节**：立项背景 / 研究内容 / 预期目标 / 特色与创新 / 实施方案 / 进度安排 / 经费预算 |
| 创业训练 | 商业计划书、可行性研究、企业模拟运行 | 一般 1 年，≤2 年 | 校内 + **企业** | **9 节**：项目简介 / 申请基础 / 行业与市场 / 竞争与营销 / 组织运营 / 财务分析 / 预期目标 / 其它 / 进度 |
| 创业实践 | 基于成果真实创业，产品或服务落地 | ≤3 年 | 校内 + **企业** | **12 节**：在前者基础上加战略与组织、生产运营、风险控制、创业愿景、实践程度 |

**再分阶段**——四个阶段四份文档：

| 阶段 | 交什么 | 要点 |
|---|---|---|
| 立项申报 | 对应赛道的《项目申请书》 | 项目简介 ≤500 字、申请基础 ≤300 字；创业类勾 A–H 类别（农林/生物医药/化工环境/电子信息软硬件/材料/机械能源/服务咨询） |
| 中期检查 | 大创管理系统提交《中期检查报告》+ 学院中期答辩 | 学院据此择优推荐省级、国家级；中期后不再受理成员与题目变更 |
| 延期 | 《项目进展报告》（附件 7） | 需指导教师签字；只能延一次、≤1 年 |
| 结题验收 | 《项目验收书》 | 结题报告 **≥3000 字 9 节**；专利/论文/其它成果三张表，附件须附专利申请书与刊物封皮目录 |

### 三、本科毕业设计（论文）（本科生院 · 全校本科生）

**三个阶段三份文档，不能互相顶替：**

| 阶段 | 交什么 | 硬指标 | 卡点 |
|---|---|---|---|
| 开题 | 《本科毕业论文（设计）开题报告》+ 开题检查组答辩 | **≥3000 字，8 节**；文献理工 10~15 / 文科 15~20 篇，外文≥3 | 汇报 5~10 min + 答问 5 min；不通过**一周内重新开题**，二次不过重修 |
| 中期检查 | 《本科毕业论文（设计）中期报告》+ 中期检查组答辩 | **5 节**；对照开题进度逐项交代 | 汇报 10~15 min；排后 5~10% 或缺席者**两周内二次中检** |
| 结题 | 论文本体 + 结题检查（论文评阅） | **正文 ≥1.5 万字（含图表）**；结论 400~2000 字；摘要 300 字左右；参考文献 ≥15 篇、外文 ≥3 篇、近五年 ≥1/3 | 指导教师 + 至少 1 位评阅教师；不合格无答辩资格，须延期答辩 |

**再分学科门类**，层次编号不通用：

| 层次 | 理工类 | 人文社科类 |
|---|---|---|
| 章 | `第1章  绪  论` | `第一章  绪  论` |
| 节 | `1.1  课题背景及研究的目的和意义` | `一、问题的提出` |
| 条 | `1.1.1  气体润滑轴承的发展` | `（一）课题来源` |
| 款 | `1.1.1.1  …` | `1. 认知风险` |
| 项 | `（1）气体静压轴承` | `首先……其次……再次……最后……` |

论文全文顺序：

```
封面（含书脊）→ 内封 → 摘  要 → Abstract → 目  录
     → 第1章 绪论 → 第2~N章 → 结  论
     → 参考文献 → 攻读学士学位期间取得创新性成果
     → 原创性声明和使用权限 → 致  谢 → 附录（非必需）
```

本科毕设与研究生论文最容易混的四处——**本科图表只用中文题注、没有英文内封、页眉固定一句话且不分奇偶页、结论不带章号**。四个里错一个，形式审查就退回。

答辩：答辩小组 ≥5 人（≥2 位高级职称），**答辩前 3 天**交论文、外文翻译、图纸与评阅记录表；15~20 分钟汇报 + 5~10 分钟答问；成绩后 5~10% 需集中答辩并查重。

### 四、研究生学位论文 / 实践成果（研究生院 · 2025 年 3 月指南）

**已建规范：学位论文本体与实践成果**（硕士 / 博士，学术学位 / 专业学位）。**未建：开题报告、中期检查、预答辩、盲审材料**——指南不覆盖，要学院模板。

**先分学位层次**，这一层决定六项硬指标：

| 项 | 硕士 | 博士 |
|---|---|---|
| 正文 | 3 万~5 万字 | 6 万~10 万字 |
| 中文摘要 | 理工 500~1000 / 人文 600~1000 字 | 1000~2000 字 |
| 图表题注 | **只用中文** | **中英双语**，中文在上 |
| 页眉 | 单面，固定“哈尔滨工业大学硕士学位论文” | 双面，奇偶不同 |
| 参考文献 | 理工 ≥40 / 人文 ≥50 篇 | 理工 ≥100 / 人文 ≥120 篇 |
| 评阅人/答辩委员会名单及答辩决议页 | 不要求 | **必加** |

**再分学科门类**，两套层次编号不通用：

| 层次 | 理工类 | 人文社科类 |
|---|---|---|
| 章 | `第1章  绪  论` | `第一章  绪  论` |
| 节 | `1.1  课题背景及研究的目的和意义` | `一、问题的提出` |
| 条 | `1.1.1  气体润滑轴承的发展` | `（一）课题来源` |
| 款 | `1.2.5.1  多孔质静压轴承的分类` | `1. 认知风险` |

**专业学位还有一个分叉**：写学位论文，还是提交**实践成果**（调研报告、案例分析报告、产品设计、方案设计、重大装备、仪器设备、软硬件产品、技术标准等，指南表 1 按序号列出）。版式与字数要求相同，内容定位不同。

全文顺序固定，缺一节就是形式审查不过：

```
封面 → 中文内封 → 英文内封 → 摘要 → Abstract → 目录 → Contents
     → 正文（第1～N章）→ 结论 → 参考文献 →（附录）
     → 攻读学位期间取得创新性成果 → 评阅人/答辩委员会名单及答辩决议（博士）
     → 原创性声明和使用权限 → 索引（可选）→ 致谢 → 个人简历
```

和本科毕设差距最大的四处：

- **题注按层次**：硕士中文题注、博士中英双语；图题在下、表题在上，5 号字；三线表，跨页写“表6-1（续表）”并重复表头
- **页眉按层次**：博士奇偶页不同（奇数页本章标题、偶数页校名），硕士单面固定一句话
- **摘要四段式**：背景与目的（≤400 字）/ 主要内容 / 创新成果 / 理论实际意义
- **每章闭环**：除绪论外，每章第一节“引言”、最后一节“本章小结”，缺了盲审直接提

另外两条容易漏：**AI 生成内容要按《标识办法》逐处标注**；**博士必须加评阅人、答辩委员会名单及答辩决议页**。

### 五、课程报告（六类）

实验报告、调研报告、文献综述、课程设计、读书报告、小论文——按评分点反推章节，见 `assignment-types.md`。

### 写之前，一定先问清这四件事

> **① 哪一类？** 大一年度项目 / 大创 / 毕设 / 研究生论文 / 课程作业
> **② 哪个分支？** 大一年度项目问**本部还是深圳**；大创问**哪个赛道**、**校级/省级/国创**；研究生论文问**博士还是硕士**、**学术还是专业学位**、**理工类还是人文社科类**
> **③ 哪个阶段？** 立项 / 中期 / 延期 / 结题（大创四份文档完全不同）；研究生开题/中期/预答辩**没有内置规范**
> **④ 有没有学院模板？** 有就照模板填，没有才按内置规范生成

问错一步的代价：大一年度项目中期（本部 2000 字五小节）、大创创新训练开题（7 节、简介 ≤500 字）、大创创业实践结题（12 节 + 验收书 ≥3000 字）是三套表格、三套字数、三套封面字段；研究生论文的学科门类问错，`第1章/1.1/1.1.1` 与 `第一章/一、/（一）/1.` 全篇标题要重排。skill 的第一步就是这套盘问，见 [`grill-intake.md`](skills/hit-assignment-report/references/grill-intake.md)。

改完按清单逐项自检，不是“看着差不多”。系统缺宋体 / 黑体 / Times New Roman 时自动安装内置开源替代字体，字体回退链写成“宋体, Noto Serif SC”，学校打印店有原字体时会自动用原字体，版式不跑位。

<a id="academic-integrity"></a>

> ## 学术诚信声明
>
> 本项目只解决三件事：**格式合规、文献真实、表达质量**。不提供、也不为以下行为提供任何帮助：
>
> - **代写**：生成作业/报告/论文供他人作为本人成果提交
> - **抄袭与洗稿**：搬运他人成果、拼接段落、用同义词替换规避查重
> - **伪造**：编造实验数据、调研结果、参考文献、页码卷期、评审意见或签字
> - **规避审查**：绕过查重系统、AIGC 检测、答辩或中期检查
>
> 使用本工具产出的一切内容，**署名与学术责任由使用者本人承担**。请遵守《高等学校预防与处理学术不端行为办法》、哈尔滨工业大学学术规范及院系具体规定；引用他人观点必须标注来源，提交前自行核对每一条数据与文献。知网资源仅限个人学习使用，须遵守其服务条款。
>
> 若你的诉求是“帮我写一份能交上去的作业”，请先向任课教师确认 AI 使用的边界。本 skill 在流程里强制要求确认真实文献与真实数据，正是为了避免把工具变成学术不端的加速器。

## 目录

- [能写什么](#能写什么)
- [Word 排版](#word-format)
- [报告全景](#report-map)
- [学校规范原件（templates/ 全部模板）](#templates)
- [学术诚信声明](#academic-integrity)
- [获取 WorkBuddy](#获取-workbuddy)
- [Skills 一览](#skills-一览)
- [快速开始](#快速开始)
- [典型用法：一份课程报告](#典型用法一份课程报告)
- [设计要点](#设计要点)
- [目录结构](#目录结构)
- [依赖](#依赖)
- [常见问题](#常见问题)
- [维护约定](#维护约定)
- [License](#license)

## 获取 WorkBuddy

这些 skill 面向 [WorkBuddy](https://www.workbuddy.cn) 这样的 Agent 客户端编写，装进去就能用。还没有的话，扫码或点邀请链接注册：

<p align="center">
  <a href="https://www.workbuddy.cn/events/invite?inviteCode=08foyuwog">
    <img src="assets/workbuddy-qr.png" width="150" alt="WorkBuddy 邀请二维码">
  </a>
</p>

**邀请链接**：https://www.workbuddy.cn/events/invite?inviteCode=08foyuwog
（通过该链接注册可得 2000 积分，活动规则以官方页面为准）

<details>
<summary>展开邀请海报</summary>
<p align="center">
  <img src="assets/workbuddy-invite.png" width="300" alt="WorkBuddy 邀请海报">
</p>
</details>

## Skills 一览

| Skill | 用途 | 触发示例 |
|---|---|---|
| [hit-assignment-report](skills/hit-assignment-report/SKILL.md) | 报告与论文撰写主流程：需求采集 → 按评分点/评审点搭结构 → 真实文献支撑 → 去 AI 味 → 引用对账 → 封面与排版。含**大一年度项目**立项/中期/结题、**校级大创**四类文档、**本科毕业设计（论文）**开题/中期/结题三阶段、**研究生学位论文**（硕士/博士）的骨架 | “写课程报告”、“写实验报告”、“写立项报告”、“大一年度项目”、“写开题报告”、“写毕设论文”、“写学位论文” |
| [hit-cnki-refs](skills/hit-cnki-refs/SKILL.md) | 知网检索 → 批量读摘要 → 筛选候选 → 下载 PDF/CAJ → 校验归档。CDP 驱动本机浏览器，校园网 IP 免登录 | “查文献”、“下载知网文献”、“参考文献” |
| [hit-standard-word-type](skills/hit-standard-word-type/SKILL.md) | 按 HIT 排版规范排版 Word：字体字号、三线表、图题、公式编号、GB/T 7714-2005 参考文献、打印装订。含**大一年度项目**（本部 + 深圳）、**大创**、**研究生学位论文**（理工类/人文社科类）专用格式 | “HIT 排版”、“论文格式规范”、“调整报告格式” |

### 开工先盘问，不猜着写

`hit-assignment-report` 的第 1 步是**盘问协议**（[`grill-intake.md`](skills/hit-assignment-report/references/grill-intake.md)），照着 grill-me 的做法：一次只问一个问题，每题先给推荐答案，等用户回话再走下一个。顺序固定：

```
规范归属 → 版本（校区/学院）→ 阶段 → 题目与要求原文 → 评分标准 → 素材 → 文献 → 交付
```

典型第一句是：**“这次是课程作业，还是学校统一组织的项目报告（大一年度项目 / 大创 / 毕设）？哪个校区、哪个阶段？”** —— 问清才动笔，避免写完才发现校区写错、字数差一倍。

八项都有确定值、没有“待定”才结束盘问；答案落进 `00-intake.md`，复述一遍让用户确认。用户说“你看着办”时按默认值处理，但要写明假设。

### 已封装的学校专用规范

| 规范 | 覆盖内容 | 文件 | 状态 |
|---|---|---|---|
| 大一年度项目（写作） | 立项 / 中期 / 结题 × 本部 / 深圳两校区：封面字段差异、成员表列名、字数（本部中期 2000 字 / 深圳中期 1500 字+600 字基本信息）、章节配比、评审关注点、交付清单 | [`annual-project.md`](skills/hit-assignment-report/references/annual-project.md) | ✅ |
| 大一年度项目（排版） | A4 + 页边距 2cm + 网格 46×43 + 行距 16 磅、封面一号黑体、正文小四宋体、标题层级 `一`→`1.`→`（1）`、结题论文体（二号黑体题名 / 四号楷体作者 / 五号摘要）、8 类参考文献著录示例 | [`annual-project-format.md`](skills/hit-standard-word-type/references/annual-project-format.md) | ✅ |
| 大创（写作） | 三个赛道的申请书（创新训练 7 节 / 创业训练 9 节 / 创业实践 12 节）、中期检查报告、延期用的项目进展报告、项目验收书（≥3000 字结题报告 + 专利/论文成果表）、全流程时间线与经费规则（中期后可用 30%，结题合格报 70%） | [`dachuang.md`](skills/hit-assignment-report/references/dachuang.md) | ✅ |
| 大创（排版） | 封面宋体加粗小二（18pt）、字段小四加粗、表头五号、正文小四宋体、行距保持模板原样；进展报告标题小三、要点五号；与大一年度项目模板的差异对照 | [`dachuang-format.md`](skills/hit-standard-word-type/references/dachuang-format.md) | ✅ |
| 本科毕业设计（论文）（写作） | 三阶段分开：开题 8 节 ≥3000 字（含文献数量与外文比例）、中期 5 节、结题论文结构与字数；每章“引言 + 本章小结”、结论三段式、成果页、答辩与结题检查要点、常见扣分点、与研究生论文的差异对照 | [`undergrad-thesis.md`](skills/hit-assignment-report/references/undergrad-thesis.md) | ✅ |
| 本科毕业设计（论文）（排版） | A4 + 上 3.8/下 3.0/左右 3.0 cm、版心 150×240 mm、单面；封面题头宋体小1号加粗、中英题目字号、中文内封七行（冒号左黑体4号右宋体4号、行距1.5）；页眉粗细双线不分奇偶页；章标题段前1行段后0.8行；图表**中文单语**题注、序号后空 2 个半角字符；三线表与续表；公式与引用标注；参考文献 GB/T 7714—2015；成果页/原创性声明/致谢/附录；附版式截图 | [`undergrad-thesis-format.md`](skills/hit-standard-word-type/references/undergrad-thesis-format.md) | ✅ |
| 研究生学位论文 / 实践成果（写作） | 五问前置（硕/博 × 学术/专业 × 论文/实践成果 × 理工/人文 × 学院模板）、硬指标表（字数/摘要/文献/题注/页眉/评阅人页）、学位论文类型表与实践成果类型表、摘要四段式、绪论四块、结论三段式、成果页、AI 标识、盲审扣分点、与本科毕设的差异 | [`graduate-thesis.md`](skills/hit-assignment-report/references/graduate-thesis.md) | ✅ |
| 研究生学位论文 / 实践成果（排版） | A4 + 上 3.8/下 3.0/左右 3.0 cm、版心 150×240 mm；封面全字段字号、内封 9 项（冒号左黑体4号右宋体4号、行距1.5）、摘要题头与 1.2 倍行距、中英目录格式、两套层次编号、**硕士中文题注/博士双语**、三线表与续表、公式式中说明、引用标注（GB/T 7714—2015）、**博士奇偶页眉/硕士单面固定**、成果页/评阅人页/索引/书脊、AIGC 标识、**与 2021 范例的 9 处差异对照** | [`graduate-thesis-format.md`](skills/hit-standard-word-type/references/graduate-thesis-format.md) | ✅ |
| 研究生开题 / 中期 / 预答辩 | 开题报告、中期检查、预答辩材料 | — | 🚧 待收录（范例未覆盖） |

大一年度项目来自基础部下发的立项 / 中期检查 / 结题模板（两校区共 6 份）；大创来自本科生院《大学生创新训练计划管理办法》（校本〔2024〕61 号）与四类制式模板；本科毕设来自本科生院《本科毕业论文（设计）写作指南》（2022 年 10 月，理工类 / 人文社科类）与《本科毕业设计（论文）工作实施细则》及配套模板；研究生学位论文来自研究生院发布的两份书写范例（理工类、人文社科类）。字段、字数、格式、时间线、经费规则已逐条抽成可执行规范，用户不用再翻原件。遇到还没收录的规范，skill 会直说“还没内置”并索要模板，不凭通用经验硬写。

新增一份规范的做法见 [`spec-catalog.md`](skills/hit-assignment-report/references/spec-catalog.md)（抽结构 → 抽格式 → 写两份文件 → 挂路由 → 标注推定值）。

三者可独立使用，串起来即一条完整的课程报告流水线：

```
hit-cnki-refs（找真文献） → hit-assignment-report（写） → hit-standard-word-type（排版）
```

## 快速开始

### 方式一：把提示词发给 AI，让它自己装（推荐）

不用手动敲命令。把下面整段复粘给你的 Agent（WorkBuddy / Claude Code / Cursor 等），它会自己完成克隆、复制、校验：

```text
请帮我把 GitHub 仓库 YiYiMi11/HIT-skills 里的 3 个 Agent Skill 装到本机。

步骤：
1. 克隆到临时目录（只取最新一次提交）：
   git clone --depth 1 https://github.com/YiYiMi11/HIT-skills.git "${TMPDIR:-/tmp}/hit-skills"
2. 把 skills/ 下这三个文件夹复制到我的用户级 skill 目录：
   hit-assignment-report、hit-cnki-refs、hit-standard-word-type
   - WorkBuddy 用户级目录是 ~/.workbuddy/skills/（不存在就创建）
   - 若你跑在别的工具里，换成该工具的 skill 目录，并在最后告诉我实际路径
3. 若目标目录已有旧名 skill（cnki-refs、HIT-standard-word-type），先删除旧目录，避免两套并存。
4. 校验并报告：
   - 每个 SKILL.md 的 frontmatter name 与所在文件夹名一致
   - scripts/*.sh 有可执行权限（必要时 chmod +x）
   - assets/fonts/ 下 5 个 .ttf 齐全（约 41MB），缺失说明克隆不完整
5. 删除临时克隆目录。
6. 输出结果：装成功的 skill 名称、绝对路径、每个 skill 的触发词。

约束：
- 不要修改 skill 内任何文件。
- 不要执行 scripts/ 下的脚本：hit-cnki-refs 依赖校园网与本机浏览器，我会自己跑 check。
- 需要覆盖已有文件前先列出来问我。
```

只装其中一个也可以，把第 2 步的文件夹名换成你要的那个（常单独装的是 `hit-standard-word-type`）。

嫌上面太长时，这段一行版同样够用：

```text
把 https://github.com/YiYiMi11/HIT-skills 里 skills/ 下的三个文件夹装到你的用户级 skill 目录
（WorkBuddy 为 ~/.workbuddy/skills/），保持 frontmatter name 一致、.sh 可执行，装完告诉我路径和触发词。
```

装完后**新开一个会话**，skill 才会被加载。问一句“你现在有哪些 skill”可以验证。

### 方式二：手动安装

```bash
git clone https://github.com/YiYiMi11/HIT-skills.git
cd HIT-skills
```

**WorkBuddy**：复制到用户级 skill 目录，新会话即可自动触发：

```bash
mkdir -p ~/.workbuddy/skills
cp -r skills/hit-cnki-refs skills/hit-assignment-report skills/hit-standard-word-type ~/.workbuddy/skills/
```

**其他 Agent Skills 工具**：skill 遵循 [Agent Skills 规范](https://agentskills.io)——每个 skill 是含 `SKILL.md`（YAML frontmatter + 指令）的文件夹，可选附 `scripts/`、`references/`、`assets/`。放入对应工具的 skill 目录即可。

> 若之前装过旧名（`cnki-refs`、`HIT-standard-word-type`），先删除旧目录再复制，避免两套并存。


## 典型用法：一份课程报告

`hit-assignment-report` 是主流程，另外两个是它的工具。

### 0. 环境自检

```bash
bash skills/hit-cnki-refs/scripts/start_browser.sh   # 以调试端口启动浏览器，只需一次
python3 skills/hit-cnki-refs/scripts/cnki.py check   # 检查浏览器连接 + 知网可达 + 机构权限
```

`check` 不过就先解决环境，不要用记忆里的文献凑数。

### 1. 检索 → 泛读 → 筛选

```bash
python3 skills/hit-cnki-refs/scripts/cnki.py search "锂离子电池 热失控 机理" "锂电池 预警 方法" --limit 20
python3 skills/hit-cnki-refs/scripts/cnki.py abstract --limit 40
python3 skills/hit-cnki-refs/scripts/cnki.py shortlist --n 30
# ↑ 此处停下来，把 A/B/C 分档清单交给用户确认
```

### 2. 确认 → 下载 → 校验

```bash
python3 skills/hit-cnki-refs/scripts/cnki.py confirm --keys k1,k2,k3
python3 skills/hit-cnki-refs/scripts/cnki.py download --prefer pdf
python3 skills/hit-cnki-refs/scripts/cnki.py verify    # md5 / 大小 / 摘要快照全部对得上才算过
```

### 3. 写作与对账

正文只写 `[@key]` 占位，参考文献列表由脚本从 `refs/refs.json` 渲染：

```bash
python3 skills/hit-assignment-report/scripts/refs_audit.py check  --draft 03-final.md --refs refs
python3 skills/hit-assignment-report/scripts/refs_audit.py render --draft 03-final.md --refs refs --out 04-交付稿.md
python3 skills/hit-assignment-report/scripts/style_lint.py 04-交付稿.md
```

`refs_audit.py check` 退出码非 0 就不允许交付：正文里每个 `[@key]` 必须在 `refs.json` 里有条目、有原文文件、且文件校验通过；反过来 `refs.json` 里也不许有正文未引用的死条目。

### 4. 排版

交给 `hit-standard-word-type`。缺宋体/黑体/Times New Roman 的机器：

```bash
bash skills/hit-standard-word-type/scripts/install_fonts.sh
```

## 设计要点

**为什么参考文献不会编造。** 模型没有权限写参考文献列表。正文只允许写 `[@key]`，编号与条目全部由 `refs_audit.py` 从 `refs/refs.json` 渲染；而 `refs.json` 每一条都来自知网页面 DOM，并绑定一个真实存在的 PDF/CAJ 文件（校验存在性、大小、md5、摘要快照）。对账不过，脚本退出码非 0。

**为什么下载能跑通。** 知网下载接口校验 Referer 与来源应用，程序化点击和直接 navigate 都会失败。唯一可行方式是页面内 `focus + Enter`（保留用户手势与上下文），且 PDF 要从详情页 `#pdfDown` 取。细节与选择器校准方法见 [`hit-cnki-refs/references/cnki-workflow.md`](skills/hit-cnki-refs/references/cnki-workflow.md)。

**为什么去 AI 味靠流程而不是靠改写。** 写完再润色只会变成“AI 文本 + 同义词替换”，痕迹更重。规则（句长节奏、段落长短交错、禁用套话表）在写作时就用，`style_lint.py` 只做机检兜底：段落长度变异系数、短句占比、套话计数。

**为什么规范原文单独放 references/。** SKILL.md 只留触发条件、速查表和工作流，细则按需读取，避免每次对话都把上万字规范塞进上下文。

<a id="templates"></a>

## 学校规范原件

学校下发的模板、管理办法与书写范例原件放在 [`templates/`](templates/)，文件格式与版式就是官方原件，可直接复制去填。

### 来源一览（每次收录新文件都要更新这张表）

| 类别 | 官方来源 | 发布单位 / 版本 | 入库路径 | 对应规范文件 |
|---|---|---|---|---|
| 大一年度项目 | 待补 | 基础学部《大一年度项目计划管理规范（试行）》2016-10-09 + 两校区三套模板 | [`templates/annual-project/`](templates/annual-project/) | `annual-project.md` + `annual-project-format.md` |
| 校级大创 | 待补 | 本科生院，《管理办法》校本〔2024〕61 号（2024-12-23 印发） | [`templates/dachuang/`](templates/dachuang/) | `dachuang.md` + `dachuang-format.md` |
| 本科毕业设计（论文） | <https://hituc.hit.edu.cn/2025/0411/c18057a366366/page.psp> | 本科生院，《本科毕业论文（设计）写作指南》2022 年 10 月 | [`templates/undergrad-thesis/`](templates/undergrad-thesis/) | `undergrad-thesis.md` + `undergrad-thesis-format.md` |
| 研究生学位论文 / 实践成果 | <https://hitgs.hit.edu.cn/2021/0513/c17373a317228/page.htm>（范例·理工类）<br><https://hitgs.hit.edu.cn/2021/0508/c17373a317224/page.htm>（范例·人文社科类）<br>《写作指南》《实践成果写作指南》网址待补 | 研究生院：《研究生学位论文写作指南》《研究生实践成果写作指南》**2025 年 3 月**；书写范例 2021-05 | [`templates/graduate-thesis/`](templates/graduate-thesis/) | `graduate-thesis.md` + `graduate-thesis-format.md` |

> “待补”表示来源网址尚未取得，不要凭猜测填写。补齐后替换本行。

### 各目录文件清单

| 目录 | 内容 |
|---|---|
| [`templates/annual-project/`](templates/annual-project/) | 大一年度项目 7 份：本部与深圳各 3 份（立项 / 中期检查 / 结题）+ 管理规范（试行），全部为 .docx |
| [`templates/dachuang/`](templates/dachuang/) | 大创 5 份（三赛道申请书 + 进展报告 + 验收书）+ 管理办法 PDF（校本〔2024〕61 号） |
| [`templates/graduate-thesis/`](templates/graduate-thesis/) | 研究生 6 份：学位论文写作指南 2、实践成果写作指南 2、书写范例 2（理工类 13 MB，含插图示例） |
| [`templates/undergrad-thesis/`](templates/undergrad-thesis/) | 本科毕业设计（论文）12 份：写作指南 2、书写范例 2、开题/中期报告、过程管理记录表、工作实施细则、撰写规范、原创性声明、封面参考与封面样例（21 MB，含插图与校色封面） |

清单与来源说明见 [`templates/README.md`](templates/README.md)。大一年度项目与大创已核查全部为空白件，不含姓名、学号、手机号；研究生范例是公开发布的示范稿。模板可能随年度修订，**正式提交以学院当年下发版本为准**。

研究生学位论文的两份范例取自研究生院官网，内容与官网下载件一致（原件为 .doc，仓库内统一转存为 .docx，逐页页数/字符数与转换前完全相同）：

| 文件 | 官方地址 | 对应 skill 规范 |
|---|---|---|
| `研究生学位论文书写范例-理工类.docx` | <https://hitgs.hit.edu.cn/2021/0513/c17373a317228/page.htm> | `graduate-thesis-format.md` §0 理工类编号 |
| `研究生学位论文书写范例-人文社科类.docx` | <https://hitgs.hit.edu.cn/2021/0508/c17373a317224/page.htm> | `graduate-thesis-format.md` §0 人文社科类编号 |

两份范例均由哈尔滨工业大学研究生院发布。它们不是空白模板，而是**带批注的示范稿**（用“↑（宋体小1号字加粗）”这类标注指出每处格式），填写时须把示例文字与示例图表全部替换掉，示例论文的研究内容不复制、不转述。

本科毕业设计（论文）的全套原件来自本科生院：<https://hituc.hit.edu.cn/2025/0411/c18057a366366/page.psp>

| 类别 | 文件 | 用途 |
|---|---|---|
| 规范 | `本科毕业论文写作指南-理工类.docx` / `-人文社科类.docx` | 2022 年 10 月版，现行写作与排版依据（含六类文献著录示例、封面示例） |
| 规范 | `哈尔滨工业大学本科生毕业论文撰写规范.docx` | 旧版全文（GB/T 7714—2005 时期），差异对照见 `undergrad-thesis-format.md` §17 |
| 流程 | `哈尔滨工业大学本科毕业设计（论文）工作实施细则.docx` | 选题/开题/中期/结题/答辩全流程要求与时间点 |
| 范例 | `本科毕业论文书写范例-理工类.docx` / `-人文社科类.docx` | 带批注的版式示范稿 |
| 模板 | `本科毕业论文（设计）开题报告.docx` / `中期报告.docx` | 教务处制式表格，直接填 |
| 模板 | `本科毕业论文（设计）过程管理记录表.docx` | 任务书 + 开题/中期/结题/答辩四张记录表，院系归档用 |
| 模板 | `本科毕业论文单独封面参考.docx` / `本科毕业论文（设计）封面样例.jpg` | 蓝色统一封面与书脊，照此打印 |
| 附件 | `HIT本科毕业论文原创性声明和使用权限.docx` | 声明页，签名留空手签 |

skill 里的规范就是从这些原件里逐条抽出来的：原件看版式，规范看要求。

## 目录结构

```
HIT-skills/
├── README.md
├── LICENSE                                # Apache-2.0
├── assets/                                # 邀请二维码与海报
│   ├── workbuddy-qr.png
│   └── workbuddy-invite.png
├── templates/                             # 学校下发的模板与规范原件
│   ├── annual-project/                    # 大一年度项目 6 份（本部 .doc / 深圳 .docx）
│   ├── dachuang/                          # 大创 5 份 + 管理办法 PDF
│   ├── graduate-thesis/                   # 研究生学位论文书写范例 2 份（理工类 / 人文社科类）
│   └── undergrad-thesis/                  # 本科毕设 12 份（指南/范例/开题/中期/细则/声明/封面）
└── skills/
    ├── hit-assignment-report/             # 课程报告撰写主流程
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── intake.md                  # 需求采集单
    │   │   ├── grill-intake.md            # 盘问协议：开工前八问
    │   │   ├── spec-catalog.md            # 规范库索引 + 新增规范的流程
    │   │   ├── assignment-types.md        # 六类作业骨架
    │   │   ├── annual-project.md          # 大一年度项目：立项/中期/结题 × 两校区
    │   │   ├── dachuang.md                # 大创：三赛道 × 申请书/中期/进展/验收
    │   │   ├── undergrad-thesis.md        # 本科毕设：开题8节/中期5节/结题论文、答辩要点
    │   │   ├── graduate-thesis.md         # 研究生学位论文：章节骨架、绪论/结论写法、盲审扣分点
    │   │   ├── rubric-mapping.md          # 评分点 → 结构映射
    │   │   ├── anti-ai-style.md           # 去 AI 味规则
    │   │   └── cover-spec.md              # 封面规范
    │   └── scripts/
    │       ├── refs_audit.py              # 引用三向对账（硬闸门）
    │       └── style_lint.py              # 去 AI 味机械检测
    ├── hit-cnki-refs/                     # 知网文献检索/泛读/下载/校验
    │   ├── SKILL.md
    │   ├── references/cnki-workflow.md    # 选择器、踩坑、人工接管协议
    │   └── scripts/
    │       ├── cnki.py                    # check/search/abstract/shortlist/confirm/download/ingest/verify
    │       ├── cdp_min.py                 # 零依赖 CDP 客户端
    │       └── start_browser.sh           # 以调试模式启动浏览器
    └── hit-standard-word-type/            # HIT 报告排版规范
        ├── SKILL.md
        ├── references/
        │   ├── formatting-spec.md         # 通用排版规范完整原文
        │   ├── annual-project-format.md   # 大一年度项目专用模板格式
        │   ├── dachuang-format.md         # 大创模板格式（含与大一年度项目差异）
        │   ├── graduate-thesis-format.md  # 研究生学位论文格式（理工类 / 人文社科类两套编号）
        │   └── undergrad-thesis-format.md # 本科毕设格式（开题/中期/结题，附版式截图）
        ├── scripts/install_fonts.sh       # 内置替代字体一键安装
        └── assets/
            ├── fonts/                     # 开源替代字体（Noto Serif/Sans SC、Liberation Serif）
            └── undergrad-thesis-examples/ # 本科毕设版式截图（封面/内封/目录/三线表/续表）
```

## 依赖

| 项目 | 要求 |
|---|---|
| Python | 3.8+，**仅标准库**，无需 `pip install` |
| 浏览器 | Chrome / Edge / Chromium 任一（`hit-cnki-refs` 需要） |
| 网络 | 知网需校园网环境，IP 自动识别机构权限，无需账号登录 |
| 字体 | 可选；缺字体时用 `install_fonts.sh` 装内置开源替代字体 |

## 常见问题

**装完 skill 但 AI 不触发。**
先新开会话（skill 列表在会话启动时加载）。仍不触发就检查：文件夹直接位于 `<skill 目录>/hit-xxx/`，而不是多套了一层；`SKILL.md` 在文件夹根、frontmatter 有 `name` 与 `description`；`name` 与文件夹名一致。

**`cnki.py check` 报连不上浏览器。**
先 `bash skills/hit-cnki-refs/scripts/start_browser.sh`。该脚本会用独立 user-data-dir 和调试端口启动浏览器，不要用日常浏览器实例。

**找不到 PDF 下载按钮 / 选择器全部失效。**
知网前端会改版。按 `cnki-workflow.md` 的方法在页面里重新探测选择器，再更新 `cnki.py` 顶部常量。

**下载全部失败，产出 `refs/pending-download.md`。**
走人工接管协议：脚本已放弃自动重试，改用人工或 Computer Use 在页面里点击下载，之后 `cnki.py ingest` 把文件登记进 `refs.json`。

**Word 里字体显示不对。**
系统缺宋体/黑体/Times New Roman。跑 `install_fonts.sh` 装内置替代字体，规范里的字号字距会保持等效。

**报告读起来还是有 AI 味。**
说明写作阶段没按 `anti-ai-style.md` 执行，靠 `style_lint.py` 事后修补无效。回到写作环节重来。

## 维护约定

- 每个 skill 一个文件夹，文件夹名与 frontmatter `name` 一致；一律小写、`hit-` 前缀、单词间用 `-` 连接。
- 细则规范放 `references/`，`SKILL.md` 只保留触发条件、速查表与工作流（渐进式加载，省上下文）。
- **写与排必须双写**：新增/修改一份规范，`hit-assignment-report/references/` 与 `hit-standard-word-type/references/` 要同时落地，只改一侧等于没改完。
- 脚本只依赖标准库；知网选择器失效时按 `cnki-workflow.md` 的方法重新探测。
- 新增 skill 后同步更新 README 的 [Skills 一览](#skills-一览) 与目录结构。
- 学校原件统一放 `templates/<主题>/`，用中文可读名字归档，原件只读不改。
- **模板、范例、制式表格类原件先转 PDF 截图核对版式**，再动笔写规范：表题是否居中、续表靠哪边、页眉在哪一侧、字段是否分散对齐，这些纯文本读不出来。
- 本仓库文档自身也遵守中文标点规范：全角标点、双引号“”、单引号‘’，不用英文直引号（代码与命令示例除外）。

## License

代码与文档：[Apache-2.0](LICENSE)。
内置字体：Noto Serif SC / Noto Sans SC 为 SIL Open Font License 1.1，Liberation Serif 为 SIL OFL，详见 [`skills/hit-standard-word-type/assets/fonts/`](skills/hit-standard-word-type/assets/fonts/)。

> 本项目仅供个人学习与校内作业流程自动化使用。**禁止用于代写、抄袭、伪造数据或规避学术审查**——详见开头的[学术诚信声明](#academic-integrity)。使用知网资源请遵守其服务条款与学校相关规定。
