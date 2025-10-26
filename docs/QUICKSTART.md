# 快速开始指南

本指南将帮助你在5分钟内创建第一个MCP服务器。

## 安装

```bash
# 1. 克隆或下载项目
cd d:\mcp-generator

# 2. 安装依赖
pip install -r requirements.txt

# 3. 安装CLI工具
pip install -e .
```

## 创建第一个MCP服务器

### 步骤1：生成示例配置

```bash
mcp-gen init -o my-first-api.yaml
```

这会创建一个示例配置文件`my-first-api.yaml`。

### 步骤2：查看配置

打开`my-first-api.yaml`，你会看到：

```yaml
server:
  name: "example-api"
  version: "1.0.0"
  description: "Example API MCP Server"
  base_url: "https://api.example.com"
  timeout: 30
  authentication:
    type: "bearer"
    description: "Bearer token authentication"

tools:
  - name: "get_user"
    description: "Get user information by ID"
    endpoint: "/users/{user_id}"
    method: "GET"
    parameters:
      - name: "user_id"
        type: "string"
        location: "path"
        description: "User ID"
        required: true
  # ... 更多工具
```

### 步骤3：验证配置

```bash
mcp-gen validate my-first-api.yaml
```

如果配置正确，你会看到：
```
✓ Configuration parsed successfully
✓ Configuration validated successfully
```

### 步骤4：预览生成的代码

```bash
mcp-gen preview my-first-api.yaml
```

这会显示将要生成的服务器代码。

### 步骤5：生成服务器代码

```bash
mcp-gen generate my-first-api.yaml -o ./my-first-server
```

成功后你会看到：
```
✓ Code generated successfully!

Output directory: D:\mcp-generator\my-first-server

Next steps:
1. cd my-first-server
2. pip install -r requirements.txt
3. python server.py
```

### 步骤6：测试服务器（使用真实API）

让我们用一个真实的公开API测试。创建`jsonplaceholder.yaml`：

```yaml
server:
  name: "jsonplaceholder-api"
  version: "1.0.0"
  description: "MCP Server for JSONPlaceholder API"
  base_url: "https://jsonplaceholder.typicode.com"
  timeout: 30

tools:
  - name: "get_post"
    description: "Get a specific post by ID"
    endpoint: "/posts/{post_id}"
    method: "GET"
    parameters:
      - name: "post_id"
        type: "integer"
        location: "path"
        description: "Post ID"
        required: true
```

生成并运行：

```bash
# 生成代码
mcp-gen generate jsonplaceholder.yaml -o ./jsonplaceholder-server

# 进入目录
cd jsonplaceholder-server

# 安装依赖
pip install -r requirements.txt

# 运行服务器
python server.py
```

## 使用现有示例

项目提供了多个现成的示例：

### JSONPlaceholder API（无需认证）

```bash
mcp-gen generate examples/basic-api.yaml -o ./test-server
cd test-server
pip install -r requirements.txt
python server.py
```

### GitHub API（需要Token）

```bash
# 生成服务器
mcp-gen generate examples/github-api.yaml -o ./github-server

# 设置你的GitHub Token
set API_AUTH_TOKEN=ghp_your_token_here

# 运行服务器
cd github-server
pip install -r requirements.txt
python server.py
```

### Weather API（需要API Key）

```bash
# 生成服务器
mcp-gen generate examples/weather-api.yaml -o ./weather-server

# 设置你的Weather API Key
set API_AUTH_TOKEN=your_weather_api_key

# 运行服务器
cd weather-server
pip install -r requirements.txt
python server.py
```

## 与Claude Desktop集成

生成的服务器可以直接与Claude Desktop集成。

1. 找到Claude Desktop配置文件：
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. 添加服务器配置：

```json
{
  "mcpServers": {
    "my-first-server": {
      "command": "python",
      "args": ["D:\\mcp-generator\\my-first-server\\server.py"]
    },
    "github-api": {
      "command": "python",
      "args": ["D:\\mcp-generator\\github-server\\server.py"],
      "env": {
        "API_AUTH_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

3. 重启Claude Desktop

4. 现在你可以在Claude中使用这些工具了！

## 下一步

- 📖 阅读完整文档：`README.md`
- 🔧 修改配置文件来适配你自己的API
- 🎯 探索更多示例：`examples/` 目录
- 🧪 运行测试：`pytest tests/`
- 🤝 贡献代码或报告问题

## 常见问题

### Q: 如何添加认证？

A: 在配置文件的`server`部分添加`authentication`：

```yaml
server:
  # ... 其他配置
  authentication:
    type: "bearer"  # 或 "apikey"
    description: "Your API token"
```

对于API Key认证：
```yaml
authentication:
  type: "apikey"
  location: "header"  # 或 "query"
  name: "X-API-Key"   # Header或Query参数名
```

### Q: 服务器无法启动？

检查：
1. 是否安装了所有依赖：`pip install -r requirements.txt`
2. Python版本是否>=3.9
3. 配置文件格式是否正确
4. 如果需要认证，是否设置了环境变量

### Q: 如何调试？

在生成的`server.py`中，日志级别默认为INFO。修改为DEBUG获取更多信息：

```python
logging.basicConfig(level=logging.DEBUG)
```

### Q: 可以修改生成的代码吗？

当然可以！生成的代码是标准Python代码，你可以自由修改。但建议：
1. 保留原始配置文件
2. 在生成代码基础上修改
3. 版本控制你的修改

## 需要帮助？

- 查看完整文档：`README.md`
- 提交Issue：[GitHub Issues](https://github.com/yourusername/mcp-generator/issues)
- 查看MCP文档：[modelcontextprotocol.io](https://modelcontextprotocol.io)
