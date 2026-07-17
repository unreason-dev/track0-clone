# OpenFRP74 — D-5 node graph (ratified as working basis, 2026-07-17)

Operator ruling: "i think that looks like a good start, or at least i can't
anticipate the problems myself easily" — ratified as the working basis for
Stage B; problems surface through the pilot census, not up-front review.
Guiding principle (operator): where an entity overlaps 5.1-srd (e.g.
spell-sleep) we take the 5.1 node type and share the entry ID; we reuse as
much of the 5.1-srd taxonomy as possible, just as the shipped retroclone will
reuse CC-BY 5.1 text; 1974-native subsystems get new structures.

## The graph

### Tier 1 — reused as-is (shared node types; shared entry IDs on overlap)

| 5.1-srd taxonomy | OpenFRP74 instantiation |
|---|---|
| abilities/ | ability-strength … ability-charisma — same six; prime-requisite and XP-mod semantics are fields, not new nodes |
| alignments/ | alignment-law, alignment-neutrality, alignment-chaos (3-point axis, subset of 5.1 domain) |
| classes/ | class-fighting-man, class-magic-user, class-cleric |
| races/ | race-human, race-dwarf, race-elf, race-halfling (post-scrub) |
| spells/ | ~100 spells; large majority have direct 5.1 name-mates → shared IDs (spell-sleep, spell-charm-person, spell-fireball, spell-hold-portal …) |
| monsters/ | monster-orc, monster-ogre, monster-troll … Tolkien-name entries carried under working IDs with punch-list flags until the firewall pass assigns scrub-IDs |
| monster-types/ | undead, dragon, giant, lycanthrope, elemental … (the Vol 3 type-lists group this way natively) |
| items/ | mundane equipment + magic items; intelligent swords via the 5.1 sentient-item precedent (Intelligence/Egoism) |
| conditions/ damage-types/ sizes/ languages/ | only members 1974 attests |
| traps/ | the Tricks & Traps inventory |
| adventure-rules/ | time, movement/turns, light & infravision, doors & listening, rest, healing-wounds |
| system-rules/ | encumbrance, XP + support/upkeep, currency exchange, languages rule |
| combat-rules/ | melee conventions, missile fire, surprise, evasion/pursuit |

### Tier 2 — reused with adaptation (5.1 taxonomy, 1974-shaped optional fields)

- classes/*: + level_titles[], prime_requisite, xp_thresholds[], spell-slot
  tables, fighting_capability (CHAINMAIL key).
- spells/*: + reversibility; underworld/wilderness range duality
  (inches → feet/yards).
- monsters/*: parallel 1974 statline block — HD, descending AC, Move, % in
  lair, treasure-type ref, alignment. NOT a forced 5E stat conversion; the
  retroclone's fidelity is to the 1974 statline.

### Tier 3 — new structures (no 5E analog)

- **matrices/** — the load-bearing new kind: one typed node "matrix" with
  axes[] + cells[][], verbatim-traceable. Instances: attack-matrix (AC ×
  level bands), saving-throw-matrix (5 categories × level bands),
  monster-determination-matrix, wilderness-encounter-matrix (terrain × die),
  turning-undead-matrix. 1974 is a game of lookup matrices the way 5E is a
  game of DCs.
- **encounter-tables/** — monster-level-table-1…6; wilderness
  men/flyer/undead/giant/lycanthrope/swimmer/dragon/animal tables (Barsoom
  columns carried pre-firewall).
- **treasure-types/** — treasure-type-a … treasure-type-i; gems/jewelry value
  ladders.
- **strongholds/** — construction costs (p21 plate + price lists), barony
  rules, angry-villager rule.
- **hirelings/** — specialists (alchemist…spy), men-at-arms upkeep,
  loyalty/obedience.
- **vessels/** — naval statlines as an entity kind: movement modes, crew,
  hit points, fatigue.
- **aerial-combat/** — BITS subsystem: turn-category table, dive/climb,
  hit-location + critical-hit matrices, bombing.
- **external-refs/** — typed registry of every "use rules from CHAINMAIL /
  OUTDOOR SURVIVAL" site, located to page/block, so the retroclone knows
  exactly what it must replace with original text.

### Dropped 5.1 taxonomies

backgrounds, feats, skills, subclasses, schools-of-magic, deities/pantheons,
madness, diseases, poisons, weapon-properties, planes (OTHER WORLDS becomes a
single adventure-rule). Referee-facing prose (dungeon design walkthrough,
sample expedition, Afterward) stays out of the corpus graph; it informs the
homebrew's own authored text.

## Program-level forward item: openfwg1972 (operator, same ruling)

"we probably need to do a openfwg1972 for Chainmail 2nd edition at some point
in making openfrp74 real." — OpenFRP74's combat core delegates to CHAINMAIL
(melee/missile resolution, jousting, fantasy combat table, morale); the
external-refs registry will enumerate the exact dependency surface, which
then becomes the scope-seed for an openfwg1972 adapter (Chainmail 2nd ed.,
1972). Not chartered yet; recorded here so the external-refs work is done
with that future consumer in mind. OUTDOOR SURVIVAL (Avalon Hill) is the
other external dependency — board-as-map; likely needs replacement mechanics
rather than an adapter, since it is a different publisher's boardgame.

## Next

Stage B pilot census (charter §5) over the normalized intermediate, using
this graph as the classification target. Census results feed back as the
first stress test of the graph — expect Tier 2/3 boundaries to move.
