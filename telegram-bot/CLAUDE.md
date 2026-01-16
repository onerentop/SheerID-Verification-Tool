[根目录](../CLAUDE.md) > **telegram-bot**

# Telegram Bot 模块

## 模块职责

提供 Telegram 机器人界面，封装所有 8 个验证工具，用户通过 Telegram 直接完成验证操作。

## 入口与启动

```bash
# Docker 部署
docker compose up -d telegram-bot

# 直接运行
cd telegram-bot
python main.py
```

## 对外接口

### 主要类

| 类名 | 文件 | 职责 |
|------|------|------|
| `UnifiedVerifier` | verifier.py | 统一验证接口封装 |
| `VerificationResult` | verifier.py | 验证结果数据类 |
| `UserSession` | main.py | 用户会话状态管理 |

### Bot 命令

| 命令 | 处理函数 | 说明 |
|------|----------|------|
| `/start` | `start_command` | 显示主菜单 |
| `/help` | `help_command` | 帮助信息 |
| `/stats` | `stats_command` | 统计数据 |
| `/verify` | `verify_command` | 通用验证 |
| `/<tool>` | `tool_shortcut_command` | 快捷验证 |

## 关键依赖

| 依赖 | 用途 |
|------|------|
| `python-telegram-bot>=21.0` | Telegram Bot API |
| 所有验证工具模块 | 动态加载调用 |

## 架构设计

```
用户 Telegram 消息
        ↓
    main.py (Bot 逻辑)
        ↓
    verifier.py (统一接口)
        ↓
    动态加载对应工具的 Verifier 类
        ↓
    执行验证并返回结果
```

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `TELEGRAM_BOT_TOKEN` | ✅ | Bot Token |
| `PROXY` | ❌ | 代理服务器 |
| `LOG_LEVEL` | ❌ | 日志级别 |

## 相关文件清单

| 文件 | 描述 |
|------|------|
| `main.py` | Bot 主程序 |
| `verifier.py` | 验证器封装 |
| `requirements.txt` | Python 依赖 |
| `Dockerfile` | Docker 构建 |
| `README.md` | 用户文档 |

## 变更记录

| 日期 | 变更 |
|------|------|
| 2026-01-16 | 创建 Telegram Bot 模块 |
