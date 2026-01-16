[根目录](../CLAUDE.md) > **youtube-verify-tool**

# YouTube 学生验证工具

## 模块职责

自动化 YouTube Premium 学生折扣的 SheerID 验证流程。

## 入口与启动

```bash
python main.py "https://services.sheerid.com/verify/...?verificationId=abc123"
```

## 对外接口

### 主要类

| 类名 | 职责 |
|------|------|
| `YouTubeVerifier` | 核心验证逻辑 |
| `Stats` | 成功率追踪 |

## 关键依赖与配置

- `httpx`, `Pillow`, `anti_detect` (可选)

### 大学列表特点

专注亚洲地区大学 (越南、印度、印尼、泰国、菲律宾)，YouTube Premium 在这些地区完全支持。

| 地区 | 数量 |
|------|------|
| 越南 | 15 |
| 印度 | 15 |
| 印尼 | 10 |
| 泰国 | 8 |
| 菲律宾 | 8 |
| 美国 | 10 |
| 其他 | 15+ |

## 与 Spotify 工具的区别

代码结构几乎相同，区别在于：
- 品牌显示为 YouTube
- 大学列表侧重不同地区

## 相关文件清单

| 文件 | 描述 |
|------|------|
| `main.py` | 主程序 |
| `README.md` | 说明文档 |

## 变更记录

| 日期 | 变更 |
|------|------|
| 2026-01-15 | 创建模块级 CLAUDE.md |
