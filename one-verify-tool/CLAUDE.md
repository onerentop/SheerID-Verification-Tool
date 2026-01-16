[根目录](../CLAUDE.md) > **one-verify-tool**

# Google One (Gemini) 学生验证工具

## 模块职责

自动化 Google One AI Premium (Gemini Advanced) 学生折扣的 SheerID 验证流程。

## 入口与启动

```bash
python main.py "URL"
python main.py "URL" --proxy http://...
```

## 对外接口

### 主要类

| 类名 | 职责 |
|------|------|
| `GeminiVerifier` | 核心验证逻辑 |
| `Stats` | 成功率追踪 |

## 关键依赖与配置

### 重要说明

截至 2026年1月，Gemini 学生验证 **仅限美国大学**。其他国家可能对现有用户有效，但新注册受限。

### 大学列表

| 地区 | 数量 | 权重范围 |
|------|------|----------|
| 美国 (高优先) | 35+ | 84-100 |
| 其他国家 | 10 | 15-40 (低权重) |

## 文档生成

支持两种文档类型：
1. **成绩单** (70% 概率) - `generate_transcript()`
2. **学生证** (30% 概率) - `generate_student_id()`

## 相关文件清单

| 文件 | 描述 |
|------|------|
| `main.py` | 主程序 |
| `stats.json` | 成功率统计 |
| `README.md` | 说明文档 |

## 变更记录

| 日期 | 变更 |
|------|------|
| 2026-01-15 | 创建模块级 CLAUDE.md |
