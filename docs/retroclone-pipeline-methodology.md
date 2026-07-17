# RetroClone pipeline — durable methodology

**Goal state (operator directive, 2026-07-16):** drop a PDF scan of a new
system into the pipeline and it runs to a schema-corpus basically
autonomously, with operator attention only at the registered decision
points. This document accumulates the durable, system-agnostic methodology
as OpenFRP74 (the pilot node) is built. It is a living doc during the pilot;
at pilot close it is the template the next node inherits.

Conventions here follow Track 0 practice: watch-for at 1st instance,
durable rule at 2nd; honest absence is informative; instrument before
engine.

---

## Stage A — digitization substrate

### A.1 Spread split (durable, parameterized)

`tools/split_spreads.py`. Universal mechanics:

- Render every PDF page at 300 DPI (poppler `pdftoppm`).
- **Aspect-ratio self-check** decides single-vs-spread per page — never
  trust a layout map alone. (1st-instance validation: the map said PDF p63
  was a spread; aspect said single; single was right — it was the
  Correction Sheet insert.)
- Spreads split at a darkness-scanned gutter (spine shadow) confined to the
  central band, midpoint fallback when the signal is flat.
- Booklet page numbers derived arithmetically are **claims**
  (`booklet_page_claimed`), verified later against printed page numbers by
  the vision pass. Never trusted before verification.
- Per-half embedded-text extraction (`pdftotext` crop) rides along as
  pass 1 of the dual-pass discipline.
- Manifest with sha256 per artifact + source-PDF hash = the provenance
  anchor for everything downstream.

Per-system configuration (the ONLY part a new system needs authored):
booklet/unit ranges within the PDF and their titles. Everything else is
mechanical. *Autonomy note:* unit ranges are discoverable (cover-page
detection — covers are aspect-single and/or carry VOLUME-style text); the
pilot hand-authored them from a 5-minute probe. Automate at 2nd system if
the probe pattern repeats.

### A.2 Known hazards of embedded OCR layers (durable)

Scanned-era PDFs carry OCR text layers that are prose-grade only. Verified
failure classes (see openfrp74-source-disposition-2026-07-16.md §4):
silent numeric cell dropout; systematic range-bound loss (`1 - N` → `N`);
percent-sign mangling; case collapse; 2-up reading-order interleaving.
**Rule: no numeric value from an embedded text layer is ever trusted
without pass-2 agreement.**

### A.3 Pass-2 vision transcription (durable design)

`tools/transcribe_pages.py`. Each split page image is transcribed by a
vision-capable Claude model into **block-model JSON** (schema:
`tools/page-transcript.schema.json`): ordered blocks (heading | paragraph |
table | list | figure | footnote), tables with verbatim string cells,
continuation flags for cross-page blocks, printed page number as observed
(verifies the split's arithmetic claim), per-token uncertainty markers.

Fidelity rules baked into the prompt (durable):

- **Verbatim transcription including source typos** — the transcript is a
  record of the page, not an edition. Normalization/typing happens at
  extraction, with the transcript as `_raw` anchor.
- Table cells are strings exactly as printed (`"30 - 300"`, `"1-1/1/2"`);
  no interpretation at transcription time.
- Uncertain tokens are flagged, never silently guessed.
- Figures/illustrations are described, not omitted (they carry no rules
  content but their presence is provenance).

Execution (operator-corrected 2026-07-16): **the worker agent transcribes
in-session** — the agent reads each split page image directly and emits the
schema-conformant transcript, sharded across supervisor invocations for
scale. This is the standing Track 0 pattern (the worker agent IS the vision
system); no API credential, no separate billing surface. The optional
`tools/transcribe_pages.py` batch tool is retained as an alternative
execution path for future scale, but it is NOT the default and is NOT a
pipeline dependency. Transcriber independence note: the in-session
transcriber inevitably sees page ids/labels; independence is preserved at
the observation level — `printed_page_number` records only what is printed
on the page, and the differ compares content regardless.

Durable table conventions (surfaced by the v2-p03 gold exemplar — author a
gold exemplar of the hardest page type BEFORE any API spend; it is where
representational gaps appear):

- Column-spanning values ("All variable - - - -") live in the FIRST spanned
  cell; remaining spanned cells are empty strings — row arrays always align
  to the column count.
- Cell content wrapped across printed lines joins with a newline.
- Figure blocks are described, but their descriptions are transcriber prose
  and are EXCLUDED from pass-comparison text.

### A.3.1 Pilot lessons (2026-07-16, in-session transcription of errata-sheet + v1-p19)

- **Inline print emphasis needs markup**: underlines are semantic in this
  era (the Correction Sheet marks corrected readings by underline). Format:
  `__underlined__`, `~~struck-through~~` in any text surface. Handwritten
  ink annotations are described in `transcriber_note`, never transcribed as
  text.
- **Tables carry spanning super-headers** → `caption` field on the table
  block.
- **Facing-page slivers**: the gutter cut leaves character fragments from
  the facing page at the bound edge. Transcribers ignore them (noted on the
  first block); the pass-1 TEXT crop pulls back from the gutter by 1.2% of
  page width (`GUTTER_TEXT_INSET_FRAC`) so slivers don't inject phantom
  tokens — verified to clear the whole noise class on v1-p19.
- **Schema enforcement works**: the validator rejected a transcript carrying
  a field not in the schema — run `--validate` after every transcription
  batch, before the differ.
- **Pass-1 I/l/O confusion** ("lOth", "An II th level", "8 + I") is partly
  recoverable by conservative token normalization on the pass-1 side only
  (≥1-digit-or-O guard so roman numerals don't mint phantom numbers);
  the irreducible remainder stays queued for adjudication, correctly.
- Residual queue volume after both fixes: ~2–11 numeric tokens per dense
  page — sized for agent adjudication (D-3), not operator review.

### A.3.2 Table-representation conventions (durable, from pilot rounds 2–3)

- **Side-by-side parallel tables** (e.g. per-class XP tables): one table
  block each, ordered left-to-right, `caption` = the printed group title,
  `columns: null` when the print has no column headers.
- **Shared-row-rail bands** (e.g. the Spells Table: one numbered rail
  indexing three level columns, rows baseline-aligned): ONE table, rail as
  an unnamed first column (empty-string header). Row numbers verbatim
  including punctuation.
- **Numeral+ordinal spacing is normalized to attached** ("11th", "1st") —
  a documented exception to strict verbatim: typewriter tracking makes
  "11 th"/"11th" unreliable page-to-page, and inconsistent transcription is
  worse than either reading. Same reasoning family as the 3.5 charter's
  dash disambiguation.
- **Both consumers bind to blocks**: the schema builder extracts from
  blocks; the rules-oracle sweep keys questions to {booklet, page, block}.
  After the full transcription run, a mechanical stamping step adds
  per-block content hashes to complete the charter's provenance unit
  {work, booklet, page, block-index, content-hash} — computed, not
  model-emitted.

### A.3.3 Pilot verdict (2026-07-16): format LOCKED

Seven transcripts spanning every major page type of the source — display
cover, errata insert (lists, inline emphasis, ink annotation), side-by-side
tables, dense reference table (gold), attack matrix + prose, shared-rail
spell tables, monster-description prose with stub-leader table, and the
wandering-monster matrix pair. All validate; disagreement-queue residue is
pass-1-side noise only (4 of 7 pages fully clean both directions). The
block-model schema, prompt conventions, and differ are locked for the full
run; further schema changes require a documented reason and a retrofit
script (two precedents: caption, inline markup).

Cross-artifact corroborations already banked: the Correction Sheet's
"Skeletons/Zombies 1/2/1" amends the v2-p03 table; its "Balrogs Die 9"
amends v3-p11, whose printed Lords/Balrogs duplicate-8 is verified in the
transcript. The errata↔booklet join is real data and the fidelity policy
(D-6) will govern its typed-value posture.

### A.4 Disagreement queue (validated)

`tools/diff_passes.py` — digit-run multiset comparison per page between
pass 1 and pass 2 (digit-runs, not formatted tokens, so pass-1 mangling
like "2()0A," for "20%" still fires). Validated against the v2-p03 gold
exemplar: the queue caught all known planted-by-reality defects — the Orcs
Hit-Dice silent dropout, all nine range-bound losses, and both percent
manglings — as pass2-only/pass1-only asymmetries. Agreement clears a
numeric token; disagreement queues it for adjudication (decision D-3).

### A.4 Disagreement queue (durable design)

After pass 2: token-level comparison of pass-1 and pass-2 **numeric tokens**
per page. Disagreements (including tokens present in one pass only) queue
per page. Adjudication policy — see operator decision D-3 below.

---

## Operator decision registry

Decisions that shape the pipeline, reserved for the operator, batched.
Status: OPEN / RATIFIED.

| # | Decision | Status | Notes |
|---|---|---|---|
| D-1 | Repo scope: public-distro only; intermediates gitignored | RATIFIED 2026-07-16 | Supersedes charter "committed intermediate" |
| D-2 | Errata insert (Correction Sheet) is its own work, separate from booklets | RATIFIED 2026-07-16 | Typed-value posture where errata contradicts booklet text still OPEN (batched with fidelity policy) |
| D-3 | Disagreement adjudication autonomy: charter says numeric disagreements get a "human-eyes check"; amended for the autonomy goal — an agent-vision re-read adjudicates first, and only residues genuinely confusing after re-read escalate to the operator | RATIFIED 2026-07-17 ("yes, do d-3 - only surface things that are genuinely confusing to me") | Executed same day: 65/65 queue entries adjudicated pass-1-artifact (verdicts in digitization/transcripts/adjudication-log.json); one residue surfaced (v3-p24 ink dropout, both passes blind) |
| D-4 | ~~API credential provisioning~~ | RETIRED 2026-07-16 | Operator-corrected: pass 2 runs in-session (the worker agent reads pages directly, per standing Track 0 practice). No credential needed. |
| D-5 | Node graph ratification (74/76/77b/79a…) | OPEN | Charter §11.1; needed before any second node, not before pilot completion |
| D-6 | Fidelity policy for source typos (record-don't-correct posture assumed from 3.5 charter precedent) | OPEN | Register seeded in source-disposition memo §5 |

## Autonomy ledger

What the pilot did manually that a drop-in-a-PDF run must do itself:

1. Source-suitability probes (printing identification, OCR-layer quality,
   page mapping) — currently conversational; automatable as a "Stage 0
   disposition report" the operator approves rather than performs.
2. Booklet-range configuration (see A.1 autonomy note).
3. Prompt/format tuning for pass 2 — pilot validates once; future systems
   inherit the format and only re-tune on measured failure.
