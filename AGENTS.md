# AGENTS.md — Universal Agent Instructions

> 本文件供主流 AI coding agent 自动读取：
> Claude Code (`CLAUDE.md`)、Codex CLI (`CODEX.md`)、OpenCode、OpenClaw 等。
> 完整操作指令在 `SKILL.md`，理论深度在 `references/`。

## 项目简介

中国公募基金组合管理 skill。为个人投资者提供持仓分析、定投优化、再平衡建议、净值监控。

## 核心架构

**核心-卫星双层模型**：

- **核心层 (80-90%)**：Bogleheads 被动投资。永不择时。定投纪律、资产配置、再平衡日历始终生效。
- **卫星层 (10-20%)**：有限战术操作。有条件触发，受核心层约束。止盈/补仓基于配置偏离，非盈亏%或市场预测。

## 关键文件

| 文件 | 用途 | 何时读取 |
|------|------|---------|
| `SKILL.md` | Agent 运行时指令（操作手册） | 每次任务必读 |
| `references/investment-philosophy.md` | 投资理论基础 | 需要解释"为什么"时 |
| `references/fund-types.md` | 中国公募基金类型速查 | 分类/诊断时 |
| `references/apis.md` | 天天基金 + 新浪 API 参考 | API 格式疑问 |
| `references/portfolio-state.md` | 用户持仓数据（gitignored） | 每次分析必读 |
| `scripts/fetch_all_nav.py` | 实时净值拉取 | 需要最新净值时 |

## 关键设计原则

1. **IPS 由用户定义，不硬编码** — 收益目标、回撤容忍、投资期限全部来自用户问卷
2. **矛盾检测** — 用户参数不合理时主动提醒（如年化 15% + 回撤 10%）
3. **配置驱动，非盈亏驱动** — 止盈触发于配置偏离，而非"涨了 40%"
4. **不输出 PESTEL、K 线信号、宏观预测** — 对被动投资者无操作价值
5. **中文为主** — 专用术语（DCA、IPS、QDII、ETF、NAV）保留英文

## 首次使用

当 `references/portfolio-state.md` 不存在或含 `XXXXXX` 占位符时：
1. 引导用户完成 IPS 问卷（6 个问题：期限、收益、回撤、定投额、持仓、流动性）
2. 矛盾检测（收益 vs 回撤、时间 vs 仓位、定投 vs 目标）
3. 写入确认后的参数到 `portfolio-state.md`

## 运行要求

- Python 3.8+（仅标准库）
- 网络（天天基金 API）
- 不依赖 pip 包（除非用户需要批量历史数据）

## 许可

MIT
