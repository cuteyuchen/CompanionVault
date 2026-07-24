# PersonaDock

**PersonaDock 是一个本地优先的 AI 人格工具，用于从自然语言、聊天记录或两者的组合创建人格，生成 SOUL、Skill 和 Memory，并将其打包、一键安装到不同智能体平台。**

人格、聊天记录和记忆默认只保存在本地。使用 PersonaDock 不需要 Fork 仓库、提交 PR 或公开人格；公共分享是用户明确选择后的可选步骤。

## 核心流程

```text
自然语言描述 / 选择聊天记录 / 两者混合 / 修改已有工程
                          ↓
Codex / Claude / OpenCode 使用 persona-builder Skill
                          ↓
Skill 自动判断 Create / Distill / Hybrid / Refine 模式
                          ↓
生成短 SOUL + 详细人格 Skill + 已审核 Memory + 场景测试
                          ↓
打包为 .personapack
                          ↓
安装到 Hermes / OpenClaw
```

## 安装 PersonaDock

```bash
pip install persona-dock
```

开发安装：

```bash
git clone https://github.com/cuteyuchen/PersonaDock.git
cd PersonaDock
pip install -e .[dev]
```

查看命令：

```bash
personadock --help
# 或
pdock --help
```

## 安装统一人格 Skill

PersonaDock wheel 内置一个统一的 `persona-builder` Skill。它同时负责自然语言创建、聊天蒸馏、混合生成和已有工程优化，用户不需要安装或选择多个 Skill。

Codex 全局安装：

```bash
personadock skill install --target codex --scope global
```

Codex 当前项目安装：

```bash
personadock skill install --target codex --scope project
```

其他编辑器：

```bash
personadock skill install --target claude --scope global
personadock skill install --target opencode --scope global
personadock skill install --target agents --scope global
personadock skill install --target generic --scope project
```

指定自定义父目录：

```bash
personadock skill install \
  --target generic \
  --path /custom/agent-skills
```

安装结果：

```text
<skills-directory>/
└── persona-builder/
    ├── SKILL.md
    └── references/
        ├── output-contract.md
        ├── prompt-contract.md
        ├── evidence-contract.md
        └── memory-contract.md
```

## Skill 自动模式判断

`persona-builder` 根据用户目标自动选择内部模式，不要求用户学习技术概念。

| 模式 | 适用输入 | 主要规则 |
|---|---|---|
| Create | 自然语言描述想要的人格 | 用户的明确设计要求是主要来源 |
| Distill | 选择聊天记录并希望还原说话人的稳定行为 | 只采纳有来源和置信度的观察 |
| Hybrid | 人格设定与聊天参考同时存在 | 区分“设计要求”和“聊天证据” |
| Refine | 修改已有 PersonaDock 工程 | 保留已审核内容并展示差异 |

典型路由：

```text
“创建一个嘴硬心软的赛博伙伴”
→ Create

“读取这些聊天，分析小柚稳定的说话和冲突修复方式”
→ Distill

“人格设定以我的描述为准，同时参考聊天学习短句节奏”
→ Hybrid

“修改已有工程，让日常场景更活泼”
→ Refine
```

## 使用自然语言创建人格

在 Codex、Claude 或 OpenCode 中输入：

```text
请使用 persona-builder Skill，在 ./xiaoyou-persona 创建一个人格。

她叫小柚，是一个嘴硬心软、偶尔犯迷糊但有独立判断的赛博伙伴。
平时会轻微吐槽；当我真的难过或疲惫时停止开玩笑，先听我说。
发生争吵时她会指出具体介意的事情，但发现误解后会明确道歉。
她不会假装记得我没有提供的经历，也不会无条件迎合。
回复以简短自然的中文为主，不要写成小说。

请把不同场景写进 Skill references，SOUL 只保留核心身份和路由规则。
完成后运行 validate、build、pack，并生成 PersonaPack。
```

Skill 会把自然语言要求转换为可执行规则：

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

完整设定不会被直接复制进 SOUL。

## 从聊天记录蒸馏人格

用户只需要选择聊天记录并继续使用同一个 Skill：

```text
请使用 persona-builder Skill，读取我选择的这些聊天记录：

- ./chats/2026-01.txt
- ./chats/2026-02.json

目标说话人是“小柚”，人格 ID 为 xiaoyou，输出到 ./xiaoyou-persona。
请根据重复出现的表达、情绪回应和冲突修复方式生成待审核工程。
展示 SOUL 结论、Skill 规则、证据来源和 Memory 候选，确认后再打包。
```

Skill 会自动进入 Distill 模式，并遵守：

- 只读取用户明确选择的文件
- 不修改原始聊天记录
- 将归一化记录写入 `.private/normalized.jsonl`
- 将行为证据、来源和置信度写入 `.private/evidence.jsonl`
- 将未审核真实事实写入 `.private/memory-candidates.jsonl`
- 将详细表达和场景行为写入人格 Skill references
- 只把用户明确确认的事实写入 `memory/seed.jsonl`
- 不声称生成的人格就是聊天中的现实人物

单次现象、MBTI、星座、职业或推测不能直接成为稳定人格规则。

## 混合生成

当用户同时提供设定和参考材料时，仍使用同一个 Skill：

```text
请使用 persona-builder 创建 ./study-partner。
核心设定以我的描述为准，同时参考我选择的聊天记录学习自然的短句节奏。
聊天记录只作为表达参考，不要自动继承里面的现实关系和私人事件。
```

Hybrid 模式会区分：

- 用户明确设计的人格要求
- 聊天记录中有证据支持的观察
- 系统补充的非敏感默认项
- 真实用户事实与共享事件

冲突处理顺序默认是：

```text
用户最新明确要求
→ 已审核的现有人格内容
→ 有证据支持的来源观察
→ 明确标记的默认设计
```

无法同时成立的冲突会保存在 `.private/design-notes.md` 中等待用户决定。

## 修改现有人格

```text
请使用 persona-builder 修改 ./xiaoyou-persona：

- 日常聊天更活泼，但不要每句话都傲娇。
- 用户咨询技术问题时减少人格表演，优先说清楚答案。
- 增加“长时间没见后重逢”的场景。
- 保留现有已审核 Memory，不要覆盖。

修改后展示差异并重新打包。
```

## PersonaDock 工程结构

所有内部模式最终生成同一种标准工程：

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
- `memory/seed.jsonl` 只允许包含明确审核且带有 `reviewed: true` 的真实事实。
- `.private/` 保存原始资料、证据、设计假设和未审核候选，永不打包。

## 手工创建工程

```bash
personadock init ./my-companion \
  --id my-companion \
  --name "我的伙伴"
```

验证和构建：

```bash
personadock validate ./my-companion
personadock build ./my-companion
```

## 轻量备用蒸馏

对于简单的“说话人：内容”文本，可以不依赖 AI 编辑器：

```bash
personadock distill ./chat.txt ./xiaoyou \
  --id xiaoyou \
  --name 小柚 \
  --speaker 小柚
```

该命令只生成待审核骨架、表达候选和记忆候选。复杂上下文、多文件分析和混合生成应使用统一 `persona-builder` Skill。

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

检查包：

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

管理安装：

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

仓库使用 GitHub Actions 和 PyPI Trusted Publishing。推送与 `pyproject.toml` 版本一致的标签后，工作流会：

1. 运行测试。
2. 构建 wheel 和 source distribution。
3. 检查统一 Skill 是否进入 wheel。
4. 构建示例 PersonaPack。
5. 发布到 PyPI。
6. 创建 GitHub Release。

首次发布前需要配置：

```text
GitHub Environment: pypi
PyPI Project: persona-dock
Owner: cuteyuchen
Repository: PersonaDock
Workflow: release.yml
Environment: pypi
```

发布 `0.1.0`：

```bash
git tag -a v0.1.0 -m "PersonaDock v0.1.0"
git push origin v0.1.0
```

## 命令

```text
personadock init            创建本地人格工程
personadock skill install   安装统一 AI 编辑器人格 Skill
personadock distill         简单文本的轻量备用蒸馏
personadock validate        验证工程、隐私和记忆审核状态
personadock build           生成平台目标文件
personadock pack            生成 .personapack
personadock inspect         校验人格包完整性
personadock install         安装到智能体
personadock rollback        恢复安装前文件
personadock uninstall       移除 PersonaDock 管理的文件
personadock status          查看安装状态
personadock export-public   导出无私人记忆的公共版本
```

## 当前支持

人格包安装目标：

- Hermes
- OpenClaw
- Generic system prompt

统一 Skill 安装目标：

- Codex
- Claude
- OpenCode
- 通用 Agent Skills 目录

## License

MIT
