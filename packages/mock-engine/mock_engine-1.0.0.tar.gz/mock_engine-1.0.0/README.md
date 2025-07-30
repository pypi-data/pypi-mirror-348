# Mock Engine

Mock Engine 是一个强大的 Python 模拟执行引擎，提供了模板渲染和代码执行功能，支持调试模式，帮助开发者更好地理解和调试代码执行过程。

## 功能特点

- 模板引擎：支持变量替换和自定义方法
- 代码引擎：支持 SQL 查询和上下文变量
- 调试模式：详细的执行日志和调试信息
- 数据库支持：内置 SQL 查询功能
- 上下文管理：支持变量传递和共享

## 安装

```bash
pip install mock-engine
```

## 快速开始

### 模板引擎示例

```python
from mock_engine.core.template_engine import TemplateEngine

# 创建引擎实例
engine = TemplateEngine(debug=True)

# 创建模板
template = {
    "name": "{{name}}",
    "age": "{{age}}"
}

# 创建请求数据
request = {
    "name": "张三",
    "age": 25
}

# 生成数据
result, debug_output = engine.generate(template, request)
```

### 代码引擎示例

```python
from mock_engine.core.code_engine import CodeEngine

# 创建引擎实例
engine = CodeEngine(debug=True)

# 数据库配置
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123456',
    'port': 3306,
    'database': 'webtest'
}

# 执行代码
code = f"""
result = sql("SELECT * FROM webtest.t_ui_user LIMIT 1", db_config={db_config})
print("查询结果:", result)
"""

result = engine.execute(code)
```

## 文档

- [调试模式使用文档](docs/debug_mode.md)
- [API 文档](docs/api.md)

## 开发

### 环境设置

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/mock-engine.git
cd mock-engine
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

### 运行测试

```bash
python -m unittest discover tests
```

## 贡献

欢迎提交 Pull Request 或创建 Issue。

## 许可证

MIT License
# mock_engine
