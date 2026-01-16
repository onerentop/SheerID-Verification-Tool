[根目录](../CLAUDE.md) > **veterans-extension**

# Veterans Extension (Chrome MV3)

## 模块职责

Chrome Manifest V3 扩展，自动化 ChatGPT Plus 退伍军人验证的完整流程，包括重定向、表单填充、错误处理和临时邮箱支持。

## 安装

1. 打开 `chrome://extensions/`
2. 启用 **开发者模式**
3. 点击 **加载已解压的扩展程序**
4. 选择 `veterans-extension/` 目录

## 核心功能

| 功能 | 描述 |
|------|------|
| 自动重定向 | veterans-claim -> SheerID |
| 批量填充 | 支持多条退伍军人数据 |
| 自动重试 | 检测错误后自动获取新链接 |
| 成功检测 | 成功后自动禁用 |
| 统计面板 | 追踪 Success/Failed/Skipped |
| 导入/导出 | 备份和恢复配置 |
| 临时邮箱 | 支持 1secmail, Mail.tm |

## 文件结构

| 文件 | 职责 |
|------|------|
| `manifest.json` | 扩展配置 (权限、内容脚本) |
| `background.js` | Service Worker |
| `content.js` | 自动填充逻辑、错误检测、API 调用 |
| `popup.html` | 弹出窗口 UI |
| `popup.js` | 弹出窗口逻辑 |
| `sidepanel.html` | 侧边面板 UI |
| `sidepanel.js` | 侧边面板逻辑 |
| `icon*.png` | 扩展图标 |

## 权限

```json
{
    "permissions": ["storage", "activeTab", "scripting", "sidePanel", "cookies"],
    "host_permissions": [
        "https://*.sheerid.com/*",
        "https://*.openai.com/*",
        "https://chatgpt.com/*",
        "https://api.mail.tm/*",
        "https://www.1secmail.com/*"
    ]
}
```

## 数据格式

```
JOHN|DOE|Army|1985-01-15|2025-06-01
```

格式: `FirstName|LastName|Branch|DOB|DischargeDate`

## 临时邮箱支持

| 服务 | 域名 |
|------|------|
| 1secmail | 1secmail.com, 1secmail.org, wwjmp.com, esiix.com |
| Mail.tm | mail.tm, mail.gw |

## 错误处理

自动检测并处理以下错误：

| 错误模式 | 动作 |
|----------|------|
| verification limit exceeded | 使用下一条数据重试 |
| unable to verify | 重试 |
| information does not match | 重试 |
| already been used | 跳过，使用下一条 |
| fraudRulesReject | 使用不同数据重试 |

## 相关文件清单

| 文件 | 描述 |
|------|------|
| `manifest.json` | 扩展配置 |
| `background.js` | Service Worker |
| `content.js` | 内容脚本 |
| `popup.html/js` | 弹出窗口 |
| `sidepanel.html/js` | 侧边面板 |
| `README.md` | 说明文档 |

## 变更记录

| 日期 | 变更 |
|------|------|
| 2026-01-15 | 创建模块级 CLAUDE.md |
