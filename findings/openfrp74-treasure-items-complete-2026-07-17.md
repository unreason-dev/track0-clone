# OpenFRP74 — treasure & magic-item families COMPLETE (2026-07-17)

Third and fourth Stage C families extracted and pushed. **Corpus now 306
ids**, referentially clean end to end (spells ↔ items ↔ monsters ↔ tables ↔
treasure types all resolve).

## Treasure types (`treasure-types/`, 9 entries + schema)

Fully **rollable**: every cell typed as {chance_percent, amount min-max,
×1000 multiplier} — an engine can roll a Type H hoard with no text parsing.
Type A carries its Land/Desert/Water terrain variants; the two-line
Gems/Jewelry cells split per the printed footnote; magic columns are typed
grant specs (any_items/magic_items/maps/potions/scrolls + exclusions like
F's "no weapons"); the Men-type prisoner/pocket-money footnotes and the
lair-only rule ride as notes.

## Rollable tables (`items/tables/`, 23 + schema)

The whole determination chain: magic-or-map (75/25) → category (d%) →
per-category tables (sword, armor, misc weapons, potions, scrolls + curse
d8, rings, wands/staves, misc magic) → map payoffs (2×d8), plus gem/jewelry
value ladders and the sword sub-system set (alignment, intelligence d12,
primary powers, languages, extraordinary abilities, influence check) and
the magical-item saving-throws table (d20 targets with the printed +3 gap
noted). Normalized rows keep `result_raw` (Dimenuation→Diminution,
Telekenisis→Telekinesis, Paralization→Paralyzation, Bag ot→of Holding,
Censor→Censer); the potions table applies the ir-a1 ESP/Delusion split and
the sword-languages table the ir-a2 fix, raw ranges preserved.

## Items (`items/`, 103 entries + schema)

- **item-magic-sword** carries the full sword system: alignment damage
  (2d6/1d6), the Int+Ego ≥ +6 control threshold, egoism behaviors,
  origin/purpose powers (Law paralyzes / Neutrality +1 saves / Chaos
  disintegrates), the influence-check procedure with condition modifiers.
- 26 potions (default 6+1d6-turn duration typed; Heroism carries its errata
  rider; Poison keeps its referee-deception framing).
- Scroll system applies both errata riders (25% clerical; writing vanishes
  after one reading) + curse scroll + 4 protection scrolls with typed
  durations.
- 17 rings (default rule: unlisted rings act as the like spell/potion,
  unlimited duration — encoded per entry).
- Wand/staff system (6-die/8-die, 100/200 charges) + 12 wands + 7 staves
  (Final Strike: 8 × remaining charges, 3\" radius).
- 24 miscellaneous magic + Artifacts (referee-adjudicated, off-table,
  ir-a14 applied).

## Running totals

88 spells + 84 monsters + 9 treasure types + 23 tables + 103 items
= **306 corpus entries** (census projected ~330 total including the
remaining families). Remaining: classes/races (F7), the combat/saving
matrices (F3), subsystem rules (F8), external-refs registry consolidation.
