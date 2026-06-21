# 基金组合管理 Skill

一份 Hermes Agent 专用的中国公募基金组合管理 skill —— 持仓分析、定投优化、再平衡、自动化日报。

## 功能概览

- **组合健康评分** —— 0-100 分，覆盖 8 个维度（资产分配、集中度、定投流向、止盈合规、亏损处理、再平衡、行为偏差、风格漂移）
- **定投流向分析** —— 检测自动定投是否在悄悄重塑你的组合结构
- **再平衡建议** —— 基于博格头 + 耶鲁/斯文森框架，含优先级矩阵和 C 类费率规则
- **行为护栏** —— 每次建议前检查 7 种认知偏误
- **自动化日报** —— 通过 cron 定时推送市场概览 + 持仓快照 + 偏离度监测
- **实时净值拉取** —— 调用天天基金 API，无需额外 pip 依赖

## 安装

### 1. 克隆 skill

```bash
mkdir -p ~/.hermes/skills/productivity
git clone https://github.com/herricane/fund-portfolio-management.git \
  ~/.hermes/skills/productivity/fund-portfolio-management
```

### 2. 创建你的持仓文件

```bash
cd ~/.hermes/skills/productivity/fund-portfolio-management
cp references/portfolio-state.example.md references/portfolio-state.md
```

编辑 `references/portfolio-state.md`，填入你的真实持仓：

- 基金代码、名称、成本价、持有份额
- 定投设置（每周 base 金额、限购额度）
- IPS 目标配置比例

此文件已被 `.gitignore` 排除，不会上传到 GitHub。

### 3. 修改净值拉取脚本

编辑 `scripts/fetch_all_nav.py`，把 `funds` 列表改成你的基金代码：

```python
funds = [
    "XXXXXX", "XXXXXX",  # 你的基金代码
    ...
]
```

### 4. Python 环境（可选）

Skill 只依赖 Python 标准库（`urllib`、`json`），无需 pip 安装任何包。

### 5. 验证

在 Hermes 里说：

> 分析一下我的基金持仓

Skill 会在提到 基金/持仓/定投/补仓 时自动加载。

## 使用方式

### 快速诊断

> 我的持仓怎么样？

跑 8 项 checklist + 健康评分，约 5 秒完成。

### 标准分析（日报级别）

> 基金日报

完整报告：市场概览 + 持仓快照 + 偏离度监测 + 行为护栏 + 一句话总结。

### 深度分析

> 深度分析我的基金持仓

标准级全部内容 + 逐只基金诊断（含同类对比）+ 再平衡方案 + IPS 符合性审查。

### 调整定投

> 把半导体的定投从 375 降到 250

自动更新 `portfolio-state.md` 并重算定投流向。

### 设置定时日报

```bash
# 在 Hermes 中执行：
/cron add "30 14 * * 1-5" --skill fund-portfolio-management \
  --prompt "生成今日基金日报" \
  --toolsets web,terminal
```

## 文件结构

```
fund-portfolio-management/
├── SKILL.md                          # skill 主定义（agent 读取）
├── README.md                         # 本文件
├── .gitignore                        # 排除你的私有 portfolio-state.md
├── scripts/
│   └── fetch_all_nav.py             # 从天天基金拉取实时净值
└── references/
    ├── portfolio-state.example.md    # 模板 — 复制为 portfolio-state.md 后填写
    ├── eastmoney-api.md             # 天天基金 API 文档
    ├── sina-api.md                  # 新浪财经 API（降级方案）
    ├── bogleheads-principles.md     # 博格头被动投资框架
    ├── swensen-yale-model.md        # 耶鲁捐赠基金模型
    ├── behavioral-finance-biases.md # 7 种认知偏误
    └── fund-types.md                # 基金分类指南
```

## 运行要求

- Hermes Agent（Nous Research）
- Python 3.8+（仅标准库，无需 pip）
- 网络连接（调用天天基金 API）

## 许可

MIT
