# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 变更记录 (Changelog)

| 日期 | 版本 | 变更内容 |
|------|------|---------|
| 2026-01-16 | 2.1.0 | 新增 Telegram Bot 模块 |
| 2026-01-15 | 2.0.0 | 完整重构文档结构，增加模块级 CLAUDE.md，Mermaid 架构图 |

---

## 项目愿景

SheerID 身份验证工具集 - 一套自动化多平台（Spotify、YouTube、Google One、Bolt.new、ChatGPT、Perplexity、Canva）学生/教师/军人身份验证的 Python CLI 工具、Chrome 扩展和 Telegram 机器人。

---

## 架构总览

```mermaid
graph TD
    A["SheerID-Verification-Tool<br/>(根目录)"] --> B["anti_detect.py<br/>共享反检测模块"]
    A --> C["Python CLI 工具"]
    A --> D["Chrome 扩展"]
    A --> E["docs/<br/>多语言文档"]
    A --> F["telegram-bot<br/>Telegram 机器人"]

    C --> C1["spotify-verify-tool"]
    C --> C2["youtube-verify-tool"]
    C --> C3["one-verify-tool"]
    C --> C4["boltnew-verify-tool"]
    C --> C5["k12-verify-tool"]
    C --> C6["veterans-verify-tool"]
    C --> C7["perplexity-verify-tool"]
    C --> C8["canva-teacher-tool"]

    D --> D1["veterans-extension"]
    D --> D2["veterans-autofill"]

    click C1 "./spotify-verify-tool/CLAUDE.md" "查看 Spotify 模块"
    click C2 "./youtube-verify-tool/CLAUDE.md" "查看 YouTube 模块"
    click C3 "./one-verify-tool/CLAUDE.md" "查看 Google One 模块"
    click C4 "./boltnew-verify-tool/CLAUDE.md" "查看 Bolt.new 模块"
    click C5 "./k12-verify-tool/CLAUDE.md" "查看 K12 模块"
    click C6 "./veterans-verify-tool/CLAUDE.md" "查看 Veterans 模块"
    click C7 "./perplexity-verify-tool/CLAUDE.md" "查看 Perplexity 模块"
    click C8 "./canva-teacher-tool/CLAUDE.md" "查看 Canva 模块"
    click D1 "./veterans-extension/CLAUDE.md" "查看 Veterans Extension"
    click D2 "./veterans-autofill/CLAUDE.md" "查看 Veterans Autofill"
    click F "./telegram-bot/CLAUDE.md" "查看 Telegram Bot"
```

---

## 模块索引

| 模块 | 类型 | 语言 | 验证模式 | 目标平台 | 入口 |
|------|------|------|----------|----------|------|
| [spotify-verify-tool](./spotify-verify-tool/) | CLI | Python | Student | Spotify Premium | main.py |
| [youtube-verify-tool](./youtube-verify-tool/) | CLI | Python | Student | YouTube Premium | main.py |
| [one-verify-tool](./one-verify-tool/) | CLI | Python | Student | Gemini Advanced | main.py |
| [boltnew-verify-tool](./boltnew-verify-tool/) | CLI | Python | Teacher | Bolt.new Pro | main.py |
| [k12-verify-tool](./k12-verify-tool/) | CLI | Python | K12 Teacher | ChatGPT Plus | main.py |
| [veterans-verify-tool](./veterans-verify-tool/) | CLI | Python | Military | ChatGPT Plus | main.py |
| [perplexity-verify-tool](./perplexity-verify-tool/) | CLI | Python | Student | Perplexity Pro | main.py |
| [canva-teacher-tool](./canva-teacher-tool/) | CLI | Python | Teacher | Canva Education | main.py |
| [telegram-bot](./telegram-bot/) | Bot | Python | All | Telegram 机器人 | main.py |
| [veterans-extension](./veterans-extension/) | Chrome MV3 | JavaScript | Military | ChatGPT Plus | background.js |
| [veterans-autofill](./veterans-autofill/) | Chrome MV3 | JavaScript | Military | ChatGPT Plus | content.js |

### 共享模块

| 模块 | 路径 | 职责 |
|------|------|------|
| anti_detect.py | ./anti_detect.py | HTTP 反检测：UA 轮换、TLS 指纹伪装、NewRelic 头生成 |

### 已废弃模块

| 模块 | 路径 | 原因 |
|------|------|------|
| _deprecated_auto-verify-tool | ./_deprecated_auto-verify-tool/ | 旧版 Node.js 实现，仅供参考 |

---

## 运行与开发

### 环境准备

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# [可选] 增强反检测
pip install curl_cffi cloudscraper
```

### 运行工具

```bash
# 进入工具目录并运行
cd spotify-verify-tool && python main.py "SHEERID_URL"

# 使用代理
python main.py "URL" --proxy http://user:pass@host:port

# 交互模式
python main.py
```

### 加载 Chrome 扩展

1. 打开 `chrome://extensions/`
2. 启用 **开发者模式**
3. 点击 **加载已解压的扩展程序**
4. 选择 `veterans-extension/` 或 `veterans-autofill/` 目录

### 语法检查

```bash
# 无自动化测试，使用编译检查
python -m compileall .
```

---

## 核心验证流程

所有 SheerID 工具遵循统一的五步 "瀑布式" 流程：

```
1. collectStudentPersonalInfo / collectTeacherPersonalInfo  - 提交身份信息
2. DELETE /step/sso                                         - 跳过学校 SSO 登录
3. docUpload                                                - 请求 S3 预签名 URL
4. PUT S3                                                   - 上传生成的证件图片
5. completeDocUpload                                        - 完成验证提交
```

### 验证类型对照

| 验证类型 | API 端点 | 年龄范围 | 文档类型 |
|----------|----------|----------|----------|
| Student | collectStudentPersonalInfo | 18-25 | 学生证/成绩单 |
| Teacher | collectTeacherPersonalInfo | 25-55 | 雇佣证明/教师证 |
| K12 | collectTeacherPersonalInfo | 25-55 | 教师工牌 |
| Military | collectInactiveMilitaryPersonalInfo | N/A | 无需文档 (DoD 数据库验证) |

---

## 反检测机制 (anti_detect.py)

### HTTP 库优先级

```
curl_cffi > cloudscraper > httpx > requests
```

自动降级：若高优先级库不可用，自动使用下一个。

### 核心功能

| 功能 | 描述 |
|------|------|
| **TLS 指纹伪装** | curl_cffi 模拟 Chrome JA3/JA4 指纹 |
| **UA 轮换** | 10+ 真实浏览器 User-Agent 字符串 |
| **NewRelic 头** | SheerID API 必需的追踪头 |
| **随机延迟** | 200-800ms 请求间隔避免限流 |
| **设备指纹** | MD5 生成的虚拟浏览器指纹 |

### 使用方法

```python
from anti_detect import get_headers, create_session, random_delay

session, lib_name = create_session(proxy="http://...")
headers = get_headers(for_sheerid=True)
random_delay()
```

---

## 测试策略

当前项目 **无自动化测试套件**。质量保证依赖：

1. 手动功能测试
2. 编译检查：`python -m compileall .`
3. 成功率追踪：各工具的 `stats.json` 文件

---

## 编码规范

| 规范项 | 要求 |
|--------|------|
| 入口文件 | `main.py` |
| CLI 工具目录 | `*-verify-tool/` |
| Chrome 扩展目录 | `*-extension/` 或 `*-autofill/` |
| 提交格式 | Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`) |
| 语言 | Python 3.8+ / JavaScript ES6+ |

---

## 依赖

### 必需

```
httpx       # 异步 HTTP 客户端
Pillow      # 图像生成
```

### 推荐

```
curl_cffi      # TLS 指纹伪装 (最佳反检测)
cloudscraper   # Cloudflare 绕过
```

### 可选

```
requests       # 备用 HTTP 客户端
pymupdf        # PDF 处理 (perplexity/canva 工具)
```

---

## AI 使用指引

### 理解项目时

1. 先读根 `CLAUDE.md` 了解全局架构
2. 进入具体模块时读取模块级 `CLAUDE.md`
3. 核心流程在 `anti_detect.py` 和各 `main.py` 中

### 修改代码时

1. 遵循现有代码风格
2. 保持 `anti_detect.py` 作为共享模块不被破坏
3. 新工具应遵循 `*-verify-tool/` 命名约定
4. 更新对应的 README.md

### 常见任务

| 任务 | 参考文件 |
|------|----------|
| 添加新大学 | 各工具的 `UNIVERSITIES` 列表 |
| 修改文档生成 | 各工具的 `generate_*` 函数 |
| 调整反检测 | `anti_detect.py` |
| 添加新平台 | 复制现有工具目录并修改 |

---

## 文档

| 文档 | 路径 | 描述 |
|------|------|------|
| 主 README | ./README.md | 项目介绍与快速开始 |
| 多语言文档 | ./docs/ | 16 种语言翻译 |
| 部署指南 | ./DEPLOYMENT.md | Docker 部署说明 |
| AI 代理指南 | ./AGENTS.md | 给 AI 工具的指引 |

---

## 文件结构

```
SheerID-Verification-Tool/
├── anti_detect.py              # 共享反检测模块
├── requirements.txt            # Python 依赖
├── CLAUDE.md                   # 本文件
├── README.md                   # 项目主文档
├── AGENTS.md                   # AI 代理指引
├── DEPLOYMENT.md               # 部署文档
├── Dockerfile                  # Docker 配置
├── docker-compose.yml          # Docker Compose
│
├── spotify-verify-tool/        # Spotify 学生验证
├── youtube-verify-tool/        # YouTube 学生验证
├── one-verify-tool/            # Google One 学生验证
├── boltnew-verify-tool/        # Bolt.new 教师验证
├── k12-verify-tool/            # K12 教师验证
├── veterans-verify-tool/       # 退伍军人验证
├── perplexity-verify-tool/     # Perplexity 学生验证
├── canva-teacher-tool/         # Canva 教师文档生成
│
├── veterans-extension/         # Chrome MV3 扩展 (完整功能)
├── veterans-autofill/          # Chrome MV3 扩展 (表单填充)
│
├── docs/                       # 多语言文档 (16 种)
├── _deprecated_auto-verify-tool/ # 废弃的 Node.js 版本
└── .claude/                    # Claude 索引数据
    └── index.json
```
