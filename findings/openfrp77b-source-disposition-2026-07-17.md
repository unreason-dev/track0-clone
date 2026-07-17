# OpenFRP77b — source disposition: Holmes Basic (2026-07-17)

## Source

`/Users/jon/dev/ai/reference/Holmes-Basic.pdf` — 48 pages, **single-leaf
portrait scans** (CanoScan 9000F, 599×772 pt), text layer by Adobe Acrobat
11 Paper Capture (2013). Imprint: "© 1974, 1977 TACTICAL STUDIES RULES /
TSR HOBBIES, INC. POB 756" — the same PoB 756 hand-inked onto the
OpenFRP74 Correction Sheet, dating that slip to the 1977 transition.
Edited by Eric Holmes; "Rules for Fantastic Medieval Role Playing
Adventure Game Campaigns"; basic game, levels 1-3 only.

## Suitability

Substantially friendlier than the 1974 scan:
- **No spreads** — the whole gutter-splitting apparatus is bypassed;
  digitized via the new `tools/render_singles.py` (same manifest shape,
  `checkpoint.py --work OpenFRP77b` works unchanged).
- **Typeset two-column layout**, clean and high-contrast; tables crisp.
- **Pass-1 quality is a different class from 74's**: zero hits on the
  %→"0k" failure-class grep; statlines parse cleanly ("Move: 120
  feet/turn"); residual noise is light l/1 and display-face mangling
  ("BUlfilOIS l DB!IOIS" for the logo). Expect a small disagreement queue.
- **New artifact class: show-through** — the reverse page's ink mirrors
  faintly through (seen mid-page on p20). Transcriber convention: ignore
  mirrored bleed-through; it is not page content. (Same family as 74's
  facing-page slivers.)

## Pipeline deltas recorded

- `tools/render_singles.py` (new, public): single-leaf sibling of
  split_spreads.py — render + per-page pass-1 + hashed manifest.
- `tools/checkpoint.py` gains `--work` (default OpenFRP74).
- Labels are `hb-p01..hb-p48` by PDF order (claims); printed page numbers
  observed independently during the vision pass per the 74 convention.

## Expected content deltas for the census (77b vs 74 graph)

Five-point alignment (two-axis), the Thief class, 3-level progression cap,
scroll-scribing rules, d8-era hit dice conventions, expanded monster list,
"Dungeon Master" vocabulary. These are graph-walk deltas per charter §9 —
the delta pipeline's first live test.

## LoE (operator-requested, 2026-07-17)

Stage A ≈ one session (pipeline adaptation done in under an hour; 48-page
vision grind; adjudication under ratified D-3 expected small). Stage B
census fast (taxonomy carries over). Stage C is the delta pipeline's first
real test — estimated 1-2 sessions, low confidence by nature.
