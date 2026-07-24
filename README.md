# PersonaDock

**PersonaDock 是一个本地优先的 AI 人格工具，用于创建或蒸馏人格，生成 SOUL、Skill 和 Memory，并将其打包、一键安装到不同智能体平台。**

PersonaDock 不要求用户提交人格 PR。人格、聊天记录和记忆默认只保存在本地；公开分享是用户明确选择后的可选步骤。

## 核心流程

```text
用户选择聊天记录
      ↓
Codex / Claude / OpenCode 使用 persona-distiller Skill
      ↓
生成 PersonaDock 本地人格工程
      ↓
生成短 SOUL + 人格 Skill + 已审核 Memory
      ↓
打包为 .personapack
      ↓
一键安装到 Hermes / OpenClaw
```

内置 `personadock distill` 只是轻量备用功能。复杂聊天、多文件上下文和高质量人格分析优先交给支持 Skill 的 AI 编辑器完成。

## 安装

```bash
pip install persona-dock
```

开发安装：

```bash
git clone https://github.com/cuteyuchen/PersonaDock.git
cd PersonaDock
pip install -e .[dev]
```

```bash
personadock --help
# 或
pdock --help
```

## 推荐方式：在 AI 编辑器中蒸馏

PersonaDock wheel 内置 `persona-distiller` Skill。可以一键安装到不同编辑器：

### Codex

全局安装：

```bash
personadock skill install --target codex --scope global
```

当前项目安装：

```bash
personadock skill install --target codex --scope project
```

### Claude

```bash
personadock skill install --target claude --scope global
```

### OpenCode

```bash
personadock skill install --target opencode --scope global
```

### 通用 Agent Skills 目录

```bash
personadock skill install --target agents --scope global
personadock skill install --target generic --scope project
```

也可以指定自定义父目录：

```bash
personadock skill install \
  --target generic \
  --path /custom/agent-skills
```

安装后的 Skill 目录包含：

```text
persona-distiller/
├── SKILL.md
└── references/
    ├── output-contract.md
    └── memory-contract.md
```

### 在编辑器中使用

向编辑器明确选择聊天记录，并要求使用 `persona-distiller`：

```text
请使用 persona-distiller Skill，读取我选择的这些聊天记录：

- ./chats/2026-01.txt
- ./chats/2026-02.json

目标说话人是“小柚”，人格 ID 为 xiaoyou，输出到 ./xiaoyou-persona。
先生成待审核的人格工程，展示 SOUL、Skill 和 Memory 候选，确认后再打包。
```

Skill 会直接生成 PersonaDock 可用的标准工程，不需要先运行内置 `distill`：

```text
xiaoyou-persona/
├── companion.yaml
├── skills/
│   └── persona/
│       ├── SKILL.md
│       └── references/
├── memory/
│   ├── profile.yaml
│   ├── seed.jsonl
│   └── policy.yaml
├── tests/
│   └── scenarios.yaml
├── .private/
└── .gitignore
```

其中：

- `.private/` 保存原始资料、中间证据和未审核记忆候选。
- `companion.yaml` 保存短 SOUL 所需的稳定核心和路由规则。
- `skills/persona/` 保存详细场景、表达、关系行为和示例。
- `memory/seed.jsonl` 只允许写入用户明确确认且带有 `reviewed: true` 的事实。

完成审核后，编辑器运行：

```bash
personadock validate ./xiaoyou-persona
personadock build ./xiaoyou-persona
personadock pack ./xiaoyou-persona
personadock inspect ./xiaoyou-persona/dist/xiaoyou-0.1.0.personapack
```

## 手工创建人格工程

不使用聊天记录时，可以直接创建模板：

```bash
personadock init ./my-companion \
  --id my-companion \
  --name "我的伙伴"
```

然后编辑：

```text
my-companion/
├── companion.yaml
├── skills/persona/
├── memory/
├── tests/
└── .private/
```

验证并构建：

```bash
personadock validate ./my-companion
personadock build ./my-companion
```

构建输出：

```text
.personadock/build/
├── manifest.json
├── source/
├── targets/
│   ├── hermes/
│   │   ├── SOUL.md
│   │   ├── skills/
│   │   └── memory/
│   ├── openclaw/
│   │   ├── SOUL.md
│   │   ├── skills/
│   │   └── memory/
│   └── generic/
└── tests/
```

SOUL 只保留稳定身份、核心人格、边界、Skill 路由和记忆真实性规则。详细场景、关系阶段和示例放在 Skill references 中，避免 SOUL 过长。

## 轻量备用蒸馏

对于简单的“说话人：内容”文本，可以不依赖 AI 编辑器：

```bash
personadock distill ./chat.txt ./xiaoyou \
  --id xiaoyou \
  --name 小柚 \
  --speaker 小柚
```

这个命令只生成待审核骨架、表达候选和记忆候选。它不负责复杂上下文推断，也不会自动把候选记忆标记为已审核。

## 打包 PersonaPack

```bash
personadock pack ./my-companion
```

输出：

```text
my-companion/dist/my-companion-0.1.0.personapack
```

`.personapack` 是可校验的 ZIP 格式，包含：

- 目标平台的 SOUL
- 人格 Skill 与 references
- 经过明确审核的 Memory
- 场景测试
- Manifest 与每个文件的 SHA-256

```bash
personadock inspect ./my-companion/dist/my-companion-0.1.0.personapack
```

## 安装到智能体

Hermes：

```bash
personadock install ./persona.personapack --target hermes
```

OpenClaw：

```bash
personadock install ./persona.personapack --target openclaw
```

指定安装目录：

```bash
personadock install ./persona.personapack \
  --target hermes \
  --path /custom/hermes/home
```

PersonaDock 会备份被替换的文件，并只管理自己安装的 SOUL、Skill 和 Memory 目录。

```bash
personadock status
personadock rollback --target hermes
personadock uninstall --target openclaw
```

## SOUL、Skill 与 Memory

| 层 | 负责内容 | 加载方式 |
|---|---|---|
| SOUL | 身份、核心特征、边界、路由规则 | 始终加载，严格控制长度 |
| Skill | 场景行为、表达细节、关系处理、示例 | 需要时按需加载 |
| Memory | 真实偏好、事件与关系事实 | 检索后加载，不得虚构 |
| Runtime | 当前会话和临时状态 | 由目标智能体管理 |

## 隐私模型

默认行为：

- 不需要 GitHub 账号
- 不提交 Pull Request
- 不上传人格或聊天记录
- 只读取用户明确选择的蒸馏资料
- `.private/` 永不打包
- 未审核记忆不能进入 PersonaPack
- 只有用户明确要求时才公开导出

生成不含私人记忆的公共版本：

```bash
personadock export-public ./my-companion
```

## 命令

```text
personadock init            创建本地人格工程
personadock skill install   安装 AI 编辑器蒸馏 Skill
personadock distill         简单文本的轻量备用蒸馏
personadock validate        验证 Schema、隐私和记忆审核状态
personadock build           生成平台目标文件
personadock pack            生成 .personapack
personadock inspect         校验人格包完整性
personadock install         安装到智能体
personadock rollback        恢复安装前文件
personadock uninstall       移除 PersonaDock 管理的文件
personadock status          查看安装状态
personadock export-public   导出无私人记忆的公共版本
```

## 当前目标

人格包安装目标：

- Hermes
- OpenClaw
- Generic system prompt

蒸馏 Skill 安装目标：

- Codex
- Claude
- OpenCode
- Agent Skills 兼容目录
- 自定义目录

## 开发验证

```bash
pytest

personadock skill install --target generic --path /tmp/skills
personadock init /tmp/persona-demo --id persona-demo --name "Persona Demo"
personadock validate /tmp/persona-demo
personadock build /tmp/persona-demo
personadock pack /tmp/persona-demo
```

## 许可证

MIT
