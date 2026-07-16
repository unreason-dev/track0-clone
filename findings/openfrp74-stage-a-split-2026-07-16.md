# OpenFRP74 Stage A — spread split run, 2026-07-16

`tools/split_spreads.py` run against the source scan (sha256 recorded in the
local pages-manifest). 122 page records, zero warnings: each 2-up spread
rendered at 300 DPI, gutter-split by darkness scan, per-half embedded-text
extraction (pass 1) alongside each page image, provenance manifest with
per-file content hashes. Outputs are local-only intermediates
(`OpenFRP74/digitization/pages/`, gitignored).

## Structure confirmed

| Unit | PDF pages | Records | Numbered pages |
|---|---|---|---|
| v1 Men & Magic | 1–20 | 39 | 2–37 (36 + cover/ifc/title) |
| v2 Monsters & Treasure | 21–42 | 43 | 2–41 (40 + cover/ifc/title) |
| v3 Underworld & Wilderness Adventures | 43–62 | 39 | 2–37 (36 + cover/ifc/title) |
| errata Correction Sheet | 63 | 1 | single leaf |

- Printed page numbers verified against arithmetic claims on 6 sampled
  halves (v1 18/19, v2 2/3, v3 2/3) — mapping holds. Full verification of
  every claim lands with the vision pass.
- Booklet tails identified: v1 ends in TSR product ads + blank inside
  cover; v2 in the Graphic Printing Company colophon; v3 in reference
  charts. Their arithmetic labels stand as claims.
- Split-quality spot check (v2-p03, the Monster Reference Table): no
  clipped text, minor spine strip at the bound edge, faint reverse-side
  bleed-through that does not obstruct reading.

## Discovery: the Correction Sheet (PDF p63)

The final PDF page is not V3 p38 — it is the **single-leaf Correction Sheet
errata insert** shipped with early printings (caught by the splitter's
aspect-ratio self-check: single page where the layout map expected a
spread). It carries TSR's own corrections to all three booklets, e.g.
"Page 9: add Griffons under the Neutrality column," "Page 22, line 21: the
'T' cross index for Zombie/Adept should be 7."

Consequences:

1. It is registered as its own work (`errata-sheet`), not a V3 page.
2. **Design question for the fidelity policy** (queued for operator
   disposition alongside the charter's interpretation-record machinery):
   where the Correction Sheet contradicts a booklet page, which reading is
   the typed value? The insert is part of the same shipped printing — this
   is source-internal errata, not a later edition. Candidate posture:
   booklet reading in `_raw`, corrected value typed, correction-sheet
   provenance on the correction — but this is an operator call, batched
   with the other §11 decisions.
3. The sheet's existence is printing-identification evidence (early
   printings shipped it) — consistent with the pre-excision text findings
   in the source-disposition memo.

## Next

Pass 2 (LLM-vision transcription) + the disagreement queue over the split
pages; then the pilot census (charter §5).
