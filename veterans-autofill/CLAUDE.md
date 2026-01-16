[根目录](../CLAUDE.md) > **veterans-autofill**

# Veterans Autofill Extension (Chrome MV3)

## 模块职责

Chrome Manifest V3 扩展，专注于 SheerID 表单自动填充和指纹伪装。相比 veterans-extension，功能更简化，专注于填充。

## 安装

1. 打开 `chrome://extensions/`
2. 启用 **开发者模式**
3. 点击 **加载已解压的扩展程序**
4. 选择 `veterans-autofill/` 目录

## 核心功能

| 功能 | 描述 |
|------|------|
| 自动邮箱 | 生成临时邮箱 (mail.tm) |
| 用户数据 | 填写退伍军人信息 |
| 一键填充 | 自动填充表单 |
| 获取 OTP | 从邮箱获取验证码 |
| 反检测 | 指纹伪装绕过 |

## 文件结构

| 文件 | 职责 |
|------|------|
| `manifest.json` | 扩展配置 |
| `popup.html` | UI 面板 |
| `popup.js` | 弹出窗口逻辑 + 邮箱 API |
| `content.js` | 自动填充逻辑 |
| `fingerprint-spoofer.js` | 反指纹脚本 |
| `icon*.png` | 扩展图标 |

## 反检测功能 (fingerprint-spoofer.js)

在 MAIN world 运行，伪装以下指纹：

| 指纹类型 | 伪装方法 |
|----------|----------|
| Canvas | 添加噪点 |
| WebGL | 随机化 GPU vendor/renderer |
| Audio | 修改 AudioContext |
| Navigator | 隐藏 webdriver 标志，随机化硬件信息 |
| Screen | 随机化屏幕分辨率 |
| Timezone | 随机化为常见美国时区 |

## 权限

```json
{
    "permissions": ["storage", "activeTab", "tabs"],
    "host_permissions": [
        "https://services.sheerid.com/*",
        "https://api.mail.tm/*",
        "https://www.1secmail.com/*",
        "https://chatgpt.com/*"
    ]
}
```

## 内容脚本配置

```json
{
    "content_scripts": [
        {
            "matches": ["https://services.sheerid.com/*"],
            "js": ["fingerprint-spoofer.js"],
            "run_at": "document_start",
            "world": "MAIN"  // 在页面上下文运行
        },
        {
            "matches": ["https://services.sheerid.com/*"],
            "js": ["content.js"],
            "run_at": "document_idle",
            "world": "ISOLATED"  // 在隔离上下文运行
        }
    ]
}
```

## 与 veterans-extension 的区别

| 方面 | veterans-extension | veterans-autofill |
|------|-------------------|-------------------|
| 功能 | 完整流程 | 仅填充 |
| 重定向 | 有 | 无 |
| 侧边面板 | 有 | 无 |
| 反指纹 | 无 | 有 (fingerprint-spoofer.js) |
| 复杂度 | 高 | 低 |

## 相关文件清单

| 文件 | 描述 |
|------|------|
| `manifest.json` | 扩展配置 |
| `popup.html/js` | 弹出窗口 |
| `content.js` | 填充脚本 |
| `fingerprint-spoofer.js` | 反指纹 |
| `README.md` | 说明文档 |

## 变更记录

| 日期 | 变更 |
|------|------|
| 2026-01-15 | 创建模块级 CLAUDE.md |
