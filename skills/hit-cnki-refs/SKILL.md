---
name: hit-cnki-refs
description: 从中国知网（CNKI）检索真实文献、批量读摘要、筛选候选、下载 PDF/CAJ 到本地文件夹并校验。当需要为课程报告/论文查找真实参考文献、需要"文献必须真实且带原文文件"、或提到"知网""CNKI""查文献""下载文献""参考文献"时使用。可通过 CDP 驱动本机浏览器在校园网环境下自动化操作知网。
---

# 知网文献检索与归档

## 这个 skill 解决什么

让报告里每一条参考文献都有**真实的原文文件**躺在 `refs/` 里。模型的职责是筛选和判断，不是回忆文献——所有题录从知网页面 DOM 抓取，模型没有机会编造。

## 前置条件（每次开工先跑）

```bash
python3 scripts/cnki.py check
```

输出里这三项必须成立，否则后面的步骤全部会失败：

| 字段 | 要求 | 不满足时 |
|---|---|---|
| `cdp` | 浏览器已以调试模式启动 | 见 `references/cnki-workflow.md` 的启动命令 |
| `org` | 页面显示本校机构名（IP 识别） | 校园网没连上，或需 WebVPN |
| `search_ready` | 检索框存在 | 被安全验证页拦住 |

退出码 2 = 环境不可用，别硬往下做。

## 命令一览

| 命令 | 作用 | 关键参数 |
|---|---|---|
| `check` | 环境自检 | `--org 哈尔滨工业大学` |
| `search "词1" "词2"` | 检索，写入候选池 | `--limit 20`（每组词取多少条） |
| `abstract` | 逐篇打开详情页抓摘要（泛读层） | `--limit 40` |
| `shortlist` | 生成分档候选清单供人确认 | `--n 30` |
| `confirm --keys a,b,c` | 锁定要引用的条目 | `--section 第2章` |
| `download` | 下载已确认条目，**PDF 优先** | `--prefer pdf` `--limit 15` |
| `ingest --from ~/Downloads` | 归档手工下载的文件 | `--threshold 0.5` |
| `verify` | 校验文件存在/大小/md5/摘要 | — |

## 标准流程

**第 1 步 · 多角度检索（宁可多，不可少）**

按报告的每一节各生成 1–2 组检索词，一次跑完：

```bash
python3 scripts/cnki.py search "锂离子电池 热失控 机理" "锂电池 热失控 预警 方法" "储能电池 安全 评估"
```

检索词写法：主题词 + 限定词（机理/方法/综述/应用），必要时加年份。不同检索词会带出不同文献池，这是"大量阅读"的基础。

**第 2 步 · 泛读摘要**

```bash
python3 scripts/cnki.py abstract --limit 40
```

每篇约 1.2 秒，40 篇约 1 分钟。**必须真的读摘要再筛**——这是防编造和写好综述的前提，跳过这步等于瞎选。

**第 3 步 · 生成候选清单**

```bash
python3 scripts/cnki.py shortlist --n 30
```

产出 `refs/02-shortlist.md`：A/B/C 分档，含篇名、作者、来源、下载量、摘要前 110 字。脚本的排序只是启发式，**你要在清单基础上加自己的判断**：哪篇真正支撑哪一节、哪篇只是重复。

**第 4 步 · 停下来等用户确认（硬性闸门）**

把候选清单和你的推荐（每篇一句话说明用它支撑什么）呈现给用户，**等用户明确勾选后才执行 confirm**。不要自己替用户决定引用哪些、也不要在没确认前就下载。

**第 5 步 · 下载**

```bash
python3 scripts/cnki.py confirm --keys key1,key2,key3
python3 scripts/cnki.py download --prefer pdf
```

PDF 优先：脚本先到详情页找「PDF下载」按钮，没有才退回 CAJ。全部失败时产出 `refs/pending-download.md`，此时**改由人工或 Computer Use 接管**（见 `references/cnki-workflow.md`）。

**第 6 步 · 校验**

```bash
python3 scripts/cnki.py verify
```

退出码非 0 就回去补，不要带着未校验的文献写正文。

## 铁律

1. **不许手写参考文献**。正文用 `[@key]` 占位，编号和条目由 `hit-assignment-report` 的 `refs_audit.py` 渲染。
2. **不许用 `verify` 未通过的文献**。
3. **CAJ 只做存在性校验**，内容核对靠 `abstract` 抓下来的摘要快照；同一主题有 PDF 时不允许用 CAJ 版本。
4. **下载频率**：单批 ≤15 篇，间隔 ≥2.5s。触发滑块就停下人工过一次，别硬刷。
5. **检索留痕**：每次检索都写进 `refs.json` 的 `searches`，老师质疑时可回放。

## 已知的坑

| 现象 | 原因 | 处理 |
|---|---|---|
| 打开知网落到 `/verify/home` | 安全验证（拼图） | 等 40s 自动放行；不行就人工拖一次，cookie 会持久化 |
| 页面无「哈尔滨工业大学」 | 校园网断了/IP 未识别 | 连回校园网重跑 `check` |
| 鼠标点击下载没反应 | 弹窗被拦 + 丢 referer | 已改用 `focus + Enter`，勿改回鼠标点击 |
| `bar.cnki.net/bar/ErrorMsg.html` | 直接访问 order 链接，来源应用校验失败 | 必须从页面内触发，不能直接 navigate |
| 只有 CAJ 没有 PDF | 部分期刊/学位论文只提供 CAJ | 允许，但记 `presence_only`；看摘要快照核对 |
| 结果行数 0 | 检索词过窄或限定了错误的库 | 放宽词，或去掉特殊符号 |

细节操作与选择器见 `references/cnki-workflow.md`。
