# HIT Skills

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](#依赖)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-brightgreen.svg)](https://agentskills.io)
[![Dependencies](https://img.shields.io/badge/deps-stdlib%20only-informational.svg)](#依赖)

哈尔滨工业大学（HIT）日常工作流 AI Skill 集。每个 skill 把一项学校工作的规范或流程封装成可复用的 AI 能力，可被 [WorkBuddy](https://www.workbuddy.cn) 等支持 Agent Skills 的工具直接加载。

核心思路：**把「不许编造」做成流程约束，而不是靠模型自觉。** 文献来自知网页面 DOM 并绑定真实原文文件，引用由脚本渲染，对账不过不允许交付。

## 目录

- [Skills 一览](#skills-一览)
- [快速开始](#快速开始)
- [典型用法：一份课程报告](#典型用法一份课程报告)
- [设计要点](#设计要点)
- [目录结构](#目录结构)
- [依赖](#依赖)
- [常见问题](#常见问题)
- [维护约定](#维护约定)
- [License](#license)

## Skills 一览

| Skill | 用途 | 触发示例 |
|---|---|---|
| [hit-assignment-report](skills/hit-assignment-report/SKILL.md) | 课程报告作业撰写主流程：需求采集 → 按评分点搭结构 → 真实文献支撑 → 去 AI 味 → 引用对账 → 封面与排版 | "写课程报告"、"写实验报告"、"写文献综述" |
| [hit-cnki-refs](skills/hit-cnki-refs/SKILL.md) | 知网检索 → 批量读摘要 → 筛选候选 → 下载 PDF/CAJ → 校验归档。CDP 驱动本机浏览器，校园网 IP 免登录 | "查文献"、"下载知网文献"、"参考文献" |
| [hit-standard-word-type](skills/hit-standard-word-type/SKILL.md) | 按 HIT 排版规范排版 Word：字体字号、三线表、图题、公式编号、GB/T 7714-2005 参考文献、打印装订 | "HIT 排版"、"论文格式规范"、"调整报告格式" |

三者可独立使用，串起来即一条完整的课程报告流水线：

```
hit-cnki-refs（找真文献） → hit-assignment-report（写） → hit-standard-word-type（排版）
```

## 快速开始

```bash
git clone https://github.com/YiYiMi11/HIT-skills.git
cd HIT-skills
```

### WorkBuddy

把目标 skill 文件夹复制到用户级 skill 目录，新会话即可自动触发：

```bash
mkdir -p ~/.workbuddy/skills
cp -r skills/hit-cnki-refs skills/hit-assignment-report skills/hit-standard-word-type ~/.workbuddy/skills/
```

### 其他 Agent Skills 工具

skill 遵循 [Agent Skills 规范](https://agentskills.io)：每个 skill 是一个含 `SKILL.md`（YAML frontmatter + 指令）的文件夹，可选附 `scripts/`、`references/`、`assets/`。放入对应工具的 skill 目录即可。

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
└── skills/
    ├── hit-assignment-report/             # 课程报告撰写主流程
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── intake.md                  # 需求采集单
    │   │   ├── assignment-types.md        # 六类作业骨架
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
        ├── references/formatting-spec.md  # 排版规范完整原文
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

> 本项目仅供个人学习与校内作业流程自动化使用。使用知网资源请遵守其服务条款与学校相关规定。
