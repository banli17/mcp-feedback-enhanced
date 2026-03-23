# MCP Feedback Enhanced

## 尝试 uvx 命令

```
uvx --from https://github.com/banli17/mcp-feedback-enhanced.git mcp-feedback-enhanced
```

## uvx 配置示例

```json
{
  "servers": {
    "mcp-feedback-enhanced": {
      "command": "uvx",
      "args": [
        "--from",
        "https://github.com/banli17/mcp-feedback-enhanced.git",
        "mcp-feedback-enhanced@latest",
      ],
      "timeout": 3600,
      "env": {
        "MCP_DESKTOP_MODE": "true",
        "MCP_WEB_HOST": "127.0.0.1",
        "MCP_WEB_PORT": "8767",
        "MCP_DEBUG": "false",
      },
      "autoApprove": ["interactive_feedback"],
      "type": "stdio",
    }
  }
}
```

## 如果在使用 uvx 命令时遇到网络问题，可以尝试以下步骤来配置 git 代理

```
git config --global http.https://github.com.proxy http://127.0.0.1:7890
git config --global https.https://github.com.proxy http://127.0.0.1:7890
```

## 如果仍然遇到问题，可以尝试以下步骤来清除 git 全局代理配置并重置 uv 缓存

```
# 清除 git 全局代理配置
git config --global --unset http.https://github.com.proxy
git config --global --unset https.https://github.com.proxy

# 重置 uv 缓存（避免缓存的错误连接信息）
uv cache clean
```