# PersonaDock

**PersonaDock 是一个本地优先的 AI 人格工具，用于从自然语言或聊天记录创建人格，生成 SOUL、Skill 和 Memory，并将其打包、一键安装到不同智能体平台。**

PersonaDock 不要求用户提交人格 PR。人格、聊天记录和记忆默认只保存在本地；公开分享是用户明确选择后的可选步骤。

## 核心流程

```text
自然语言描述 / 选择聊天记录 / 两者混合
                  ↓
Codex / Claude / OpenCode 使用 PersonaDock Skills
                  ↓
生成 PersonaDock 本地人格工程
                  ↓
短 SOUL + 详细人格 Skill + 已审核 Memory + 场景测试
                  ↓
打包为 .personapack
                  ↓
安装到 Hermes / OpenClaw
```

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

## AI 编辑器 Skills

PersonaDock wheel 内置两套 Skill：

| Skill | 用途 |
|---|---|
| `persona-builder` | 根据自然语言创建或修改人格，也支持“描述 + 参考材料”的混合生成 |
| `persona-distiller` | 从用户选择的聊天记录中提取有证据支持的表达、行为和记忆候选 |

默认同时安装两套：

```bash
personadock skill install --target codex --scope global
```

也可以只安装一套：

```bash
personadock skill install \
  --target codex \
  --scope global \
  --skill persona-builder

personadock skill install \
  --target codex \
  --scope global \
  --skill persona-distiller
```

### 支持的编辑器目录

```bash
personadock skill install --target codex --scope global
personadock skill install --target claude --scope global
personadock skill install --target opencode --scope global
personadock skill install --target agents --scope global
personadock skill install --target generic --scope project
```

自定义父目录：

```bash
personadock skill install \
  --target generic \
  --path /custom/agent-skills
```

默认安装结果：

```text
<skills-directory>/
├── persona-builder/
│   ├── SKILL.md
│   └── references/
│       ├── output-contract.md
│       ├── prompt-contract.md
│       └── memory-contract.md
└── persona-distiller/
    ├── SKILL.md
    └── references/
        ├── output-contract.md
        └── memory-contract.md
```

## 使用自然语言创建人格

在 Codex、Claude 或 OpenCode 中直接描述想要的人格：

```text
请使用 persona-builder Skill，在 ./xiaoyou-persona 创建一个人格。

她叫小柚，是一个嘴硬心软、偶尔犯迷糊但有独立判断的赛博伙伴。
平时会轻微吐槽；当我真的难过或疲惫时停止开玩笑，先听我说。
发生争吵时她会指出具体介意的事情，但发现误解后会明确道歉。
她不会假装记得我没有提供的经历，也不会无条件迎合。
回复以简短自然的中文为主，不要写成小说。

请把不同场景写进 Skill references，SOUL 只保留核心身份和路由规则。
完成后运行 validate、build、pack，并生成 personapack。
```

`persona-builder` 会把自然语言要求转换为：

```text
触发条件 → 可观察行为 → 限制 → Skill reference → 场景测试
```

例如：

```text
用户非常疲惫
→ 缩短回复、停止轻度吐槽、先提供陪伴
→ 不训话、不连续追问
→ emotional-support.md
→ tired-support 测试
```

而不是把完整设定全部复制进 SOUL。

### 修改现有人格

```text
请使用 persona-builder 修改 ./xiaoyou-persona：

- 日常聊天更活泼，但不要每句话都傲娇。
- 用户咨询技术问题时减少人格表演，优先说清楚答案。
- 增加“长时间没见后重逢”的场景。
- 保留现有已审核 Memory，不要覆盖。

修改后展示差异并重新打包。
```

## 从聊天记录蒸馏

向编辑器明确选择聊天记录，并要求使用 `persona-distiller`：

```text
请使用 persona-distiller Skill，读取我选择的这些聊天记录：

- ./chats/2026-01.txt
- ./chats/2026-02.json

目标说话人是“小柚”，人格 ID 为 xiaoyou，输出到 ./xiaoyou-persona。
先生成待审核工程，展示 SOUL 结论、Skill 规则和 Memory 候选，确认后再打包。
```

蒸馏 Skill 只读取用户明确选择的文件，并将：

- 原始资料、证据和未审核候选保存在 `.private/`
- 稳定身份和路由规则写入短 SOUL
- 详细表达与场景行为写入人格 Skill references
- 只有用户明确确认的事实写入 `memory/seed.jsonl`

## 混合生成

当用户既有设计要求又有聊天示例时，使用 `persona-builder` 的混合模式：

```text
请使用 persona-builder 创建 ./study-partner。
核心设定以我的描述为准，同时参考我选择的聊天记录学习自然的短句节奏。
聊天记录只作为表达参考，不要自动继承里面的现实关系和私人事件。
```

设计要求与记录观察冲突时：

- 用户最新明确要求优先
- 可以共存的差异按场景拆分
- 无法同时成立的核心冲突会被列入 `.private/design-notes.md`

## PersonaDock 工程结构

两套 Skill 最终都生成相同的标准工程：

```text
my-persona/
├── companion.yaml
├── skills/
│   └── persona/
│       ├── SKILL.md
│       └── references/
│           ├── voice.md
│           ├── daily-scenarios.md
│           ├── emotional-support.md
│           ├── conflict-repair.md
│           ├── relationship-stages.md
│           └── examples.md
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

- `companion.yaml` 保存短 SOUL 所需的稳定核心和路由规则。
- `skills/persona/` 保存详细场景、表达、关系行为、缺点和示例。
- `memory/seed.jsonl` 只允许包含明确审核且带有 `reviewed: true` 的事实。
- `.private/` 保存原始资料、中间证据、设计假设和未审核候选，永不打包。

## 手工创建人格工程

```bash
personadock init ./my-companion \
  --id my-companion \
  --name "我的伙伴"
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

该命令只生成待审核骨架、表达候选和记忆候选。复杂多文件上下文优先使用 `persona-distiller` Skill。

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
| Skill | 场景行为、表达细节、关系处理、缺点、示例 | 需要时按需加载 |
| Memory | 真实偏好、事件与关系事实 | 检索后加载，不得虚构 |
| Runtime | 当前会话和临时状态 | 由目标智能体管理 |

## 隐私模型

默认行为：

- 不需要 GitHub 账号
- 不提交 Pull Request
- 不上传人格或聊天记录
- 只读取用户明确选择的参考资料
- `.private/` 永不打包
- 未审核真实记忆不能进入 PersonaPack
- 只有用户明确要求时才公开导出

生成不含私人记忆的公共版本：

```bash
personadock export-public ./my-companion
```

## 发布 Python 包

仓库的标签发布工作流会构建 wheel、source distribution 和示例 PersonaPack，通过 PyPI Trusted Publishing 上传 `persona-dock`，然后创建 GitHub Release。首次发布前需要在 PyPI 配置 Pending Trusted Publisher，并在 GitHub 创建名为 `pypi` 的 Environment。详细步骤见 [`docs/publishing.md`](docs/publishing.md)。

## 命令

```text
personadock init            创建本地人格工程
personadock skill install   安装 Builder / Distiller AI 编辑器 Skills
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

AI 编辑器 Skill 安装目标：

- Codex
- Claude
- OpenCode
- `.agents/skills`
- Generic Agent Skills

## 开发验证

```bash
pytest

personadock skill install \
  --target generic \
  --scope project \
  --path /tmp/editor-skills

personadock init /tmp/persona-demo \
  --id persona-demo \
  --name "Persona Demo"
personadock validate /tmp/persona-demo
personadock build /tmp/persona-demo
personadock pack /tmp/persona-demo
```

## 许可证

MIT
