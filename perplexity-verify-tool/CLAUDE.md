[根目录](../CLAUDE.md) > **perplexity-verify-tool**

# Perplexity 学生验证工具

## 模块职责

自动化 Perplexity Pro 学生折扣的 SheerID 验证流程，专门针对荷兰格罗宁根大学绕过策略。

## 入口与启动

```bash
python main.py
python main.py "https://services.sheerid.com/verify/...?verificationId=..."
```

## 对外接口

### 主要类

| 类名 | 职责 |
|------|------|
| `PerplexityVerifier` | 核心验证逻辑 |
| `Stats` | 成功率追踪 (按大学统计) |

## 特殊功能

### 格罗宁根大学绕过

此工具专门针对 **荷兰 University of Groningen** 优化：

1. **必须使用荷兰 IP** - VPN 或代理切换到荷兰
2. **PDF 文档生成** - 使用 PyMuPDF 生成高质量学费发票
3. **模板系统** - 从 `assets/docs.pdf` 读取基础模板

### 成功率追踪

`Stats` 类按大学追踪成功率并保存到 `stats.json`：

```python
stats.record("University of Groningen", success=True)
rate = stats.get_rate("University of Groningen")  # 返回百分比
```

## 关键依赖

- `httpx`, `Pillow`
- `PyMuPDF` (fitz) - PDF 处理
- `anti_detect` (可选)

## 文件结构

```
perplexity-verify-tool/
├── main.py
├── stats.json        # 成功率统计
├── assets/
│   ├── docs.pdf      # 学费发票模板
│   ├── groningen_logo.png  # 备用 Logo
│   └── signature.png       # 备用签名
└── README.md
```

## 相关文件清单

| 文件 | 描述 |
|------|------|
| `main.py` | 主程序 |
| `stats.json` | 成功率统计 |
| `assets/` | 模板资源目录 |
| `README.md` | 说明文档 |

## 变更记录

| 日期 | 变更 |
|------|------|
| 2026-01-15 | 创建模块级 CLAUDE.md |
