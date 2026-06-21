# 天天基金 API 参考文档

## 实时估值（盘中）

**接口：**
```
GET https://fundgz.1234567.com.cn/js/{CODE}.js
```

**响应格式（JSONP）：**
```json
jsonpgz({
  "fundcode": "000001",
  "name": "示例基金名称",
  "jzrq": "2026-01-01",
  "dwjz": "1.2345",
  "gsz": "1.2500",
  "gszzl": "1.26",
  "gztime": "2026-01-02 15:00"
})
```

**字段说明：**

| 字段 | 含义 |
|------|------|
| `fundcode` | 6 位基金代码 |
| `name` | 基金全称 |
| `jzrq` | 上一交易日净值日期 |
| `dwjz` | 上一交易日单位净值 |
| `gsz` | 盘中估算净值 |
| `gszzl` | 今日估算涨跌幅（%） |
| `gztime` | 估算时间戳 |

**curl 示例：**
```bash
curl -s "https://fundgz.1234567.com.cn/js/000001.js"
```

**⚠️ JSONP 解析——禁止使用 `str.lstrip()`：**
`str.lstrip('jsonpgz(')` 是逐字符剥离，不是前缀剥离，会损坏 JSON。必须用切片：
```python
raw = response  # 'jsonpgz({...});'
inner = raw[len("jsonpgz("):-2]  # 去除前缀和尾部 ');
data = json.loads(inner)
```
这是最常见的解析失败原因。

**注意：** QDII 基金更新时点不同（例如美股基金约北京时间凌晨 4:00），`gztime` 字段会体现。

## 历史净值

**接口：**
```
GET https://fundf10.eastmoney.com/F10DataApi.aspx?type=lsjz&code={CODE}&page=1&sdate={YYYY-MM-DD}&edate={YYYY-MM-DD}&per=20
```

**响应：** `var apidata={ content:"<table>...</table>" }` 包裹的 HTML 表格。

**正则解析（Python，macOS 无 `grep -P`）：**
```python
import re
navs = re.findall(
    r'<td>(\d{4}-\d{2}-\d{2})</td>\s*<td[^>]*>([\d.]+)</td>\s*<td[^>]*>([\d.]+)</td>\s*<td[^>]*>([^<]+)</td>',
    html_content
)
# 返回: [(日期, 净值, 累计净值, 日涨跌幅), ...]
```

## 基金持仓（前十大，季度更新）

**接口：**
```
GET https://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code={CODE}&topline=10&year=&month=
```

**响应：** 含股票代码、名称、权重%、持有股数、市值的 HTML 表格。

## 基金代码规律

| 代码模式 | 典型类型 |
|----------|---------|
| 00XXXX | 混合型 |
| 01XXXX | 股票型或新发混合型 |
| 16XXXX | QDII |
| 51XXXX | ETF |
| 58XXXX | 科创 50 ETF |
| 5XXXXX | 交易所上市 ETF |

## C 类与 A 类对比

- **C 类**（例如 000001）：零申购费，持有 ≥30 天免赎回费。管理费略高（约 0.5-0.8%/年）。**适合定投 / 持有 <1 年。**
- **A 类**：前端申购费（支付宝常折至 0.15%）。管理费更低。**适合一次性投入 / 持有 >2 年。**

大多数定投用户应选择 C 类基金。

## 常见指数与基金映射

- **沪深 300:** 大盘宽基
- **中证 500:** 中盘宽基
- **纳斯达克 100:** 美股科技龙头，通过 QDII 渠道
- **中证红利:** A 股高股息策略
- **国证芯片/半导体:** 半导体产业链
- **黄金:** 黄金 ETF 联接
- **科创 50:** 科创板科技

## 资产分类

### 按类型

- **宽基指数:** 沪深 300、中证 500、上证 50
- **行业主题:** 半导体/芯片、新能源、医药
- **QDII:** 纳斯达克 100、标普 500、全球配置
- **债券:** 纯债、可转债、信用债
- **商品:** 黄金 ETF 联接、资源优选
- **策略:** 红利、低波动、等权
