#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
style_lint.py —— 去 AI 味机械检测。

不做"AI 检测"，只查可量化的写作特征。判据来自对比：AI 生成的报告段落长度均匀、
句式整齐、爱用连接词开场、爱在段末总结。人写的东西长短不一、有具体的数字和
第一人称观察、允许局部不对称。

用法：
    python3 style_lint.py 03-final.md
    python3 style_lint.py 03-final.md --strict   # 有 FAIL 就退出码 1

输出：PASS / WARN / FAIL 三档 + 具体命中的句子，便于逐条改。
"""

import argparse
import re
import statistics
import sys
from pathlib import Path

# 1. 高频 AI 腔开场与套话
BANNED = [
    "首先", "其次", "再次", "最后，", "综上所述", "总而言之", "总的来说",
    "值得注意的是", "不难发现", "显而易见", "众所周知",
    "随着社会的发展", "随着经济的发展", "随着科技的进步", "随着时代的发展",
    "在当今社会", "在当今时代", "近年来，随着",
    "不仅……而且", "既是……也是", "一方面……另一方面",
    "具有重要意义", "具有重要的理论意义和实践价值", "提供了有益的参考",
    "本文旨在", "本文试图", "本文将从以下几个方面",
    "总的来说，", "可以预见", "为此，我们需要",
]

# 2. 机械化的三段式枚举
ENUM_PATTERNS = [
    r"第一[，,、].{0,40}第二[，,、]",
    r"其一[，,].{0,40}其二[，,]",
    r"一方面.{0,60}另一方面",
]

DASH = "——"


def split_paras(text):
    body = re.sub(r"^#{1,6}\s.*$", "", text, flags=re.M)
    body = re.split(r"\n#{1,3}\s*参考文献", body)[0]
    paras = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    return [p for p in paras if len(p) > 25 and not p.startswith("|") and not p.startswith("[")]


def split_sents(text):
    parts = re.split(r"[。！？!?]\s*", text)
    return [s.strip() for s in parts if len(s.strip()) > 3]


def run(path, strict=False):
    text = Path(path).read_text(encoding="utf-8")
    paras = split_paras(text)
    if not paras:
        print("没有可分析的正文段落")
        return 0

    fails, warns = [], []

    # --- 禁用词 ---
    for w in BANNED:
        n = text.count(w)
        if n:
            (fails if n >= 2 else warns).append("套话「%s」出现 %d 次" % (w, n))

    # --- 三段式 ---
    for pat in ENUM_PATTERNS:
        m = re.search(pat, text, re.S)
        if m:
            fails.append("机械三段式：「%s」" % m.group(0)[:40].replace("\n", " "))

    # --- 段落长度均匀度 ---
    lens = [len(p) for p in paras]
    mean = statistics.mean(lens)
    if len(lens) >= 4:
        cv = statistics.pstdev(lens) / mean
        if cv < 0.35:
            fails.append("段落长度过于均匀（变异系数 %.2f）：AI 特征，需长短交错" % cv)
        elif cv < 0.5:
            warns.append("段落长度偏均匀（变异系数 %.2f）" % cv)

    # --- 句长分布 ---
    sents = []
    for p in paras:
        sents.extend(split_sents(p))
    if len(sents) >= 10:
        slens = [len(s) for s in sents]
        short = len([x for x in slens if x <= 15]) / len(slens)
        if short < 0.10:
            fails.append("短句占比仅 %.0f%%（应 ≥15%%）：全篇长句是典型 AI 节奏" % (short * 100))
        avg = statistics.mean(slens)
        if avg > 45:
            fails.append("平均句长 %.0f 字，偏长" % avg)

    # --- 段末总结句 ---
    tail_hits = 0
    for p in paras:
        tail = p[-30:]
        if re.search(r"(因此|所以|综上|可见|这表明|这说明|由此可见)", tail):
            tail_hits += 1
    if len(paras) >= 4 and tail_hits / len(paras) > 0.6:
        fails.append("%d/%d 段落以总结句收尾：模板感强" % (tail_hits, len(paras)))

    # --- 破折号密度 ---
    if text.count(DASH) > max(3, len(paras) // 3):
        warns.append("破折号 %d 处，偏多" % text.count(DASH))

    # --- 具体性检查（正面指标） ---
    has_num = len(re.findall(r"\d+(\.\d+)?\s*(%|％|℃|mA|mAh|V|W|s|min|h|kg|mm|次|篇)", text))
    has_first = len(re.findall(r"我(们)?(在|观察|注意|发现|实测|测得|尝试)", text))
    if has_num < 5:
        warns.append("具体数据点只有 %d 处（建议 ≥8）：加大实测/引用数字，能显著降低模板感" % has_num)
    if has_first == 0:
        warns.append("没有第一人称的观察/操作痕迹（实验类报告建议有）")

    total = len(paras)
    print("正文段落 %d 段，句子 %d 句，平均句长 %.0f 字" % (
        total, len(sents), statistics.mean([len(s) for s in sents]) if sents else 0))
    for w in warns:
        print("  WARN " + w)
    for f in fails:
        print("  FAIL " + f)

    if fails:
        print("\n判定：FAIL（%d 项必须改）" % len(fails))
        return 1 if strict else 0
    if warns:
        print("\n判定：PASS（有 %d 条建议）" % len(warns))
        return 0
    print("\n判定：PASS")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    sys.exit(run(a.file, a.strict))
