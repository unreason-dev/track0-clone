# OpenFRP74 — rules-oracle smoke test (2026-07-17)

## What ran

`tools/oracle_smoke.py` — a deterministic, no-LLM harness in the oracle's
own idiom (frozen JSONL suite rows with gold answers, per
ttrpg-app `docs/question-generation.md`). Of the operator's two routes
(reuse frozen b170 questions vs synthesize from the decode), it takes the
second, and makes it a genuine test: **gold values are extracted from the
pass-2 intermediate (the PDF decode); answers are resolved from the
extracted corpus by typed paths.** A mismatch is an extraction-fidelity
finding, not a tautology.

## Result

**311 suite rows — 310 pass, 1 expected divergence, 0 failures.**

| Family | Checks | What it exercises |
|---|---|---|
| A monster statlines | ~80 | v2 reference table AC + % in lair → monster entries (incl. slash-pair splits) |
| B spell parameters | ~90 | Range/Duration parsed from entry prose → range_inches / duration_turns / duration_formula |
| C class XP | 29 | p16 threshold tables → class level arrays |
| D attack matrix | 48 | every cell of Attack Matrix I → matrix node |
| E treasure types | 24 | coin cells of types B-I → typed rollable rows |
| F turning undead | 64 | every cell → matrix node; the Zombie/Adept cell scores `expected_divergence` (errata T→7, declared) |

The harness's own first run surfaced 4 false failures — its gold-regex had
grabbed the "6" out of formula durations ("6 turns + the level of the
user") that the corpus correctly types as formulas. Fixed to test formulas
as formulas; the corpus was right each time.

Suite frozen at `OpenFRP74/oracle-smoke/suite-openfrp74-smoke-01.jsonl`
(b170-compatible row shape + gold {value, path, source} + status), ready to
become `audit/suites/openfrp74-smoke-01.jsonl` in the oracle repo when
integration starts.

## On reusing the frozen b170 questions

Assessed and recommended against porting rows directly: b170 rows are
5.1-SRD-page-keyed and their gold answers are 5.1 values — "what is the
armor class of the vampire?" is subject-portable but the gold flips meaning
under descending AC (exactly the cross-system silent-wrongness the charter
§6 warns on). Port the QUESTION SHAPES (openers/subjects taxonomy), not
the rows; the generator here already follows that pattern.

## Integration gaps for pointing the real engine at OpenFRP74

(Extends the session-start homebrew investigation.)
1. `tools/build-corpus` ingests only `system/5.1-srd` — needs a system
   parameter + ingestion of the openfrp74 schema family.
2. Reader assumptions: descending AC (system-scoped semantics required on
   `armor_class` before any reader touches it), matrix-lookup to-hit
   instead of modifier math, level-band saves, inches-with-context units.
3. `DEFAULT_ALLOWED_BLOCKS` and kind-registry entries for the new kinds
   (matrix, rollable table, treasure-type, vessel, hireling).
4. New reader families needed: matrix-cell lookup, rollable-table
   resolution (the D-5 "1974 is a game of lookup matrices" point).
5. The smoke suite gives integration a ready acceptance bar: the engine
   should reproduce these 311 resolutions before anything else is trusted.
