# 数据源 API 参考

> agent 按需读取。所有接口免费、无需 API key。

---

## 天天基金 — 实时估值（盘中）

```bash
curl -s "https://fundgz.1234567.com.cn/js/{CODE}.js"
```

**响应**（JSONP）：
```json
jsonpgz({"fundcode":"000001","name":"示例基金名称","jzrq":"2026-01-01","dwjz":"1.2345","gsz":"1.2500","gszzl":"1.26","gztime":"2026-01-02 15:00"})
```

| 字段 | 含义 |
|------|------|
| `fundcode` | 6 位基金代码 |
| `name` | 基金全称 |
| `dwjz` | 上一交易日单位净值 |
| `gsz` | 盘中估算净值 |
| `gszzl` | 估算涨跌幅 (%) |
| `gztime` | 估算时间戳 |

**⚠️ JSONP 解析陷阱**：`str.lstrip('jsonpgz(')` 会逐字符剥离而非前缀剥离，损坏 JSON。必须用切片：

```python
raw = response  # 'jsonpgz({...});'
inner = raw[len("jsonpgz("):-2]
data = json.loads(inner)
```

**QDII 注意**：美股 QDII 更新时点不同（约北京时间凌晨），`gztime` 会体现。

---

## 天天基金 — 历史净值

```
GET https://fundf10.eastmoney.com/F10DataApi.aspx?type=lsjz&code={CODE}&page=1&sdate={YYYY-MM-DD}&edate={YYYY-MM-DD}&per=20
```

**解析**：
```python
import re
navs = re.findall(
    r'<td>(\d{4}-\d{2}-\d{2})</td>\s*<td[^>]*>([\d.]+)</td>\s*<td[^>]*>([\d.]+)</td>\s*<td[^>]*>([^<]+)</td>',
    html_content
)
# → [(日期, 净值, 累计净值, 日涨跌幅), ...]
```

---

## 天天基金 — 前十大持仓（季度更新）

```
GET https://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code={CODE}&topline=10&year=&month=
```

---

## 新浪财经 — 指数行情（降级方案）

东财不可用时使用。

```bash
curl -s -H "Referer: https://finance.sina.com.cn" \
  "https://hq.sinajs.cn/list=sh000001,sz399001,sz399006,sh000688"
```

**响应**（GBK 编码）：
```
var hq_str_sh000001="上证指数,4053.58,4031.15,...";
```

> GBK → UTF-8: `content.decode('gbk')`

**常用指数代码**：

| 代码 | 指数 |
|------|------|
| sh000001 | 上证指数 |
| sz399001 | 深证成指 |
| sz399006 | 创业板指 |
| sh000688 | 科创 50 |

---

## 基金代码规律

| 前缀 | 类型 | 典型持有建议 |
|------|------|------------|
| 00XXXX | 混合型 | C 类持有 ≥30 天零赎回费 |
| 16XXXX | QDII | 常限购，多只绕开是合法策略 |
| 51XXXX | ETF 联接 | A 类适合长持 (>2 年) |
| 5XXXXX | 交易所 ETF | 需证券账户 |

---

## C 类 vs. A 类

| | C 类 | A 类 |
|------|------|------|
| 申购费 | ¥0 | 0.15%（支付宝折扣后） |
| 管理费 | 0.5-0.8%/年 | 0.15-0.5%/年 |
| 赎回费 | ≥30 天 ¥0 | 持有越久越低 |
| 适合 | 定投 / 持有 <2 年 | 一次性投入 / 持有 >2 年 |

**原则**：定投用户选 C 类。
