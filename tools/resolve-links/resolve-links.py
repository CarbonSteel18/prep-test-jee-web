#!/usr/bin/env python3
"""
Parse a list of "Title | Drive URL" lines (or the raw links you already
have on your clipboard) and emit data/papers.json.

Usage:
    python resolve-links.py links.txt > ../../data/papers.json
"""
import json, re, sys
from collections import OrderedDict

ID_RE = re.compile(r"/file/d/([A-Za-z0-9_-]{20,})")
TITLE_RE = re.compile(
    r"JEE Main (\d{4}) \((\d{2}) (\w{3}) Shift (\d)\).*? - MathonGo"
)

def parse_line(line):
    line = line.strip()
    if not line or ' | ' not in line:
        return None
    title, url = line.split(' | ', 1)
    m = TITLE_RE.search(title)
    if not m:
        return None
    year, day, month, shift = m.groups()
    fid = ID_RE.search(url)
    if not fid:
        return None
    return year, month, int(shift), f"{day} {month}", fid.group(1)

def main():
    out = OrderedDict()
    for line in sys.stdin:
        parsed = parse_line(line)
        if not parsed:
            continue
        year, month, shift, d, fid = parsed
        out.setdefault(year, OrderedDict()).setdefault(month, []).append(
            {"d": d, "s": shift, "i": fid}
        )
    # sort years descending
    ordered = OrderedDict(
        sorted(out.items(), key=lambda kv: kv[0], reverse=True)
    )
    print(json.dumps(ordered, indent=2))

if __name__ == "__main__":
    main()