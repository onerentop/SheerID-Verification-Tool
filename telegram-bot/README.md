# SheerID Telegram Bot 🤖

通过 Telegram 机器人自动完成多平台学生/教师/军人身份验证。

## 功能特性

- 🎵 **Spotify Premium** 学生验证
- 📺 **YouTube Premium** 学生验证
- 🤖 **Google One (Gemini)** 学生验证
- ⚡ **Bolt.new Pro** 教师验证
- 👩‍🏫 **ChatGPT Plus** K-12 教师验证
- 🎖️ **ChatGPT Plus** 军人验证
- 🔍 **Perplexity Pro** 学生验证
- 🎨 **Canva Education** 教师验证

## 快速开始

### 1. 创建 Telegram Bot

1. 在 Telegram 中搜索 [@BotFather](https://t.me/BotFather)
2. 发送 `/newbot` 创建新机器人
3. 按提示设置名称和用户名
4. 保存获得的 **Bot Token**

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
nano .env
```

配置以下变量：
```env
# 必填：Bot Token
TELEGRAM_BOT_TOKEN=your-bot-token-here

# 可选：代理服务器
PROXY=http://user:pass@host:port

# 可选：日志级别
LOG_LEVEL=INFO
```

### 3. Docker 部署（推荐）

```bash
# 构建并启动
docker compose up -d telegram-bot

# 查看日志
docker compose logs -f telegram-bot

# 停止
docker compose stop telegram-bot
```

### 4. 直接运行（开发）

```bash
# 安装依赖
cd telegram-bot
pip install -r requirements.txt

# 设置环境变量
export TELEGRAM_BOT_TOKEN="your-bot-token"
export PROXY="http://host:port"  # 可选

# 运行
python main.py
```

## 使用方法

### 命令列表

| 命令 | 说明 |
|------|------|
| `/start` | 启动机器人，显示主菜单 |
| `/help` | 获取帮助信息 |
| `/stats` | 查看验证统计 |
| `/verify <工具> <URL>` | 直接验证 |

### 快捷验证命令

| 命令 | 说明 |
|------|------|
| `/spotify <URL>` | Spotify 学生验证 |
| `/youtube <URL>` | YouTube 学生验证 |
| `/one <URL>` | Google One 学生验证 |
| `/boltnew <URL>` | Bolt.new 教师验证 |
| `/k12 <URL>` | ChatGPT K-12 教师验证 |
| `/veterans <URL>` | ChatGPT 军人验证 |
| `/perplexity <URL>` | Perplexity 学生验证 |
| `/canva <URL>` | Canva 教师验证 |

### 使用示例

```
# 方式1：通过主菜单选择工具
/start

# 方式2：快捷命令
/one https://services.sheerid.com/verify/...?verificationId=xxx

# 方式3：通用验证命令
/verify spotify https://services.sheerid.com/verify/...?verificationId=xxx
```

## 文件结构

```
telegram-bot/
├── main.py           # Bot 主程序
├── verifier.py       # 验证器封装
├── requirements.txt  # Python 依赖
├── Dockerfile        # Docker 构建文件
└── README.md         # 本文档
```

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `TELEGRAM_BOT_TOKEN` | ✅ | Telegram Bot Token |
| `PROXY` | ❌ | 代理服务器 (http/socks5) |
| `LOG_LEVEL` | ❌ | 日志级别 (默认: INFO) |

## 注意事项

1. **代理推荐**：强烈建议使用住宅代理，数据中心 IP 容易被检测
2. **验证等待**：提交后需等待 24-48 小时人工审核
3. **链接格式**：URL 必须包含 `sheerid.com` 和 `verificationId`

## 故障排除

### Bot 无响应

```bash
# 检查日志
docker compose logs telegram-bot

# 验证 Token
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

### 验证失败

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `fraudRulesReject` | IP 被标记 | 更换住宅代理 |
| `Already verified` | 链接已使用 | 获取新链接 |
| `Invalid step` | 链接过期 | 获取新链接 |

## 开发

```bash
# 开发模式运行
LOG_LEVEL=DEBUG python main.py

# 语法检查
python -m compileall .
```

## License

MIT License
