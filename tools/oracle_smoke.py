#!/usr/bin/env python3
"""OpenFRP74 rules-oracle smoke test — SPECIFIC TO OpenFRP74 (not --work generic).

The grind tools (checkpoint/render/stamp/diff) take --work; this harness is
keyed to the OpenFRP74 corpus and its question families. A sibling would be
written per system. Reads corpus from system/OpenFRP74/, transcripts from
digitization/OpenFRP74/, writes the frozen suite to tools/openfrp74-oracle-smoke/.

The oracle discipline (ttrpg-app docs/question-generation.md): frozen JSONL
suites of single-entity lookup questions with gold answers, resolved by a
deterministic engine. This harness does both halves for OpenFRP74:

1. SYNTHESIZE a question suite by walking the pass-2 intermediate (the
   PDF decode) — b170-style rows, gold values taken from the TRANSCRIPTS.
2. RESOLVE each question against the extracted corpus (system/OpenFRP74/*/) via
   typed paths — no LLM, pure lookups.

Because gold comes from the transcripts and answers from the corpus, a
mismatch is an extraction-fidelity finding, not a tautology. Expected
divergences (errata applied in the normalized layer per D-6) are declared
and scored as `expected_divergence`.

Output: tools/openfrp74-oracle-smoke/suite-openfrp74-smoke-01.jsonl (frozen-style
suite for later oracle integration) + a scored report on stdout.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / 'digitization' / 'OpenFRP74' / 'transcripts'
C = ROOT / 'system' / 'OpenFRP74'
OUT = ROOT / 'tools' / 'openfrp74-oracle-smoke'


def tr(pid):
    return json.loads((T / f'{pid}.pass2.json').read_text())


def corpus(rel):
    return json.loads((C / rel).read_text())


def slug(name):
    s = name.lower().replace("'", "").replace('.', '').replace(',', '')
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s


rows = []          # suite rows
results = []       # (id, status, note)


def check(qid, question, gold, got, path, *, expected_divergence=None, page=None):
    ok = (str(gold).strip() == str(got).strip())
    if ok:
        status = 'pass'
    elif expected_divergence:
        status = 'expected_divergence'
    else:
        status = 'FAIL'
    rows.append({
        'id': qid, 'source_page': page, 'question': question,
        'gold': {'value': str(gold), 'path': path,
                 'source': 'pass2-intermediate'},
        'resolved': str(got), 'expected_outcome': 'answer',
        'divergence_note': expected_divergence,
        'status': status})
    results.append((qid, status, expected_divergence or ''))


# ---------------- Family A: monster statlines (v2 reference table) --------
NAME_MAP = {
    'goblins/kobolds': ['monster-goblin', 'monster-kobold'],
    'hobgoblins/gnolls': ['monster-hobgoblin', 'monster-gnoll'],
    'skeletons/zombies': ['monster-skeleton', 'monster-zombie'],
    'men': ['monster-men'], 'manticoras': ['monster-manticora'],
    'dragons***': ['monster-dragon'], 'lycanthropes***': ['monster-lycanthrope'],
    'medusae': ['monster-medusa'], 'invisible stalkers': ['monster-invisible-stalker'],
    'elementals': ['monster-elemental'], 'djinn': ['monster-djinni'],
    'efreet': ['monster-efreeti'], 'pegasi': ['monster-pegasus'],
    'hippogriffs': ['monster-hippogriff'],
    'small insects or animals': ['monster-small-insects-or-animals'],
    'large insects or animals': ['monster-large-insects-or-animals'],
}
PLURAL_ONES = {'mule': 'monster-mule'}


def monster_ids(raw):
    key = re.sub(r'\s*/\s*', '/', raw.replace('\n', ' ')).strip().lower()
    if key in NAME_MAP:
        return NAME_MAP[key]
    base = slug(raw.replace('\n', ' '))
    cands = [f'monster-{base}']
    if base.endswith('ies'): cands.append(f'monster-{base[:-3]}y')
    if base.endswith('ves'): cands.append(f'monster-{base[:-3]}f')
    if base.endswith('es'): cands.append(f'monster-{base[:-2]}')
    if base.endswith('s'): cands.append(f'monster-{base[:-1]}')
    for cand in cands:
        if cand and (C / 'monsters' / f'{cand}.json').exists():
            return [cand]
    return []


qn = 0
for pid, blk in (('v2-p03', 3), ('v2-p04', 1)):
    for r in tr(pid)['blocks'][blk]['rows']:
        name = r[0].replace('\n', ' ').strip()
        ids = monster_ids(r[0])
        if not ids:
            results.append((f'A-{slug(name)}', 'SKIP-nomap', name))
            continue
        ent = corpus(f'monsters/{ids[0]}.json')
        # AC check (skip variable rows)
        ac_raw = r[2].strip()
        if ac_raw and 'ariable' not in ac_raw and ac_raw != '---' and 'referee' not in r[1]:
            qn += 1
            gold = ac_raw.split('/')[0] if '/' in ac_raw and len(ids) > 1 else ac_raw
            check(f'ofrp-smoke-A{qn:03d}',
                  f'what is the armor class of {ids[0][8:].replace("-", " ")}?',
                  gold, ent.get('armor_class_raw'),
                  f'{ids[0]}.armor_class_raw', page=pid)
        # % in lair
        if len(r) > 5 and r[5].strip() and r[5].strip() not in ('Nil', ''):
            qn += 1
            check(f'ofrp-smoke-A{qn:03d}',
                  f'what percentage of the time is {ids[0][8:].replace("-", " ")} found in its lair?',
                  r[5].strip(), ent.get('percent_in_lair_raw'),
                  f'{ids[0]}.percent_in_lair_raw', page=pid)

# ---------------- Family B: spell range/duration from entry prose ---------
spell_pages = [f'v1-p{n:02d}' for n in range(23, 35)]
for pid in spell_pages:
    d = tr(pid)
    for b in d['blocks']:
        t = b.get('text') or ''
        m = re.match(r'__([^_]{2,45}?):?__:?\s', t)
        if not m:
            continue
        name = m.group(1).strip().rstrip(':')
        sid = {'Dispell Magic': 'spell-dispel-magic',
               'Lightening Bolt': 'spell-lightning-bolt',
               'Telekenesis': 'spell-telekinesis',
               'Dispell Evil': 'spell-dispel-evil',
               'The Finger of Death': 'spell-finger-of-death',
               'Detect Invisible (Objects)': 'spell-detect-invisible-objects',
               'Phantasmal Forces': 'spell-phantasmal-forces',
               "Protection from Evil, 10' Radius": 'spell-protection-from-evil-10-foot-radius',
               "Protection from Evil, 10' radius": 'spell-protection-from-evil-10-foot-radius',
               'Invisibility, 10" Radius': 'spell-invisibility-10-foot-radius',
               'Purify Food & Water': 'spell-purify-food-and-water',
               'Growth of Plants': 'spell-growth-of-plants',
               'Growth of Animals': 'spell-growth-of-animals',
               'Contact Higher Plane': 'spell-contact-higher-plane',
               'Pass-Wall': 'spell-pass-wall',
               'Transmute Rock to Mud': 'spell-transmute-rock-to-mud',
               'Stone to Flesh': 'spell-stone-to-flesh',
               'Anti-Magic Shell': 'spell-anti-magic-shell',
               'Slow Spell': 'spell-slow-spell',
               'Haste Spell': 'spell-haste-spell',
               'Turn Sticks to Snakes': 'spell-turn-sticks-to-snakes',
               'Continual Light': 'spell-continual-light',
               'ESP': 'spell-esp',
               }.get(name, f'spell-{slug(name)}')
        f = C / 'spells' / f'{sid}.json'
        if not f.exists():
            if name not in ('Anti-Clerics', 'Numbers', 'ibility'):
                results.append((f'B-{slug(name)}', 'SKIP-nomap', name))
            continue
        ent = json.loads(f.read_text())
        rm = re.search(r'Range[:\s]+([0-9]+)"(?!\s*[+x/])', t)
        if rm and '+' not in t[rm.start():rm.end()+8]:
            qn += 1
            got = ent.get('range_inches')
            check(f'ofrp-smoke-B{qn:03d}', f'what is the range of {name.lower()}?',
                  rm.group(1), got if got is None else int(got),
                  f'{sid}.range_inches', page=pid)
        dm = re.search(r'Duration[:\s]+([0-9]+) turns(?!\s*[+])', t)
        if dm and not re.search(r'Duration[:\s]+[0-9]+ turns\s*\+', t):
            qn += 1
            got = ent.get('duration_turns')
            check(f'ofrp-smoke-B{qn:03d}', f'how long does {name.lower()} last?',
                  dm.group(1), got if got is None else int(got),
                  f'{sid}.duration_turns', page=pid)
        fm = re.search(r'Duration[:\s]+([0-9]+) turns\s*\+\s*(the level|the number of levels|level)', t)
        if fm:
            qn += 1
            got = (ent.get('duration_formula') or '')
            check(f'ofrp-smoke-B{qn:03d}', f'how long does {name.lower()} last (formula)?',
                  f"{fm.group(1)} + caster level", got,
                  f'{sid}.duration_formula', page=pid)

# ---------------- Family C: class XP thresholds (v1-p16) ------------------
classes = {1: ('classes/class-fighting-man.json', 'Fighting-Men'),
           2: ('classes/class-magic-user.json', 'Magic-Users'),
           3: ('classes/class-cleric.json', 'Clerics')}
for blk, (rel, cname) in classes.items():
    ent = corpus(rel)
    lv = {l['title']: l for l in ent['levels']}
    for r in tr('v1-p16')['blocks'][blk]['rows']:
        title = r[0].replace('*', '').strip()
        if title not in lv:
            results.append((f'C-{slug(title)}', 'SKIP-nomap', title))
            continue
        qn += 1
        check(f'ofrp-smoke-C{qn:03d}',
              f'how many experience points does a {cname[:-1].lower()} need to become a {title.lower()}?',
              r[1].strip(), lv[title]['xp'], f'{ent["id"]}.levels[{title}].xp',
              page='v1-p16')

# ---------------- Family D: attack matrix cells (v1-p19/p20) --------------
mx = corpus('matrices/matrix-attack-men.json')
cells = {r['label']: r['cells'] for r in mx['rows']}
for r in tr('v1-p19')['blocks'][8]['rows']:
    ac = r[0].strip()
    for ci, band in enumerate(mx['columns']):
        qn += 1
        check(f'ofrp-smoke-D{qn:03d}',
              f'what does a level {band} man need to hit armor class {ac}?',
              r[2 + ci].strip(), cells[ac][ci],
              f'matrix-attack-men[{ac}][{band}]', page='v1-p19')

# ---------------- Family E: treasure type cells (v2-p22) ------------------
tt_rows = tr('v2-p22')['blocks'][2]['rows']
CAT = ['copper', 'silver', 'gold']
for r in tt_rows:
    label = r[0].strip()
    if label in ('A',) or label.startswith(('Land', 'Desert', 'Water')):
        continue  # variant handling below
    letter = label.lower()
    if len(letter) != 1:
        continue
    ent = corpus(f'treasure-types/treasure-type-{letter}.json')
    trows = {x['category']: x for x in ent['variants'][0]['rows']}
    for ci, cat in enumerate(CAT):
        raw = r[1 + ci].strip()
        qn += 1
        got = trows[cat]['raw'].replace(' ', '')
        check(f'ofrp-smoke-E{qn:03d}',
              f'how much {cat} is in treasure type {letter.upper()}?',
              raw.replace(' ', ''), got,
              f'treasure-type-{letter}.{cat}.raw', page='v2-p22')

# ---------------- Family F: turning undead incl. errata cell --------------
mt = corpus('matrices/matrix-turning-undead.json')
tcells = {r['label']: r['cells'] for r in mt['rows']}
for r in tr('v1-p22')['blocks'][5]['rows']:
    und = r[0].strip()
    for ci in range(8):
        qn += 1
        gold = r[1 + ci].strip()
        got = tcells[und][ci]
        div = None
        if und == 'Zombie' and ci == 1:
            div = "errata: Correction Sheet corrects Zombie/Adept T -> 7 (applied in normalized layer)"
        check(f'ofrp-smoke-F{qn:03d}',
              f'can a {mt["columns"][ci].lower()} turn a {und.lower()}, and on what score?',
              gold, got, f'matrix-turning-undead[{und}][{mt["columns"][ci]}]',
              expected_divergence=div, page='v1-p22')

# ---------------- score ----------------
OUT.mkdir(exist_ok=True)
with open(OUT / 'suite-openfrp74-smoke-01.jsonl', 'w') as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')

from collections import Counter
tally = Counter(s for _, s, _ in results)
print(f"suite rows: {len(rows)}  |  {dict(tally)}")
for qid, s, note in results:
    if s == 'FAIL':
        row = next(r for r in rows if r['id'] == qid)
        print(f"  FAIL {qid}: {row['question']}  gold={row['gold']['value']!r} got={row['resolved']!r}  ({row['gold']['path']})")
    elif s == 'SKIP-nomap':
        print(f"  skip (no id map): {note}")
sys.exit(1 if tally.get('FAIL') else 0)
