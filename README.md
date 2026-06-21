# 基金组合管理 Skill

中国公募基金组合管理工具 —— 持仓分析、定投优化、再平衡、净值监控。

基于**核心-卫星双层架构**：博格头被动投资为压舱石，斯文森多资产配置为框架，行为金融为操作护栏。

## 功能

- **IPS 初始化** — 引导式问卷 + 参数矛盾检测，而非硬编码假设
- **组合诊断** — 8 项 Checklist + 偏离度 + 定投流向分析
- **再平衡方案** — 基于配置偏离（非盈亏%）的优先级矩阵
- **操作护栏** — 操作前必问 3 题 + 7 天冷却期
- **净值拉取** — 天天基金 API，零额外依赖
- **定时简报** — 可配合 cron 生成日报/周报

## 支持的 Agent

| Agent | 上下文文件 |
|-------|----------|
| Claude Code | `CLAUDE.md`（自动读取） |
| Codex CLI / OpenCode / OpenClaw 等 | `AGENTS.md`（自动读取） |
| Hermes | `SKILL.md`（`hermes skills install` 安装） |

## 安装

本 skill 不依赖特定 agent 框架。克隆到本地即可：

```bash
git clone https://github.com/herricane/fund-portfolio-management.git
cd fund-portfolio-management
```

**各 agent 的安装方式**：

- **Claude Code**：在项目目录下自动加载 `CLAUDE.md`，无需额外配置。也可注册为全局 skill。
- **Codex / OpenCode**：在项目目录下自动读取 `AGENTS.md`。
- **Hermes**：`hermes skills install` 指向本目录。

## 首次使用

在任何 AI Agent 中说：

> 分析一下我的基金持仓

Skill 会自动检测 `references/portfolio-state.md` 尚未创建，引导你完成：

1. 投资期限、收益目标、回撤容忍
2. 月定投能力、当前持仓（代码+份额+成本，或直接发截图）
3. 流动性、大额支出计划、卫星止盈目标（可选）
4. 参数矛盾检测（如"年化 15% + 回撤 10%"会被提醒不可行）
5. 确认后写入 `portfolio-state.md`，下次直接使用

### 验证净值拉取

```bash
# 自动从 portfolio-state.md 读取基金代码，无需手动编辑
python3 scripts/fetch_all_nav.py
```

输出每日净值快照。

## 使用方式

| 场景 | 示例（在任何 Agent 中） |
|------|------|
| 快速诊断 | 「我的持仓怎么样？」 |
| 标准分析 | 「基金日报」 |
| 深度复盘 | 「深度分析我的持仓」 |
| 调整定投 | 「把半导体的定投降到 250/周」 |
| 定时简报 | 配合 cron，交易日定时推送 |

## 文件结构

```
fund-portfolio-management/
├── SKILL.md                       # Agent 运行时指令（操作手册）
├── CLAUDE.md                      # Claude Code 上下文
├── AGENTS.md                      # 通用 Agent 指南
├── README.md                      # 本文件
├── .gitignore                     # 排除 portfolio-state.md
├── scripts/
│   └── fetch_all_nav.py           # 天天基金净值拉取
└── references/
    ├── investment-philosophy.md   # 投资理论（博格头+斯文森+行为金融+反脆弱+配置推导）
    ├── fund-types.md              # 中国公募基金完整分类 + 投资逻辑速查
    ├── apis.md                    # API 参考（天天基金+新浪）
    └── portfolio-state.example.md # 持仓模板（复制为 portfolio-state.md 后填写）
```

## 依赖

- Python 3.8+（仅标准库，无需 pip）
- 网络连接（天天基金 API）

## 许可

MIT
