#!/usr/bin/env bash
# 安装本 skill 内置的排版替代字体到当前用户。
# 用途：当系统缺少 宋体/黑体/Times New Roman 时，安装开源替代字体，
#       使 Word 排版在缺少商业字体的机器上仍能正确显示。
# 用法：bash install_fonts.sh
set -euo pipefail

FONT_DIR="$(cd "$(dirname "$0")/../assets/fonts" && pwd)"

install_mac() {
  DEST="$HOME/Library/Fonts"
  mkdir -p "$DEST"
  cp -f "$FONT_DIR"/*.ttf "$DEST/"
  echo "已安装字体到 $DEST"
}

install_linux() {
  DEST="$HOME/.local/share/fonts/hit-standard-word"
  mkdir -p "$DEST"
  cp -f "$FONT_DIR"/*.ttf "$DEST/"
  fc-cache -f "$DEST" >/dev/null 2>&1 || true
  echo "已安装字体到 $DEST"
}

install_windows() {
  # Git Bash / MSYS2 环境
  DEST="$HOME/AppData/Local/Microsoft/Windows/Fonts"
  mkdir -p "$DEST"
  cp -f "$FONT_DIR"/*.ttf "$DEST/"
  # 注册到当前用户（HKCU，无需管理员权限）
  for f in "$FONT_DIR"/*.ttf; do
    name="$(basename "$f")"
    reg add "HKCU\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Fonts" \
      /v "${name%.*} (TrueType)" /t REG_SZ /d "$DEST\\$name" /f >/dev/null
  done
  echo "已安装字体到 $DEST"
}

case "$(uname -s)" in
  Darwin) install_mac ;;
  Linux)  install_linux ;;
  MINGW*|MSYS*|CYGWIN*) install_windows ;;
  *) echo "未知系统 $(uname -s)，请手动将 assets/fonts/*.ttf 安装到系统字体目录" && exit 1 ;;
esac

echo "字体映射：宋体→Noto Serif SC，黑体→Noto Sans SC，Times New Roman→Liberation Serif"
