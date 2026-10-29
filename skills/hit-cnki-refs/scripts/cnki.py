#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cnki.py —— 中国知网（CNKI）文献检索 / 泛读 / 筛选 / 下载 / 归档 / 校验。

设计原则（针对"防 AI 编造文献"）：
1. 题录只能来自知网页面 DOM，不允许模型手写；
2. 单一事实源 refs/refs.json，所有状态流转都记在里面；
3. 下载失败不静默 —— 产出 pending-download.md，交人工或 Computer Use 接管；
4. ingest 只做"认领"，认领不上就报出来，绝不猜测。

典型流程：
    cnki.py check                                   # 环境与机构识别自检
    cnki.py search "锂离子电池 热失控" --limit 30     # 检索，写入候选池
    cnki.py abstract --limit 30                     # 逐篇读摘要（泛读层）
    cnki.py shortlist                               # 生成 02-shortlist.md 供人决策
    cnki.py confirm --keys k1,k2,k3                 # 用户确认后锁定
    cnki.py download                                # 尝试自动下载，失败则待办
    cnki.py ingest --from ~/Downloads               # 归档手工下载的文件
    cnki.py verify                                  # 校验文件与题录一致性

退出码：0 成功；1 失败；2 环境不可用（CDP/校园网/验证码）。
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cdp_min import Browser, CDPError, Page, list_targets  # noqa: E402

KNS_HOME = "https://kns.cnki.net/kns8s/defaultresult/index"
MIN_BYTES = 50 * 1024  # 小于此值基本是错误页/空文件
ORG_DEFAULT = "哈尔滨工业大学"


# ------------------------------------------------------------------ 工具
def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(msg):
    print(msg, flush=True)


def die(msg, code=1):
    print("错误：" + msg, file=sys.stderr, flush=True)
    sys.exit(code)


def slug(text, n=18):
    """把中文标题压成短 key：保留中文与字母数字。"""
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "", text)
    return s[:n] or "ref"


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def next_seq(refs_dir):
    """扫描已有文件的最大三位序号，返回下一个。避免删文件后重号。"""
    mx = 0
    for p in Path(refs_dir).glob("[0-9][0-9][0-9]-*"):
        try:
            mx = max(mx, int(p.name[:3]))
        except ValueError:
            pass
    return mx + 1


def snapshot(d):
    """目录内文件的快照，用于识别"新增了哪个文件"。"""
    try:
        return {p.name for p in Path(d).iterdir() if p.is_file()}
    except FileNotFoundError:
        return set()


def wait_new_file(d, before, timeout=45.0, quiet=2.0):
    """
    等目录里出现一个新文件且大小稳定。
    比 CDP 的 downloadProgress 事件更可靠：Chrome 各版本发事件的行为不一致。
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        fresh = [p for p in Path(d).iterdir()
                 if p.is_file() and p.name not in before and not p.name.endswith(".crdownload")]
        if fresh:
            p = max(fresh, key=lambda x: x.stat().st_mtime)
            try:
                s1 = p.stat().st_size
            except FileNotFoundError:
                return None
            time.sleep(quiet)
            try:
                s2 = p.stat().st_size
            except FileNotFoundError:
                return None
            if s1 == s2 and s2 > 0:
                return p
        time.sleep(0.8)
    return None


def load_db(refs_dir):
    p = Path(refs_dir) / "refs.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"project": Path(refs_dir).resolve().parent.name, "updated": now(), "entries": [], "searches": []}


def save_db(refs_dir, db):
    p = Path(refs_dir) / "refs.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    db["updated"] = now()
    p.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


def find_entry(db, key=None, title=None):
    for e in db["entries"]:
        if key and e["key"] == key:
            return e
        if title and e["title"] == title:
            return e
    return None


# ------------------------------------------------------------------ 浏览器连接
def connect(url_contains="kns.cnki.net"):
    try:
        return Page(url_contains=url_contains)
    except CDPError:
        return None


def ensure_kns_page():
    """拿到（或新建）一个可检索的知网页面，并确保已过验证。"""
    b = Browser()
    page = connect("kns.cnki.net")
    if page is None or not page.eval("!!document.querySelector('#txt_search')"):
        # 当前标签是详情页/错误页，需要回到检索首页
        if page is not None:
            page.navigate(KNS_HOME, timeout=40)
        else:
            tid = b.call("Target.createTarget", {"url": KNS_HOME})["targetId"]
            page = Page(target_id=tid)
        page.wait_js("document.readyState=='complete'", timeout=30)
    if "verify" in (page.url() or ""):
        log("遇到安全验证，等待自动放行（最长 40s）；若需人工拖动拼图请在浏览器里完成…")
        ok = page.wait_js("location.href.indexOf('verify')<0", timeout=40)
        if not ok:
            b.close()
            die("验证未通过。请在弹出的浏览器窗口里手动完成拼图后重跑本命令。", code=2)
    b.close()
    return page


# ------------------------------------------------------------------ check
def cmd_check(args):
    info = {"cdp": False, "browser": None, "org": None, "verified": None, "search_ready": None}
    try:
        b = Browser()
        info["cdp"] = True
        info["browser"] = b.call("Browser.getVersion").get("product")
        b.close()
    except CDPError as exc:
        info["error"] = str(exc)
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return 2

    page = ensure_kns_page()
    txt = page.eval("document.body ? document.body.innerText : ''") or ""
    info["org"] = args.org if args.org in txt else None
    info["verified"] = "verify" not in (page.url() or "")
    info["search_ready"] = bool(page.eval("!!document.querySelector('#txt_search')"))
    info["url"] = page.url()
    page.close()
    print(json.dumps(info, ensure_ascii=False, indent=2))
    if not info["org"]:
        log("⚠ 页面未见机构名 %r —— 校园网可能未生效，下载会失败。" % args.org)
    return 0 if (info["org"] and info["search_ready"]) else 2


# ------------------------------------------------------------------ search
EXTRACT_ROWS_JS = r"""
(()=>{
  const rows=[...document.querySelectorAll('table.result-table-list tbody tr')];
  return JSON.stringify(rows.map((r,i)=>{
    const n=r.querySelector('td.name a');
    const cb=r.querySelector('td.seq input.cbItem');
    const q=s=>{const e=r.querySelector(s);return e?e.innerText.replace(/\s+/g,' ').trim():''};
    return {
      rank:i+1,
      title:n?n.innerText.replace(/\s+/g,' ').trim():'',
      url:n?n.href:null,
      authors:[...r.querySelectorAll('td.author a')].map(a=>a.innerText.trim()).join(';'),
      source:q('td.source'),
      date:q('td.date'),
      db:q('td.data'),
      downloads:q('td.download'),
      order_url:(r.querySelector('a.downloadlink')||{}).href||null,
      doc_id:cb?cb.value:null
    };
  }).filter(x=>x.title));
})()
"""


def do_search(page, kw, limit=20):
    page.navigate(KNS_HOME, timeout=40)
    page.wait_js("!!document.querySelector('#txt_search')", timeout=30)
    page.eval("(()=>{const i=document.querySelector('#txt_search');i.value='';i.focus();return 1})()")
    for ch in kw:
        page.conn.call("Input.dispatchKeyEvent", {"type": "char", "text": ch})
    page.eval("document.querySelector('.search-btn').click()")
    if not page.wait_js("document.querySelectorAll('table.result-table-list tbody tr').length>0", timeout=35):
        return []
    rows = json.loads(page.eval(EXTRACT_ROWS_JS))
    return rows[:limit]


def cmd_search(args):
    page = ensure_kns_page()
    db = load_db(args.refs)
    total_new = 0
    for kw in args.keywords:
        log("检索：%s" % kw)
        rows = do_search(page, kw, args.limit)
        log("  命中 %d 条" % len(rows))
        for r in rows:
            if find_entry(db, title=r["title"]):
                continue
            key = slug(r["title"]) + str(len(db["entries"]) + 1)
            db["entries"].append(
                {
                    "key": key,
                    "cite_no": None,
                    "title": r["title"],
                    "authors": [a for a in r["authors"].split(";") if a],
                    "source": r["source"],
                    "date": r["date"],
                    "db": r["db"],
                    "downloads": r["downloads"],
                    "keywords": None,
                    "abstract": None,
                    "url": r["url"],
                    "order_url": r["order_url"],
                    "doc_id": r["doc_id"],
                    "search": {"kw": kw, "rank": r["rank"], "at": now()},
                    "status": "candidate",
                    "section": None,
                    "file": None,
                    "format": None,
                    "bytes": None,
                    "md5": None,
                    "verify": None,
                    "note": None,
                }
            )
            total_new += 1
        db["searches"].append({"kw": kw, "at": now(), "count": len(rows)})
        time.sleep(args.delay)
    p = save_db(args.refs, db)
    page.close()
    log("新增 %d 条，候选池共 %d 条 → %s" % (total_new, len(db["entries"]), p))


# ------------------------------------------------------------------ abstract
DETAIL_JS = r"""
(()=>{
  const t=s=>{const e=document.querySelector(s);return e?e.innerText.replace(/\s+/g,' ').trim():null};
  return JSON.stringify({
    title:t('.wx-tit h1'),
    authors:t('.author'),
    abstract:t('#ChDivSummary')||t('.abstract-text'),
    keywords:t('.keywords'),
    tip:t('.top-tip')
  });
})()
"""


def cmd_abstract(args):
    page = ensure_kns_page()
    db = load_db(args.refs)
    todo = [e for e in db["entries"] if not e.get("abstract") and e.get("url")]
    if args.only:
        todo = [e for e in todo if e["status"] in args.only.split(",")]
    todo = todo[: args.limit]
    log("待补摘要 %d 篇" % len(todo))
    b = Browser()
    hit = 0
    for i, e in enumerate(todo, 1):
        try:
            tid = b.call("Target.createTarget", {"url": e["url"]})["targetId"]
            d = Page(target_id=tid)
            d.wait_js("!!(document.querySelector('#ChDivSummary')||document.querySelector('.abstract-text'))", timeout=25)
            info = json.loads(d.eval(DETAIL_JS))
            if info.get("abstract"):
                e["abstract"] = info["abstract"]
                e["keywords"] = info.get("keywords")
                e["source_line"] = info.get("tip")
                if info.get("title"):
                    e["title_cnki"] = info["title"]
                hit += 1
            b.call("Target.closeTarget", {"targetId": tid})
            log("  [%d/%d] %s" % (i, len(todo), e["title"][:40]))
        except (CDPError, json.JSONDecodeError) as exc:
            log("  [%d/%d] 失败：%s" % (i, len(todo), exc))
        time.sleep(args.delay)
        if i % 10 == 0:
            save_db(args.refs, db)
    b.close()
    save_db(args.refs, db)
    log("补全 %d 篇摘要" % hit)


# ------------------------------------------------------------------ shortlist
def cmd_shortlist(args):
    db = load_db(args.refs)
    cands = [e for e in db["entries"] if e.get("abstract")]
    if not cands:
        die("候选池里没有摘要，先跑 `cnki.py abstract`")

    def score(e):
        s = 0.0
        d = e.get("downloads") or "0"
        m = re.search(r"\d+", d)
        if m:
            s += min(int(m.group()) / 500.0, 3.0)
        if "学位论文" in (e.get("db") or ""):
            s += 1.2
        if "综述" in e["title"] or "进展" in e["title"] or "现状" in e["title"]:
            s += 1.5
        y = re.search(r"(20\d\d)", e.get("date") or "")
        if y:
            s += max(0, (int(y.group(1)) - 2015) * 0.15)
        if e.get("keywords"):
            s += 0.3
        return s

    cands.sort(key=score, reverse=True)
    top = cands[: args.n]
    tiers = [("A 档·强烈建议引用", top[: max(1, args.n // 3)]),
             ("B 档·可作支撑", top[max(1, args.n // 3): max(2, 2 * args.n // 3)]),
             ("C 档·背景/备选", top[max(2, 2 * args.n // 3):])]

    lines = ["# 参考文献候选清单", "", "> 由 `cnki.py shortlist` 生成，%s。**需人工确认后才会下载。**" % now(), ""]
    lines.append("共检索 %d 条，有摘要 %d 条，此处列前 %d 条。" % (len(db["entries"]), len(cands), len(top)))
    lines.append("")
    for name, group in tiers:
        if not group:
            continue
        lines.append("## " + name)
        lines.append("")
        lines.append("| 选择 | key | 篇名 | 作者 | 来源 | 时间 | 下载 | 拟支撑章节 |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for e in group:
            lines.append("| [ ] | `%s` | %s | %s | %s | %s | %s | |" % (
                e["key"], e["title"][:40], "、".join(e["authors"][:2]),
                (e["source"] or "")[:16], (e["date"] or "")[:10], e.get("downloads") or "-"))
        lines.append("")
        for e in group:
            ab = (e.get("abstract") or "").strip()
            lines.append("- **%s** — %s" % (e["title"][:36], ab[:110] + ("…" if len(ab) > 110 else "")))
        lines.append("")

    out = Path(args.refs) / "02-shortlist.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    log("已生成 %s（%d 条候选，分 %d 档）" % (out, len(top), len([g for _, g in tiers if g])))
    log("下一步：把要引用的 key 交给用户确认，然后 `cnki.py confirm --keys a,b,c`")


# ------------------------------------------------------------------ confirm
def cmd_confirm(args):
    db = load_db(args.refs)
    keys = [k.strip() for k in args.keys.split(",") if k.strip()]
    ok, miss = 0, []
    for k in keys:
        e = find_entry(db, key=k)
        if not e:
            miss.append(k)
            continue
        e["status"] = "confirmed"
        if args.section:
            e["section"] = args.section
        ok += 1
    save_db(args.refs, db)
    log("已确认 %d 条待下载" % ok)
    if miss:
        log("⚠ 找不到这些 key：%s" % ", ".join(miss))


# ------------------------------------------------------------------ download
def sniff_format(path):
    """按文件头判断真实格式，不轻信扩展名。"""
    try:
        head = Path(path).open("rb").read(8)
    except OSError:
        return "unknown"
    if head.startswith(b"%PDF"):
        return "pdf"
    if head[:3] in (b"CAJ", b"KDH") or head[:2] == b"\xc8\xdf":
        return "caj"
    if head.startswith(b"NH"):
        return "nh"
    return "unknown"


def press_enter(page):
    for kt in ("keyDown", "keyUp"):
        page.conn.call("Input.dispatchKeyEvent", {
            "type": kt, "key": "Enter", "code": "Enter",
            "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13,
        })


def download_via_detail(b, entry, dl_dir, prefer, timeout):
    """在详情页点 PDF/CAJ 下载按钮。PDF 优先。"""
    before = snapshot(dl_dir)
    tid = b.call("Target.createTarget", {"url": entry["url"]})["targetId"]
    page = Page(target_id=tid)
    try:
        page.wait_js("!!(document.querySelector('#pdfDown')||document.querySelector('#cajDown'))",
                     timeout=30)
        order = ["#pdfDown", "#cajDown"] if prefer == "pdf" else ["#cajDown", "#pdfDown"]
        for sel in order:
            ok = page.eval("(()=>{const a=document.querySelector('%s');"
                           "if(!a||!a.offsetParent) return false;"
                           "a.scrollIntoView({block:'center'});a.focus();"
                           "return document.activeElement===a;})()" % sel)
            if not ok:
                continue
            press_enter(page)
            got = wait_new_file(dl_dir, before, timeout=timeout)
            if got:
                return got
    finally:
        try:
            b.call("Target.closeTarget", {"targetId": tid})
        except CDPError:
            pass
    return None


def download_via_list(b, page, entry, dl_dir, timeout):
    """兜底：在检索结果列表里对该行按 Enter（老路径，只能拿到平台默认格式）。"""
    before = snapshot(dl_dir)
    rows = do_search(page, entry["title"][:60], limit=10)
    idx = next((r for r in rows if r["title"].strip() == entry["title"].strip()), None)
    if not idx:
        return None, "重检索未找到完全匹配的记录"
    focused = page.eval(r"""(()=>{
      const rs=[...document.querySelectorAll('table.result-table-list tbody tr')];
      const r=rs[%d]; if(!r) return false;
      const a=r.querySelector('a.downloadlink'); if(!a) return false;
      a.scrollIntoView({block:'center'}); a.focus();
      return document.activeElement===a;
    })()""" % (idx["rank"] - 1))
    if not focused:
        return None, "行内无可用下载按钮（无权限或仅支持 HTML 阅读）"
    press_enter(page)
    got = wait_new_file(dl_dir, before, timeout=timeout)
    return got, None if got else "列表页下载超时"


def cmd_download(args):
    page = ensure_kns_page()
    db = load_db(args.refs)
    todo = [e for e in db["entries"] if e["status"] == "confirmed" and not e.get("file")]
    if not todo:
        log("没有待下载条目（状态需为 confirmed）")
        return 0
    log("待下载 %d 条，格式优先：%s" % (len(todo), args.prefer.upper()))

    b = Browser()
    dl_dir = b.set_download_dir(Path(args.refs) / "_incoming")
    ok, bad = [], []

    for i, e in enumerate(todo[: args.limit], 1):
        log("  [%d/%d] %s" % (i, min(len(todo), args.limit), e["title"][:40]))
        got, why = None, None
        try:
            got = download_via_detail(b, e, dl_dir, args.prefer, args.timeout)
            if got is None:
                got, why = download_via_list(b, page, e, dl_dir, args.timeout)
        except CDPError as exc:
            why = "CDP 异常：%s" % exc

        if got:
            fmt = sniff_format(got)
            dest = Path(args.refs) / ("%03d-%s.%s" % (next_seq(args.refs), e["key"],
                                                      fmt if fmt != "unknown" else got.suffix.lstrip(".")))
            got.replace(dest)
            size = dest.stat().st_size
            e.update({"file": dest.name, "bytes": size, "md5": md5_of(dest),
                      "format": fmt,
                      "verify": "presence_only" if fmt == "caj" else "pending"})
            if size < MIN_BYTES:
                e["verify"] = "too_small"
                bad.append((e, "文件过小（%d B），疑似失败页" % size))
            else:
                e["status"] = "downloaded"
                ok.append(e)
            log("      ✓ %s  %s  %d KB" % (dest.name, fmt.upper(), size // 1024))
        else:
            bad.append((e, why or "未取到文件"))
            log("      ✗ %s" % (why or "未取到文件"))
        time.sleep(args.delay)
        save_db(args.refs, db)

    b.close()
    page.close()
    save_db(args.refs, db)

    # 清掉空的中转目录
    try:
        if not any(dl_dir.iterdir()):
            dl_dir.rmdir()
    except OSError:
        pass

    pdf_n = len([x for x in ok if x["format"] == "pdf"])
    caj_n = len([x for x in ok if x["format"] == "caj"])
    log("\n成功 %d 条（PDF %d / CAJ %d），失败 %d 条" % (len(ok), pdf_n, caj_n, len(bad)))
    if caj_n:
        log("  ⚠ 有 %d 篇只有 CAJ：已入库，按 presence_only 校验（内容核对靠摘要快照）" % caj_n)
    if bad:
        lines = ["# 待人工下载清单", "",
                 "> 自动下载失败。请按此表在知网逐条下载，存到任意目录后运行：",
                 "> `python3 cnki.py ingest --from <目录>`", "",
                 "| key | 篇名 | 作者 | 来源 | 年份 | 知网链接 |",
                 "|---|---|---|---|---|---|"]
        for e, why in bad:
            lines.append("| `%s` | %s | %s | %s | %s | [打开](%s) |" % (
                e["key"], e["title"][:40], "、".join(e["authors"][:2]),
                (e["source"] or "")[:16], (e["date"] or "")[:10], e["url"]))
        lines.append("")
        lines.append("失败原因汇总：")
        for e, why in bad:
            lines.append("- `%s`：%s" % (e["key"], why))
        p = Path(args.refs) / "pending-download.md"
        p.write_text("\n".join(lines), encoding="utf-8")
        log("已生成 %s" % p)
        return 1
    return 0


# ------------------------------------------------------------------ ingest
def title_tokens(t):
    return set(re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-z]{3,}", t))


def cmd_ingest(args):
    db = load_db(args.refs)
    src_dir = Path(args.src).expanduser()
    if not src_dir.exists():
        die("目录不存在：%s" % src_dir)
    waiting = [e for e in db["entries"] if e["status"] == "confirmed" and not e.get("file")]
    if not waiting:
        log("没有待归档条目")
        return 0

    files = [p for p in src_dir.iterdir()
             if p.is_file() and p.suffix.lower() in (".pdf", ".caj", ".nh", ".kdh")]
    files = sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)[: args.scan]
    log("扫描 %d 个候选文件，待归档 %d 条" % (len(files), len(waiting)))

    used, assigned = set(), 0
    for e in waiting:
        et = title_tokens(e["title"])
        best, best_score = None, 0.0
        for f in files:
            if f in used:
                continue
            ft = title_tokens(f.stem)
            if not et:
                continue
            score = len(et & ft) / float(len(et))
            if score > best_score:
                best, best_score = f, score
        if best and best_score >= args.threshold:
            dest = Path(args.refs) / ("%03d-%s%s" % (next_seq(args.refs), e["key"], best.suffix.lower()))
            best.replace(dest)
            used.add(best)
            e.update({"file": dest.name, "bytes": dest.stat().st_size, "md5": md5_of(dest),
                      "format": dest.suffix.lstrip("."),
                      "verify": "presence_only" if dest.suffix.lower() == ".caj" else "pending",
                      "note": "ingest 匹配度 %.0f%%" % (best_score * 100)})
            e["status"] = "downloaded"
            assigned += 1
            log("  ✓ %s ← %s (%.0f%%)" % (dest.name, best.name, best_score * 100))
        else:
            log("  ✗ %s —— 未找到匹配文件（最佳 %.0f%%）" % (e["key"], best_score * 100))

    save_db(args.refs, db)
    log("归档 %d / %d 条" % (assigned, len(waiting)))
    if assigned < len(waiting):
        log("仍有 %d 条未归档，请核对 pending-download.md 后手工放入。" % (len(waiting) - assigned))
        return 1
    return 0


# ------------------------------------------------------------------ verify
def cmd_verify(args):
    db = load_db(args.refs)
    refs = Path(args.refs)
    problems, checked = [], 0
    for e in db["entries"]:
        if e["status"] not in ("downloaded", "cited", "verified"):
            continue
        checked += 1
        if not e.get("file"):
            problems.append(("缺文件", e))
            continue
        f = refs / e["file"]
        if not f.exists():
            problems.append(("文件不存在", e))
            continue
        size = f.stat().st_size
        if size < MIN_BYTES:
            problems.append(("文件过小(%dB)" % size, e))
            continue
        if e.get("md5") and md5_of(f) != e["md5"]:
            problems.append(("md5 不符（文件被改动）", e))
            continue
        if not e.get("abstract"):
            problems.append(("无摘要快照", e))
        e["verify"] = "verified" if e.get("abstract") else "presence_only"

    save_db(args.refs, db)
    log("校验 %d 条已下载条目" % checked)
    if problems:
        for why, e in problems:
            log("  ✗ %s —— %s" % (e["key"], why))
        log("共 %d 个问题" % len(problems))
        return 1
    log("全部通过：文件存在、大小正常、md5 一致、摘要快照齐备")
    return 0


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(description="知网文献检索/泛读/下载/归档")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("check", help="环境与机构识别自检")
    p.add_argument("--org", default=ORG_DEFAULT)
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("search", help="检索并写入候选池")
    p.add_argument("keywords", nargs="+")
    p.add_argument("--refs", default="refs")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--delay", type=float, default=3.0)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("abstract", help="逐篇抓摘要（泛读层）")
    p.add_argument("--refs", default="refs")
    p.add_argument("--limit", type=int, default=40)
    p.add_argument("--only", default=None, help="只处理这些状态，逗号分隔")
    p.add_argument("--delay", type=float, default=1.2)
    p.set_defaults(func=cmd_abstract)

    p = sub.add_parser("shortlist", help="生成候选清单供人确认")
    p.add_argument("--refs", default="refs")
    p.add_argument("--n", type=int, default=30)
    p.set_defaults(func=cmd_shortlist)

    p = sub.add_parser("confirm", help="确认要引用的文献")
    p.add_argument("--refs", default="refs")
    p.add_argument("--keys", required=True)
    p.add_argument("--section", default=None)
    p.set_defaults(func=cmd_confirm)

    p = sub.add_parser("download", help="尝试自动下载已确认条目")
    p.add_argument("--refs", default="refs")
    p.add_argument("--limit", type=int, default=15)
    p.add_argument("--delay", type=float, default=2.5)
    p.add_argument("--timeout", type=int, default=35)
    p.add_argument("--prefer", choices=["pdf", "caj"], default="pdf",
                   help="优先格式，默认 pdf")
    p.set_defaults(func=cmd_download)

    p = sub.add_parser("ingest", help="归档手工下载的文件")
    p.add_argument("--refs", default="refs")
    p.add_argument("--from", dest="src", default="~/Downloads")
    p.add_argument("--scan", type=int, default=200)
    p.add_argument("--threshold", type=float, default=0.5)
    p.set_defaults(func=cmd_ingest)

    p = sub.add_parser("verify", help="校验已下载文件")
    p.add_argument("--refs", default="refs")
    p.set_defaults(func=cmd_verify)

    args = ap.parse_args()
    sys.exit(args.func(args) or 0)


if __name__ == "__main__":
    main()
