[根目录](../CLAUDE.md) > **spotify-verify-tool**

# Spotify 学生验证工具

## 模块职责

自动化 Spotify Premium 学生折扣的 SheerID 验证流程。

## 入口与启动

```bash
# 带 URL 参数
python main.py "https://services.sheerid.com/verify/...?verificationId=abc123"

# 使用代理
python main.py "URL" --proxy http://user:pass@host:port

# 交互模式
python main.py
```

## 对外接口

### CLI 参数

| 参数 | 必需 | 描述 |
|------|------|------|
| `url` | 可选 | SheerID 验证 URL (不提供则进入交互模式) |
| `--proxy` | 可选 | 代理服务器地址 |

### 主要类

| 类名 | 职责 |
|------|------|
| `SpotifyVerifier` | 核心验证逻辑 |
| `Stats` | 成功率追踪 |

## 关键依赖与配置

### 依赖

- `httpx` - HTTP 客户端
- `Pillow` - 学生证图片生成
- `anti_detect` (可选) - 反检测模块

### 配置常量

| 常量 | 值 | 描述 |
|------|-----|------|
| `PROGRAM_ID` | `67c8c14f5f17a83b745e3f82` | Spotify SheerID 程序 ID |
| `MIN_DELAY` | 300ms | 最小请求延迟 |
| `MAX_DELAY` | 800ms | 最大请求延迟 |

## 数据模型

### 大学列表 (UNIVERSITIES)

包含 60+ 所全球大学，按权重选择：

| 地区 | 数量 | 权重范围 |
|------|------|----------|
| 美国 | 15 | 88-100 |
| 加拿大 | 5 | 82-88 |
| 英国 | 8 | 79-88 |
| 德国 | 6 | 79-85 |
| 法国 | 5 | 78-82 |
| 澳大利亚 | 6 | 79-85 |
| 日本 | 5 | 78-83 |
| 巴西 | 5 | 76-82 |
| 印尼 | 5 | 77-82 |
| 其他 | 10+ | 77-85 |

### 验证流程

```
1. check_link()      - 检查 URL 有效性
2. generate_name()   - 生成随机姓名
3. select_university() - 加权选择大学
4. generate_student_id() - 生成学生证图片
5. verify()          - 执行 5 步验证流程
```

## 测试与质量

- 无自动化测试
- 成功率追踪在 `stats.json`
- 编译检查: `python -m compileall main.py`

## 常见问题 (FAQ)

### Q: 遇到 `fraudRulesReject` 错误？

A: 使用住宅代理，等待 5-10 分钟后重试。

### Q: 如何添加新大学？

A: 在 `UNIVERSITIES` 列表中添加新条目：
```python
{"id": 12345, "name": "大学名称", "domain": "example.edu", "weight": 80}
```

### Q: 验证成功后需要等多久？

A: 通常 24-48 小时人工审核。

## 相关文件清单

| 文件 | 描述 |
|------|------|
| `main.py` | 主程序入口 |
| `stats.json` | 成功率统计 (运行时生成) |
| `README.md` | 模块说明文档 |

## 变更记录

| 日期 | 变更 |
|------|------|
| 2026-01-15 | 创建模块级 CLAUDE.md |
