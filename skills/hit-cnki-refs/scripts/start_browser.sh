#!/usr/bin/env bash
# 以调试模式启动 Chromium 内核浏览器，供 hit-cnki-refs 使用。
# 用法：bash start_browser.sh [端口]
set -euo pipefail

PORT="${1:-9222}"
PROFILE="$HOME/.workbuddy/cnki-profile"
mkdir -p "$PROFILE"

if curl -s --max-time 2 "http://127.0.0.1:${PORT}/json/version" >/dev/null 2>&1; then
  echo "CDP 已在 ${PORT} 端口运行，无需重启"
  curl -s "http://127.0.0.1:${PORT}/json/version" | sed -n 's/.*"Browser": "\([^"]*\)".*/浏览器：\1/p'
  exit 0
fi

if [ -d "/Applications/Google Chrome.app" ]; then
  BIN="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
elif [ -d "/Applications/Microsoft Edge.app" ]; then
  BIN="/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
elif [ -d "/Applications/Chromium.app" ]; then
  BIN="/Applications/Chromium.app/Contents/MacOS/Chromium"
else
  echo "未找到 Chrome / Edge / Chromium，请先安装其一" >&2
  exit 1
fi

echo "启动：$BIN"
nohup "$BIN" \
  --remote-debugging-port="$PORT" \
  --user-data-dir="$PROFILE" \
  --no-first-run --no-default-browser-check \
  about:blank >/dev/null 2>&1 &

for _ in $(seq 1 20); do
  sleep 0.5
  if curl -s --max-time 2 "http://127.0.0.1:${PORT}/json/version" >/dev/null 2>&1; then
    echo "就绪，CDP 端口 ${PORT}"
    exit 0
  fi
done

echo "启动超时，请手动检查浏览器窗口" >&2
exit 1
