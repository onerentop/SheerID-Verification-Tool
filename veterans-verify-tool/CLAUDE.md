[根目录](../CLAUDE.md) > **veterans-verify-tool**

# 退伍军人验证工具

## 模块职责

自动化 ChatGPT Plus 美国退伍军人折扣的验证流程。通过 ChatGPT API 创建验证请求，然后与 SheerID 交互。

## 入口与启动

```bash
python main.py
python main.py --proxy host:port
python main.py --no-dedup
```

## 对外接口

### CLI 参数

| 参数 | 描述 |
|------|------|
| `--proxy` | 使用指定代理 |
| `--no-dedup` | 禁用去重检查 |

### 主要类

| 类名 | 职责 |
|------|------|
| `VeteransVerifier` | 核心验证逻辑 |
| `EmailClient` | IMAP 邮箱客户端 |

## 与其他工具的区别

1. **需要 ChatGPT accessToken** - 通过 ChatGPT API 创建验证
2. **需要真实军人数据** - SheerID 对接 DoD/DEERS 数据库验证
3. **需要邮箱配置** - 用于接收验证邮件
4. **批量数据处理** - 从 `data.txt` 读取多条记录

## 关键配置

### config.json

```json
{
    "accessToken": "ChatGPT访问令牌",
    "programId": "690415d58971e73ca187d8c9",
    "email": {
        "imap_server": "imap.gmail.com",
        "imap_port": 993,
        "email_address": "your@email.com",
        "email_password": "app_password"
    }
}
```

### data.txt 格式

```
JOHN|SMITH|Army|1990-05-15|2025-06-01
```

格式: `firstName|lastName|branch|birthDate|dischargeDate`

## 军种代码

| 军种 | 组织 ID |
|------|---------|
| Army | 4070 |
| Air Force | 4073 |
| Navy | 4072 |
| Marine Corps | 4071 |
| Coast Guard | 4074 |
| Space Force | 4544268 |

## 验证流程

```
1. create_verification()        - 通过 ChatGPT API 创建验证
2. submit_military_status()     - 提交状态为 VETERAN
3. submit_personal_info()       - 提交个人信息
4. wait_for_email()             - 等待验证邮件
5. submit_email_token()         - 提交邮件验证码
```

## 相关文件清单

| 文件 | 描述 |
|------|------|
| `main.py` | 主程序 |
| `config.example.json` | 配置模板 |
| `data.example.txt` | 数据格式示例 |
| `proxy.example.txt` | 代理格式示例 |
| `debug_email.py` | 邮箱连接调试工具 |
| `used.txt` | 已使用数据记录 (运行时生成) |

## 常见问题

### Q: 403 Forbidden 错误？

A: accessToken 过期，需要重新获取。

### Q: "Not approved" 错误？

A: 数据不在 DoD 数据库中，或 IP 被阻止。使用代理并检查数据有效性。

### Q: 退伍日期规则？

A: 必须在过去 12 个月内退伍。

## 变更记录

| 日期 | 变更 |
|------|------|
| 2026-01-15 | 创建模块级 CLAUDE.md |
