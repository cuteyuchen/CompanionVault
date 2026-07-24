# PersonaDock

**PersonaDock 是一个本地优先的 AI 人格工具，用于创建或蒸馏人格，生成 SOUL、Skill 和 Memory，并将其打包、一键安装到不同智能体平台。**

它不是一个要求用户提交人格 PR 的仓库。用户的人格、聊天记录和记忆默认只保存在本地；公开分享是明确选择后的可选步骤。

## 核心流程

```text
创建或蒸馏人格
      ↓
生成短 SOUL + 人格 Skill + 已审核 Memory
      ↓
构建 Hermes / OpenClaw / Generic 目标
      ↓
打包为 .personapack
      ↓
一键安装、卸载或回滚
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

主命令：

```bash
personadock --help
# 或
pdock --help
```

## 快速开始

### 1. 创建私有人格项目

```bash
personadock init ./my-companion \
  --id my-companion \
  --name "我的伙伴"

cd my-companion
```

项目默认包含：

```text
my-companion/
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

`.private/` 默认被 Git 忽略，原始聊天和未审核的记忆候选不会进入人格包。

### 2. 验证并构建

```bash
personadock validate
personadock build
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

SOUL 只保留稳定身份、核心人格、边界、Skill 路由和记忆真实性规则。详细场景、表达方式、关系阶段和示例放在 Skill references 中，避免 SOUL 过长。

### 3. 打包 PersonaPack

```bash
personadock pack
```

输出：

```text
dist/my-companion-0.1.0.personapack
```

`.personapack` 是可校验的 ZIP 格式，包含：

- 目标平台的 SOUL
- 人格 Skill 与 references
- 经过明确审核的 Memory
- 场景测试
- Manifest 与每个文件的 SHA-256

检查人格包：

```bash
personadock inspect dist/my-companion-0.1.0.personapack
```

### 4. 安装到智能体

Hermes：

```bash
personadock install dist/my-companion-0.1.0.personapack \
  --target hermes
```

OpenClaw：

```bash
personadock install dist/my-companion-0.1.0.personapack \
  --target openclaw
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

## 从聊天记录蒸馏

输入文件可使用简单的说话人格式：

```text
用户：今天有点累。
小柚：那先别逼自己解决所有事情，坐一会儿，我听着。
```

创建蒸馏项目：

```bash
personadock distill ./chat.txt ./xiaoyou \
  --id xiaoyou \
  --name 小柚 \
  --speaker 小柚
```

蒸馏命令会：

- 将原始聊天保存到 `.private/raw/`
- 将人格说话示例放入 Skill reference
- 将可能的事实生成未审核记忆候选
- 生成明确的人工审核说明

未设置 `reviewed: true` 的记忆不能构建或打包。PersonaDock 不会把未审核候选或原始聊天装进 PersonaPack。

## SOUL、Skill 与 Memory 的职责

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
- 不上传人格
- 不上传聊天记录
- `.private/` 永不打包
- 只有明确审核的记忆进入私有 PersonaPack

需要公开时，先生成不含私人记忆的导出：

```bash
personadock export-public
```

输出目录中的 Memory seed 会被清空。用户之后可以自行选择上传 GitHub Release、私下分享或提交到其他公共目录。

## 命令

```text
personadock init            创建本地人格工程
personadock distill         从聊天文本创建待审核工程
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

## 当前目标平台

- Hermes
- OpenClaw
- Generic system prompt

平台适配器会继续独立演进，不要求人格工程改变其核心内容。

## 开发验证

```bash
pytest

personadock init /tmp/persona-demo \
  --id persona-demo \
  --name "Persona Demo"
personadock validate /tmp/persona-demo
personadock build /tmp/persona-demo
personadock pack /tmp/persona-demo
```

## 许可证

MIT
