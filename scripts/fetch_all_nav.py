"""Fetch real-time estimated NAVs for all funds in portfolio.
Usage: python3 scripts/fetch_all_nav.py
Replace the 'funds' list with your own fund codes."""
import urllib.request
import json
import sys

# Replace with your fund codes:
funds = [
    # "XXXXXX", "XXXXXX", ...
]

results = []
for code in funds:
    try:
        url = f"https://fundgz.1234567.com.cn/js/{code}.js"
        raw = urllib.request.urlopen(url, timeout=10).read().decode()
        # Strip jsonpgz(...); wrapper
        inner = raw[len("jsonpgz("):-2]
        d = json.loads(inner)
        results.append(d)
        # Format: name | dwjz | gsz | gszzl% | gztime
        print(f"{d['name']:<28s} | 昨收:{d['dwjz']} | 估算:{d['gsz']} | 涨幅:{d['gszzl']:>6}% | {d['gztime']}")
    except Exception as e:
        print(f"{code} ERROR: {e}", file=sys.stderr)

if not results:
    print("No fund data retrieved.", file=sys.stderr)
    sys.exit(1)
