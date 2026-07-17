# OpenFRP74 — monster node COMPLETE (2026-07-17)

**84 monster entries** (`OpenFRP74/monsters/`), schema-validated,
referentially clean, all 58 reference-table rows covered, pushed.

- **Statline model**: the parallel 1974 statline landed as designed —
  descending AC with system-scoped semantics, HD grammar typed
  ({min,max,bonus} with fractional support), Move/fly split per the
  flying-speed footnote, % in Lair, treasure-type refs (targets for the
  coming treasure-types/ family), tri-axis alignment from the v1-p09 lists
  with errata applied.
- **Slash-pair rows** (Goblins/Kobolds, Hobgoblins/Gnolls,
  Skeletons/Zombies) split into paired entries via `statline_shared_with`;
  Skeleton/Zombie HD read from the errata's 1/2/1 correction.
- **Family nodes** for shared-rules clusters: Dragons (breath economy,
  maturity pips, full subdual procedure, mated pairs/families,
  treasure-by-age) + 6 color entries with weapon-efficacy specials;
  Elementals (16/12/8 HD by summoning source, control-loss permanence) + 4
  types; Lycanthropes (pack structure, infection) + 4 breeds; Men + 9
  subtypes with the Bandits leader-pyramid formulas typed.
- **D-7 posture**: Balrogs, Ents, Hobbits-adjacent text, Nazgûl
  reclassification note, Tolkien/Barsoom references all stand; the
  scrub-package mapping is pre-wired via `counterpart_5_1srd`
  (balor, treant, etc.).
- **External refs**: CHAINMAIL delegation sites recorded per entry
  (Goblins base description, Ghoul paralysis, Giant catapult behavior, war
  horse melee, Balrog characteristics) — openfwg1972 scope-seed grows.
- 47 entries carry verified 5.1-srd counterpart links; the rest are
  period-only (nixie, pixie, green-slime, yellow-mold, sea-monster …).

Open follow-ons for later families: treasure-type refs currently point at
not-yet-extracted `treasure-type-a..i` (F5 family next candidate); Golden
Dragon's Lawful exception recorded on the entry (the Alignment table's own
omission, per source).

Remaining Stage C families: treasure-types + magic items (F5/F2b),
classes/races (F7), matrices (F3), subsystem rules (F8), external-refs
registry consolidation.
