[根目录](../CLAUDE.md) > **canva-teacher-tool**

# Canva 教师文档生成工具

## 模块职责

为 Canva Education 教师验证生成英国教师文档。

**重要：此工具不使用 SheerID**，Canva 使用 Goodstack 进行验证，需要手动上传文档。

## 入口与启动

```bash
# 生成所有文档
python main.py

# 生成特定文档
python main.py -d teacher_id
python main.py -d employment_letter

# 自定义教师信息
python main.py --name "John Smith" --school "Eton College" --position "Head of Mathematics"

# 列出可用学校
python main.py --list-schools
```

## 对外接口

### CLI 参数

| 参数 | 描述 |
|------|------|
| `-d, --document` | 文档类型: `teacher_id`, `employment_letter`, `teaching_license` |
| `--name` | 教师姓名 |
| `--school` | 学校名称 |
| `--position` | 职位 |
| `--list-schools` | 列出所有可用学校 |

### 主要类

| 类名 | 职责 |
|------|------|
| `UKSchoolDatabase` | 英国学校数据库管理 |
| 文档生成函数 | 各种教师文档生成 |

## 验证工作流 (手动)

1. 访问 canva.com/education -> 点击 "Get Verified"
2. 选择国家: **United Kingdom**
3. 输入学校邮箱或勾选 "I don't have a school email"
4. 输入学校位置和名称
5. **上传文档 1**: 教师 ID (teacher_id)
6. **上传文档 2**: 教学许可 (employment_letter)
7. 等待 24-48 小时审核

## 生成的文档

| 文档 | 文件名 | 用途 |
|------|--------|------|
| Employment Letter | `employment_letter_*.png` | Teaching licence |
| Teacher ID Card | `teacher_id_*.png` | Teaching ID |
| Teaching License | `teaching_license_*.png` | Teaching licence (备选) |

## 英国学校数据库

包含 10+ 所英国知名学校：

| 学校 | 城市 |
|------|------|
| Leeds Grammar School | Leeds |
| Manchester Grammar School | Manchester |
| Eton College | Windsor |
| Harrow School | Harrow |
| Westminster School | London |

## 关键依赖

- `PyMuPDF` (fitz) - PDF 处理
- `Pillow` - 图像生成

## 文件结构

```
canva-teacher-tool/
├── main.py
├── assets/
│   └── templates/     # 文档模板
├── data/
│   └── uk_schools.json  # 学校数据库
├── output/            # 生成的文档
└── README.md
```

## 相关文件清单

| 文件 | 描述 |
|------|------|
| `main.py` | 主程序 |
| `assets/templates/` | PDF 模板 |
| `data/uk_schools.json` | 学校数据 |
| `output/` | 输出目录 |
| `README.md` | 说明文档 |

## 变更记录

| 日期 | 变更 |
|------|------|
| 2026-01-15 | 创建模块级 CLAUDE.md |
