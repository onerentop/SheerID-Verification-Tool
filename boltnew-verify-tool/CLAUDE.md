[根目录](../CLAUDE.md) > **boltnew-verify-tool**

# Bolt.new 教师验证工具

## 模块职责

自动化 Bolt.new 教师折扣的 SheerID **教师验证**流程。

## 入口与启动

```bash
python main.py "https://services.sheerid.com/verify/...?verificationId=abc123"
```

## 对外接口

### 主要类

| 类名 | 职责 |
|------|------|
| `BoltnewVerifier` | 核心验证逻辑 |

## 与学生验证的区别

| 方面 | 学生验证 | 教师验证 |
|------|----------|----------|
| API 端点 | `collectStudentPersonalInfo` | `collectTeacherPersonalInfo` |
| 年龄范围 | 18-25 | 25-55 |
| 文档类型 | 学生证 | 雇佣证明 |

## 关键配置

| 常量 | 值 |
|------|-----|
| `PROGRAM_ID` | `68cc6a2e64f55220de204448` |

## 文档生成

`generate_teacher_document()` 生成教师雇佣证明，包含：
- 学校名称
- 教师姓名
- 职位: Faculty Member
- 部门: Education
- 签发日期

## 相关文件清单

| 文件 | 描述 |
|------|------|
| `main.py` | 主程序 |
| `README.md` | 说明文档 |

## 变更记录

| 日期 | 变更 |
|------|------|
| 2026-01-15 | 创建模块级 CLAUDE.md |
