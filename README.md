# MCP Generator

**快速生成MCP服务器代码，连接AI与HTTP后端**

MCP Generator 是一个代码生成工具，帮助开发者快速创建 [Model Context Protocol (MCP)](https://modelcontextprotocol.io) 服务器。通过简单的配置文件，自动生成完整的、可直接运行的MCP服务器代码，让AI代理能够安全、可靠地与各类HTTP后端API交互。

## ✨ 特性

- 🚀 **快速生成** - 从配置到代码，几秒钟完成
- 📝 **简单配置** - 使用YAML/JSON描述API，无需编写代码
- 🔒 **安全可靠** - 支持多种认证方式（Bearer Token、API Key、Basic Auth）
- 🎯 **类型安全** - 基于Pydantic的配置验证
- 📦 **开箱即用** - 生成的代码包含完整依赖和文档
- 🛠️ **CLI工具** - 友好的命令行界面，支持验证、预览、生成

## 📦 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/mcp-generator.git
cd mcp-generator

# 安装依赖
pip install -r requirements.txt

# 安装为命令行工具
pip install -e .
```

## 🚀 快速开始

### 1. 创建配置文件

```bash
mcp-gen init -o my-api-config.yaml
```

### 2. 编辑配置文件

```yaml
server:
  name: "my-api"
  version: "1.0.0"
  description: "My API MCP Server"
  base_url: "https://api.example.com"
  timeout: 30

tools:
  - name: "get_user"
    description: "Get user information"
    endpoint: "/users/{user_id}"
    method: "GET"
    parameters:
      - name: "user_id"
        type: "string"
        location: "path"
        description: "User ID"
        required: true
```

### 3. 生成服务器代码

```bash
mcp-gen generate my-api-config.yaml -o ./output
```

### 4. 运行服务器

```bash
cd output
pip install -r requirements.txt
python server.py
```

## 📖 使用说明

### 命令行工具

MCP Generator 提供以下命令：

#### 生成代码

```bash
mcp-gen generate <config-file> [-o <output-dir>]
```

从配置文件生成MCP服务器代码。

选项：
- `-o, --output` - 输出目录（默认：`./generated`）
- `--validate-only` - 仅验证配置，不生成代码

#### 验证配置

```bash
mcp-gen validate <config-file>
```

验证配置文件的正确性。

#### 预览代码

```bash
mcp-gen preview <config-file> [--template <template-name>]
```

预览生成的代码，不写入磁盘。

选项：
- `--template` - 要预览的模板（`server`, `readme`, `requirements`）

#### 初始化配置

```bash
mcp-gen init [-o <output-file>]
```

创建示例配置文件。

### 配置文件格式

#### 服务器配置

```yaml
server:
  name: string              # 服务器名称（必需）
  version: string           # 版本号（默认：1.0.0）
  description: string       # 服务器描述（可选）
  base_url: string          # API基础URL（必需）
  timeout: integer          # 请求超时时间（默认：30秒）
  authentication:           # 认证配置（可选）
    type: string            # 认证类型：bearer, apikey, basic
    location: string        # API Key位置：header, query（仅apikey类型）
    name: string            # Header/Query参数名（仅apikey类型）
    description: string     # 认证说明
```

#### 工具配置

```yaml
tools:
  - name: string            # 工具名称（必需，需为有效Python标识符）
    description: string     # 工具描述（必需）
    endpoint: string        # API端点路径（必需，可包含{param}占位符）
    method: string          # HTTP方法：GET, POST, PUT, PATCH, DELETE
    parameters:             # 参数列表
      - name: string        # 参数名称
        type: string        # 参数类型：string, integer, number, boolean, array, object
        location: string    # 参数位置：path, query, header, body
        description: string # 参数描述（可选）
        required: boolean   # 是否必需（默认：false）
        default: any        # 默认值（可选）
        items_type: string  # 数组元素类型（仅array类型）
        properties: object  # 对象属性（仅object类型）
```

## 📚 示例

项目提供了多个示例配置文件：

### JSONPlaceholder API

```bash
mcp-gen generate examples/basic-api.yaml -o ./jsonplaceholder-server
```

### GitHub API

```bash
mcp-gen generate examples/github-api.yaml -o ./github-server
```

需要设置环境变量：
```bash
export API_AUTH_TOKEN="your-github-token"
```

### Weather API

```bash
mcp-gen generate examples/weather-api.yaml -o ./weather-server
```

需要设置环境变量：
```bash
export API_AUTH_TOKEN="your-weather-api-key"
```

## 🏗️ 项目结构

```
mcp-generator/
├── src/
│   └── mcp_generator/
│       ├── models.py           # 数据模型
│       ├── parser/             # 配置解析器
│       ├── validator/          # 配置验证器
│       ├── generator/          # 代码生成器
│       ├── templates/          # Jinja2模板
│       └── cli/                # 命令行工具
├── examples/                   # 示例配置文件
├── tests/                      # 测试代码
└── docs/                       # 文档
```

## 🤝 贡献

欢迎贡献！请随时提交Issues或Pull Requests。

## 📄 许可证

MIT License

## 🔗 相关链接

- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

## ❓ 常见问题

### 生成的服务器如何使用？

生成的服务器是一个标准的MCP服务器，可以与Claude Desktop或其他MCP客户端配合使用。在Claude Desktop的配置文件中添加：

```json
{
  "mcpServers": {
    "my-api": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "API_AUTH_TOKEN": "your-token"
      }
    }
  }
}
```

### 支持哪些认证方式？

目前支持：
- **Bearer Token** - Authorization: Bearer {token}
- **API Key** - 自定义Header或Query参数
- **Basic Auth** - 未来版本支持

### 如何添加自定义请求逻辑？

生成的代码是标准Python代码，你可以直接修改`server.py`文件来添加自定义逻辑，如：
- 自定义请求头
- 请求/响应处理
- 错误处理
- 日志记录

### 性能如何？

生成的服务器使用`httpx`异步HTTP客户端，性能优秀。单个服务器可以处理大量并发请求。