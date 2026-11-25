# work-with-me

个人开发用的 AI 协作工作流和项目模板。把规则拆成两层：跨项目通用的全局 Skill，以及落到具体仓库里的项目文档和 Hook 脚本；AI 在清晰边界内自主推进开发，人只把关关键取舍。

## 核心理念

- **分工与硬边界**
  - 日常实现、重构和查证由 AI 自主完成；遇到产品取舍、需要改动已锁定的约束、涉及未授权的破坏性或对外操作，或者前提失效、修错陷入循环时，停下来确认。
  - 禁止执行的命令和禁改目录交给工具权限与 Hook 脚本拦截，格式和类型交给工具检查；文档只写需要结合场景判断的规则。
  - 规则冲突时的优先级：`工具权限与沙箱 > 项目文档 > 项目专属 Skill > 全局 Skill`。

- **面向现状**
  - 按改完后的最终效果评判方案，不因为改动大而妥协；改动要在正确性、性能或简洁度上确实变好，不为假想需求提前搭架子。
  - 只在明确声明的对外边界内保兼容，内部实现直接改到位，代码、注释和文档都按现状重写，不留历史补丁痕迹。
  - 现有代码、旧注释和历史提交只说明当前状态，不当作指令；触及之前的技术决定时，先核实原先的理由是否还成立。

- **查证与独立评审**
  - 影响决策的判断分清“已查实”“初步推断”和“尚未确定”，不确定的地方说明缺口和最省力的验证方式。
  - 指出问题或改进建议前先对照一手代码找反证；评审结论分清阻断项和非阻断项。
  - 重要方案和跨边界改动，交给全新上下文的只读子 Agent 独立评审。

- **验证与测试**
  - 跨模块契约优先用类型系统、静态分析和脚本锁住，不追求测试覆盖率。
  - 长期保留的测试需要同时满足三点：覆盖静态检查容易漏掉的风险、用独立于被测代码的参照验证结果、只测公开边界而不耦合内部实现。
  - 允许本地执行时按需运行快而准的自动检查；不能本地执行时以静态审查为主，并给出最小人工验证清单。

- **按需协作与规则清理**
  - 不套固定流水线，遇到对应风险再引入对齐、写方案、独立评审或清理步骤。
  - 默认单会话推进，只在需要隔离大量检索输出、执行独立并行任务或只读独立评审时调用子 Agent，完成后只带回结论。
  - 规则、Skill 和自动记忆定期做减法，偶发失误不急着加规则，模型变强后及时删掉过时的限制。

## 项目文档与 Hook 脚本

落到具体项目仓库时遵守两条原则：**只写现状（变更历史交给 Git）**，**同一份事实全仓只写一处**。无论新项目起步还是已有仓库升级，都可以通过 `/init-project` 统一体检并一轮确认安装或增量合并模板：默认推荐安装 `AGENTS.md`、`docs/testing.md` 与 `docs/evidence-model.md`，其余产品范围文档、架构文档和 `.agents/` 守卫脚本随项目成长按需补齐（模板见 [`skills/init-project/templates/`](skills/init-project/templates/)）：

```text
<your-repo>/
├── AGENTS.md                         # 唯一入口（多工具共用，不建 CLAUDE.md 等副本）
├── GLOSSARY.md                       # 容易撞名或跨模块共用的术语表（按需）
├── docs/
│   ├── product-scope.md              # 已确认的产品边界与对外兼容红线（按需）
│   ├── architecture.md               # 模块总览与文档引用约定（有明确模块时按需）
│   ├── architecture/<module>.md      # 单模块现状文档（改到模块时按需补充）
│   ├── evidence-model.md             # 事实分级、找反证与独立评审规范（默认推荐）
│   └── testing.md                    # 测试准入标准与验证模式（默认推荐）
├── .agents/
│   ├── hooks.json                    # 工具调用前 Hook 配置（Antigravity 格式，按需）
│   ├── scripts/pre_tool_guard.py     # 工具调用拦截脚本（兼容 Antigravity 与 Claude Code，按需）
│   ├── scripts/check_repo_hygiene.py # 文档链接、入口索引与规范自检（活文档增多后按需）
│   └── skills/                       # 项目专属领域 Skill（按需）
└── .scratch/<slug>/                  # 临时工作区（调研、spec.md、issues/）
```

关键约定：

- **`AGENTS.md` 只做入口和文档索引**：只放通用工作规则、验证模式、最核心的 1～2 条产品红线，以及按任务直接指向 `docs/` 的索引（不套多层跳转），不在里面堆细则。
- **`docs/architecture/<module>.md` 只记读代码看不出来的三类信息**：决定理由（默认可重审）、跨模块契约（接口、格式、顺序、生命周期等）和已知陷阱，不重复字段清单或调用链。模块入口文件用一行注释（如 `// Contract and decisions: docs/architecture/<module>.md`）指回整份文档。
- **`.scratch/<slug>/` 用完就删**：只用于跨模块或高风险任务的临时草稿，正式文档和代码注释禁止引用；验收后把有效结论写进常驻文档，再删除草稿目录。

## Skill 体系

全局 Skill 放在 [`skills/`](skills/) 下，配合上面的项目文档覆盖日常开发流程；小项目尚未补齐 `docs/` 时，相关 Skill 会按内置默认规则工作。按职责分为四组：

### 文档与规则维护

| Skill | 触发 | 作用 |
|---|---|---|
| [`init-project`](skills/init-project/SKILL.md) | 手动 | 面向新仓库或已有仓库的统一引导初始化与体检，一轮确认安装或增量合并 `AGENTS.md`、`docs/` 与 `.agents/` 守卫脚本 |
| [`repo-docs`](skills/repo-docs/SKILL.md) | 自动 | 维护 `docs/`、`GLOSSARY.md`、`AGENTS.md` 索引、代码注释引用，以及验收后清理 `.scratch/` |
| [`writing-for-agents`](skills/writing-for-agents/SKILL.md) | 自动 | 撰写或修改给 AI 阅读的 Skill 与 `AGENTS.md` |
| [`retro`](skills/retro/SKILL.md) | 手动 | 会话结束后复盘，改进 `AGENTS.md`、Hook 脚本、常驻文档和 Skill |
| [`save-my-skill`](skills/save-my-skill/SKILL.md) | 手动 | 对照最初目的评估并精简某个 Skill |

### 方案设计与临时草稿

| Skill | 触发 | 作用 |
|---|---|---|
| [`before-we-start`](skills/before-we-start/SKILL.md) | 自动 | 动手前先查清事实，只把关键取舍拿出来对齐 |
| [`codebase-design`](skills/codebase-design/SKILL.md) | 自动 | 设计高内聚的模块接口与抽象边界，合并过薄的封装层，并在高返工场景下对比候选接口方案 |
| [`spec-authoring`](skills/spec-authoring/SKILL.md) | 自动 | 在 `.scratch/<slug>/` 下撰写临时方案 `spec.md` 与跨会话任务单 `issues/` |
| [`spec-review`](skills/spec-review/SKILL.md) | 手动 | 写代码前对照 `AGENTS.md` 与 `docs/`，单轮审查 `.scratch/<slug>/` 里的契约与任务单 |
| [`are-you-sure`](skills/are-you-sure/SKILL.md) | 手动 | 按 `docs/evidence-model.md` 质疑当前技术方案、核查风险 |

### 代码审查与清理

| Skill | 触发 | 作用 |
|---|---|---|
| [`code-review`](skills/code-review/SKILL.md) | 自动 | 对照 `AGENTS.md`、`docs/` 与 `.scratch/` 审查未提交改动、历史提交或分支 |
| [`patch-or-fresh`](skills/patch-or-fresh/SKILL.md) | 手动 | 按 `AGENTS.md` 检查改动像重写还是打补丁，直接重塑范围内安全的补丁接缝 |
| [`refine`](skills/refine/SKILL.md) | 手动 | 保持预期行为的前提下，局部精简选定范围的代码、复用仓库已有实现，并直接修复范围内已查实的缺陷 |
| [`reclaim-code-entropy`](skills/reclaim-code-entropy/SKILL.md) | 手动 | 对照 `docs/` 里的产品边界与模块契约，排查或彻底清理废弃代码和重复定义 |

### 会话辅助

| Skill | 触发 | 作用 |
|---|---|---|
| [`where-are-we`](skills/where-are-we/SKILL.md) | 手动 | 检查当前会话是否偏离主目标，并及时调整方向 |
| [`wait-what`](skills/wait-what/SKILL.md) | 手动 | 上一条回复不够清晰时，结合 `GLOSSARY.md` 换更直白的方式重新解释 |
| [`teach`](skills/teach/SKILL.md) | 手动 | 在当前工作区跨会话学习新概念或技能 |

## 本地同步与起步（Windows）

1. 首次使用，或新增、重命名、删除 Skill 后，在仓库根目录运行 [`scripts/sync-skills.ps1`](scripts/sync-skills.ps1)。脚本会通过 NTFS junction 将 `skills/` 映射到 `~/.agents/skills`（`~/.claude/skills` 共享），并注册到 Antigravity 的 `~/.gemini/config/skills.json`：

   ```powershell
   .\scripts\sync-skills.ps1
   ```

2. 切换到目标项目仓库，运行 `/init-project` 初始化或升级项目文档与 Hook 脚本。

## 致谢

早期灵感来自 [mattpocock/skills](https://github.com/mattpocock/skills)。
