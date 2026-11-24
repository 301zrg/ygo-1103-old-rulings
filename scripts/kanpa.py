#!/usr/bin/env python3
"""Kanpatei (寒波亭) "1103環境　主要カード　裁定まとめ" — download once, then search locally.
Python 3.8+, standard library only. Proxies come from HTTPS_PROXY / HTTP_PROXY.

  python kanpa.py fetch                 download the note body to ./cache/kanpa.txt (one line per paragraph)
  python kanpa.py section <name> [n]    the section whose heading line is exactly <name> (card name in
                                        Japanese, no 《》), n lines (default 40)
  python kanpa.py grep <kw|kw> [ctx]    every line containing a keyword, with ctx lines of context (default 1)

The note is at https://note.com/sabae5280/n/n95ba4b085cf6 . Its rulings are "the ruling closest to the
1103 period under Master Rule 2"; entries carry no dates, and some say 当時調整中 or give a later answer.
"""
import json
import os
import re
import html
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'cache')
TEXT = os.path.join(CACHE, 'kanpa.txt')
API = 'https://note.com/api/v3/notes/n95ba4b085cf6'


def fetch():
    os.makedirs(CACHE, exist_ok=True)
    req = urllib.request.Request(API, headers={'User-Agent': 'Mozilla/5.0 (old-ruling research)'})
    data = json.loads(urllib.request.urlopen(req, timeout=90).read().decode('utf-8'))
    body = data['data'].get('body', '')
    text = html.unescape(re.sub(r'<[^>]+>', '\n', body))
    out = [l.strip() for l in text.splitlines() if l.strip()]
    with open(TEXT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    print(f'{len(out)} lines -> {TEXT}  (title: {data["data"].get("name")}, published {data["data"].get("publish_at")})')


def load():
    if not os.path.exists(TEXT):
        fetch()
    with open(TEXT, encoding='utf-8') as f:
        return f.read().split('\n')


def main(argv):
    if not argv:
        sys.exit(__doc__)
    if argv[0] == 'fetch':
        return fetch()
    lines = load()
    if argv[0] == 'section':
        name, n = argv[1], int(argv[2]) if len(argv) > 2 else 40
        idx = [i for i, l in enumerate(lines) if l == name]
        if not idx:
            near = sorted({i for i, l in enumerate(lines) if name in l})[:15]
            sys.exit(f'no heading "{name}"; lines mentioning it: {[i + 1 for i in near]} (try grep)')
        for i in idx:
            print(f'== line {i + 1}: {name}')
            for l in lines[i + 1:i + 1 + n]:
                print('  ' + l[:400])
    elif argv[0] == 'grep':
        kws, ctx = argv[1].split('|'), int(argv[2]) if len(argv) > 2 else 1
        for i, l in enumerate(lines):
            if any(k in l for k in kws):
                print(f'-- line {i + 1}')
                for j in range(max(0, i - ctx), min(len(lines), i + ctx + 1)):
                    print(('> ' if j == i else '  ') + lines[j][:400])
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    main(sys.argv[1:])
