#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
refs_audit.py —— 引用与文献文件的三向对账（交付前硬闸门）。

三个方向都必须对齐，任一不过就退出码非 0，不允许交付：
  正文 `[@key]` 引用  ←→  refs/refs.json 条目  ←→  refs/ 下的真实文件

为什么这样设计：
模型最容易在参考文献上编造。本脚本让模型**没有机会**写参考文献列表——
它只能在正文里写 `[@key]`，编号和条目全部由脚本从 refs.json 渲染。

用法：
    python3 refs_audit.py check  --draft 03-final.md --refs refs
    python3 refs_audit.py render --draft 03-final.md --refs refs --out 04-交付稿.md
    python3 refs_audit.py bib    --refs refs          # 只打印参考文献列表

`render` 做的事：按首次出现顺序重排编号、把 [@key] 换成 [n]、追加参考文献。
"""

import argparse
import json
import re
import sys
from pathlib import Path

CITE_RE = re.compile(r"\[@([A-Za-z0-9_\-\u4e00-\u9fff]+)\]")
MIN_BYTES = 50 * 1024

GB_TYPE = {
    "期刊": "J", "博士": "D", "硕士": "D", "学位论文": "D",
    "会议": "C", "报纸": "N", "图书": "M", "专利": "P", "标准": "S",
}


def load(refs):
    p = Path(refs) / "refs.json"
    if not p.exists():
        sys.exit("找不到 %s —— 先跑 cnki.py search / confirm / download" % p)
    return json.loads(p.read_text(encoding="utf-8"))


def gb_type(entry):
    db = entry.get("db") or ""
    for k, v in GB_TYPE.items():
        if k in db:
            return v
    return "J"


def authors_gb(entry):
    names = entry.get("authors") or []
    if not names:
        return "[佚名]"
    if len(names) > 3:
        return ", ".join(names[:3]) + ", 等"
    return ", ".join(names)


def format_bib(entry, no):
    """GB/T 7714-2015 顺序编码制。缺失字段只用已有信息，绝不编造。"""
    t = gb_type(entry)
    title = (entry.get("title") or "").rstrip("。.")
    src = entry.get("source") or ""
    line = entry.get("source_line") or ""
    year = (entry.get("date") or "")[:4]

    # 从详情页的刊名行里捞 年, 卷(期): 页
    tail = ""
    m = re.search(r"(20\d\d)[,，]\s*(\d+)\s*\((\d+)\)\s*[:：]\s*([\d\-–]+)", line)
    if m:
        tail = ", %s, %s(%s): %s" % (m.group(1), m.group(2), m.group(3), m.group(4))
    elif year:
        tail = ", " + year

    if t == "D":
        return "[%d] %s. %s[D]. %s%s." % (no, authors_gb(entry), title, src or "学位授予单位", tail)
    if t == "C":
        return "[%d] %s. %s[C]//%s%s." % (no, authors_gb(entry), title, src, tail)
    return "[%d] %s. %s[%s]. %s%s." % (no, authors_gb(entry), title, t, src, tail)


def cmd_check(args):
    db = load(args.refs)
    refs_dir = Path(args.refs)
    draft = Path(args.draft).read_text(encoding="utf-8")
    cited = []
    for m in CITE_RE.finditer(draft):
        if m.group(1) not in cited:
            cited.append(m.group(1))

    by_key = {e["key"]: e for e in db["entries"]}
    problems, warns = [], []

    if not cited:
        problems.append("正文里没有任何 [@key] 引用标记 —— 等于没有文献支撑")

    for k in cited:
        e = by_key.get(k)
        if not e:
            problems.append("引用了不存在的 key：%s（候选池里没有这条）" % k)
            continue
        if not e.get("file"):
            problems.append("%s 未下载（status=%s）" % (k, e.get("status")))
            continue
        f = refs_dir / e["file"]
        if not f.exists():
            problems.append("%s 文件不存在：%s" % (k, e["file"]))
        elif f.stat().st_size < MIN_BYTES:
            problems.append("%s 文件过小（%d B）" % (k, f.stat().st_size))
        if not e.get("abstract"):
            warns.append("%s 缺摘要快照，老师质疑时无旁证" % k)
        if not e.get("source"):
            warns.append("%s 缺刊名" % k)

    cited_set = set(cited)
    unused = [e["key"] for e in db["entries"]
              if e.get("status") in ("downloaded", "verified") and e["key"] not in cited_set]
    for k in unused:
        warns.append("下载了但正文未引用：%s（要么引用，要么删文件，别留着占位）" % k)

    print("正文引用 %d 条，候选池 %d 条，已下载 %d 条" % (
        len(cited), len(db["entries"]),
        len([e for e in db["entries"] if e.get("file")])))
    for w in warns:
        print("  ⚠ " + w)
    if problems:
        print("\n阻断交付：")
        for p in problems:
            print("  ✗ " + p)
        return 1
    print("\n✓ 三向对账通过：每条引用都有真实文件")
    return 0


def cmd_render(args):
    db = load(args.refs)
    by_key = {e["key"]: e for e in db["entries"]}
    draft = Path(args.draft).read_text(encoding="utf-8")

    order = []
    for m in CITE_RE.finditer(draft):
        k = m.group(1)
        if k not in order:
            order.append(k)

    missing = [k for k in order if k not in by_key or not by_key[k].get("file")]
    if missing:
        print("阻断：这些 key 没有对应的已下载文献，不能渲染：", file=sys.stderr)
        for k in missing:
            print("  ✗ " + k, file=sys.stderr)
        return 1

    num = {k: i + 1 for i, k in enumerate(order)}

    def repl(m):
        k = m.group(1)
        return "[%d]" % num[k]

    body = CITE_RE.sub(repl, draft)

    # 去掉草稿里可能存在的旧参考文献段
    body = re.split(r"\n#{1,3}\s*参考文献\s*\n", body)[0].rstrip()

    bib = ["", "## 参考文献", ""]
    for k in order:
        e = by_key[k]
        e["cite_no"] = num[k]
        bib.append(format_bib(e, num[k]))
    out = body + "\n" + "\n".join(bib) + "\n"

    Path(args.out).write_text(out, encoding="utf-8")
    Path(args.refs, "refs.json").write_text(
        json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
    print("已渲染 %s：%d 条引用，编号按首次出现顺序" % (args.out, len(order)))
    return 0


def cmd_bib(args):
    db = load(args.refs)
    ents = [e for e in db["entries"] if e.get("cite_no")]
    ents.sort(key=lambda e: e["cite_no"])
    if not ents:
        print("还没有编号，先跑 render", file=sys.stderr)
        return 1
    for e in ents:
        print(format_bib(e, e["cite_no"]))
    return 0


def main():
    ap = argparse.ArgumentParser(description="引用三向对账")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("check")
    p.add_argument("--draft", required=True)
    p.add_argument("--refs", default="refs")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("render")
    p.add_argument("--draft", required=True)
    p.add_argument("--refs", default="refs")
    p.add_argument("--out", required=True)
    p.set_defaults(func=cmd_render)

    p = sub.add_parser("bib")
    p.add_argument("--refs", default="refs")
    p.set_defaults(func=cmd_bib)

    args = ap.parse_args()
    sys.exit(args.func(args) or 0)


if __name__ == "__main__":
    main()
