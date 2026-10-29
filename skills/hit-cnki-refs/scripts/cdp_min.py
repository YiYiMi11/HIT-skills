#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cdp_min.py —— 零依赖 Chrome/Edge DevTools Protocol 客户端（精简版）。

仅供 hit-cnki-refs 使用，只做三件事：
1. 连接已以 --remote-debugging-port 启动的 Chromium 内核浏览器；
2. 在页面上执行 JS / 导航 / 等待条件；
3. 在浏览器级别把下载目录重定向到指定文件夹，并可靠地等到下载完成。

只用标准库。已规避三个经典坑：
- 响应循环必须跳过 event 消息，否则事件会被当成下一条命令的响应；
- 导航超时必须返回 False，否则下游静默失败；
- 下载完成必须以 downloadProgress.state == "completed" 为准，不能靠文件大小稳定猜测。

命令行自检：
    python3 cdp_min.py check
"""

import base64
import json
import os
import socket
import ssl
import struct
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_PORT = 9222
DEFAULT_HOST = "127.0.0.1"


class CDPError(Exception):
    pass


# ---------------------------------------------------------------- WebSocket
class WSClient:
    """RFC 6455 客户端子集：文本帧、分片合并、掩码发送。"""

    def __init__(self, url, timeout=15.0):
        if not isinstance(url, str) or not url.startswith(("ws://", "wss://")):
            raise CDPError("非法 WebSocket URL：%r" % (url,))
        self.url = url
        self.sock = None
        self._buf = b""
        self._handshake(timeout)

    def _handshake(self, timeout):
        u = urlparse(self.url)
        host = u.hostname
        port = u.port or (443 if u.scheme == "wss" else 80)
        try:
            self.sock = socket.create_connection((host, port), timeout=timeout)
        except OSError as exc:
            raise CDPError("连接 %s:%s 失败：%s" % (host, port, exc))
        if u.scheme == "wss":
            ctx = ssl.create_default_context()
            self.sock = ctx.wrap_socket(self.sock, server_hostname=host)
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        path = (u.path or "/") + (("?" + u.query) if u.query else "")
        req = (
            "GET %s HTTP/1.1\r\nHost: %s:%s\r\nUpgrade: websocket\r\n"
            "Connection: Upgrade\r\nSec-WebSocket-Key: %s\r\n"
            "Sec-WebSocket-Version: 13\r\nOrigin: http://%s:%s\r\n\r\n"
            % (path, host, port, key, host, port)
        )
        self.sock.sendall(req.encode("ascii"))
        buf = b""
        deadline = time.time() + timeout
        while b"\r\n\r\n" not in buf:
            self.sock.settimeout(max(0.1, deadline - time.time()))
            try:
                chunk = self.sock.recv(4096)
            except (socket.timeout, TimeoutError):
                raise CDPError("WebSocket 握手超时")
            if not chunk:
                raise CDPError("WebSocket 握手失败：连接被关闭")
            buf += chunk
        head, rest = buf.split(b"\r\n\r\n", 1)
        if b"101" not in head.split(b"\r\n")[0]:
            raise CDPError("WebSocket 握手被拒绝：%s" % head.split(b"\r\n")[0])
        self._buf = rest

    def _read_exact(self, n):
        while len(self._buf) < n:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise CDPError("WebSocket 连接已关闭")
            self._buf += chunk
        data, self._buf = self._buf[:n], self._buf[n:]
        return data

    def _recv_frame(self):
        while True:
            b1, b2 = self._read_exact(2)
            fin, opcode = b1 & 0x80, b1 & 0x0F
            masked, length = b2 & 0x80, b2 & 0x7F
            if length == 126:
                length = struct.unpack(">H", self._read_exact(2))[0]
            elif length == 127:
                length = struct.unpack(">Q", self._read_exact(8))[0]
            mask = self._read_exact(4) if masked else None
            payload = self._read_exact(length) if length else b""
            if mask:
                payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
            if opcode == 0x8:
                raise CDPError("WebSocket 收到关闭帧")
            if opcode in (0x9, 0xA):
                continue
            return fin, opcode, payload

    def send_text(self, text):
        payload = text.encode("utf-8")
        header = bytearray([0x81])
        n = len(payload)
        mask = os.urandom(4)
        if n < 126:
            header.append(0x80 | n)
        elif n < 65536:
            header.append(0x80 | 126)
            header += struct.pack(">H", n)
        else:
            header.append(0x80 | 127)
            header += struct.pack(">Q", n)
        header += mask
        self.sock.sendall(bytes(header) + bytes(b ^ mask[i % 4] for i, b in enumerate(payload)))

    def recv_text(self, timeout=None):
        chunks = []
        while True:
            if timeout is not None:
                self.sock.settimeout(timeout)
            fin, opcode, payload = self._recv_frame()
            if opcode in (0x0, 0x1):
                chunks.append(payload)
            if fin:
                break
        return b"".join(chunks).decode("utf-8", "replace")

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except OSError:
                pass
            self.sock = None


# ---------------------------------------------------------------- 连接封装
class Conn:
    """一条 CDP 连接：同步 call + 事件缓存。"""

    def __init__(self, ws_url, timeout=20.0):
        self.ws = WSClient(ws_url, timeout=timeout)
        self._id = 0
        self.events = []

    def call(self, method, params=None, timeout=20.0):
        self._id += 1
        mid = self._id
        self.ws.send_text(json.dumps({"id": mid, "method": method, "params": params or {}}))
        deadline = time.time() + timeout
        while True:
            remain = deadline - time.time()
            if remain <= 0:
                raise CDPError("CDP 调用超时：%s" % method)
            data = json.loads(self.ws.recv_text(timeout=remain))
            if data.get("id") == mid:
                if "error" in data:
                    raise CDPError("%s 失败：%s" % (method, data["error"].get("message")))
                return data.get("result", {})
            if "method" in data:
                self.events.append(data)

    def drain(self, timeout=0.2):
        """取走已到达的事件。"""
        out = self.events[:]
        self.events.clear()
        if timeout:
            try:
                data = json.loads(self.ws.recv_text(timeout=timeout))
                if "method" in data:
                    out.append(data)
            except (socket.timeout, TimeoutError, CDPError):
                pass
        return out

    def close(self):
        self.ws.close()


def _http_json(host, port, path, timeout=5.0):
    url = "http://%s:%d%s" % (host, port, path)
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.URLError as exc:
        raise CDPError(
            "无法连接 CDP（%s）。浏览器需以调试模式启动，"
            "见 references/cnki-workflow.md 的「启动调试浏览器」。原始错误：%s" % (url, exc)
        )


def list_targets(host=DEFAULT_HOST, port=DEFAULT_PORT):
    return _http_json(host, port, "/json/list")


def pick_page(host=DEFAULT_HOST, port=DEFAULT_PORT, url_contains=None):
    pages = [t for t in list_targets(host, port) if t.get("type") == "page"]
    if url_contains:
        pages = [p for p in pages if url_contains in (p.get("url") or "")]
    if not pages:
        raise CDPError("没有可用的标签页（过滤条件：%r）" % (url_contains,))
    return pages[0]


class Page:
    """页面级操作。"""

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT, url_contains=None, target_id=None):
        if target_id:
            targets = list_targets(host, port)
            match = [t for t in targets if t.get("id") == target_id]
            if not match:
                raise CDPError("找不到 targetId=%s 的标签页" % target_id)
            tgt = match[0]
        else:
            tgt = pick_page(host, port, url_contains)
        self.target = tgt
        self.conn = Conn(tgt["webSocketDebuggerUrl"])
        self.conn.call("Runtime.enable", timeout=10)
        self.conn.call("Page.enable", timeout=10)

    # ---- 基础 ----
    def eval(self, expr, timeout=30.0, await_promise=True):
        r = self.conn.call(
            "Runtime.evaluate",
            {"expression": expr, "returnByValue": True, "awaitPromise": await_promise},
            timeout=timeout,
        )
        if r.get("exceptionDetails"):
            d = r["exceptionDetails"]
            desc = (d.get("exception") or {}).get("description") or d.get("text")
            raise CDPError("JS 执行异常：%s" % desc)
        return r.get("result", {}).get("value")

    def url(self):
        return self.eval("location.href", timeout=10)

    def title(self):
        return self.eval("document.title", timeout=10)

    def navigate(self, url, timeout=30.0):
        """导航并等待 load 事件；超时返回 False（不抛异常）。"""
        self.conn.call("Page.navigate", {"url": url}, timeout=timeout)
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.eval("document.readyState", timeout=5) == "complete":
                return True
            time.sleep(0.4)
        return False

    def wait_js(self, expr, timeout=30.0, interval=0.4):
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                if self.eval(expr, timeout=max(5, timeout)):
                    return True
            except CDPError:
                pass
            time.sleep(interval)
        return False

    def new_tab(self, url="about:blank"):
        """在同浏览器内开新标签页，返回新的 Page。"""
        host = urlparse(self.target["webSocketDebuggerUrl"]).hostname or DEFAULT_HOST
        port = urlparse(self.target["webSocketDebuggerUrl"]).port or DEFAULT_PORT
        b = Browser(host, port)
        try:
            tid = b.call("Target.createTarget", {"url": url})["targetId"]
        finally:
            b.close()
        return Page(host, port, target_id=tid)

    def close(self):
        self.conn.close()


class Browser:
    """浏览器级操作：下载目录重定向、下载事件监听。"""

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        ver = _http_json(host, port, "/json/version")
        self.conn = Conn(ver["webSocketDebuggerUrl"])

    def call(self, method, params=None, timeout=15.0):
        return self.conn.call(method, params, timeout=timeout)

    def set_download_dir(self, path):
        """把后续所有下载重定向到 path，并开启下载事件。"""
        p = Path(path).expanduser().resolve()
        p.mkdir(parents=True, exist_ok=True)
        self.call(
            "Browser.setDownloadBehavior",
            {"behavior": "allow", "downloadPath": str(p), "eventsEnabled": True},
        )
        return p

    def wait_download(self, timeout=120.0, settle=1.5):
        """
        等到一次下载完成。返回 {guid, filename, path, bytes} 或 None。
        以 downloadProgress.state == completed 为准。
        """
        started = {}
        done = {}
        deadline = time.time() + timeout
        last_event = time.time()
        while time.time() < deadline:
            events = self.conn.drain(timeout=0.5)
            for ev in events:
                m = ev.get("method")
                prm = ev.get("params") or {}
                if m == "Browser.downloadWillBegin":
                    started[prm.get("guid")] = prm.get("suggestedFilename")
                    last_event = time.time()
                elif m == "Browser.downloadProgress":
                    last_event = time.time()
                    if prm.get("state") == "completed":
                        done[prm.get("guid")] = prm
            for guid, prm in list(done.items()):
                if guid in started or prm.get("suggestedFilename"):
                    name = started.get(guid) or prm.get("suggestedFilename")
                    return {
                        "guid": guid,
                        "filename": name,
                        "downloadPath": prm.get("filePath") or None,
                        "totalBytes": prm.get("totalBytes"),
                    }
            # 长时间无事件且已有 started，视为完成（部分版本不发进度事件）
            if started and time.time() - last_event > settle:
                for guid, name in started.items():
                    return {"guid": guid, "filename": name, "downloadPath": None, "totalBytes": None}
        return None

    def close(self):
        self.conn.close()


# ---------------------------------------------------------------- 自检
def check(host=DEFAULT_HOST, port=DEFAULT_PORT):
    out = {"cdp": False, "browser": None, "pages": []}
    try:
        ver = _http_json(host, port, "/json/version")
        out["cdp"] = True
        out["browser"] = ver.get("Browser")
        out["pages"] = [
            {"title": t.get("title"), "url": (t.get("url") or "")[:100]}
            for t in list_targets(host, port)
            if t.get("type") == "page"
        ]
    except CDPError as exc:
        out["error"] = str(exc)
    return out


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "check":
        info = check()
        print(json.dumps(info, ensure_ascii=False, indent=2))
        sys.exit(0 if info["cdp"] else 2)
    print(__doc__)
