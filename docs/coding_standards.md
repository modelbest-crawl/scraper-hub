# 编码规范

## Python 版本

- 最低 Python 3.10

## 代码风格

- 使用 **ruff** 做 lint 和格式化
- 行宽上限 120 字符
- 提交前自动检查（pre-commit 已配置）

## 命名

- 文件名：`snake_case.py`
- 类名：`PascalCase`
- 函数/变量：`snake_case`
- 常量：`UPPER_SNAKE_CASE`

## 项目结构

每个爬虫项目必须包含：

```
项目名/
├── scraper.py          # 主入口，继承 BaseScraper
├── config.yaml         # 项目配置
├── requirements.txt    # 私有依赖
├── README.md           # 项目说明（含 frontmatter 元信息）
└── tests/
    ├── fixtures/       # 样本数据
    ├── test_parser.py  # 解析逻辑测试
    └── test_smoke.py   # 冒烟测试
```

## Commit 规范

```
格式：{类型}({范围}): {描述}

类型：feat / fix / refactor / docs / chore
范围：成员名/项目名 或 packages/模块名

示例：
  feat(zhangsan/douyin-video): 新增去水印功能
  fix(packages/http): 修复代理池连接泄漏
```

## 配置规范

- 每个项目的 `config.yaml` 必须包含 `compliance` 字段
- `rate_limit` 不得超过 10 req/s
- `personal_data` 为 true 时需要 Lead 审批

## 测试规范

- 解析逻辑（parse）必须有单元测试
- 测试数据放 `tests/fixtures/`，需脱敏
- 冒烟测试标记 `@pytest.mark.smoke`

## 敏感信息

- API Key、Token、Cookie、密码 → **绝不提交到 Git**
- 使用 `.env` 文件管理，已在 `.gitignore` 中排除
