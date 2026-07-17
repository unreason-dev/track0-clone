# OpenFRP74 — spell node COMPLETE (2026-07-17)

Stage C's first family is extracted end to end: **88 spell entries**
(`OpenFRP74/spells/`), schema-validated, referentially clean, pushed.

- Coverage matches the source indices exactly: Magic-User 8/10/14/12/14/12
  by level (70), Cleric 6/4/4/6/6 by level (26 incl. 9 cross-class shared
  entries), plus The Finger of Death as the named Anti-Cleric reversal of
  Raise Dead.
- Cross-class model: one node per spell; `available_to` notes carry the
  Cleric parameter variants (Hold Person 9 turns/18", Detect Evil 6
  turns/12", Locate Object base 9", Continual Light = full daylight).
- Reversibility: typed from the p22 underline data (underlines-as-data
  transcription convention paid off directly) — 11 Anti-Cleric-reversible
  spells plus Stone to Flesh / Transmute Rock to Mud self-reversals.
- Counterparts: 43 shared 5.1 IDs + 12 renamed-descendant links, every one
  verified to exist in `system/5.1-srd/spells/` at HEAD; all
  `related_spells` references resolve within the node.
- Provenance: every entry carries booklet/page/block plus content SHA-256s
  from the intermediate's block-hash manifest; index-table sites recorded
  as secondary sources.
- Expression: descriptions are original wording (mechanics preserved
  exactly — formulas typed: Fire Ball 1d6/level, Confusion 1d12−level
  delay, Telekinesis 200 GP-weight/level, Animate Dead 1d6/level>8, Raise
  Dead 4 days/level>8, healing 1d6+1 / 2d6+2).
- D-7 honored: Balrog (Hold Portal), Ents (Speak with Plants) stand.

One provisional interpretation record awaiting operator review:
**ir-a15** — Invisibility radius printed 10" (explanation) vs 10' (table);
normalized to feet by parallel with Protection from Evil, 10' Radius.

Next families per census order: monsters (F1/F2c, ~60 entries) or the
matrices (F3). Monster extraction should precede matrices so
encounter-table refs have targets.
