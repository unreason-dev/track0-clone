# OpenFRP74 — Stage A disagreement-queue adjudication (2026-07-17)

## Ruling executed

D-3 ratified by operator ("yes, do d-3 - only surface things that are
genuinely confusing to me"). Protocol run same day: for each of the **65
queued pages** in `disagreements.json`, the disagreement sites were located in
both passes (pass-1 line context vs pass-2 block context) and re-checked
against the page image wherever the discrepancy was value-bearing rather than
a self-evident OCR mangle. Verdicts (with per-page failure-class notes) are in
`digitization/transcripts/adjudication-log.json` (local-only, gitignored with
the rest of the intermediates).

## Result

**65/65 entries: `pass1_artifact`. Zero pass-2 transcription errors found.
Zero corrections applied to the pass-2 layer.**

Every disagreement traced to a documented pass-1 (embedded OCR) failure
class:

- **%-glyph mangling** (the dominant class): `500A>`=50%, `2()0A,`=20%,
  `600/b`=60%, `9()0tf,`=90%, `1000k`=100%, `100A,fturn`=10%/turn, `{91-1000k)`=(91-100%) …
- **l/I/O ↔ 1/0 confusion**: table 1s as `l`/`I`, `I 00%`=100%, `I: I 200`=1:1200,
  `II th`=11th, letter-O percentages.
- **Word mangles minting digits**: `fv4ove Earth`=Move Earth, `Hold Pel'$0n`=Hold
  Person, `C10ssbow`=Crossbow, `do1,1ble`=double, `le11guages`=languages,
  `COII'In'1and`=command, `1-lonster`=Monster, `TUr1<s`=lurks, `1103 points`=1 to 3 points.
- **Glyph substitutions**: `#`→`11`/`1` (treasure-table refs, crew footnote),
  `©`→`0` (both title pages), typewriter quote→`11`, `!`→`1`.
- **Right-edge truncation / comma gluing**: `$ 1`=$1.75, `51 000-30 1000`=5,000-30,000.
- **Hand-lettering garbage** (v3-p04 map, v3-p21 CONSTRUCTION plate) — where,
  usefully, the garbage fragments *corroborate* the four registered-uncertain
  hand-written costs on v3-p21 (`I CoN D<OOil 5o 7s` = IRON DOOR 50/75,
  `2' 30` = REINFORCED 20/30, `lifo` = 140, `2o%` = +20%).

Two image re-reads settled value-bearing sites in pass-2's favor and
identified **genuine source anomalies** (as-printed, preserved verbatim):

1. **v1-p18**: print says `962.5 x 7 = 6,037.5.` — the source's own arithmetic
   is wrong (962.5 × 7 = 6,737.5). Both passes agree on the 0-3-7 glyphs.
2. **errata-sheet**: the struck-through publisher address prints `342 SAGE
   STREET` (with handwritten `PoB 756`), vs `542 SAGE STREET` on the booklet
   inside covers. Two independent vision reads agree on the 3.

## The one residue (surfaced to operator)

**v3-p24, BARONIES**: "Territory up to ___ miles distant from a stronghold may
be kept clear of monsters once cleared" — the distance is destroyed by ink
dropout in this copy, and the pass-1 layer is blind at the same spot
("up t, niles dis-"). **Unrecoverable from this source copy.** External
copies/editions of the 1974 printing could supply the value, but importing it
would breach the no-fabrication/verbatim posture without an operator ruling —
folded into the D-6 fidelity discussion.

## Methodology note (durable)

The two-pass + digit-multiset-differ design worked as intended: the differ
caught 100% of the numeric divergences, every one adjudicated in pass-2's
favor, and the single unrecoverable site was independently flagged by the
transcriber's uncertain-token register before adjudication began. For future
retroclone sources: the adjudication pass costs ~1 image re-read per 30 queue
entries when pass-1 mangles are classified first from text context (the
failure-class taxonomy in the source-disposition doc makes most verdicts
self-evident without reopening the image).
