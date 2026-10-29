# 内置字体说明

HIT 排版规范要求使用 宋体、黑体、Times New Roman，但这三者均为商业授权字体（中易/微软/Monotype 所有），**不能随 skill 分发**。本目录提供开源替代字体，仅在用户系统缺少原字体时使用。

## 字体清单

| 文件 | 用途 | 授权 |
|------|------|------|
| NotoSerifSC.ttf | 宋体（SimSun）替代，可变字重 | SIL OFL 1.1 |
| NotoSansSC.ttf | 黑体（SimHei）替代，可变字重 | SIL OFL 1.1 |
| LiberationSerif-Regular.ttf | Times New Roman 替代（度量兼容） | SIL OFL 1.1 |
| LiberationSerif-Bold.ttf | 同上，粗体 | SIL OFL 1.1 |
| LiberationSerif-Italic.ttf | 同上，斜体 | SIL OFL 1.1 |

- Noto Serif SC / Noto Sans SC 与 Adobe 思源宋体 / 思源黑体同源，覆盖 GB 常用汉字。
- Liberation Serif 与 Times New Roman 度量兼容（同宽度），打印版式不会跑位。
- 各字体授权文本见 `OFL-*.txt` 与 `LICENSE`。

## 安装方式

```bash
bash ../../scripts/install_fonts.sh
```

或手动：将 `*.ttf` 复制到系统字体目录（macOS: `~/Library/Fonts`；Windows: 双击字体文件点"安装"；Linux: `~/.local/share/fonts` 后执行 `fc-cache -f`）。

## 使用注意

- 若文档最终提交到打印店或学校服务器，且对方机器装有正版宋体/黑体，优先使用原字体排版；替代字体仅保证本地预览与自印效果。
- 可变字体（Noto *.ttf）在旧版 Word（2016 以前）中可能只显示默认字重，如遇此情况可改用静态字重版本（从 Google Fonts 下载）。
