#!/usr/bin/env python3
"""1103 card pool lookup (names in four languages + type / ATK / DEF / level / setcode). Works offline.

  python cards.py <id|name> [...]                 look up by id or name substring (any language)
  python cards.py --set 0x103d [--atk 1000] [--main]
                                                  list cards of an archetype (setcode), optionally with
                                                  a given current-printed ATK, main-deck monsters only
  python cards.py --db <dir> <id|name> [...]      use cards.cdb files (<dir>/zh-CN, ja-JP, ...) instead
                                                  of the bundled ../references/cards-1103.tsv

Output: id | alias | zh | ja | en | ko | type | ATK/DEF | Lv | setcode.
--main keeps monsters that can be in the Main Deck (not Fusion / Synchro / Xyz). A setcode matches
when any of its four 16-bit parts equals the given one, or (for sub-archetypes such as 0x103d) when
the low 12 bits match and the high 4 bits are included (YGOPro IsSetCard semantics).
Use the Japanese name exactly as printed for yugioh-wiki page names and Kanpatei headings.
"""
import os
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TSV = os.path.join(HERE, '..', 'references', 'cards-1103.tsv')
LANGS = ('zh-CN', 'ja-JP', 'en-US', 'ko-KR')
TYPE_MONSTER, EXTRA = 0x1, 0x40 | 0x2000 | 0x800000


def load_tsv():
    rows = {}
    with open(TSV, encoding='utf-8') as f:
        header = next(f).rstrip('\n').split('\t')
        for line in f:
            c = dict(zip(header, line.rstrip('\n').split('\t')))
            rows[int(c['id'])] = {
                'alias': int(c['alias']), 'names': [c['zh'], c['ja'], c['en'], c['ko']],
                'type': int(c.get('type', '0x0'), 16), 'atk': int(c.get('atk', 0)), 'def': int(c.get('def', 0)),
                'level': int(c.get('level', 0)), 'setcode': int(c.get('setcode', '0x0'), 16)}
    return rows


def load_db(root):
    rows = {}
    for idx, lang in enumerate(LANGS):
        path = os.path.join(root, lang, 'cards.cdb')
        if not os.path.exists(path):
            continue
        db = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
        for cid, alias, typ, atk, de, lvl, setcode in db.execute(
                'select id, alias, type, atk, def, level, setcode from datas'):
            r = rows.setdefault(cid, {'alias': alias, 'names': [''] * 4, 'type': typ, 'atk': atk, 'def': de,
                                      'level': lvl & 0xff, 'setcode': setcode})
            name = db.execute('select name from texts where id=?', (cid,)).fetchone()
            r['names'][idx] = name[0] if name else ''
    if not rows:
        sys.exit(f'no cards.cdb under {root}/<lang>/')
    return rows


def is_set(setcode, want):
    for k in range(4):
        part = (setcode >> (16 * k)) & 0xffff
        if part and (part & 0xfff) == (want & 0xfff) and (part & want & 0xf000) == (want & 0xf000):
            return True
    return False


def show(cid, r):
    t = r['type']
    stats = f"{r['atk']}/{r['def']} | Lv{r['level']}" if t & TYPE_MONSTER else '- | -'
    kind = 'extra' if t & EXTRA else ('monster' if t & TYPE_MONSTER else ('spell' if t & 0x2 else 'trap'))
    print(f"{cid} | alias {r['alias']} | " + ' | '.join(n or '-' for n in r['names'])
          + f" | {kind} {hex(t)} | {stats} | set {hex(r['setcode'])}")


def main(argv):
    def take(flag, has_value=True):
        if flag not in argv:
            return None
        i = argv.index(flag)
        value = argv[i + 1] if has_value else True
        del argv[i:i + (2 if has_value else 1)]
        return value
    db = take('--db')
    want_set, want_atk, main_only = take('--set'), take('--atk'), take('--main', False)
    rows = load_db(db) if db else load_tsv()
    if want_set:
        s = int(want_set, 16)
        hits = [cid for cid, r in rows.items() if is_set(r['setcode'], s)
                and (want_atk is None or (r['type'] & TYPE_MONSTER and r['atk'] == int(want_atk)))
                and (not main_only or (r['type'] & TYPE_MONSTER and not r['type'] & EXTRA))
                and not r['alias']]
        for cid in sorted(hits, key=lambda c: (rows[c]['atk'], c)):
            show(cid, rows[cid])
        print(f'{len(hits)} cards')
        return
    if not argv:
        sys.exit(__doc__)
    for q in argv:
        hits = [int(q)] if q.isdigit() and int(q) in rows else (
            [] if q.isdigit() else [cid for cid, r in rows.items() if any(q in n for n in r['names'])])
        if not hits:
            print(f'{q}: not in the 1103 pool')
        for cid in sorted(hits)[:50]:
            show(cid, rows[cid])
        if len(hits) > 50:
            print(f'  ... {len(hits) - 50} more; narrow the query')


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    main(sys.argv[1:])
