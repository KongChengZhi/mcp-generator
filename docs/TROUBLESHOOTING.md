# 故障排除指南

## 问题：`mcp-gen` 命令找不到

### 问题描述
在终端输入 `mcp-gen` 时显示：
```
'mcp-gen' 不是内部或外部命令，也不是可运行的程序或批处理文件。
```

### 原因分析

在安装时你可能看到了这个警告：
```
WARNING: The script mcp-gen.exe is installed in 'C:\Users\singsky\AppData\Roaming\Python\Python312\Scripts' which is not on PATH.
```

这意味着 `mcp-gen.exe` 已经成功安装，但安装位置（`C:\Users\singsky\AppData\Roaming\Python\Python312\Scripts`）不在系统的 PATH 环境变量中。

### 解决方案

#### 方案1：添加到 PATH 环境变量（推荐）

**步骤：**

1. 按 `Win + X`，选择"系统"
2. 点击"高级系统设置"
3. 点击"环境变量"
4. 在"用户变量"中找到 `Path`，点击"编辑"
5. 点击"新建"，添加：
   ```
   C:\Users\singsky\AppData\Roaming\Python\Python312\Scripts
   ```
6. 点击"确定"保存
7. **重新打开终端**（必须重启终端才能生效）
8. 测试：
   ```bash
   mcp-gen --version
   ```

**快捷方式（PowerShell管理员权限）：**
```powershell
# 查看当前用户 PATH
[Environment]::GetEnvironmentVariable("Path", "User")

# 添加 Scripts 目录到用户 PATH
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$scriptsPath = "C:\Users\singsky\AppData\Roaming\Python\Python312\Scripts"
if ($userPath -notlike "*$scriptsPath*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$scriptsPath", "User")
    Write-Host "已添加到 PATH，请重启终端"
}
```

#### 方案2：使用 Python 模块方式运行（无需配置）

无需修改 PATH，直接使用：

```bash
# 使用完整模块路径
python -m mcp_generator.cli.main --help
python -m mcp_generator.cli.main init -o config.yaml
python -m mcp_generator.cli.main generate config.yaml -o ./output
python -m mcp_generator.cli.main validate config.yaml
python -m mcp_generator.cli.main preview config.yaml
```

**创建别名（临时，仅当前会话有效）：**

PowerShell:
```powershell
# 创建别名
function mcp-gen { python -m mcp_generator.cli.main $args }

# 使用
mcp-gen --help
mcp-gen init -o config.yaml
```

Cmd:
```cmd
doskey mcp-gen=python -m mcp_generator.cli.main $*
```

#### 方案3：创建批处理文件

在项目根目录创建 `mcp-gen.bat`：

```batch
@echo off
python -m mcp_generator.cli.main %*
```

然后将项目目录添加到 PATH，或直接使用：
```bash
.\mcp-gen.bat --help
```

#### 方案4：全局安装（不推荐）

如果不想使用用户安装，可以全局安装：

```bash
# 需要管理员权限
pip install -e . --no-user
```

这会安装到系统 Python 的 Scripts 目录（通常已在 PATH 中）。

### 验证安装

**检查是否安装成功：**
```bash
pip show mcp-generator
```

应该显示：
```
Name: mcp-generator
Version: 0.1.0
Location: d:\mcp-generator\src
```

**检查命令是否可用：**

方案1（PATH配置后）:
```bash
mcp-gen --version
```

方案2（模块方式）:
```bash
python -m mcp_generator.cli.main --version
```

两种方式都应该显示：
```
mcp-gen, version 0.1.0
```

### 常见问题

#### Q: 添加到 PATH 后仍然找不到命令？

A: 确保：
1. 路径拼写完全正确
2. 已经**重启终端**（必须！）
3. 如果使用 IDE 内置终端，需要重启 IDE

#### Q: 如何查看 PATH 环境变量？

A: 
```powershell
# PowerShell
$env:PATH -split ';'

# Cmd
echo %PATH%
```

#### Q: Python 版本不同怎么办？

A: 你的路径可能是：
- Python 3.9: `...\Python\Python39\Scripts`
- Python 3.10: `...\Python\Python310\Scripts`
- Python 3.11: `...\Python\Python311\Scripts`
- Python 3.12: `...\Python\Python312\Scripts`

检查你的 Python 版本：
```bash
python --version
```

#### Q: 为什么使用 `pip install -e .`？

A: 
- `-e` 表示"可编辑模式"（editable mode）
- 这样修改源代码后无需重新安装
- 适合开发环境
- 生产环境可以用 `pip install .`

### 推荐配置

**开发环境（本项目）：**
```bash
# 1. 可编辑安装
pip install -e .

# 2. 使用模块方式
python -m mcp_generator.cli.main generate config.yaml -o ./output
```

**日常使用：**
```bash
# 1. 添加 Scripts 到 PATH
# 2. 直接使用命令
mcp-gen generate config.yaml -o ./output
```

### 快速测试

安装后立即测试：

```bash
# 方式1：如果 PATH 已配置
mcp-gen --version
mcp-gen init -o test.yaml
mcp-gen validate test.yaml

# 方式2：使用模块方式（总是可用）
python -m mcp_generator.cli.main --version
python -m mcp_generator.cli.main init -o test.yaml
python -m mcp_generator.cli.main validate test.yaml
```

### 完整示例

**使用 Python 模块方式（无需配置 PATH）：**

```bash
# 进入项目目录
cd d:\mcp-generator

# 确保已安装
pip install -e .

# 创建配置
python -m mcp_generator.cli.main init -o my-config.yaml

# 验证配置
python -m mcp_generator.cli.main validate my-config.yaml

# 生成服务器
python -m mcp_generator.cli.main generate my-config.yaml -o ./my-server

# 运行生成的服务器
cd my-server
pip install -r requirements.txt
python server.py
```

### 原理说明

#### 为什么会有这个问题？

1. **用户级安装 vs 系统级安装**
   - `pip install`（用户级）→ `%APPDATA%\Python\Python3xx\Scripts`
   - `pip install --no-user`（系统级）→ `Python安装目录\Scripts`

2. **PATH 环境变量**
   - Windows 通过 PATH 查找可执行文件
   - 如果路径不在 PATH 中，系统找不到命令
   - Python 的 Scripts 目录默认不一定在 PATH 中

3. **为什么 `python -m` 总是可用？**
   - Python 安装时会配置 `python` 命令到 PATH
   - `-m` 参数告诉 Python 运行模块
   - 不依赖 Scripts 目录

#### pip install 的工作流程

```
pip install -e .
    ↓
读取 pyproject.toml
    ↓
解析 [project.scripts]
    mcp-gen = "mcp_generator.cli:main"
    ↓
在 Scripts 目录创建 mcp-gen.exe
    ↓
检查 Scripts 是否在 PATH
    ↓
否 → 显示警告
是 → 安装完成
```

### 总结

**最简单的方案**（推荐新手）：
使用 `python -m mcp_generator.cli.main` 代替 `mcp-gen`

**最方便的方案**（推荐日常使用）：
添加 Scripts 目录到 PATH，重启终端

**创建便捷脚本**（推荐本项目）：
在项目根目录创建 `mcp-gen.bat`
