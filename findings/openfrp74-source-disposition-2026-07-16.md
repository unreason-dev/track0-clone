# OpenFRP74 — source disposition (initial look), 2026-07-16

Initial suitability assessment of the furnished source scan for the
OpenFRP74 pilot node (the 1974 three-booklet D&D set). Assessment performed
interactively with the operator at project start; probes were run against
the PDF's embedded text layer and page images. **Verdict: SUITABLE — proceed
to Stage A**, with the dual-pass transcription discipline mandatory for all
tables (evidence below).

The source file itself is local-only (`reference/` in the private working
tree) and is not part of this repo; this memo records what was measured.

## 1. Source identity

- Single PDF, 63 pages, ~30.9 MB. Scanner: CanoScan 9000F; embedded OCR
  layer produced by Adobe Acrobat 11 "Paper Capture" (scan dated 2013-03-02).
- Complete 1974 three-booklet set, scanned as **2-up spreads** (two facing
  booklet pages per PDF page; covers are single pages).
- ©1974 Tactical Studies Rules; Forward signed "E. Gary Gygax, Tactical
  Studies Rules Editor, 1 November 1973, Lake Geneva, Wisconsin."

### Booklet → PDF page map

| Booklet | PDF pages |
|---|---|
| Vol. 1, Men & Magic | 1–20 |
| Vol. 2, Monsters & Treasure | 21–42 |
| Vol. 3, The Underworld & Wilderness Adventures | 43–63 |

## 2. Printing identification: early, pre-Tolkien-excision

Term probes over the full text layer:

| Term | Result |
|---|---|
| Hobbit | present (V1 pp. 5–6 region; V3) |
| Halfling | **zero occurrences** |
| Ent | present (V1, V2, V3, incl. Monster Reference Table) |
| Treant | **zero occurrences** |
| Balrog | present throughout V2 incl. the Monster Reference Table row with stats |
| Nazgul | present (V2) |

This is an early printing predating TSR's own Tolkien-name excisions.
Consequences:

- **Naming punch list (charter §8) is concrete from day one.** Hobbit, Ent,
  Balrog, Nazgûl are the canonical distinctive-IP names; TSR's own later
  excisions are the disposition precedent. Mechanics survive under any
  disposition — the Balrog's table row is mechanical fact regardless of what
  the entity is named in the shipped corpus.
- Historically the more valuable text for the edge-changelog research
  artifact (the later-printing excisions become discoverable deltas if a
  later-printing node is ever added).

## 3. Image quality: excellent

Spot-checked spreads across all three booklets (covers, prose pages, and the
dense tables: Attack Matrix I & II, Saving Throw Matrix, Spells Table,
Monster Reference Table). Clean, high-contrast, no skew, no bleed-through;
every table cell legible at the image level. LLM-vision transcription (the
planned second pass) is fully supported by this scan quality.

## 4. Embedded OCR text layer: prose-grade only — UNTRUSTWORTHY for tables

The 2013 Acrobat text layer is usable as one transcription pass for prose,
with known error classes. For numeric tables it exhibits exactly the silent
corruption the charter's Stage A discipline anticipates. Verified by
cell-level diff of the extracted text against the page images:

**Monster Reference Table (V2 p. 3 / PDF p. 22) — verified failures:**

- **Silent cell dropout**: the Orcs row's Hit Dice value (`1`) is absent
  from the extracted text entirely. Attack Matrix rows on the same probe
  extracted clean — the failure is row-dependent and silent.
- **Systematic range-bound loss**: Number Appearing ranges of the form
  `1 - N` extract as bare `N` on many rows (Giants, Mummies, Spectres,
  Vampires, Cockatrices, Basilisks, Medusae, Gorgons, Manticoras). A naive
  reader would take "Mummies: 12" as the value where the page says
  "1 – 12."
- **Percent-sign mangling**: 20% → `2()0A,`; 60% → `60".-b`; 10% → `10"k`.
- **2-up interleaving**: the text layer merges facing booklet pages in
  scrambled reading order (V2's INDEX page is woven line-by-line into the
  Monster Reference Table). Reading order from the raw layer is unusable
  without page splitting.

**Prose-region error classes (V1 pp. 18–21 / PDF pp. 11–12 probe):**

- `c→o` confusion: score → `soore` (systematic — digit-adjacent hazard
  class; treat 0/O, 5/S, 3/8, 1/l/I as suspect corpus-wide).
- `L→l` case collapse throughout; Lock → `lack`; turn → `tum`;
  horn → `hom`; move → `mave`; written → `w!itten`; % → `o/o`.
- Title-face lines garble completely (cover logotypes).

**Contrast**: the Attack Matrix I/II and Saving Throw Matrix numeric cells
extracted correctly in the same probe — so the layer is not uniformly bad,
which is precisely what makes its failures dangerous. One clean table proves
nothing about the next.

## 5. Period-fidelity register (seed)

Source readings observed that must be preserved as source facts, not
silently corrected (fidelity policy per the charter — record, don't fix):

- `% In Liar` — Monster Reference Table column header (V2 p. 3).
- `seperate` (V2 p. 3), `descretion` (Sea Monsters row, V2 p. 3),
  `Paralization` (Saving Throw Matrix, V1 p. 20), `indefinately`
  (V3, naval rules).

These are the seed of the node's tolerance/correction register; Stage A's
transcription carries them verbatim with the normalization documented.

## 6. Stage A implications (design consequences of this assessment)

1. **Split spreads first**: each PDF page must be split into its two booklet
   pages so provenance can be keyed `{work, booklet, page, block-index,
   content-hash}` — the 2-up interleaving makes the raw text layer's
   reading order unusable otherwise.
2. **Dual-pass transcription**: embedded text layer as pass 1 (prose-grade),
   LLM-vision transcription from the page images as pass 2; disagreement on
   ANY numeric token queues for human-eyes check against the scan image.
   The pass-1 failure classes verified above (silent dropout, range-bound
   loss) are exactly what the disagreement queue exists to catch.
3. **Cell-level verification on every matrix** (attack, saving throw,
   monster reference, treasure, level progression), with internal
   consistency checks (monotone progressions) as automated validators.
4. **Intermediates are local-only** (operator ruling 2026-07-16): the
   verified intermediate is still the single substrate everything downstream
   reads, and is content-hash-verified — but it is gitignored, never
   committed to this public repo. This supersedes the charter's Stage A
   "committed intermediate" phrasing; the commitment is to verification and
   stability, not publication.

## 7. Operator rulings recorded this session

1. **Repo scope**: this repo (unreason-dev/track0-clone) carries exclusively
   public-distribution content. Digitization intermediates and source
   materials are gitignored/local-only.
2. **Layout**: directory conventions follow `system/5.1-srd/` where the
   source ontology allows; node-specific divergences are authored from the
   source's own structure.
3. **Node directory**: `OpenFRP74/`.

## 8. Verdict and next step

**Suitable.** Complete set, early printing, image quality fully supporting
vision-pass transcription; the embedded OCR layer's table failures are
characterized and the Stage A design already covers them. Next step is
Stage A tooling: spread-splitting + the dual-pass transcription substrate,
then the pilot census (charter §5) over the normalized intermediate.
