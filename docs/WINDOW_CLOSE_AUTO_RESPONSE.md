# 窗口关闭自动响应功能说明

## 🎯 问题背景

之前当 VS Code Copilot 智能体调用 `interactive_feedback` 工具后，如果用户直接关闭 MCP feedback 窗口而不提交反馈，会导致智能体一直转圈（挂起），必须等待 timeout 超时（默认 600 秒）才能继续。

## ✅ 解决方案

实现了**窗口关闭自动响应机制**，当用户关闭反馈窗口时：

1. **自动检测**：WebSocket 断开时检测用户是否已提交反馈
2. **立即响应**：如果未提交，自动设置"用户已关闭反馈窗口"的取消标记
3. **解除阻塞**：立即触发 `feedback_completed` 事件，让 AI 智能体收到响应
4. **正常流程**：AI 智能体收到取消通知后可以继续工作

## 📝 技术实现

### 修改的文件

#### 1. `feedback_session.py`

添加了 `cancel_by_window_close()` 方法：

```python
async def cancel_by_window_close(self):
    """
    用户关闭窗口时自动取消会话
    此方法会立即触发 feedback_completed 事件，让等待中的 AI 智能体解除阻塞
    """
    if self.feedback_completed.is_set():
        return
    
    debug_log(f"⚠️ 会话 {self.session_id} 检测到用户关闭窗口，自动取消会话")
    
    # 设置取消标记的反馈内容
    self.feedback_result = "[用户已关闭反馈窗口]"
    self.status = SessionStatus.COMPLETED
    self.status_message = "用户取消反馈（关闭窗口）"
    self.last_activity = time.time()
    
    # 立即触发完成事件，释放等待中的 wait_for_feedback
    self.feedback_completed.set()
    
    debug_log(f"✅ 会话 {self.session_id} 已自动取消，AI 智能体将收到取消通知")
```

#### 2. `main_routes.py`

在 WebSocket 断开处理中添加自动取消逻辑：

```python
finally:
    # 安全清理 WebSocket 连接
    current_session = manager.get_current_session()
    if current_session and current_session.websocket == websocket:
        # 🔴 检测用户是否在未提交反馈的情况下关闭窗口
        if not current_session.feedback_completed.is_set():
            debug_log(f"⚠️ 检测到会话 {current_session.session_id} 窗口被关闭但未提交反馈，自动取消")
            await current_session.cancel_by_window_close()
        
        current_session.websocket = None
        debug_log("已清理会话中的 WebSocket 连接")
```

#### 3. `wait_for_feedback()` 方法优化

添加了窗口关闭取消的处理：

```python
if completed:
    # 检查是否是用户关闭窗口导致的取消
    if self.feedback_result == "[用户已关闭反馈窗口]":
        debug_log(f"会话 {self.session_id} 因用户关闭窗口而取消")
        return {
            "logs": "\n".join(self.command_logs),
            "interactive_feedback": self.feedback_result,
            "images": [],
            "settings": {},
            "cancelled": True,  # 添加取消标记
        }
```

## 🧪 测试方法

运行测试脚本：

```powershell
python test_window_close.py
```

**测试步骤**：
1. 脚本启动反馈窗口
2. 直接关闭浏览器窗口（不提交反馈）
3. 观察脚本是否在 1-2 秒内收到响应

**预期结果**：
- ✅ 关闭窗口后，脚本应该在 1-2 秒内收到响应
- ✅ 反馈内容为 `[用户已关闭反馈窗口]`
- ✅ 不应该等待 60 秒 timeout

## 🔄 工作流程

```
用户关闭窗口
    ↓
WebSocket 断开
    ↓
检测 feedback_completed 状态
    ↓
未设置 → 调用 cancel_by_window_close()
    ↓
设置取消标记反馈
    ↓
触发 feedback_completed.set()
    ↓
wait_for_feedback() 立即返回
    ↓
AI 智能体收到取消通知并继续工作
```

## 📊 对比

### 修改前

| 场景 | 行为 | 等待时间 |
|------|------|----------|
| 用户关闭窗口 | 智能体挂起，一直转圈 | 等待 timeout（默认 600 秒） |
| 用户提交反馈 | 正常 | 立即响应 |

### 修改后

| 场景 | 行为 | 等待时间 |
|------|------|----------|
| 用户关闭窗口 | 智能体收到取消通知并继续 | **1-2 秒** ⚡ |
| 用户提交反馈 | 正常 | 立即响应 |

## 🎯 用户体验改进

1. **无需等待**：关闭窗口后立即解除智能体阻塞
2. **明确提示**：AI 收到 `[用户已关闭反馈窗口]` 明确知道用户取消操作
3. **保持流畅**：不会因为误关窗口导致长时间挂起

## 🔧 兼容性

- ✅ 向后兼容：不影响正常提交反馈的流程
- ✅ 优雅降级：如果窗口关闭检测失败，仍会在 timeout 后正常结束
- ✅ 状态一致：会话状态正确更新为 `COMPLETED`

## 📝 注意事项

1. 此功能仅在用户**未提交反馈**的情况下触发
2. 如果用户已经提交反馈，关闭窗口不会影响已提交的内容
3. AI 智能体会收到明确的取消标记，可以根据需要调整后续行为

## 🚀 后续优化建议

可以考虑添加以下增强功能：

1. **会话恢复**：允许用户重新打开已关闭的会话窗口
2. **快捷键**：提供快捷键快速取消/关闭窗口
3. **确认对话框**：在用户尝试关闭窗口时显示确认提示
4. **自动保存**：在窗口关闭前自动保存用户已输入的内容

这些功能可以根据实际需求逐步实现。
