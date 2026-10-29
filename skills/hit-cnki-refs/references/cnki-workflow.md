# 知网操作细节与踩坑记录

> 本文所有选择器、行为特征均在 Edge 156 / Chromium 内核下实测确认（2026-10）。知网改版频繁，选择器失效时先跑 `scripts/cnki.py check`，再按本文最后的「校准方法」重新探测。

## 1. 启动调试浏览器

本机只装了 Edge，用 Edge 即可（同为 Chromium 内核，CDP 完全兼容）：

```bash
mkdir -p ~/.workbuddy/cnki-profile
open -na "Microsoft Edge" --args \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.workbuddy/cnki-profile" \
  --no-first-run --no-default-browser-check about:blank
```

要点：

- **必须用专用 profile 目录**。用默认 profile 会和已在运行的 Edge 抢锁，导致调试端口起不来。
- 专用 profile 首访知网会遇一次安全验证，通过后 cookie 持久化在 `~/.workbuddy/cnki-profile`，后续不再弹。
- 机构识别靠校园网 IP，**不靠 cookie**，所以换 profile 不影响权限。

## 2. 已确认的页面结构

### 检索首页 `https://kns.cnki.net/kns8s/defaultresult/index`

| 元素 | 选择器 |
|---|---|
| 检索框 | `#txt_search` |
| 检索按钮 | `.search-btn` |
| 结果行 | `table.result-table-list tbody tr` |

结果行内单元格：

| 内容 | 选择器 |
|---|---|
| 篇名 + 详情页链接 | `td.name a` |
| 作者 | `td.author a` |
| 刊名 | `td.source` |
| 日期 | `td.date` |
| 文献类型（期刊/硕士/博士/会议） | `td.data` |
| 下载量 | `td.download` |
| 列表页下载链接 | `td.operat a.downloadlink` |
| 文献密文 ID | `td.seq input.cbItem` 的 `value` |

### 详情页 `https://kns.cnki.net/kcms2/article/abstract?v=...`

| 内容 | 选择器 |
|---|---|
| 题名 | `.wx-tit h1` |
| 作者 | `.author` |
| 摘要 | `#ChDivSummary`，回退 `.abstract-text` |
| 关键词 | `.keywords` |
| 刊名行（含年卷期页） | `.top-tip` |
| **PDF 下载** | `#pdfDown` |
| **CAJ 下载** | `#cajDown` |

## 3. 三个必须知道的机制

### 3.1 输入必须用真实键盘事件

直接 `input.value = "..."` 不行，Vue 双向绑定收不到。正确做法：

```python
page.eval("(()=>{const i=document.querySelector('#txt_search');i.value='';i.focus();})()")
for ch in keyword:
    page.conn.call("Input.dispatchKeyEvent", {"type": "char", "text": ch})
page.eval("document.querySelector('.search-btn').click()")
```

（检索按钮用 `.click()` 是可以的，它不涉及弹窗/新标签。）

### 3.2 下载必须用 focus + Enter，不能用鼠标点击

这是本项目最关键的发现，改回鼠标点击会直接坏掉：

| 方式 | 结果 |
|---|---|
| `a.click()`（JS） | 无反应——弹窗被拦，且没有用户手势 |
| `Input.dispatchMouseEvent` 点坐标 | 无反应——同样被拦 |
| **`a.focus()` + `Input.dispatchKeyEvent` Enter** | ✅ 正常下载 |

原因：知网下载链接 `target="_blank"` 指向 `bar.cnki.net/bar/download/order?id=...`，该接口会校验 **Referer + 来源应用**。键盘激活保留完整上下文和用户手势，鼠标坐标点击与程序化点击都会丢失。

### 3.3 绝不能直接 navigate 到下载链接

`Page.navigate("https://bar.cnki.net/bar/download/order?id=...")` 会跳到
`bar.cnki.net/bar/ErrorMsg.html?ErrMsg=来源应用不存在`。

即使补 `Network.setExtraHTTPHeaders({"Referer": ...})` 也不行——它还校验会话侧的应用来源。**只能在页面内触发。**

### 3.4 格式：PDF 优先

列表页的 `a.downloadlink` 给的是平台默认格式（多数期刊是 CAJ）。
要 PDF 必须进详情页点 `#pdfDown`。两篇实测：同一文献 `#pdfDown` 得到 `PDF document, version 1.6`，`#cajDown` 得到 CAJ。

`download` 命令的顺序：
1. 详情页 `#pdfDown`（`--prefer pdf`，默认）
2. 详情页 `#cajDown`
3. 列表页 `a.downloadlink` 兜底

下载完成后用**文件头魔数**判定真实格式，不信扩展名（`sniff_format()`）。

### 3.5 下载完成检测用文件轮询，不用 CDP 事件

`Browser.downloadProgress` 事件在不同 Chromium 版本行为不一致，实测经常收不到。
改用：轮询下载目录 → 发现新文件 → 等 2s 文件大小不变 → 判定完成（`wait_new_file()`）。

下载目录通过 `Browser.setDownloadBehavior` 重定向到 `refs/_incoming`，下完立即改名归档。

## 4. 人工接管协议

自动下载失败时（无权限、验证码、仅 HTML 阅读），`download` 会：

1. 退出码 1
2. 生成 `refs/pending-download.md`：含 key、篇名、作者、来源、年份、知网直链
3. 失败原因逐条写在文件末尾

接管方式二选一：

**A. 用户手动下载**
用户按清单在浏览器里逐篇点下载，存到任意目录，然后：

```bash
python3 scripts/cnki.py ingest --from ~/Downloads
```

`ingest` 靠**篇名分词匹配**认领文件（知网下载的文件名形如 `篇名_第一作者.pdf`，匹配度通常 >90%）。匹配度低于阈值就报出来让你手工指定，**绝不猜测**。

**B. Computer Use 接管**
用浏览器控制能力（`mcp__browser__*` 或 `workbuddy-browser-use`）在用户浏览器里逐篇点「PDF下载」，下完同样跑 `ingest`。

## 5. 频率与风控

| 动作 | 建议间隔 | 说明 |
|---|---|---|
| 检索 | ≥3s | 过快会弹滑块 |
| 打开详情页抓摘要 | ≥1.2s | 40 篇约 1 分钟 |
| 下载 | ≥2.5s | 单批 ≤15 篇 |

触发滑块的表现：URL 跳到 `/verify/home?captchaType=blockPuzzle`。脚本会自动等 40s；不过就提示人工拖一次。

## 6. 校准方法（选择器失效时）

```bash
# 1. 抓结果行结构
python3 - <<'PY'
from cdp_min import Page
p = Page(url_contains="kns.cnki.net")
print(p.eval("document.querySelector('table.result-table-list tbody tr').outerHTML.slice(0,2000)"))
PY

# 2. 抓详情页按钮
python3 - <<'PY'
from cdp_min import Page
p = Page(url_contains="kcms2/article/abstract")
print(p.eval("[...document.querySelectorAll('a[id]')].map(a=>a.id+'|'+a.innerText.trim()).join('\\n')"))
PY
```

拿到新结构后，只改 `scripts/cnki.py` 里 `EXTRACT_ROWS_JS`、`DETAIL_JS` 和 `download_via_detail()` 中的选择器，其余逻辑不用动。

## 7. 字段缺失怎么处理

知网列表页给的信息有限，GB/T 7714 需要的**卷、期、页码**常缺：

- 网络首发（`marktip` 标注"网络首发"）通常没有卷期页 → 参考文献只写到年份，**不要编造卷期页**
- 详情页 `.top-tip` 有时含完整刊名行，已存进 `refs.json` 的 `source_line`，`refs_audit.py` 会尝试解析
- 解析不出来就留空，宁可不完整也不能假
