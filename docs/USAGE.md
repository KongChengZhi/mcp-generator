# MCP Generator 使用指南

## 快速命令参考

### 基础命令

```bash
# 查看帮助
mcp-gen --help

# 查看版本
mcp-gen --version

# 创建示例配置
mcp-gen init -o config.yaml

# 验证配置
mcp-gen validate config.yaml

# 预览生成的代码
mcp-gen preview config.yaml

# 生成服务器代码
mcp-gen generate config.yaml -o ./output
```

## 本地直接使用与全局注册

- **在项目根目录直接使用（无需安装）**

```cmd
./mcp-gen.bat --help
./mcp-gen.bat init -o config.yaml
./mcp-gen.bat generate config.yaml -o out
```

- **通过模块入口使用（无需 PATH）**

```cmd
python -m mcp_generator --help
python -m mcp_generator init -o config.yaml
python -m mcp_generator generate config.yaml -o out
```

- **全局注册（把项目根目录加入 PATH）**

```cmd
scripts\register-mcp-gen-global.bat
REM 重开一个新的终端窗口后生效
mcp-gen --help
```

- **经典安装方式（需保证用户级 Scripts 在 PATH 中）**

```cmd
pip install -e .
REM 如提示 mcp-gen 不在 PATH：
setx PATH "%PATH%;%APPDATA%\Python\Python312\Scripts"
REM 重开终端
mcp-gen --help
```

## 完整工作流程

### 1. 准备工作

确保已安装项目：
```bash
cd d:\mcp-generator
pip install -e .
```

### 2. 创建配置文件

**方法A：从模板开始**
```bash
mcp-gen init -o my-api.yaml
```

**方法B：使用示例**
```bash
# 复制并修改示例
copy examples\basic-api.yaml my-api.yaml
```

**方法C：手动创建**
创建 `my-api.yaml`:
```yaml
server:
  name: "my-api"
  version: "1.0.0"
  description: "My API MCP Server"
  base_url: "https://api.example.com"
  timeout: 30

tools:
  - name: "my_tool"
    description: "Tool description"
    endpoint: "/endpoint"
    method: "GET"
    parameters: []
```

### 3. 验证配置

```bash
mcp-gen validate my-api.yaml
```

如果有错误，会显示详细信息：
```
✗ Validation failed with the following errors:
  • Tool name 'my-tool' is not a valid Python identifier
  • Parameter 'user_id' in endpoint is not defined in parameters
```

### 4. 预览代码

```bash
# 预览服务器代码
mcp-gen preview my-api.yaml

# 预览README
mcp-gen preview my-api.yaml --template readme

# 预览依赖文件
mcp-gen preview my-api.yaml --template requirements
```

### 5. 生成代码

```bash
mcp-gen generate my-api.yaml -o ./my-server
```

成功后会显示：
```
✓ Code generated successfully!

Output directory: D:\mcp-generator\my-server

Next steps:
1. cd my-server
2. pip install -r requirements.txt
3. python server.py
```

### 6. 测试服务器

```bash
cd my-server
pip install -r requirements.txt
python server.py
```

服务器启动后会显示：
```
INFO Starting jsonplaceholder-api v1.0.0
INFO Target API: https://jsonplaceholder.typicode.com
```

## 配置文件详解

### 服务器配置

```yaml
server:
  name: "api-name"              # 必需：服务器名称
  version: "1.0.0"              # 可选：版本号（默认1.0.0）
  description: "描述"            # 可选：服务器描述
  base_url: "https://api.com"   # 必需：API基础URL
  timeout: 30                   # 可选：超时时间（默认30秒）
```

### 认证配置

**Bearer Token 认证**
```yaml
server:
  # ... 其他配置
  authentication:
    type: "bearer"
    description: "需要Bearer Token"
```

使用时设置环境变量：
```bash
set API_AUTH_TOKEN=your_bearer_token
```

**API Key 认证（Header方式）**
```yaml
server:
  # ... 其他配置
  authentication:
    type: "apikey"
    location: "header"
    name: "X-API-Key"
    description: "API Key in header"
```

**API Key 认证（Query方式）**
```yaml
server:
  # ... 其他配置
  authentication:
    type: "apikey"
    location: "query"
    name: "api_key"
    description: "API Key in query"
```

### 工具配置

**基础GET请求**
```yaml
tools:
  - name: "get_user"
    description: "获取用户信息"
    endpoint: "/users/{user_id}"
    method: "GET"
    parameters:
      - name: "user_id"
        type: "string"
        location: "path"
        description: "用户ID"
        required: true
```

**带查询参数的GET请求**
```yaml
tools:
  - name: "search_users"
    description: "搜索用户"
    endpoint: "/users"
    method: "GET"
    parameters:
      - name: "q"
        type: "string"
        location: "query"
        description: "搜索关键词"
        required: true
      - name: "limit"
        type: "integer"
        location: "query"
        description: "结果数量"
        required: false
        default: 10
```

**POST请求**
```yaml
tools:
  - name: "create_user"
    description: "创建用户"
    endpoint: "/users"
    method: "POST"
    parameters:
      - name: "name"
        type: "string"
        location: "body"
        description: "用户名"
        required: true
      - name: "email"
        type: "string"
        location: "body"
        description: "邮箱"
        required: true
```

**带数组参数**
```yaml
tools:
  - name: "create_post"
    description: "创建文章"
    endpoint: "/posts"
    method: "POST"
    parameters:
      - name: "tags"
        type: "array"
        location: "body"
        description: "标签列表"
        items_type: "string"
        required: false
```

**带自定义Header**
```yaml
tools:
  - name: "custom_request"
    description: "自定义请求"
    endpoint: "/endpoint"
    method: "GET"
    parameters:
      - name: "X-Custom-Header"
        type: "string"
        location: "header"
        description: "自定义Header"
        required: false
```

## 参数类型详解

### 支持的类型

1. **string** - 字符串
2. **integer** - 整数
3. **number** - 数字（包括小数）
4. **boolean** - 布尔值
5. **array** - 数组（需指定items_type）
6. **object** - 对象（需指定properties）

### 参数位置

1. **path** - URL路径参数（如 `/users/{id}`）
2. **query** - URL查询参数（如 `?key=value`）
3. **header** - HTTP请求头
4. **body** - 请求体（JSON）

## 实战示例

### 示例1：公开API（无认证）

配置文件 `public-api.yaml`:
```yaml
server:
  name: "public-api"
  base_url: "https://jsonplaceholder.typicode.com"

tools:
  - name: "list_posts"
    description: "获取文章列表"
    endpoint: "/posts"
    method: "GET"
    parameters: []
```

生成并运行：
```bash
mcp-gen generate public-api.yaml -o ./public-server
cd public-server
pip install -r requirements.txt
python server.py
```

### 示例2：需要认证的API

配置文件 `auth-api.yaml`:
```yaml
server:
  name: "auth-api"
  base_url: "https://api.github.com"
  authentication:
    type: "bearer"

tools:
  - name: "get_user"
    description: "获取用户信息"
    endpoint: "/user"
    method: "GET"
    parameters: []
```

生成并运行：
```bash
mcp-gen generate auth-api.yaml -o ./auth-server
set API_AUTH_TOKEN=ghp_your_github_token
cd auth-server
pip install -r requirements.txt
python server.py
```

### 示例3：复杂参数

配置文件 `complex-api.yaml`:
```yaml
server:
  name: "complex-api"
  base_url: "https://api.example.com"

tools:
  - name: "advanced_search"
    description: "高级搜索"
    endpoint: "/search"
    method: "POST"
    parameters:
      # 路径参数
      - name: "query"
        type: "string"
        location: "query"
        required: true
      
      # 查询参数
      - name: "limit"
        type: "integer"
        location: "query"
        default: 10
      
      # 请求体
      - name: "filters"
        type: "array"
        location: "body"
        items_type: "string"
      
      # 自定义Header
      - name: "X-Request-ID"
        type: "string"
        location: "header"
```

## 常见问题解决

### Q: 工具名称验证失败

**错误**：`Tool name 'get-user' is not a valid Python identifier`

**解决**：工具名称必须是有效的Python标识符：
- ✅ 正确：`get_user`, `getUser`, `get_user_info`
- ❌ 错误：`get-user`, `get user`, `get.user`

### Q: 路径参数未定义

**错误**：`path parameter 'user_id' in endpoint is not defined in parameters`

**解决**：确保endpoint中的占位符与parameters匹配：
```yaml
endpoint: "/users/{user_id}"  # 占位符
parameters:
  - name: "user_id"           # 必须定义
    location: "path"          # 必须是path类型
```

### Q: 认证不工作

**检查**：
1. 配置文件中authentication设置正确
2. 环境变量名为 `API_AUTH_TOKEN`
3. Token有效且权限正确

### Q: 生成的服务器无法连接API

**检查**：
1. base_url是否正确（包括http/https）
2. API是否可访问（防火墙、网络）
3. timeout设置是否合理
4. 认证信息是否正确

## 与Claude Desktop集成

### 1. 找到配置文件

Windows: `%APPDATA%\Claude\claude_desktop_config.json`

### 2. 添加服务器配置

```json
{
  "mcpServers": {
    "my-api": {
      "command": "python",
      "args": ["D:\\mcp-generator\\my-server\\server.py"],
      "env": {
        "API_AUTH_TOKEN": "your-token-here"
      }
    }
  }
}
```

### 3. 重启Claude Desktop

配置会在重启后生效。

### 4. 在Claude中使用

现在可以在Claude中使用生成的工具：
```
请帮我调用get_user工具，查询用户ID为123的信息
```

## 高级技巧

### 1. 批量生成

创建脚本批量生成多个服务器：
```bash
@echo off
for %%f in (configs\*.yaml) do (
    echo Generating %%f...
    mcp-gen generate %%f -o servers\%%~nf
)
```

### 2. 自定义生成的代码

生成后可以直接修改 `server.py`：
- 添加自定义请求头
- 修改错误处理逻辑
- 添加缓存机制
- 实现重试逻辑

### 3. 环境变量管理

创建 `.env` 文件：
```
API_AUTH_TOKEN=your_token
API_BASE_URL=https://api.example.com
```

然后在启动脚本中加载。

### 4. 多环境配置

为不同环境创建不同配置：
```
configs/
  ├── dev-api.yaml
  ├── staging-api.yaml
  └── prod-api.yaml
```

## 性能优化

### 1. 调整超时时间

根据API响应时间调整：
```yaml
server:
  timeout: 60  # 对于慢速API增加超时时间
```

### 2. 并发处理

生成的服务器使用异步HTTP客户端，自动支持并发。

### 3. 错误处理

查看生成的 `server.py` 中的错误处理逻辑，可根据需要修改。

## 下一步

- 📖 阅读 `README.md` 了解更多
- 🚀 查看 `QUICKSTART.md` 快速上手
- 💡 研究 `examples/` 目录中的示例
- 🧪 运行 `pytest tests/` 查看测试
- 🤝 提交Issue或PR参与贡献

---

**提示**：遇到问题？检查配置文件格式、参数定义、认证设置和网络连接。
