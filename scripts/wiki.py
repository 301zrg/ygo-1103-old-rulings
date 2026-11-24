#!/usr/bin/env python3
"""yugioh-wiki (https://yugioh-wiki.net/) history-version lookup. Python 3.8+, standard library only.

Card pages are named 《日本語カード名》 and the page name in the URL is EUC-JP encoded; page
content itself is UTF-8. Proxies come from the usual HTTPS_PROXY / HTTP_PROXY variables.

  python wiki.py versions <page>                list every archived version (age, archive time)
  python wiki.py show     <page> [kw|kw] [age]  Q&A / dated lines of one version (default: last
                                                version archived before 2011-09-02), filtered
  python wiki.py grep     <page> <kw|kw> [age]  every line of one version containing a keyword
  python wiki.py first    <page> <phrase>       earliest version containing <phrase> (binary search)
  python wiki.py url      <page> <age>          the history-version URL to cite (offline)
  python wiki.py list     <page>                the history-list URL (offline)

<page> is a Japanese card name without 《》 (added automatically), a term page name with a
leading "=" (e.g. "=ライトロード"), or a 1103 card id (looked up in ../references/cards-1103.tsv,
or in a ja-JP cards.cdb given with --cdb).
`url` and `list` need no network: when this sandbox cannot reach yugioh-wiki.net, compute the
URL here and open it with the platform's own web-fetch / browsing tool instead.
Downloads are cached in ./cache next to this script (one file per URL, hashed names).
"""
import hashlib
import html
import os
import re
import sqlite3
import sys
import urllib.parse
import urllib.request

CUTOFF = '2011/09/02'  # versions archived before this date are "pre-cutoff"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'cache')
BASE = 'https://yugioh-wiki.net/index.php?cmd=backup&page='


def get(url):
    os.makedirs(CACHE, exist_ok=True)
    key = os.path.join(CACHE, hashlib.sha1(url.encode()).hexdigest())
    if os.path.exists(key):
        with open(key, encoding='utf-8') as f:
            return f.read()
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (old-ruling research)'})
    text = urllib.request.urlopen(req, timeout=60).read().decode('utf-8', 'replace')
    with open(key, 'w', encoding='utf-8') as f:
        f.write(text)
    return text


def page_name(arg, cdb=None):
    if arg.startswith('='):
        return arg[1:]
    if arg.isdigit():
        if cdb:
            row = sqlite3.connect(f'file:{cdb}?mode=ro', uri=True).execute(
                'select name from texts where id=?', (int(arg),)).fetchone()
        else:
            tsv = os.path.join(HERE, '..', 'references', 'cards-1103.tsv')
            with open(tsv, encoding='utf-8') as f:
                row = next(((cols[3],) for cols in (l.rstrip('\n').split('\t') for l in f) if cols[0] == arg), None)
        if not row:
            sys.exit(f'card {arg} not in the 1103 pool (cards-1103.tsv / --cdb)')
        arg = row[0]
    return '《' + arg + '》'


def encode(name):
    # Full-width hyphen and wave dash have no EUC-JP form; the wiki uses the JIS characters.
    name = name.replace('－', '−').replace('～', '〜')
    return urllib.parse.quote(name.encode('euc_jp'))


def versions(p):
    s = get(BASE + p)
    return [(int(a), d) for a, _, d in re.findall(r'age=(\d+)"[^>]*>(\d+) \((.*?)\)</a>', s)]


def lines(p, age):
    raw = get(f'{BASE}{p}&age={age}')
    raw = re.sub(r'<script.*?</script>|<style.*?</style>', '', raw, flags=re.S)
    raw = re.sub(r'<(?:br|/li|/p|/dd|/dt|/h\d|/tr|/div)[^>]*>', '\n', raw)
    body = html.unescape(re.sub(r'<[^>]+>', '', raw))
    return [l.strip() for l in body.splitlines() if l.strip()]


def default_age(vs):
    pre = [v for v in vs if v[1] < CUTOFF]
    return (pre[-1] if pre else vs[0])[0]


def main(argv):
    cdb = None
    if '--cdb' in argv:
        i = argv.index('--cdb')
        cdb = argv[i + 1]
        del argv[i:i + 2]
    if len(argv) < 2:
        sys.exit(__doc__)
    cmd, name = argv[0], page_name(argv[1], cdb)
    p = encode(name)
    if cmd == 'url':
        return print(f'{BASE}{p}&age={int(argv[2])}')
    if cmd == 'list':
        return print(BASE + p)
    vs = versions(p)
    if not vs:
        sys.exit(f'{name}: no page / no history (check the exact Japanese name)')
    dates = dict(vs)
    if cmd == 'versions':
        print(f'{name}: {len(vs)} versions; last pre-cutoff age={default_age(vs) if vs[0][1] < CUTOFF else None}')
        for a, d in vs:
            print(f'  age={a}  {d}')
    elif cmd in ('show', 'grep'):
        kws = argv[2].split('|') if len(argv) > 2 and argv[2] else []
        age = int(argv[3]) if len(argv) > 3 else default_age(vs)
        print(f'{name} age={age} ({dates[age]})  {BASE}{p}&age={age}')
        all_lines = lines(p, age)
        if kws:
            keep = {i for i, l in enumerate(all_lines) if any(k in l for k in kws)}
            # A matching question must include its answer, and vice versa.
            # Wiki stores Ｑ and Ａ as separate lines; filtering each line drops the ruling.
            for i in list(keep):
                if re.match(r'^[ＱQ][：:]', all_lines[i]):
                    for j in range(i + 1, min(len(all_lines), i + 8)):
                        if re.match(r'^[ＱQ][：:]', all_lines[j]):
                            break
                        if re.match(r'^[ＡA][：:]', all_lines[j]):
                            keep.add(j)
                            break
                elif re.match(r'^[ＡA][：:]', all_lines[i]):
                    for j in range(i - 1, max(-1, i - 8), -1):
                        if re.match(r'^[ＡA][：:]', all_lines[j]):
                            break
                        if re.match(r'^[ＱQ][：:]', all_lines[j]):
                            keep.add(j)
                            break
            indices = sorted(keep)
        elif cmd == 'show':
            indices = [i for i, l in enumerate(all_lines)
                       if l[:1] in 'ＱＡQA' or re.search(r'\(\d\d/\d\d?/\d\d?\)', l)]
        else:
            indices = range(len(all_lines))
        for i in indices:
            print('  ' + all_lines[i][:500])
    elif cmd == 'first':
        phrase = argv[2]
        ages = [a for a, _ in vs]
        has = lambda a: any(phrase in l for l in lines(p, a))
        hits = [a for a in ages[::max(1, len(ages) // 12)] + [ages[-1]] if has(a)]
        if not hits:
            sys.exit(f'{name}: phrase not found in sampled versions; try a shorter phrase or `grep`')
        lo, hi = 0, ages.index(hits[0])
        while lo < hi:  # earliest version that has the phrase, assuming it stays once added
            mid = (lo + hi) // 2
            if has(ages[mid]):
                hi = mid
            else:
                lo = mid + 1
        a = ages[lo]
        line = next(l for l in lines(p, a) if phrase in l)
        print(f'{name} first age={a} ({dates[a]})')
        print(f'  {BASE}{p}&age={a}')
        print('  ' + line[:500])
        if lo > 0:
            print(f'  (previous age={ages[lo - 1]} does not contain it)')
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    main(sys.argv[1:])
