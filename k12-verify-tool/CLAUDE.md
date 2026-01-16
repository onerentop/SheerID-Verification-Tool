[根目录](../CLAUDE.md) > **k12-verify-tool**

# K12 教师验证工具

## 模块职责

自动化 ChatGPT Plus K12 教师折扣的 SheerID 验证流程。专门针对美国 K-12 高中教师。

## 入口与启动

```bash
python main.py "URL"
python main.py "URL" --proxy http://...
```

## 对外接口

### 主要类

| 类名 | 职责 |
|------|------|
| `K12Verifier` | 核心验证逻辑 |

## 关键配置

| 常量 | 值 |
|------|-----|
| `PROGRAM_ID` | `68d47554aa292d20b9bec8f7` |

## 特殊逻辑

### 自动通过检测

K12 验证经常 **无需上传文档** 即可自动通过：

```python
if current_step == "success":
    # 自动通过！无需文档上传
```

### emailLoop 处理

若遇到 `emailLoop` 状态，需要获取新验证链接重试。

## 学校数据库

包含 40+ 所美国精英高中：

| 分类 | 示例 |
|------|------|
| NYC 特殊高中 | Stuyvesant, Bronx Science |
| 芝加哥精选 | Payton Prep, Whitney Young |
| 弗吉尼亚/DC STEM | Thomas Jefferson |
| 加州精英 | Whitney, Lowell |
| BASIS 特许 | Scottsdale, Tucson North |

## 相关文件清单

| 文件 | 描述 |
|------|------|
| `main.py` | 主程序 |
| `README.md` | 说明文档 |

## 变更记录

| 日期 | 变更 |
|------|------|
| 2026-01-15 | 创建模块级 CLAUDE.md |
