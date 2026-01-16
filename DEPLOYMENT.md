# SheerID Verification Tool 部署文档

本文档详细说明如何部署和运行 SheerID 验证工具集。

---

## 目录

1. [系统要求](#系统要求)
2. [快速开始](#快速开始)
3. [Docker 部署（推荐）](#docker-部署推荐)
4. [Python CLI 工具部署](#python-cli-工具部署)
5. [Chrome 扩展部署](#chrome-扩展部署)
6. [各工具详细说明](#各工具详细说明)
7. [代理配置](#代理配置)
8. [故障排除](#故障排除)

---

## 系统要求

### Python 环境

| 组件 | 最低版本 | 推荐版本 |
|------|---------|---------|
| Python | 3.8+ | 3.11+ |
| pip | 21.0+ | 最新版 |

### 浏览器（仅扩展）

| 浏览器 | 版本 |
|--------|------|
| Chrome | 88+ (Manifest V3) |
| Edge | 88+ |
| Brave | 1.25+ |

### Docker 环境

| 组件 | 最低版本 |
|------|---------|
| Docker | 20.10+ |
| Docker Compose | 2.0+ |

---

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
cd SheerID-Verification-Tool
```

### 2. 创建虚拟环境（推荐）

**Windows:**
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 安装基础依赖

```bash
pip install -r requirements.txt
```

### 4. 安装增强反检测依赖（强烈推荐）

```bash
pip install curl_cffi cloudscraper
```

> ⚠️ `curl_cffi` 提供 TLS 指纹伪装，可显著降低 `fraudRulesReject` 错误率

---

## Docker 部署（推荐）

使用 Docker 可以一键部署，无需手动配置 Python 环境。

### 构建镜像

```bash
# 克隆仓库
git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
cd SheerID-Verification-Tool

# 构建镜像
docker build -t sheerid-tool:latest .

# 或使用 docker compose
docker compose build
```

### 运行方式

#### 方式 1: 直接运行 (docker run)

```bash
# 查看帮助
docker run --rm sheerid-tool --help

# Google One 验证
docker run --rm -it sheerid-tool one "https://services.sheerid.com/verify/...?verificationId=xxx"

# Spotify 验证
docker run --rm -it sheerid-tool spotify "URL"

# YouTube 验证
docker run --rm -it sheerid-tool youtube "URL"

# 带代理运行
docker run --rm -it sheerid-tool one "URL" --proxy http://user:pass@host:port

# 使用环境变量传递代理
docker run --rm -it -e PROXY=http://host:port sheerid-tool one "URL"
```

#### 方式 2: Docker Compose

```bash
# 复制环境变量配置
cp .env.example .env
# 编辑 .env 设置代理（可选）

# 通用方式
docker compose run --rm verify one "URL"
docker compose run --rm verify spotify "URL"

# 快捷服务
docker compose run --rm one "URL"
docker compose run --rm spotify "URL"
docker compose run --rm youtube "URL"
docker compose run --rm veterans "URL"
```

### 可用工具列表

| 工具名 | 别名 | 说明 |
|--------|------|------|
| `spotify` | - | Spotify Premium 学生验证 |
| `youtube` | - | YouTube Premium 学生验证 |
| `one` | `gemini` | Google One/Gemini 学生验证 |
| `boltnew` | - | Bolt.new 教师验证 |
| `k12` | - | ChatGPT K-12 教师验证 |
| `veterans` | `military` | ChatGPT 军人验证 |
| `perplexity` | - | Perplexity 学生验证 |
| `canva` | - | Canva 教师验证 |

### Docker 环境变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `PROXY` | 代理服务器 | `http://user:pass@host:port` |
| `TOOL` | 默认工具 | `one` |

### 镜像信息

```bash
# 查看镜像大小
docker images sheerid-tool

# 预期大小: ~250MB (多阶段构建优化)
```

### 清理

```bash
# 删除容器
docker compose down

# 删除镜像
docker rmi sheerid-tool:latest

# 清理构建缓存
docker builder prune
```

---

## Python CLI 工具部署

### 依赖列表

#### 全局依赖 (requirements.txt)

| 包名 | 用途 | 必需 |
|------|------|------|
| `httpx` | 异步 HTTP 客户端 | ✅ |
| `Pillow` | 图片处理/证件生成 | ✅ |
| `requests` | HTTP 备用库 | ✅ |
| `cloudscraper` | Cloudflare 绕过 | ⭕ 推荐 |
| `curl_cffi` | TLS 指纹伪装 | ⭕ 强烈推荐 |

#### 特定工具依赖

| 工具 | 额外依赖 | 安装命令 |
|------|---------|---------|
| canva-teacher-tool | `pymupdf` | `pip install pymupdf pillow` |

### 安装步骤

```bash
# 1. 安装全局依赖
pip install httpx Pillow requests

# 2. 安装推荐的反检测依赖
pip install curl_cffi cloudscraper

# 3. 安装特定工具依赖（如需要）
pip install -r canva-teacher-tool/requirements.txt
```

### 验证安装

```bash
# 测试 anti_detect 模块
python anti_detect.py

# 预期输出:
# Anti-Detection Module Test
# ----------------------------------------
# [Anti-Detect] Using curl_cffi for HTTP requests
# [Anti-Detect] User-Agents: 10 variants
# ...
```

---

## Chrome 扩展部署

项目包含两个 Chrome 扩展：

| 扩展 | 目录 | 功能 |
|------|------|------|
| Veterans Verification | `veterans-extension/` | 完整军人验证自动化 |
| Veterans Autofill | `veterans-autofill/` | 表单自动填充 |

### 安装步骤

1. **打开 Chrome 扩展管理页面**
   ```
   chrome://extensions/
   ```

2. **启用开发者模式**
   - 右上角打开「开发者模式」开关

3. **加载扩展**
   - 点击「加载已解压的扩展程序」
   - 选择扩展目录（如 `veterans-extension/`）

4. **固定扩展（可选）**
   - 点击扩展图标右侧的图钉固定到工具栏

### 扩展权限说明

```json
{
  "permissions": ["storage", "activeTab", "scripting", "sidePanel", "cookies"],
  "host_permissions": [
    "https://*.sheerid.com/*",
    "https://*.openai.com/*",
    "https://chatgpt.com/*"
  ]
}
```

---

## 各工具详细说明

### 1. Spotify 学生验证

```bash
cd spotify-verify-tool
python main.py "https://services.sheerid.com/verify/...?verificationId=xxx"

# 带代理
python main.py "URL" --proxy http://user:pass@host:port
```

### 2. YouTube Premium 学生验证

```bash
cd youtube-verify-tool
python main.py "https://services.sheerid.com/verify/...?verificationId=xxx"
```

### 3. Google One (Gemini Advanced) 学生验证

```bash
cd one-verify-tool
python main.py "https://services.sheerid.com/verify/...?verificationId=xxx"

# 带住宅代理（推荐）
python main.py "URL" --proxy socks5://user:pass@host:port
```

### 4. Bolt.new 教师验证

```bash
cd boltnew-verify-tool
python main.py "https://services.sheerid.com/verify/...?verificationId=xxx"
```

### 5. ChatGPT K-12 教师验证

```bash
cd k12-verify-tool
python main.py "https://services.sheerid.com/verify/...?verificationId=xxx"
```

### 6. ChatGPT 军人验证

```bash
cd veterans-verify-tool
python main.py "https://services.sheerid.com/verify/...?verificationId=xxx"
```

### 7. Perplexity 学生验证

```bash
cd perplexity-verify-tool
python main.py "https://services.sheerid.com/verify/...?verificationId=xxx"
```

### 8. Canva 教师验证（非 SheerID）

```bash
cd canva-teacher-tool
pip install -r requirements.txt  # 安装 pymupdf
python main.py
```

---

## 代理配置

### 支持的代理格式

```bash
# HTTP 代理
--proxy http://host:port
--proxy http://user:pass@host:port

# SOCKS5 代理
--proxy socks5://host:port
--proxy socks5://user:pass@host:port

# 简化格式（自动添加 http://）
--proxy host:port
--proxy user:pass:host:port
```

### 代理推荐

| 类型 | 成功率 | 推荐场景 |
|------|--------|---------|
| 住宅代理 | ⭐⭐⭐⭐⭐ | 所有验证 |
| 移动代理 | ⭐⭐⭐⭐ | 高频使用 |
| 数据中心代理 | ⭐⭐ | 测试用途 |

> ⚠️ 强烈建议使用住宅 IP 代理，数据中心 IP 容易触发 `fraudRulesReject`

---

## HTTP 库优先级

`anti_detect.py` 自动选择最佳 HTTP 库：

```
1. curl_cffi    → TLS 指纹伪装（最佳）
2. cloudscraper → Cloudflare 绕过
3. httpx        → 现代异步客户端
4. requests     → 兼容性备选
```

查看当前使用的库：

```bash
python -c "from anti_detect import create_session; print(create_session()[1])"
```

---

## 故障排除

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `fraudRulesReject` | IP 被标记为可疑 | 使用住宅代理，等待 5-10 分钟后重试 |
| `Already verified` | 链接已使用 | 获取新的验证链接 |
| `Invalid step` | 链接状态异常 | 检查链接是否过期 |
| `ModuleNotFoundError: httpx` | 依赖未安装 | `pip install httpx` |
| `S3 upload failed` | 网络问题或签名过期 | 重试或检查网络连接 |
| `ImpersonateError` | curl_cffi 版本问题 | 更新: `pip install -U curl_cffi` |

### 依赖问题排查

```bash
# 检查已安装的包
pip list | grep -E "httpx|Pillow|curl_cffi|cloudscraper"

# 重新安装所有依赖
pip install --force-reinstall -r requirements.txt

# 验证 Python 版本
python --version  # 需要 3.8+
```

### 扩展问题排查

1. **扩展无法加载**
   - 确保 `manifest.json` 语法正确
   - 检查 Chrome 版本 ≥ 88

2. **权限错误**
   - 确保授予了所有请求的权限
   - 检查 `host_permissions` 是否正确

3. **脚本不执行**
   - 打开开发者工具 (F12) 检查控制台错误
   - 确保在正确的域名下运行

---

## 项目结构

```
SheerID-Verification-Tool/
├── anti_detect.py              # 共享反检测模块
├── requirements.txt            # 全局 Python 依赖
├── CLAUDE.md                   # AI 助手指南
├── DEPLOYMENT.md               # 本部署文档
│
├── spotify-verify-tool/        # Spotify 学生验证
│   └── main.py
├── youtube-verify-tool/        # YouTube 学生验证
│   └── main.py
├── one-verify-tool/            # Google One 学生验证
│   └── main.py
├── boltnew-verify-tool/        # Bolt.new 教师验证
│   └── main.py
├── k12-verify-tool/            # ChatGPT K-12 验证
│   └── main.py
├── veterans-verify-tool/       # ChatGPT 军人验证
│   └── main.py
├── perplexity-verify-tool/     # Perplexity 学生验证
│   └── main.py
├── canva-teacher-tool/         # Canva 教师验证
│   ├── main.py
│   └── requirements.txt        # 额外依赖: pymupdf
│
├── veterans-extension/         # Chrome 扩展 (Manifest V3)
│   ├── manifest.json
│   ├── background.js
│   ├── content.js
│   ├── popup.html/js
│   └── sidepanel.html/js
│
└── veterans-autofill/          # Chrome 自动填充扩展
    ├── manifest.json
    ├── content.js
    ├── fingerprint-spoofer.js
    └── popup.html/js
```

---

## 一键部署脚本

### Windows (PowerShell)

```powershell
# deploy.ps1
git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
cd SheerID-Verification-Tool
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install curl_cffi cloudscraper
python anti_detect.py
Write-Host "✅ 部署完成！"
```

### macOS/Linux (Bash)

```bash
#!/bin/bash
# deploy.sh
git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
cd SheerID-Verification-Tool
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install curl_cffi cloudscraper
python anti_detect.py
echo "✅ 部署完成！"
```

---

## 安全注意事项

1. **不要提交敏感信息**
   - `.env` 文件已被 gitignore
   - 代理凭证请使用环境变量

2. **使用虚拟环境**
   - 避免污染全局 Python 环境

3. **定期更新依赖**
   ```bash
   pip install --upgrade -r requirements.txt
   ```
