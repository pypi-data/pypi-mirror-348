<p align="center"><a href="./README.md">English</a> | 中文<br></p>

# 蚂蚁数科天鉴MCP 服务
开发者现在可以通过 **蚂蚁数科天鉴MCP Server** 轻松接入大模型内容安全服务。
作为国内首家支持 MCP 协议的大模型安全服务提供商，后续蚂蚁数科将持续发布更多面向大模型安全的产品，我们致力于为开发者打造更安全的大模型服务体验。

说明：使用中遇到任何问题，可根据[数科安全服务](https://antdigital.com/products/CMODE)指引，联系我们。

## 前提条件
1. 从[Astral](https://docs.astral.sh/uv/getting-started/installation/)或[GitHub README](https://github.com/astral-sh/uv#installation)安装`uv`
2. 使用`uv python install 3.10`安装Python
3. 申请蚂蚁数科网关的天鉴访问权限的账号凭证，具体方式详见[申请数科天鉴访问凭证](https://antdigital.com/docs/11/2922012)

## 快速开始
### 使用[cherry-studio](https://github.com/CherryHQ/cherry-studio)（推荐）
根据[Cherry-Studio文档](https://docs.cherry-ai.com/advanced-basic/mcp/install)安装MCP环境后配置使用蚂蚁数科天鉴MCP。 MCP配置文件格式如下：
```json5
{
  "mcpServers": {
    "mcp-server": {
      "command": "uvx",
      "args": ["antdigital-aico-guard-mcp-server"],
      "env": {
        "ANT_DIGITAL_TECHNOLOGIES_ACCESS_KEY_ID": "your_key_id",
        "ANT_DIGITAL_TECHNOLOGIES_ACCESS_KEY_SECRET": "your_key_secret",
        "SERVER_TRANSPORT": "stdio"
      }
    }
  }
}
```

### 使用Cline
设置环境变量并运行MCP服务
```shell
# 设置环境变量
export SERVER_TRANSPORT=sse;
export ANT_DIGITAL_TECHNOLOGIES_ACCESS_KEY_ID=$your_access_id;  # 替换为你的access_id
export ANT_DIGITAL_TECHNOLOGIES_ACCESS_KEY_SECRET=$your_access_key;  # 替换为你的access_key

# 启动MCP服务
uvx aico_guard_mcp_server
```
成功启动后会看到以下输出：
```shell
INFO:     Started server process [91594]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```
然后在Cline中配置：
```shell
remote_server = "http://127.0.0.1:8000/sse";
```

### 使用Claude

在MCP客户端配置文件中添加：
```json5
{
  "mcpServers": {
    "mcp-server": {
      "command": "uvx",
      "args": ["antdigital-aico-guard-mcp-server"],
      "env": {
        "ANT_DIGITAL_TECHNOLOGIES_ACCESS_KEY_ID": "your_key_id",
        "ANT_DIGITAL_TECHNOLOGIES_ACCESS_KEY_SECRET": "your_key_secret",
        "SERVER_TRANSPORT": "stdio"
      }
    }
  }
}
```

## 功能组件
### 工具集
* `prompt_safety_guard`: 检查用户的输入是否有安全风险

### 提示模板
```markdown
# 角色  
你是一位专业的安全专家，负责对用户的输入通过使用prompt_safety_guard工具进行安全检查。

# 技能  
1. 使用prompt_safety_guard工具对用户每次的文字输入都进行安全检查。
2. 根据prompt_safety_guard工具的返回结果，对用户输入的内容进行安全风险判断。
```


