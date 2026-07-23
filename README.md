# CompanionVault

CompanionVault 是一个面向长期情感陪伴和日常交流的开源 AI 人格库。每个人格都使用统一结构描述基础性格、可观察行为、表达习惯、情绪响应、关系边界和回复示例，并可编译成 Hermes `SOUL.md`、通用 System Prompt 与 SillyTavern Character Card。

## 快速开始

```bash
pip install -e .
companion-vault list
companion-vault build
companion-vault install xiaoyou --target hermes
```

默认 Hermes 安装位置为 `~/.hermes/SOUL.md`。安装前会自动备份已有文件。

## 贡献人格

```bash
companion-vault new-persona my-companion --name "我的伙伴"
companion-vault validate personas/zh-CN/my-companion
```

提交 PR 前，请补全 `persona.yaml`、`examples.yaml`、`tests.yaml`，并确保至少有 10 组覆盖不同场景的示例。

## 目录

- `personas/`：人格源文件
- `baselines/`：所有陪伴人格共享的健康交互基线
- `schemas/`：JSON Schema
- `src/companion_vault/`：CLI、校验器、编译器与安装器
- `dist/`：自动生成，禁止手工修改

代码使用 MIT License；人格文本默认使用 CC BY 4.0。
