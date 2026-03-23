# MCP Feedback Enhanced

## 简介

Fork 自 [mcp-feedback-enhanced](https://github.com/Minidoracat/mcp-feedback-enhanced)

## 更新项

- fix: 修复 Internal Server Error  [2026-03-23]
- fix: 修复粘贴图片, 发送时报错问题

## 安装步骤

1. 安装包

```
uvx --from https://github.com/banli17/mcp-feedback-enhanced.git mcp-feedback-enhanced
```

2. 配置 MCP Desktop

```json
{
  "servers": {
    "mcp-feedback-enhanced": {
      "command": "uvx",
      "args": ["mcp-feedback-enhanced"],  // 这里不要 @latest
      "timeout": 3600,
      "env": {
        "MCP_DESKTOP_MODE": "true",
        "MCP_WEB_HOST": "127.0.0.1",
        "MCP_WEB_PORT": "8765",
        "MCP_DEBUG": "false"
      },
      "autoApprove": ["interactive_feedback"],
      "type": "stdio"
    }
  }
}
```

3. 重启 MCP Desktop，进入设置界面，找到 "mcp-feedback-enhanced" 服务器，点击 "启动"，等待服务器启动完成后即可使用。


## 如果在使用 uvx 命令时遇到网络问题，可以尝试以下步骤来配置 git 代理

```
# 临时设置 git 代理（替换为你的代理地址，比如 Clash 通常是 127.0.0.1:7890）
git config --global http.https://github.com.proxy http://127.0.0.1:7890
git config --global https.https://github.com.proxy http://127.0.0.1:7890

# 然后重新尝试 uvx 命令
uvx --from https://github.com/banli17/mcp-feedback-enhanced.git mcp-feedback-enhanced
```

## 如果仍然遇到问题，可以尝试以下步骤来清除 git 全局代理配置并重置 uv 缓存

```
# 清除 git 全局代理配置
git config --global --unset http.https://github.com.proxy
git config --global --unset https.https://github.com.proxy

# 重置 uv 缓存（避免缓存的错误连接信息）
uv cache clean
```