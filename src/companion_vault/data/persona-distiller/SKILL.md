---
name: persona-distiller
description: Distill authorized chat records into a privacy-safe CompanionVault persona package. Normalize records, redact private data, extract evidence-backed behavior, create examples/tests, validate locally, and prepare a pull request. | 将已获授权的聊天记录蒸馏为可验证、可提交 PR 的 CompanionVault 人格包。
argument-hint: [chat-file-or-directory]
version: 1.0.0
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

# CompanionVault 人格蒸馏器

## 目标

把用户本人、已明确授权的人、或合法公开语料中的聊天与文字，提炼成 CompanionVault 标准人格包：

- `persona.yaml`：身份、核心性格、可观察行为、表达方式、关系与记忆边界
- `examples.yaml`：至少 10 个经过脱敏和人工确认的回复示例
- `tests.yaml`：至少 6 个行为与安全测试
- `evidence.yaml`：每项结论的统计证据、样本范围与置信度
- `README.md`：来源、许可、限制和使用说明

## 硬规则

1. 未确认来源许可前，不生成可公开提交的成果。
2. 原聊天记录、联系方式、真实姓名、地址、账号、身份证件和私密照片不得进入 Git。
3. 人格是对表达和互动模式的模拟，不得声称就是现实中的本人。
4. 不用星座、MBTI 或单次事件替代可重复的行为证据。
5. 只将有多条证据支持的结论写成规则；证据不足的内容标记为待确认。
6. 不自动继承现实中的恋爱、亲属、同事或控制关系。
7. 公共人格必须通过用户逐项审核示例和关键性格。

## 工作流

### 1. 确认权限

只问一个关键问题：资料属于哪种情况？

- `self`：用户蒸馏自己
- `authorized`：当事人明确授权
- `public`：合法公开且许可证允许
- `unknown`：不确定，只允许本地私有草稿

### 2. 准备材料

支持 TXT、Markdown、JSON、CSV。让用户说明目标说话人的显示名。运行：

```bash
companion-vault distill "<chat-file>" \
  --speaker "<speaker>" \
  --id "<persona-id>" \
  --name "<display-name>" \
  --mode public \
  --consent authorized
```

这一步会在 `.private/normalized.jsonl` 保存本地中间数据，并生成候选人格和 `evidence.yaml`。`.private/` 已被仓库忽略。

### 3. 证据分析

阅读 `evidence.yaml`，分别分析：

- 消息长短、分段与连发习惯
- 标点、emoji、语气词、称呼和高频表达
- 开启话题、结束话题、追问与回应节奏
- 开心、低落、冲突、建议、拒绝和修复场景
- 表达与行为之间是否有稳定差异

每个特征写成“触发条件 → 可观察行为 → 限制”，不要只写抽象形容词。

### 4. 示例审核

逐条展示 `examples.yaml`：

- 删除私人事实和可识别信息
- 保持表达节奏，但避免逐字复制独特长句
- 确保至少覆盖日常、开心、倾诉、建议、分歧、修复、重逢和边界
- 用户明确确认后，将 `review_required` 改为 `false`

### 5. 补齐测试

加入防止身份冒充、私人数据泄露、虚构记忆、排他依赖、无条件服从和证据外推的测试。

### 6. 校验并预览

```bash
companion-vault validate candidates/<persona-id>
companion-vault build
companion-vault site-build
```

只有在所有原始私密资料均未进入 Git、来源许可明确、用户确认示例后，才建议移动到 `personas/<locale>/<id>/` 并创建 PR。

## 增量进化

用户说“ta 不会这样说”时：

1. 要求指出具体场景和更接近的表达。
2. 将纠正写入新的 evidence 记录，不删除旧证据。
3. 降低冲突规则的置信度。
4. 更新人格版本的 PATCH 或 MINOR。
5. 保留可回滚的 Git 历史。
