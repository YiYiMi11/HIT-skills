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
| **大创**（校级 / 国家级）：立项 / 中期 / 结题 | 与大一年度项目同一套流程；规范正在入库，未收录时会向你索要学院模板，按官方表格写，不凭通用经验硬编 |
| **毕业设计（论文）**：开题 / 中期 / 结题 | 开题论证、文献综述、任务书、外文翻译；规范正在入库 |
| **研究生学位论文**：开题 / 中期 / 预答辩 | 同上，按学位类型与学院要求区分 |
| **课程报告** | 实验报告、调研报告、文献综述、课程设计、读书报告、小论文六类骨架，按评分点反推章节 |
| **参考文献** | 知网检索 → 批量读摘要 → 你确认 → 下载 PDF/CAJ → md5 校验；正文只写 `[@key]`，编号由脚本渲染 |
| **Word 排版** | [专章说明 ↓](#word-format)：大一年度项目、大创、毕设各用各的模板规格；三线表、图表编号、公式、参考文献著录、封面字段全部按规范落地 |

**它不是"帮你写一段话"的写作助手，而是把学校那套规矩做成可执行的流程：**

- **开工先盘问**：校区、阶段、字数、有没有官方模板，问清楚才动笔，不替用户猜
- **文献不许编**：每条参考文献都绑定知网上真实存在的原文文件，对账不过脚本直接拒绝交付
- **格式不用操心**：字体字号、行距、文档网格、图表编号、参考文献著录按规范落到 Word 里

<a id="word-format"></a>

## Word 排版：格式类返工，一次消掉

写报告真正耗时的往往不是内容，是把格式调成学院要求的样子。这部分直接交给 skill：

- **页面**：A4、页边距、文档网格、行距、页脚页码
- **文字**：各级标题的字体字号与段前段后、正文宋体小四、数字与英文 Times New Roman、首行缩进
- **图表**：三线表（顶线 / 栏目线 / 底线磅值）、表题在上、图题在下、按章编号、正文有"如图 X-X 所示"的提示
- **公式与参考文献**：公式居中、编号右端对齐；参考文献按 GB/T 7714-2005 顺序编码制，正文上角标与条目一一对应
- **封面**：按报告类型填字段，不留空

| 你在排什么 | 依据 | 关键规格 |
|---|---|---|
| **大一年度项目** 立项 / 中期 / 结题（本部、深圳） | `annual-project-format.md` | A4 + 四边 2cm + 文档网格 46 字×43 行 + 行距 16 磅；封面一号黑体；正文小四宋体；标题层级只用 `一` → `1.` → `（1）`；正文自建表格一律三线表（顶线/底线 1.5 磅、栏目线 0.75 磅、无竖线），模板固定的成员表与成果表保留原框线；结题论文体（题名二号黑体、作者四号楷体、摘要五号） |
| **大创、毕业设计、研究生论文、课程论文** | `formatting-spec.md`（HIT 通用规范） | 章标题黑体小二、节标题黑体小三、条标题黑体四号、正文宋体小四、多倍行距 1.25、三线表、图表按章编号、参考文献 GB/T 7714-2005 |
| **手上已有 .docx，只想改格式** | 按报告类型选上面两份之一 | 不动内容，只改样式、标题层级、图表题位置与编号、参考文献格式 |

两份规范的分工是一句话：**大一年度项目模板写明的按模板，模板没写清或没提的回落 HIT 通用规范**（三线表线宽、公式编号、插图编排、目录、物理量斜体、装订都在这一档），两边都没写的按通用规范最近条款处理并在交付说明里注明。

改完按清单逐项自检，不是"看着差不多"。系统缺宋体 / 黑体 / Times New Roman 时自动安装内置开源替代字体，字体回退链写成"宋体, Noto Serif SC"，学校打印店有原字体时会自动用原字体，版式不跑位。

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
> 若你的诉求是"帮我写一份能交上去的作业"，请先向任课教师确认 AI 使用的边界。本 skill 在流程里强制要求确认真实文献与真实数据，正是为了避免把工具变成学术不端的加速器。

## 目录

- [能写什么](#能写什么)
- [Word 排版](#word-format)
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
| [hit-assignment-report](skills/hit-assignment-report/SKILL.md) | 课程报告作业撰写主流程：需求采集 → 按评分点搭结构 → 真实文献支撑 → 去 AI 味 → 引用对账 → 封面与排版。含**大一年度项目**立项/中期/结题三类报告骨架 | "写课程报告"、"写实验报告"、"写立项报告"、"大一年度项目" |
| [hit-cnki-refs](skills/hit-cnki-refs/SKILL.md) | 知网检索 → 批量读摘要 → 筛选候选 → 下载 PDF/CAJ → 校验归档。CDP 驱动本机浏览器，校园网 IP 免登录 | "查文献"、"下载知网文献"、"参考文献" |
| [hit-standard-word-type](skills/hit-standard-word-type/SKILL.md) | 按 HIT 排版规范排版 Word：字体字号、三线表、图题、公式编号、GB/T 7714-2005 参考文献、打印装订。含**大一年度项目**专用模板格式（本部 + 深圳） | "HIT 排版"、"论文格式规范"、"调整报告格式" |

### 开工先盘问，不猜着写

`hit-assignment-report` 的第 1 步是**盘问协议**（[`grill-intake.md`](skills/hit-assignment-report/references/grill-intake.md)），照着 grill-me 的做法：一次只问一个问题，每题先给推荐答案，等用户回话再走下一个。顺序固定：

```
规范归属 → 版本（校区/学院）→ 阶段 → 题目与要求原文 → 评分标准 → 素材 → 文献 → 交付
```

典型第一句是：**"这次是课程作业，还是学校统一组织的项目报告（大一年度项目 / 大创 / 毕设）？哪个校区、哪个阶段？"** —— 问清才动笔，避免写完才发现校区写错、字数差一倍。

八项都有确定值、没有"待定"才结束盘问；答案落进 `00-intake.md`，复述一遍让用户确认。用户说"你看着办"时按默认值处理，但要写明假设。

### 已封装的学校专用规范

| 规范 | 覆盖内容 | 文件 | 状态 |
|---|---|---|---|
| 大一年度项目（写作） | 立项 / 中期 / 结题 × 本部 / 深圳两校区：封面字段差异、成员表列名、字数（本部中期 2000 字 / 深圳中期 1500 字+600 字基本信息）、章节配比、评审关注点、交付清单 | [`annual-project.md`](skills/hit-assignment-report/references/annual-project.md) | ✅ |
| 大一年度项目（排版） | A4 + 页边距 2cm + 网格 46×43 + 行距 16 磅、封面一号黑体、正文小四宋体、标题层级 `一`→`1.`→`（1）`、结题论文体（二号黑体题名 / 四号楷体作者 / 五号摘要）、8 类参考文献著录示例 | [`annual-project-format.md`](skills/hit-standard-word-type/references/annual-project-format.md) | ✅ |
| 校级 / 国家级大创 | 立项、中期检查、结题验收 | — | 🚧 待收录 |
| 本科毕业设计（论文） | 开题、中期、结题、任务书、外文翻译 | — | 🚧 待收录 |
| 研究生学位论文 | 开题、中期、预答辩、学位论文 | — | 🚧 待收录 |

大一年度项目那两份文件来自基础部下发的立项 / 中期检查 / 结题报告模板（两校区共 6 份），字段、字数、格式已逐条抽成可执行规范，用户不用再翻原件。遇到还没收录的规范，skill 会直说"还没内置"并索要模板，不凭通用经验硬写。

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

装完后**新开一个会话**，skill 才会被加载。问一句"你现在有哪些 skill"可以验证。

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

**为什么去 AI 味靠流程而不是靠改写。** 写完再润色只会变成"AI 文本 + 同义词替换"，痕迹更重。规则（句长节奏、段落长短交错、禁用套话表）在写作时就用，`style_lint.py` 只做机检兜底：段落长度变异系数、短句占比、套话计数。

**为什么规范原文单独放 references/。** SKILL.md 只留触发条件、速查表和工作流，细则按需读取，避免每次对话都把上万字规范塞进上下文。

## 目录结构

```
HIT-skills/
├── README.md
├── LICENSE                                # Apache-2.0
├── assets/                                # 邀请二维码与海报
│   ├── workbuddy-qr.png
│   └── workbuddy-invite.png
└── skills/
    ├── hit-assignment-report/             # 课程报告撰写主流程
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── intake.md                  # 需求采集单
    │   │   ├── grill-intake.md            # 盘问协议：开工前八问
    │   │   ├── spec-catalog.md            # 规范库索引 + 新增规范的流程
    │   │   ├── assignment-types.md        # 六类作业骨架
    │   │   ├── annual-project.md          # 大一年度项目：立项/中期/结题 × 两校区
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
        │   └── annual-project-format.md   # 大一年度项目专用模板格式
        ├── scripts/install_fonts.sh       # 内置替代字体一键安装
        └── assets/fonts/                  # 开源替代字体（Noto Serif/Sans SC、Liberation Serif）
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
- 脚本只依赖标准库；知网选择器失效时按 `cnki-workflow.md` 的方法重新探测。
- 新增 skill 后同步更新 README 的 [Skills 一览](#skills-一览) 与目录结构。

## License

代码与文档：[Apache-2.0](LICENSE)。
内置字体：Noto Serif SC / Noto Sans SC 为 SIL Open Font License 1.1，Liberation Serif 为 SIL OFL，详见 [`skills/hit-standard-word-type/assets/fonts/`](skills/hit-standard-word-type/assets/fonts/)。

> 本项目仅供个人学习与校内作业流程自动化使用。**禁止用于代写、抄袭、伪造数据或规避学术审查**——详见开头的[学术诚信声明](#academic-integrity)。使用知网资源请遵守其服务条款与学校相关规定。
