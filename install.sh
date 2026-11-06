#!/usr/bin/env bash
# 把仓库里的三个 HIT skill 完整装进 WorkBuddy 用户级 skill 目录。
#
#   bash install.sh                 # 装到 ~/.workbuddy/skills
#   bash install.sh --fonts         # 顺带装内置替代字体（宋体/黑体/Times 缺失时）
#   DEST=~/.workbuddy/skills bash install.sh
#
# 做的事：同步 skill 文件 → 补执行位 → 建模板软链 → 检查 python-docx。
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
DEST="${DEST:-$HOME/.workbuddy/skills}"
SKILLS=(hit-cnki-refs hit-assignment-report hit-standard-word-type)
WITH_FONTS=0
[ "${1:-}" = "--fonts" ] && WITH_FONTS=1

echo "仓库：$REPO"
echo "目标：$DEST"
echo

for s in "${SKILLS[@]}"; do
  if [ ! -f "$REPO/skills/$s/SKILL.md" ]; then
    echo "跳过 $s（仓库里没有 SKILL.md）"; continue
  fi
  mkdir -p "$DEST/$s"
  # _user_meta.json 是 WorkBuddy 的安装记录，同步时必须排除
  rsync -a --delete --exclude '_user_meta.json' "$REPO/skills/$s/" "$DEST/$s/"
  echo "已同步 $s"
done

# 模板软链：让 skill 里的相对路径 templates/... 在安装后仍然有效
ln -sfn "$REPO/templates" "$DEST/hit-standard-word-type/templates"
echo "已链接 templates -> $REPO/templates"

# 脚本执行位
chmod +x "$DEST"/hit-cnki-refs/scripts/*.sh 2>/dev/null || true
chmod +x "$DEST"/hit-standard-word-type/scripts/*.sh 2>/dev/null || true
chmod +x "$DEST"/hit-standard-word-type/scripts/fill_template.py 2>/dev/null || true
chmod +x "$DEST"/hit-assignment-report/scripts/*.py 2>/dev/null || true

echo
# 依赖检查（缺了只提示，不中断）
if python3 -c "import docx" 2>/dev/null; then
  echo "依赖：python-docx 已就绪"
else
  echo "依赖：缺 python-docx —— 模板填充要用，装一下：pip3 install python-docx"
fi

have_cjk_font() {
  # macOS：宋体（Songti SC / SimSun / STSong）任一即可
  if [ -f /System/Library/Fonts/Supplemental/Songti.ttc ] || [ -f /Library/Fonts/simsun.ttc ]; then
    return 0
  fi
  ls "$HOME/Library/Fonts" 2>/dev/null | grep -qiE "NotoSerifSC|NotoSansSC|simsun|SimHei" && return 0
  command -v fc-list >/dev/null 2>&1 && fc-list 2>/dev/null | grep -qiE "Noto Serif SC|SimSun|Songti" && return 0
  return 1
}

if [ "$WITH_FONTS" = "1" ]; then
  bash "$DEST/hit-standard-word-type/scripts/install_fonts.sh"
elif have_cjk_font; then
  echo "字体：中文字体可用（宋体/思源宋体）"
else
  echo "字体：没找到宋体 —— 需要精确排版时跑 bash install.sh --fonts 装内置替代字体"
fi

echo
echo "完成。三个 skill 已就位：${SKILLS[*]}"
echo "新开一个 WorkBuddy 会话才会加载最新版本。"
