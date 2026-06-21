#!/usr/bin/env python3
"""Fetch real-time estimated NAVs from Eastmoney (天天基金) for all funds in portfolio.

Usage:
    python3 scripts/fetch_all_nav.py               # auto-detect from portfolio-state.md
    python3 scripts/fetch_all_nav.py 000001 002003 # query specific fund codes

Auto-detection: reads references/portfolio-state.md and extracts 6-digit fund codes
from the holdings table. Falls back to the hardcoded `funds` list if portfolio-state.md
is not found or contains only XXXXXX placeholders.

Output: table with name, previous NAV, estimated NAV, change %, update time.
Requires: Python 3.8+ (stdlib only — urllib + json).
"""
from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import List


# ── Fund codes (fallback: only used when portfolio-state.md not found) ──
funds: List[str] = [
    # "XXXXXX", "XXXXXX",
]


# ── Auto-detect from portfolio-state.md ──────────────────
def _codes_from_portfolio_state() -> List[str]:
    """Parse 6-digit fund codes from references/portfolio-state.md holdings table."""
    state_file = Path(__file__).parent.parent / "references" / "portfolio-state.md"
    if not state_file.exists():
        return []

    text = state_file.read_text()
    # Match | XXXXXX | in the holdings table — 6-digit fund codes
    codes = re.findall(r"\|\s*(\d{6})\s*\|", text)
    # Filter out placeholder codes (XXXXXX → re won't match since X is not \d)
    return list(dict.fromkeys(codes))  # dedup, preserve order


# ── Fetch logic ─────────────────────────────────────────
API = "https://fundgz.1234567.com.cn/js/{code}.js"


def fetch_one(code: str) -> dict | None:
    """Fetch NAV estimate for a single fund code. Returns dict or None on error."""
    try:
        url = API.format(code=code)
        raw = urllib.request.urlopen(url, timeout=10).read().decode()
        # Strip JSONP wrapper: jsonpgz({...});
        inner = raw[len("jsonpgz("):-2]
        return json.loads(inner)
    except Exception as exc:
        print(f"[{code}] ERROR: {exc}", file=sys.stderr)
        return None


def main(codes: List[str]) -> int:
    if not codes:
        print("No fund codes found.",
              "Place your fund codes in references/portfolio-state.md or pass them as arguments.",
              "Usage: python3 fetch_all_nav.py [CODE ...]", sep="\n", file=sys.stderr)
        return 1

    results = []
    for code in codes:
        data = fetch_one(code)
        if data:
            results.append(data)
            # name | prev NAV | estimated NAV | change% | timestamp
            print(f"{data['name']:<28s} | 昨收:{data['dwjz']} | "
                  f"估算:{data['gsz']} | 涨幅:{data['gszzl']:>6}% | {data['gztime']}")

    if not results:
        print("No fund data retrieved.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    # Priority: CLI args > portfolio-state.md > hardcoded list
    if len(sys.argv) > 1:
        codes = sys.argv[1:]
    else:
        codes = _codes_from_portfolio_state() or funds
    raise SystemExit(main(codes))
