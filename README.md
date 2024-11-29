# GitLab工作报告生成器

一个用于生成GitLab提交记录报告的Python工具，可以快速生成指定时间范围内的工作进展报告。

## 功能特点

- 自动获取GitLab提交记录
- 按项目和分支分组展示
- 支持查看提交详情和文件对比
- 配置信息本地持久化
- 生成Markdown格式报告
- 支持自定义时间范围

## 安装说明

1. 克隆仓库：
```bash
git clone https://github.com/Xing0317/gitlab-report-generator.git
cd gitlab-report-generator
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 首次运行时，需要配置GitLab服务器信息：
   - GitLab服务器地址
   - Private Token（可以从GitLab个人设置页面获取）

2. 运行程序：
```bash
python -m src.main
```

3. 按提示操作：
   - 选择是否使用已保存的GitLab配置
   - 选择是否需要生成提交详情和对比链接
   - 等待报告生成

4. 查看生成的报告文件（格式：gitlab_report_YYYYMMDD_HHMMSS.md）

## 配置说明

- 配置文件位置：`~/.gitlab_report_config.json`
- 配置文件格式：
```json
{
  "gitlab": {
    "base_url": "http://your-gitlab-server",
    "private_token": "your-private-token"
  }
}
```

## 报告格式

生成的报告包含以下信息：
- 时间范围
- 项目名称
- 分支信息
- 提交记录
  - 提交时间
  - 提交说明
  - 提交详情链接（可选）
  - 文件对比链接（可选）

示例：
```markdown
# 工作进展报告

## 时间范围
2024-11-21 至 2024-11-30

## 项目：project-name

### 分支：feature/branch

- 总提交数：5

#### 提交记录：

##### 2024-11-22 03:03 - [fix]:修复某功能
- [查看提交详情](http://gitlab-server/path/to/commit)
- [查看文件对比](http://gitlab-server/path/to/compare)
```

## 项目结构

```
gitlab-report-generator/
├── src/
│   ├── __init__.py
│   ├── models.py      # 数据模型
│   ├── api_client.py  # GitLab API客户端
│   ├── config.py      # 配置管理
│   └── main.py        # 主程序
└── requirements.txt    # 项目依赖
```

## 依赖说明

- Python 3.9+
- requests==2.31.0
- pydantic==2.6.1
- python-dateutil==2.8.2

## 注意事项

1. 确保有足够的GitLab API访问权限
2. Private Token需要具有读取权限
3. 首次运行需要配置GitLab信息
4. 生成的报告默认保存在当前目录
5. 配置文件会保存在用户主目录下

## 贡献指南

欢迎提交Issue和Pull Request来改进这个项目。在提交PR之前，请确保：
1. 代码符合Python代码规范
2. 添加了必要的注释和文档
3. 所有测试通过

## 许可证

MIT License

## 作者

LuHeng

## 更新日志

### v1.0.0 (2024-03-15)
- 初始版本发布
- 实现基本的GitLab提交记录获取功能
- 支持按项目和分支分组显示
- 添加配置持久化功能
- 支持生成Markdown格式报告
- 支持可选的提交详情和对比链接