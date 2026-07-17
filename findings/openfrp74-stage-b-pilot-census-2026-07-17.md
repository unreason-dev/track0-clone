# OpenFRP74 — Stage B pilot census (2026-07-17)

Charter §5 deliverable: inventory of the booklets' content structures, the
per-family extraction spec, the first-cut ambiguity queue (§10), and the
naming punch list (§8). Grounded in the completed pass-2 intermediate
(122 pages / 1,010 hashed blocks) and checked mechanically against the
5.1-srd corpus at HEAD for every counterpart claim.

## 1. Content-structure family inventory

Block-level raw counts: 634 paragraph, 153 heading, 127 table, 48 figure,
31 footnote, 17 list. The census families cut across these:

| # | Family | Count / where | Shape |
|---|---|---|---|
| F1 | Monster reference stat-line table | 1 big table (v2-p03/p04, 58 rows) | Name, Number Appearing, AC, Move (inches, slash-variants), HD (fraction/+N grammar), % in Lair, Treasure Type ref |
| F2 | Run-in bold entry prose | **307 instances** (132 v1, 111 v2, 64 v3) | `__Name:__ body` — THE dominant entry grammar. Sub-families: F2a spell entries (~100, level from section heading, range/duration embedded in prose); F2b magic-item entries (~80: potions, rings, wands, misc); F2c monster descriptions (v2 prose); F2d procedure rules (v3: surprise, pursuit, diving…) |
| F3 | Lookup matrix | ~10 (v1 attack/saving throws, v3-p10 monster determination, v3-p18 terrain, v3-p27 hit-location/critical) | axes × cells; die-ranges as cells ("1-2", "-", "0"=10) |
| F4 | Two-column name/value listing | 74 tables | costs, movement rates, XP, fatigue, exchange rates — simplest typed extraction |
| F5 | Die-indexed table | ~20 (encounter tables, treasure types A-I, gems/jewelry ladders, castle occupants, reaction) | die spec implicit in bounds (d6, d8, d12, %) |
| F6 | Shared-rail multi-list | ~6 (v3-p18/19 type lists, v1 spell name lists) | one die rail, 2-4 parallel columns; transcribed per shared-rail convention |
| F7 | Class progression tables | v1 (levels/titles, dice+fighting capability, spell slots) | per-class row grammar with "+N" pips and CHAINMAIL keys |
| F8 | Subsystem procedure prose | v3 clusters (underworld turn, wilderness, castle, aerial, naval) | ordered paragraphs + embedded F4/F5 tables; extraction = rule nodes referencing tables |
| F9 | Referee guidance / example prose | v1 Forward+Scope, v3 dungeon design, REF/CAL dialogue, Afterward | NOT corpus entries — feeds the homebrew's authored text |
| F10 | Figures | 48 | illustrations (art, replaced in distro), 2 hand-drawn instructional plates (v3-p03 cross-section, v3-p04 sample level, v3-p21 CONSTRUCTION — the p21 costs are rules data, already lifted into a table block) |
| F11 | Errata corrections | 1 sheet, 14 correction items | typed `{target: booklet/page/line, operation: replace|add|delete, text}` — all 14 joined to verified targets |

## 2. Per-family extraction spec (→ ratified D-5 graph)

- **F1 → monsters/** with the parallel 1974 statline block (descending AC,
  HD grammar `N`, `N+M`, `A/B` split-line, `1/2`; Move `N"` with `A/B"`
  fly/ground variants; `% in Lair`; `treasure_type` as typed ref into
  treasure-types/). Slash-pair rows (Goblins/Kobolds…) split into two
  entries sharing a statline with a variance note.
- **F2a → spells/**: shared 5.1 IDs per the partition in §4; level+class
  from section headings; range/duration parsed from prose into typed fields
  with `_raw` retained; reversibility flag where text states it.
- **F2b → items/**: magic-item entries; intelligent swords use the 5.1
  sentient-item precedent (Intelligence/Egoism/Alignment typed).
- **F2c** merges into the F1 monster entries as description prose.
- **F2d → combat-rules/ + adventure-rules/** per D-5 Tier-1 mapping.
- **F3 → matrices/** (the new kind): `axes[]` + `cells[][]`, die-range cell
  grammar with `0`=10 convention documented once; verbatim traceability to
  block hashes.
- **F4/F5 → items/ (costs), system-rules/, encounter-tables/,
  treasure-types/, strongholds/, hirelings/, vessels/** per content.
- **F6 → encounter-tables/** one node per column-list, rail preserved.
- **F7 → classes/** optional-field extensions (level_titles[],
  xp_thresholds[], fighting_capability, spell-slot table).
- **F8 → the D-5 Tier-3 subsystem dirs** (aerial-combat/, naval as
  vessels/+combat-rules, strongholds/).
- **F9 → excluded from corpus**; synthesis input only.
- **F11 → applied in the normalized layer per D-6**; each correction site
  carries an errata-provenance pointer.
- **External refs**: every "use CHAINMAIL / OUTDOOR SURVIVAL / Fight in the
  Skies rules" site → external-refs/ registry (openfwg1972 scope-seed).

## 3. First-cut ambiguity / interpretation queue (§10)

Typed-field-forcing items, candidates pre-briefed. Jon calls each; genuine
referee-delegation → `open_adjudication`.

| # | Site | Ambiguity | Candidates |
|---|---|---|---|
| A1 | v2 Potions table | ESP 37-40 / Delusion 38-40 percentile overlap as printed | (i) keep overlap + note; (ii) treat as typo, adjust one bound (successor tables read 38-39/40-41-style splits) |
| A2 | v1 Languages table | Four 86-95 / Five 90-99 overlap as printed | same shape as A1 |
| A3 | v1/v2 | Telekenesis / Telekenisis / Telekensis (3 spellings) | D-6 fix → single `spell-telekinesis`; queue records the collapse |
| A4 | v1-p18 | printed `962.5 x 7 = 6,037.5` (true product 6,737.5) | (i) fix arithmetic in normalized layer (D-6 spirit); (ii) keep — it's an example, not a rule value |
| A5 | v3-p26 | `__Sharp Drive__` vs same-sentence "sharp dive" | D-6 fix → Sharp Dive |
| A6 | errata↔v1-p28 | errata "Page 28, line 9: 'each' should be east" — cited line contains no "each" | (i) apply to nearest "each" on page; (ii) printing-state mismatch, record as inapplicable-to-this-copy |
| A7 | v1 | Constitution "will withstand adversity" — untypeable as written | (i) prose-only field; (ii) open_adjudication |
| A8 | v1 Elves | class choice "at the beginning of each adventure" — race/class model | drives the D-5 parameterized races/classes split; candidates: dual-class toggle entity vs race with class-choice rule |
| A9 | v3-p15 | castle table col header `Die -1` meaning | (i) "Die" label + column "1" garbled spacing; (ii) literal die-minus-one. Layout supports (i) |
| A10 | v3-p18 | City terrain "---" for Lost/Encounter vs errata "Encounter occurs in a City on a 6" | errata resolves Encounter; Lost stays "---" (cities: never lost) — near-mechanical |
| A11 | matrices | die-range cell `0` = 10 (`7-0`, `91-00`) | document once as period convention, typed as 10/100 |
| A12 | v2/v3 | abbreviation expansion map: Myrmi's, S'bucks., Blsks., Chmrs., Grgyls., Lycs., S'heros, H'griffs, Vmprs., W. Apes, Anmls., Swim'r, misc. mg. | mechanical expansion table, one interpretation record covering all |
| A13 | v1-p09/errata | Wights duplicate in alignment lists / Griffons addition | resolved by errata (delete first Wights; add Griffons under Neutrality) — apply |
| A14 | v2-p39 | Scepter/Sceptre/Scepter across crown sets | D-6 fix → uniform spelling |

## 4. Naming punch list (§8) — partitioned against 5.1-srd at HEAD

**(a) CC counterpart exists → take the CC name/ID** (mechanically verified
present in `system/5.1-srd/`):

- Monsters, direct name-mates (47): basilisk, black-pudding, centaur,
  chimera, cockatrice, djinni, dryad, efreeti, gargoyle, ghoul, gnoll,
  goblin, gorgon, gray-ooze, griffon, hippogriff, hobgoblin, hydra,
  invisible-stalker, kobold, manticore ("Manticoras" as printed), medusa,
  minotaur, mule, mummy, ochre-jelly, ogre, orc, pegasus, purple-worm, roc,
  skeleton, specter ("Spectres"), treant (**Ents**), troll, unicorn,
  vampire, warhorse (Light/Medium/Heavy/Draft Horse family), werebear,
  wereboar, weretiger, werewolf, wight, wraith, wyvern, zombie, balor
  (**Balrogs** — the lineage's own descendant name; flagged for explicit
  operator sign-off since it doubles as the Tolkien scrub), halfling
  (**Hobbits**).
- Monster families needing variant-level projection: dragon (5.1 has
  color-variant IDs; 1974 colors map onto them), giant (5.1 hill/stone/
  frost/fire… vs 1974 unified Giants with type table), elemental
  (air/earth/fire/water present in 5.1), "Men" subtypes → 5.1 NPC entries
  (bandit, berserker, noble, mage, priest present).
- Spells, direct name-mates (43): animate-dead, bless, charm-person,
  clairvoyance, cloudkill, commune, confusion, conjure-elemental,
  contact-other-plane, control-weather, darkvision, detect-magic,
  disintegrate, dispel-magic, feeblemind, find-traps, finger-of-death,
  fireball, fly, geas, hold-person, insect-plague, invisibility, knock,
  levitate, light, lightning-bolt ("Lightening" as printed), locate-object,
  move-earth, passwall, polymorph, protection-from-poison,
  purify-food-and-drink, raise-dead, reincarnate, remove-curse, sleep,
  speak-with-animals, speak-with-plants, telekinesis, teleport,
  wall-of-fire, wall-of-ice.
- Spells, renamed CC descendants (verified): continual-light→continual-flame,
  protection-from-evil→protection-from-evil-and-good, detect-evil→
  detect-evil-and-good, dispel-evil→dispel-evil-and-good, stone-to-flesh→
  flesh-to-stone (reversal note), create-water→create-or-destroy-water,
  cure-light/serious-wounds→cure-wounds (tiering note), anti-magic-shell→
  antimagic-field, wizard-eye→arcane-eye, hold-portal→arcane-lock,
  cure-disease→lesser-restoration.

**(b) No counterpart, generic/descriptive → keep with note**: green-slime,
yellow-mold, nixie, pixie, gnome (as monster; 5.1 has the race side),
dwarf/elf (monster-side entries), sea-monster, giant animal/insect
categories, spells read-magic, phantasmal-force(→forces), charm-monster,
death-spell, massmorph, animal-growth, quest, plus all class level titles
(Veteran…Lord, Medium…Wizard, Acolyte…Patriarch), treasure types A-I,
specialists, vessel types.

**(c) Distinctive source IP → Jon dispositions each** (rename / omit):

| Name | Where | Note |
|---|---|---|
| Hobbits | v1 races, v3 rules | (a)-via-rename → halfling; listed for the record |
| Ents | v1, v3 castle table | (a)-via-rename → treant |
| Balrogs | v2 roster+description, v3 tables | → balor proposed; operator sign-off wanted |
| Nazgûl | v3-p14 illustration caption only | art, no mechanics → moot (art replaced) |
| Barsoom set: Martains (Red/Black/Yellow/White), Tharks, Apts, Banths, Thoats, Calots, Orluks, Sith, Darseen; "Desert (Mars)" column; Mars in OTHER WORLDS | v3-p18/19, v3-p24 | Burroughs IP; candidates: omit columns / rename to generic desert-nomad+beast set |
| John Carter, Conan, Howard, Burroughs, de Camp & Pratt, Leiber, Fafhrd, Gray Mouser | v1-p03 Forward, v3-p24 | F9 prose — excluded from corpus; punch-listed for synthesis text |
| Blackmoor, Greyhawk / "Grayhawk", Great Kingdom, Egg of Coot, C&C Society | v1-p03, v3-p04/p15 | TSR-campaign proper nouns in examples → rename in synthesis |
| DUNGEONS & DRAGONS mark; TSR name/address; Gygax/Arneson/Carr credits; kpowell art marks | covers, colophons | omitted from distro; recorded in provenance only |
| CHAINMAIL, OUTDOOR SURVIVAL, Fight in the Skies / "BITS" | throughout v3, v1 | → external-refs/ registry, not renamed: the retroclone replaces the dependencies (openfwg1972 seed) |

## 5. Census feedback against the D-5 graph

- The graph held. No family lacks a target; no Tier-3 dir lacks a family.
- One boundary sharpened: F2's 307 run-in entries confirm the entry grammar
  is uniform across spells/items/procedures — one shared extraction
  convention (`__Name:__` → id + body) serves three taxonomies.
- One addition earned its keep before extraction begins: the abbreviation
  expansion map (A12) should live beside the graph as a census artifact,
  not be re-derived per entry.
- Scale check: ~100 spells + ~60 monsters + ~80 magic items + ~50 rule
  nodes + ~40 tables/matrices ≈ **330 corpus entries** for the full 74 node
  — small, as the charter predicted for the pilot.

## Next

Jon dispositions: the (c) punch list rows (chiefly Balrog→balor sign-off
and the Barsoom set) and the A-queue calls that aren't mechanical (A1, A2,
A4, A6, A7, A8). Then Stage C schema projection can start on the first
family (recommendation: F2a spells — highest overlap, cleanest grammar,
exercises the shared-ID convention end to end).
