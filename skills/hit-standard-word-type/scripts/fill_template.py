#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""在学校原件（templates/ 下的 .docx）里原地填空，保住封面横线与表格版式。

用法：
    python3 fill_template.py inspect 模板.docx            # 列出可填的位置
    python3 fill_template.py inspect 模板.docx --all      # 连正文段落一起列
    python3 fill_template.py fill 模板.docx 产出.docx --map 值.json

值.json 的键就是 inspect 打印的槽位号：
    P9#1             第 9 段第 1 个下划线空位（封面字段，按原宽度补空格，横线长短不变）
    P8+              在第 8 段末尾追加（保住「题 目：」这类没有下划线的标签）
    P24              第 24 段整段替换（多行文本自动拆成同格式段落）
    after:P25@24     在第 25 段之后插入，格式克隆第 24 段（标题后接正文，别克隆标题格式）
    T0r1c1           表 0 第 1 行第 1 列（保留单元格内字体）

设计原则：只写文字，不新建段落样式、不改页面设置、不动表格结构。
"""

import argparse
import os
import copy
import json
import re
import sys

from docx import Document
from docx.shared import Emu

WIDTH_FULL = 2.0  # 全角/中文字符占 2 个半角单位
SLOT_MIN_UNITS = 4  # 少于 4 个半角宽的空格串不算空位


def _char_units(ch: str) -> float:
    if ch == "\u3000":
        return WIDTH_FULL
    if ord(ch) < 0x2E80:
        return 1.0
    return WIDTH_FULL


def text_units(s: str) -> float:
    return sum(_char_units(c) for c in s)


def _is_blank_run(run):
    return run.text and run.text.strip(" \t\u3000") == ""


def _label_before(paragraph, run_index: int) -> str:
    """取空位前面的标签文字：在最后一个冒号处切断，去掉空白。"""
    prefix = "".join(r.text for r in paragraph.runs[:run_index])
    prefix = prefix.replace(" ", "").replace("\u3000", "").replace("\t", "")
    if not prefix:
        return ""
    parts = re.split(r"[：:]", prefix)
    if len(parts) >= 2:
        # 「项目负责人：学号：」→ 取「学号」；「专业：」→ 取「专业」
        return (parts[-2] if parts[-1].strip() == "" else parts[-1]) or "(无标签)"
    return prefix


def iter_paragraphs(doc):
    """正文段落 + 表格单元格段落，带上可定位的 id。"""
    yield from ((f"P{i}", p) for i, p in enumerate(doc.paragraphs))


def slots(doc, show_all=False):
    """返回可填槽位列表：id、类型、标签、当前内容、宽度。"""
    out = []
    for i, p in enumerate(doc.paragraphs):
        for j, r in enumerate(p.runs):
            if not _is_blank_run(r) or len(r.text) < SLOT_MIN_UNITS:
                continue
            # 标签内的排版空格（「专    业」）不是空位：无下划线且很窄的一律跳过
            if not r.font.underline and text_units(r.text) < 8:
                continue
            out.append(
                {
                    "id": f"P{i}#{j}",
                    "kind": "下划线空位" if r.font.underline else "空白位",
                    "label": _label_before(p, j) or "(无标签)",
                    "current": r.text,
                    "units": round(text_units(r.text), 1),
                    "context": p.text.strip()[:40],
                }
            )
        if show_all and p.text.strip():
            out.append(
                {
                    "id": f"P{i}",
                    "kind": "整段",
                    "label": p.style.name,
                    "current": p.text.strip()[:40],
                    "units": "",
                    "context": "",
                }
            )

    for ti, table in enumerate(doc.tables):
        header = []
        if table.rows:
            header = [c.text.strip() for c in table.rows[0].cells]
        seen = set()
        for ri, row in enumerate(table.rows):
            for ci, cell in enumerate(row.cells):
                if id(cell._tc) in seen:
                    continue
                seen.add(id(cell._tc))
                text = cell.text.strip()
                label = ""
                if text.endswith(("：", ":")):
                    label = text.rstrip("：:").replace(" ", "")
                elif not text:
                    left = row.cells[ci - 1].text.strip() if ci > 0 else ""
                    if left.endswith(("：", ":")):
                        label = left.rstrip("：:").replace(" ", "")
                    elif ri == 1 and header and ci < len(header):
                        label = f"{header[ci]}（空行）" if header[ci] else ""
                if label:
                    out.append(
                        {
                            "id": f"T{ti}r{ri}c{ci}",
                            "kind": "表格单元格",
                            "label": label,
                            "current": text[:40],
                            "units": "",
                            "context": "",
                        }
                    )
    return out


def _set_paragraph_text(p, text, donor=None):
    """把 text 写进段落：保留首 run 的格式，多余 run 删除；\\n 保留在同一段落无效，交由调用方分段。"""
    runs = p.runs
    if runs:
        runs[0].text = text
        for r in runs[1:]:
            r._element.getparent().remove(r._element)
    else:
        run = p.add_run(text)
        if donor is not None and donor.rPr is not None:
            run._element.insert(0, copy.deepcopy(donor.rPr))


def _clone_paragraph_after(anchor_p, text, donor=None):
    src = donor if donor is not None else anchor_p
    new_el = copy.deepcopy(src._p)
    anchor_p._p.addnext(new_el)
    from docx.text.paragraph import Paragraph

    new_p = Paragraph(new_el, anchor_p._parent)
    _set_paragraph_text(new_p, text)
    return new_p


def _append_text(p, text):
    """段落末尾追加文字，沿用最后一个 run 的字体格式。"""
    runs = p.runs
    run = p.add_run(text)
    if runs and runs[-1]._element.rPr is not None:
        run._element.insert(0, copy.deepcopy(runs[-1]._element.rPr))


def _fill_slot(p, run_index, value):
    """按原宽度填下划线空位：文字 + 补空格，横线右端位置不变。"""
    run = p.runs[run_index]
    orig = text_units(run.text)
    vunits = text_units(value)
    pad = orig - vunits
    warning = None
    if pad < 0:
        warning = (
            f"「{value}」超出空位 {abs(pad):.1f} 个半角宽，下划线会变长；"
            "建议缩短文字或改用模板里更长的空位"
        )
        pad = 0
    run.text = value + " " * int(pad)
    return warning


def _fill_cell(cell, value, donor_run=None):
    paras = cell.paragraphs
    lines = value.split("\n")
    _set_paragraph_text(paras[0], lines[0], donor=donor_run)
    for extra in lines[1:]:
        new_el = copy.deepcopy(paras[0]._p)
        paras[0]._p.addnext(new_el)
        from docx.text.paragraph import Paragraph

        _set_paragraph_text(Paragraph(new_el, paras[0]._parent), extra)


def _donor_run_for_cell(table, ri, ci):
    row = table.rows[ri]
    for ci2, c in enumerate(row.cells):
        if ci2 == ci:
            continue
        for p in c.paragraphs:
            if p.runs:
                return p.runs[0]._element.rPr
    return None


def apply_map(doc, mapping):
    """三阶段写入：原地替换 → 多行整段（倒序）→ 段后插入（倒序）。

    段落插入会改变后续段落序号，所以带插入的操作必须按索引倒序执行。
    """
    warnings = []
    missing = []
    inplace, multiline, inserts = [], [], []
    for raw_key, value in mapping.items():
        value = "" if value is None else str(value)
        key = raw_key[:-1] if raw_key.endswith("!") else raw_key
        if key.startswith("after:P"):
            m = re.fullmatch(r"after:P(\d+)(?:@(\d+))?", key)
            if m:
                inserts.append((int(m.group(1)), raw_key, value, m.group(2)))
            else:
                missing.append(raw_key)
        elif re.fullmatch(r"P\d+", key) and "\n" in value:
            multiline.append((int(key[1:]), raw_key, value))
        else:
            inplace.append((raw_key, value))

    for key, value in inplace:
        force = key.endswith("!")
        if force:
            key = key[:-1]
        try:
            if key.startswith("P") and key.endswith("+") and key[1:-1].isdigit():
                # 段落末尾追加（「题 目：」这类没有下划线的标签）
                _append_text(doc.paragraphs[int(key[1:-1])], value)
            elif key.startswith("P") and "#" in key:
                pidx, ridx = key[1:].split("#")
                warn = _fill_slot(doc.paragraphs[int(pidx)], int(ridx), value)
                if warn:
                    warnings.append(f"{key}: {warn}")
            elif re.fullmatch(r"P\d+", key):
                p = doc.paragraphs[int(key[1:])]
                old = p.text.strip()
                if not force and ("：" in old or ":" in old) and "：" not in value and ":" not in value:
                    warnings.append(
                        f"{key} 整段替换会删掉标签「{old[:12]}」，改用 {key}+ 追加；确需覆盖请写 {key}!"
                    )
                    continue
                _set_paragraph_text(p, value)
            elif re.fullmatch(r"T\d+r\d+c\d+", key):
                t_idx, rest = key[1:].split("r", 1)
                r_idx, c_idx = rest.split("c", 1)
                table = doc.tables[int(t_idx)]
                cell = table.rows[int(r_idx)].cells[int(c_idx)]
                old = cell.text.strip()
                if not force and old.endswith(("：", ":")):
                    warnings.append(
                        f"{key} 是标签格「{old[:12]}」，值应填右侧一格 T{t_idx}r{r_idx}c{int(c_idx)+1}；确需覆盖请写 {key}!"
                    )
                    continue
                donor = _donor_run_for_cell(table, int(r_idx), int(c_idx))
                _fill_cell(cell, value, donor_run=donor)
            else:
                missing.append(key)
        except (IndexError, ValueError, KeyError) as exc:
            missing.append(f"{key} ({exc.__class__.__name__})")

    shifts = []  # (起始段落序号, 净增段落数)，供后面的插入操作换算新序号
    for idx, key, value in sorted(multiline, key=lambda x: -x[0]):
        try:
            p = doc.paragraphs[idx]
            lines = value.split("\n")
            _set_paragraph_text(p, lines[0])
            last = p
            for line in lines[1:]:
                last = _clone_paragraph_after(last, line)
            if len(lines) > 1:
                shifts.append((idx, len(lines) - 1))
        except (IndexError, ValueError) as exc:
            missing.append(f"{key} ({exc.__class__.__name__})")

    def resolve(i):
        return i + sum(delta for start, delta in shifts if start < i)

    for idx, key, value, donor_idx in sorted(inserts, key=lambda x: -x[0]):
        try:
            anchor = doc.paragraphs[resolve(idx)]
            donor = doc.paragraphs[resolve(int(donor_idx))] if donor_idx else anchor
            last = anchor
            for line in value.split("\n"):
                last = _clone_paragraph_after(last, line, donor=donor)
        except (IndexError, ValueError) as exc:
            missing.append(f"{key} ({exc.__class__.__name__})")
    return warnings, missing


def cmd_inspect(args):
    doc = Document(args.file)
    rows = slots(doc, show_all=args.all)
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    for s in rows:
        print(
            f"{s['id']:<12} {s['kind']:<8} {s['label'][:14]:<16} "
            f"{s['units']!s:>6} | {s['current'] or s['context']}"
        )
    print(f"\n共 {len(rows)} 处可填。填法见 references/template-fill.md", file=sys.stderr)
    return 0


def cmd_fill(args):
    with open(args.map, encoding="utf-8") as fh:
        mapping = json.load(fh)
    doc = Document(args.file)
    warnings, missing = apply_map(doc, mapping)
    if os.path.abspath(args.out) == os.path.abspath(args.file):
        tmp = args.out + ".tmp"
        doc.save(tmp)
        os.replace(tmp, args.out)
    else:
        doc.save(args.out)
    for w in warnings:
        print("警告：" + w, file=sys.stderr)
    if missing:
        print("以下键没找到对应位置：" + "、".join(missing), file=sys.stderr)
        return 1
    print(f"已写入 {len(mapping) - len(warnings)} 处 → {args.out}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="在学校原件里原地填空")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("inspect", help="列出可填槽位")
    p1.add_argument("file")
    p1.add_argument("--all", action="store_true", help="连正文段落一起列出")
    p1.add_argument("--json", action="store_true")
    p1.set_defaults(func=cmd_inspect)

    p2 = sub.add_parser("fill", help="按映射填值")
    p2.add_argument("file")
    p2.add_argument("out")
    p2.add_argument("--map", required=True)
    p2.set_defaults(func=cmd_fill)

    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
