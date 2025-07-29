# HackChatLike Adapter

HackChatLike 是一个适用于 **所有基于 HackChat 的聊天室** 的 **NoneBot 适配器**，可以轻松地在 HackChat 生态中构建聊天机器人

## 🚀 特性
- 📡 **支持 HackChat 及其衍生聊天室**，兼容所有基于 HackChat 的实时聊天服务
- 🔌 **NoneBot 适配**，可直接集成到 NoneBot 插件系统，实现灵活的机器人开发

<!-- - 🌐 **多聊天室支持**，可以同时连接多个不同的 HackChat 房间-->

## 📦 安装
先安装 NoneBot：
```bash
pip install nonebot2
```
然后安装 HackChatLike 适配器：
```bash
pip install nonebot-adapter-hackchatlike
```

## 🔧 配置
在 `bot.py` 中启用 HackChatLike 适配器：
```python
from nonebot import get_driver
from nonebot.adapters.hackchatlike import Adapter

driver = get_driver()
driver.register_adapter(Adapter)
```

暂不支持同时连接多个房间
<!-- 如果你希望连接多个聊天室，可以在 `.env` 或配置文件中添加：
```ini
HACKCHAT_ROOMS = "room1,room2,room3"
``` -->

## 💬 使用示例
### 消息回显
在 `plugins/echo.py` 中创建一个简单的回显插件：
```python
from nonebot import on_message
from nonebot.adapters.hackchatlike import MessageEvent

echo = on_message()

@echo.handle()
async def handle_echo(event: MessageEvent):
    await echo.send(f"你发送的消息是: {event.message}")
```

## 📖 API 参考
### `MessageEvent`
用于处理 HackChat 消息：
- `event.message`：消息内容
- `event.trip`: 加密身份标识
- `event.self_id`: Bot ID
- `event.user_id`：发送者的用户 ID
- `event.channel`：聊天室名称

### `send_chat_message`
发送消息到聊天室：
```python
await bot.send_chat_message(target="channel", message="Hello!")
```

### `send_whisper_message`
发送私聊给指定用户
```python
await bot.send_whisper_message(target="2333", message="Hello HackChat!")
```

## 🔨 开发与贡献
欢迎贡献代码！请遵循以下流程：
1. **Fork 本仓库** 并克隆代码。
2. **提交 Pull Request**，描述你的改动。

## 📜 许可证
本项目基于 **MIT 许可证** 开源，你可以自由使用和修改。
