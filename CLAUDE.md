# CLAUDE.md — Claude Code Context

> 本文件供 Claude Code 自动读取，提供项目上下文。

## 这是什么

中国公募基金组合管理 skill。用户提到基金/持仓/定投/再平衡时，自动触发 `fund-portfolio-management` skill。

## 核心架构

**核心-卫星双层模型**：

- **核心层 (80-90%)**：Bogleheads 被动投资。永不择时。定投纪律、资产配置、再平衡日历始终生效。
- **卫星层 (10-20%)**：有限战术操作。有条件触发，受核心层约束。再平衡卖出基于配置偏离，卫星止盈以目标收益为辅助信号，补仓需逻辑+配置双验证。

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
3. **核心层配置驱动，卫星层有限盈亏辅助** — 核心再平衡始终基于配置偏离；卫星止盈允许以目标收益为辅助信号，但受配置健康度约束
4. **不输出 PESTEL、K 线信号、宏观预测** — 对被动投资者无操作价值
5. **中文为主** — 专用术语（DCA、IPS、QDII、ETF）保留英文

## 首次使用流程

当 `references/portfolio-state.md` 不存在或含 `XXXXXX` 占位符时：
1. 引导用户完成 IPS 问卷（7 个问题）
2. 矛盾检测
3. 写入 `portfolio-state.md`
