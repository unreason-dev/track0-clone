# OpenFRP77b (Holmes Basic) — Stage A transcription complete

**Date:** 2026-07-18 · **Node:** OpenFRP77b (Holmes Basic Set, 1977; PoB-756 TSR imprint)
**Phase:** Stage A (dual-pass verbatim digitization) — **COMPLETE**

## Summary

All 48 single-leaf pages of `Holmes-Basic.pdf` are transcribed to the block-model
schema and validated. `checkpoint.py --work OpenFRP77b` reports **48/48, 0 invalid**.
Block content-hash provenance stamped and confirmed deterministic (byte-identical on
rerun).

- **48 pages**, **718 blocks**
- Verbatim intermediate frozen (typos preserved with `as printed.` notes; errata NOT
  applied at this layer — that is D-6, deferred to extraction).
- Grind executed by the Opus 4.8 session (pp. 32–48) continuing the Fable 5 session
  (pp. 01–31). Block grammar carried over unchanged from OpenFRP74 — zero schema
  changes; the 74 block model absorbed Holmes's typeset two-column print, the full
  8-column treasure table, the keyed sample-dungeon room descriptions, the play-of-play
  dialogue, and the perforated reference-tables sheet without new structures.

## Differ queue (D-3 adjudication)

`checkpoint` differ: **9 pages clean, 39 pages queued.** Every queued page resolves to
the **same benign class** — pass-1 (embedded OCR) digit-multiset noise, not a pass-2
transcription defect. No page required a pass-2 correction; **nothing surfaced to the
operator as genuinely confusing.** The recurring signatures:

- **Split-vs-merged numerals.** Pass-1 OCR concatenates adjacent numbers that the print
  spaces apart. The ability stat lines are the cleanest example — `S12 I10 W9 C13 D10
  C12` reads to pass-1 as merged tokens (`110`, `116`, `1212`, `114`…), to pass-2 as the
  individual scores (`12,10,9,13,10,12`). Same on the price/probability tables (p34, p45,
  p47, p48). Pass-2 matches the image in every spot-checked case.
- **Figure-embedded numerals are asymmetric.** Numbers living inside `figure` blocks
  (map labels, the POB-756 / ZIP-53147 imprint, dungeon dimensions on the map) are
  described, not tabulated, so they count on the pass-1 side but not the pass-2 side —
  showing as harmless `pass1_only` residue (p38, p41, p46).
- **Cross-reference / note digits** I added in `transcriber_note`s (e.g. "p. 35",
  "p. 37", roll references) count on the pass-2 side as harmless `pass2_only` `1`s and
  small numbers (p32, p44, p14, p15, p47).

Adjudication verdict: **queue closed, 0 escalations.** (Protocol D-3: agent adjudicates;
only genuinely-confusing residues go to Jon. There are none.)

## Uncertain tokens (5, all low-stakes, all recorded)

| Page | Token | Disposition |
|---|---|---|
| hb-p12 | `25 / 10` | 2+1 gem/jewelry row read by table position (between scan lines) |
| hb-p38 | `DOMED CITY` | hand-lettered map label; 4th glyph ambiguous (could read "DOMEO") |
| hb-p41 | `RT` | map label — **now resolved**: p44 keys `RT` = **Rat Tunnels** |
| hb-p41 | `c` | far-east hatched corridor keyed lowercase "c" = room/feature C |
| hb-p47 | `Saddle Bags` | printed "Saddle Bcgs" (ink-filled 'a') |

None blocks extraction; the `RT` map ambiguity self-resolved once the keyed descriptions
were reached.

## Delta inventory (input to Stage B census)

12 pages carry `77b delta:` / `77b internal:` transcriber flags (16 flag occurrences),
grep-able for the Stage B delta census against the ratified 74 node graph. Notable
structural deltas already visible vs OpenFRP74:

- **Coinage.** 77b adds **electrum** and **platinum** to the copper/silver/gold of 74
  (p33 exchange table; treasure table gains EP/PP columns).
- **Treasure types.** 77b treasure table (p34) is an 8-column page-wide matrix with
  **types A–T** (74 stops earlier); adds individual-carried coin types (J–N),
  gem/jewelry-only (Q), and potion/scroll-only (S, T). "Make them rollable" (operator
  ruling) is directly supported — every cell is `range:percentage` or `n pieces per
  individual`.
- **Internal name drift within 77b itself** (determination table vs description):
  Speed/Haste, Flying/Fly, "Secret Door" vs "Secret Doors", "Fire Ball" vs "Fire Balls",
  "Miscellaneous Magic Items" vs "…Item" — all flagged on pp. 35–37 for the extractor.

## D-7 names present (punch-list, stand verbatim in base corpus)

8 pages flag D-7 names: **hobbit(s)** (pp. 14, 39, 40, 44, 47), **Barrow wights "as per
Tolkien"** (p32), **Tolkien / Middle Earth / Lord of the Rings** and Fritz Leiber / Robert
E. Howard / Gardner F. Fox literary refs (p40), the **"THE HOBBIT" / Battle of the Five
Armies** catalogue entry (p46), **Hobbits** in the saving-throw class list (p47). Per D-7
these stand in the base corpus; the scrub ships as the separate homebrew swap-package.

## Program-adjacent note: CHAINMAIL

The p46 catalogue lists **CHAINMAIL — "Rules for Medieval Miniatures (plus Fantasy)"**,
the ancestor system slated for the program's **openfwg1972** node. Recorded here as a
scope pointer, not chartered.

---

## OPERATOR DECISION NEEDED — missing printed page 13 (D-6-adjacent)

**The gap (unchanged):** printed page **13** is physically absent from this PDF copy —
the scan runs printed 12 (pdf p13) straight to printed 14 (pdf p14). The lost page held
the **MAGIC SPELLS intro tail + the SAVING THROWS section, including the primary
saving-throw table.** Pass-1 confirms the same gap; it is unrecoverable *as running text*
from this copy. (Recorded at hb-p14; not a transcription error.)

**New development that changes the calculus.** The perforated tear-out reference sheet at
the back — **printed page 47** — contains a **`Saving Throw Table — Levels 1 to 3`**
(class × Spell/Staff, Wand, Death Ray/Poison, Turned to Stone, Dragon Breath). This is
almost certainly the *same numeric matrix* that appeared on the lost p13 (or a
values-identical duplicate), captured fully in `hb-p47.pass2.json`. So the **mechanical
content of the saving-throw table is very likely already in-corpus**, recovered from the
book's own reference sheet — no external witness needed for the *numbers*.

**What is still genuinely lost** is the *prose* of the SAVING THROWS section on p13 (the
explanatory text around the table) and the tail of the MAGIC SPELLS intro. Only expression
was lost there, and we don't ship source expression anyway (the firewall re-authors it).

**The ruling I need from you** — pick one; this is yours, not mine (cf. the 74 p24
precedent where an errata line saved us — here no errata sheet exists):

1. **Treat p13 as recovered-in-copy for mechanics.** Use the p47 reference table as the
   authoritative saving-throw matrix for Levels 1–3, record the p13 *prose* as a
   permanent, dated gap in the interpretation records, and proceed. (My recommendation —
   the mechanics are what we extract, and they're present.)
2. **Restore from an external witness.** Source another scan/copy of Holmes Basic p13 to
   recover the prose and confirm the table byte-for-byte before extraction.
3. **Leave a pure recorded gap.** Note the p13 loss and do *not* lean on p47 (treat the
   two as independent), pending your review.

I've made no assumption in the corpus yet — the gap and the p47 table are both recorded
verbatim; nothing is reconciled until you rule.

## Next (Stage B — awaiting go)

Delta census against the ratified 74 node graph
(`findings/openfrp74-d5-node-graph-2026-07-17.md`), charter §9 delta pipeline. **Will ask
before starting extraction.**
