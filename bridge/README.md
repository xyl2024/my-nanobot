# nanobot WhatsApp Bridge

使用 Baileys 库连接 WhatsApp Web 的桥接服务，作为 nanobot Python 后端的中间层。

## 架构

```
WhatsApp Web ←→ Bridge (Node.js) ←→ WebSocket ←→ nanobot Gateway (Python)
```

## 环境要求

- Node.js >= 20.0.0

## 安装

```bash
cd bridge
npm install
npm run build
```

## 配置

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| `BRIDGE_PORT` | `3001` | WebSocket 监听端口 |
| `AUTH_DIR` | `~/.nanobot/whatsapp-auth` | WhatsApp 认证数据存储目录 |
| `BRIDGE_TOKEN` | (无) | 认证令牌，可选 |

## 启动

```bash
# 默认配置
npm start

# 自定义端口
BRIDGE_PORT=3002 npm start

# 启用认证
BRIDGE_TOKEN=your-secret-token npm start
```

首次启动会显示 QR 码，用手机 WhatsApp 扫描完成登录。认证信息会保存在 `AUTH_DIR` 目录，后续启动自动复用。

## 消息格式

### 接收消息 (Python ← Bridge)

```json
{
  "type": "message",
  "pn": "1234567890",
  "sender": "1234567890@s.whatsapp.net",
  "content": "Hello",
  "id": "message_id",
  "timestamp": 1234567890,
  "isGroup": false
}
```

### 发送消息 (Python → Bridge)

```json
{
  "type": "send",
  "to": "1234567890@s.whatsapp.net",
  "text": "Hello back"
}
```

### 认证 (Python → Bridge)

```json
{
  "type": "auth",
  "token": "your-secret-token"
}
```

### 状态消息

```json
{ "type": "status", "status": "connected" }
{ "type": "status", "status": "disconnected" }
{ "type": "qr", "qr": "..." }
```

## 与 nanobot 配合使用

1. 启动 bridge: `npm start`
2. 配置 nanobot:

```json
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "bridge_url": "ws://localhost:3001",
      "bridge_token": ""
    }
  }
}
```

3. 启动 nanobot gateway: `nanobot gateway`

## 安全

- WebSocket 仅绑定 `127.0.0.1`，不暴露到外部网络
- 支持可选的 Token 认证
- 认证数据存储在本地目录，注意保护
