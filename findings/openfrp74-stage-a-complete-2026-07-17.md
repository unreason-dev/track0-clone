# OpenFRP74 — Stage A pass-2 transcription COMPLETE (2026-07-17)

## Status

All **122/122 pages** of the 1974 source (three booklets + Correction Sheet
errata insert) now have schema-validated pass-2 (agent-vision, in-session)
transcripts. `tools/checkpoint.py` reports **0 invalid**; every transcript
carries manifest-stamped provenance (`pdf_page`, `side`, `image`,
`image_sha256`). The block-hash stamping pass ran clean and deterministic:
**1,010 per-block content hashes across 122 pages** in
`digitization/transcripts/block-hashes.json` (sidecar manifest; computed by
`tools/stamp_block_hashes.py`, never model-emitted), completing the
`{work, booklet, page, block_index, content_hash}` provenance unit.

Transcription was split across two sessions/models: v1, v2, errata, and v3
through p09 by claude-fable-5; v3-p10 through v3-p37 by claude-opus-4-8 (each
transcript's `transcription.model` records which). Conventions held across the
handoff via the operator cookie + methodology doc — no convention drift
observed; the schema validator caught the one shape error (string-form
`uncertain_tokens` in 4 late transcripts, corrected to the object form).

## Corpus shape

- Blocks: 634 paragraph, 153 heading, 127 table, 48 figure, 31 footnote,
  17 list (1,010 total).
- 374 blocks carry `transcriber_note` (typo preservation records, table-layout
  rationale, naming punch list flags).
- 21 uncertain tokens registered across 15 pages — each with best reading in
  place and block-indexed doubt record.

## V3-specific findings banked during the grind

- **Naming punch list hits in v3**: Hobbits (p08, p09), Nazgûl illustration
  (p14), Balrogs + Ents (castle table p15, flying movement p16, wilderness
  tables p19, turn-category table p26), Ent illustration (p25).
- **Barsoom content**: wilderness MEN table (p18) and animals table (p19)
  carry Mars columns (Red/Black/Yellow/White "Martains", Tharks, Apts, Banths,
  Thoats, Calots, Orluks, Sith, Darseen); "Mars is given in these rules" under
  OTHER WORLDS (p24). Same IP-scrub class as the Tolkien names — flagged for
  the expression-firewall pass.
- **Genuine source anomalies (as-printed, noted in transcripts)**:
  - p12 "Burningoil" (no space); p28 "OaredMovement" (no space).
  - p15 "Grayhawk" vs p4 "Greyhawk Castle" spelling split.
  - p26 "__Sharp Drive__" where context reads "Sharp Dive".
  - p30 ramming rule 1 has an asterisk with no matching footnote.
  - p33 crew-table "#" footnote has no matching marker (apparently Sailed
    Warship); Must Remove? yes/no printed between row baselines.
  - p34 heading "NAVAL ADVENTURES" vs Index "Naval Adventure".
  - Recurring housestyle: space before terminal !/? ; "descretion",
    "manditory", "Lightening", "waterbourne", "catagory", "Heros" etc.
    preserved verbatim throughout.
- **Physical-copy damage (not typos)**: p22 smudge over "not"; p24 ink dropout
  obliterates the Baronies monster-clearing distance ("Territory up to
  [illegible] miles") — queued for pass-1 adjudication; p21 hand-written
  CONSTRUCTION plate has four rough digits registered uncertain.

## Dual-pass differ state

Final run: **57 pages clean, 65 pages queued, 0 skipped** →
`digitization/transcripts/disagreements.json`. Spot-checks during the grind
consistently attributed queue entries to pass-1 OCR failure classes (dropped
table cells, range-bound loss, I/l/O confusion, facing-page slivers) rather
than pass-2 error. Adjudication is deliberately NOT performed yet — pending
operator ruling D-3.

## What Stage A still needs (operator decisions to batch)

1. **D-3 — adjudication autonomy**: proposed protocol = agent vision re-reads
   each queued page against both passes and adjudicates; only residues (like
   the p24 ink dropout) go to the operator.
2. **D-5 — node graph ratification** (charter Stage B precondition).
3. **D-6 — fidelity policy**: typos are preserved verbatim in the
   intermediate; ruling needed on how the normalized layer treats them, and on
   the errata sheet's typed-value posture (booklet↔errata joins are banked in
   the v1/v2 findings docs).

After D-3/D-6: resolve the queue, then charter §5 Stage B pilot census over
the normalized intermediate.
