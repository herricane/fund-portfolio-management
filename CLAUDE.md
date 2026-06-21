# CLAUDE.md — Claude Code Context

> 本文件供 Claude Code 自动读取，提供项目上下文。

## 这是什么

中国公募基金组合管理 skill。用户提到基金/持仓/定投/再平衡时，自动触发 `fund-portfolio-management` skill。

## 核心架构

**核心-卫星双层模型**：

- **核心层 (80-90%)**：Bogleheads 被动投资。永不择时。定投纪律、资产配置、再平衡日历始终生效。
- **卫星层 (10-20%)**：有限战术操作。有条件触发，受核心层约束。止盈/补仓基于配置偏离，非盈亏%或市场预测。

## 重要文件

| 文件 | 用途 |
|------|------|
| `SKILL.md` | Agent 运行时指令（操作手册） |
| `references/investment-philosophy.md` | 投资理论基础 |
| `references/fund-types.md` | 中国公募基金类型速查 |
| `references/apis.md` | 天天基金 + 新浪 API 参考 |
| `scripts/fetch_all_nav.py` | 实时净值拉取 |

## 关键设计原则

1. **IPS 由用户定义，不硬编码** — 收益目标、回撤容忍、投资期限全部来自用户问卷
2. **矛盾检测** — 用户参数不合理时主动提醒（如年化 15% + 回撤 10%）
3. **配置驱动，非盈亏驱动** — 止盈触发于配置偏离，而非"涨了 40%"
4. **不输出 PESTEL、K 线信号、宏观预测** — 对被动投资者无操作价值
5. **中文为主** — 专用术语（DCA、IPS、QDII、ETF）保留英文

## 首次使用流程

当 `references/portfolio-state.md` 不存在时：
1. 引导用户完成 IPS 问卷（6 个问题）
2. 矛盾检测
3. 写入 `portfolio-state.md`
