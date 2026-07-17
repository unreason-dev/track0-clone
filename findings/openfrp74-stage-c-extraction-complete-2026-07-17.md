# OpenFRP74 — Stage C extraction COMPLETE (2026-07-17)

**The full 1974 corpus is extracted: 407 entries across 18 families,
referentially clean end to end, every entry schema-validated and anchored to
the intermediate by block content hashes.** The census projected ~330; the
overage is finer granularity (per-potion/ring/wand items, per-color dragons,
rule nodes split by subsystem).

## Family census (final)

| Family | Entries | Notes |
|---|---|---|
| spells | 88 | shared 5.1 IDs on name-mates; Anti-Cleric reversals typed |
| monsters | 85 | incl. Dragon Turtle; parallel 1974 statline throughout |
| items | 104 | sword system + potions/scrolls/rings/wands/staves/misc |
| items/tables | 24 | rollable d%/d8/d20 determination chain + sword sub-system |
| treasure-types | 9 | fully rollable, terrain variants, typed grants |
| encounter-tables | 15 | underworld level tables 1-6 + wilderness type set |
| matrices | 8 | attack I/II, saves, turning, determination, wilderness |
| classes / races / abilities / alignments | 3/4/6/3 | full progression tables typed |
| combat-rules | 13 | incl. naval cluster |
| adventure-rules | 11 | underworld turn → other worlds |
| system-rules | 10 | XP, encumbrance, NPC machinery, 72-row equipment list |
| strongholds / hirelings | 4/12 | construction, baronies (errata "ten"), specialists |
| aerial-combat | 4 | BITS |
| vessels | 8 | typed speeds by point of sail |
| external-refs | 1 registry | 32 delegation sites (26 CHAINMAIL / 5 OUTDOOR SURVIVAL / 1 FitS) |

## Posture confirmations

- **D-6** applied throughout: normalized layer fixes typos/applies all 14
  errata items (Balrog die 9, turning T→7, CON band, city encounter 6,
  Heroism/Scroll riders, restored "ten miles", each→east); verbatim
  intermediate untouched; `_raw` fields preserve printed forms.
- **D-7** applied throughout: Balrogs, Ents, Hobbits, Nazgûl note, Barsoom
  fauna all stand; scrub-package seed in `counterpart-map.json` (124
  verified 5.1 mappings, keyed for the future homebrew alias layer).
- All 15 interpretation records cited at their points of application.
- Expression firewall: every description is original wording; mechanics
  (numbers, formulas, tables) extracted as unprotectable facts.

## Known consciously-deferred items

- F9 referee prose (Forward, dungeon-design walkthrough, REF/CAL example,
  Afterward) excluded from corpus by census design — synthesis input only.
- Magical research & Books of Spells prose (v1-p35) folded into
  class-magic-user summary; a dedicated node can be split out if the
  rules-oracle wants it queryable.
- The openfwg1972 adapter remains chartered-not-started; its scope is now
  precisely the 26 CHAINMAIL sites in the registry.

## Next program steps (operator's call)

1. Rules-oracle smoke test: point the corpus loader at `OpenFRP74/` and
   query end to end (the layered-package machinery was verified generic at
   session start).
2. The IP-scrub homebrew package (D-7's second half) generated from
   counterpart-map.json.
3. Charter Stage D+: synthesis of the shipped retroclone text.
