# CLAUDE.md

此文件为 Claude Code (claude.ai/code) 在本项目中工作时提供指导。

## 顶级规则

- 使用 `uv add <package>` 的方式添加依赖。
- 使用 `uv run <script>` 运行python脚本，不要使用 `python <script>`，或者先激活虚拟环境后再执行 python 命令，不要使用默认的python环境。

- 此仓库是 fork 自上游仓库，会定期合并上游代码。请遵循以下最佳实践以减少合并冲突。

### 代码层面最小改动

- **只改需要的部分**：不要为了"风格一致"而修改整行/整段代码
- **避免修改上游已存在的代码**：优先用继承、Mixin、装饰器等扩展方式
- **新增而非修改**：新增文件 > 修改现有文件，新增配置项 > 修改现有配置结构
- **提交粒度要细**：每个功能独立提交，便于选择性合并

## 项目概述


**nanobot** 是一个超轻量级的个人 AI 助手框架（核心代码约 4000 行），可连接多个聊天平台（Telegram、Discord、WhatsApp、Feishu、Slack、QQ、DingTalk、Email、MoChat）。

## 技术栈

- **语言**: Python 3.11+
- **包管理**: pip / uv
- **CLI 框架**: typer
- **LLM 集成**: LiteLLM
- **测试**: pytest + pytest-asyncio
- **代码检查**: ruff
- **WhatsApp 桥接**: Node.js/TypeScript (Baileys)

## 常用命令

```bash
# 开发安装
pip install -e .

# CLI 命令
nanobot onboard                           # 初始化配置和工作区
nanobot agent -m "消息"                    # 与 Agent 对话
nanobot agent                             # 交互式对话模式
nanobot gateway                          # 启动网关（连接各渠道）
nanobot status                           # 显示状态
nanobot channels login                    # 绑定 WhatsApp（扫码）
nanobot channels status                   # 显示渠道状态

# 测试
pytest                                   # 运行所有测试
pytest tests/test_commands.py            # 运行指定测试文件
pytest -v                                # 详细输出

# Docker
docker build -t nanobot .
docker compose up -d nanobot-gateway
```

## 架构

```
nanobot/
├── agent/               # 核心 Agent 逻辑
│   ├── loop.py         # AgentLoop: 消息 → LLM → 工具 → 响应
│   ├── context.py      # ContextBuilder: 提示词构建
│   ├── memory.py       # MemoryStore: 持久化对话历史
│   ├── skills.py       # 技能加载器
│   ├── subagent.py     # 后台任务执行
│   └── tools/          # 内置工具（shell、文件系统、Web、MCP、cron）
├── channels/           # 聊天平台集成
│   ├── manager.py      # ChannelManager: 生命周期管理
│   ├── telegram.py, discord.py, whatsapp.py, feishu.py 等
├── providers/          # LLM 提供商（OpenRouter、Anthropic、DeepSeek 等）
├── bus/                # 消息路由（事件总线模式）
├── session/            # 对话会话
├── config/             # 配置 schema（Pydantic）
├── cli/                # CLI 命令（typer）
├── cron/               # 定时任务
├── heartbeat/          # 主动唤醒事件
└── skills/             # 捆绑的技能（markdown 文件）
```

### 核心处理流程

1. **Channel** 接收消息 → 创建 `InboundMessage` 事件
2. **MessageBus** 将事件路由到 `AgentLoop`
3. **AgentLoop** 构建上下文（历史 + 记忆 + 技能）
4. **LLMProvider** 调用模型
5. **ToolRegistry** 执行工具调用（如有需要）
6. **AgentLoop** 通过 **MessageBus** 发送响应
7. **Channel** 将响应发送给用户

### 核心类

- `AgentLoop` (`nanobot/agent/loop.py`): 核心处理引擎 - 接收消息、调用 LLM、执行工具
- `MessageBus` (`nanobot/bus/queue.py`): 渠道与 Agent 之间的事件路由
- `ChannelManager` (`nanobot/channels/manager.py`): 管理渠道生命周期
- `ToolRegistry` (`nanobot/agent/tools/registry.py`): 工具注册与执行
- `SessionManager` (`nanobot/session/manager.py`): 对话会话管理
- `LLMProvider` (`nanobot/providers/base.py`): LLM 提供商基类

## 配置

配置存储在 `~/.nanobot/config.json`。主要部分：
- `providers`: LLM 提供商设置（API 密钥、模型）
- `channels`: 聊天平台集成
- `agents`: Agent 设置（模型、温度、工具、记忆）
- `workspace`: 工作目录路径

## 测试

测试使用 pytest，`asyncio_mode = "auto"`。测试文件位于 `tests/`。

## 新增渠道

1. 在 `nanobot/channels/<name>.py` 创建实现 `Channel` 接口的类
2. 在 `nanobot/config/schema.py` 添加配置 schema
3. 在 `nanobot/channels/manager.py` 注册

## 新增提供商

1. 在 `nanobot/providers/<name>.py` 创建继承 `LLMProvider` 的类
2. 在提供商工厂中注册
