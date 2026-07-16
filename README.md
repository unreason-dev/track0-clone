# track0-clone — OpenFRP lineage corpora

Schema-corpora for historical D&D-family systems, built as a lineage graph of
sibling corpora walked by a delta pipeline. Each node (OpenFRP74, OpenFRP76,
…) is a full corpus — its own schemas, entries, legibility manifest, and
validation target — connected to its ancestor by a derivation edge carrying a
machine-verified changelog.

This is the RetroCloner program: unprotectable **mechanics** (systems,
procedures, numeric facts) extracted from the historical texts into typed
fields, with all shipped **expression** carrying one of three provenances —
adapted from the CC-BY-4.0 SRD 5.1 (with attribution), synthesized, or
operator-authored. No source prose ships; a mechanical similarity gate (the
expression firewall) enforces that, not a protocol.

## Public-distro rule (operator ruling, 2026-07-16)

**This repo carries exclusively content intended for public distribution.**

- Digitization intermediates (OCR output, verified transcriptions, page
  images) contain the source texts' expression and are **gitignored** —
  local working substrate only, never committed, never shipped.
- Source scans/PDFs live outside this repo (or under gitignored paths) and
  are never committed.
- What IS committed: schemas, corpus entries (mechanics + firewalled
  expression), manifests, edge changelogs, interpretation records, findings
  and disposition docs.

## Layout

Directory conventions follow the Track 0 `system/5.1-srd/` pattern where the
source ontology allows (per-section subdirectories, one JSON file per entry
with filename↔id equality, co-located `<singular>.schema.json`, generated
legibility manifest). Each node re-projects the ontology from its own source
— sections that don't exist for a node (subclasses, subraces, …) simply
don't appear, and node-specific sections (e.g. race-as-class machinery) are
authored from the source's own structure.

```
OpenFRP74/                  # the 1974 three-booklet node (pilot)
  <section>/                # per-section: schema + entries, 5.1-srd style
  digitization/             # GITIGNORED — local transcription intermediates
findings/                   # disposition/findings docs (append-only-by-creation:
                            # one new dated doc per cycle, never rewrite)
```

## Status

Pilot node OpenFRP74 is at Stage A (digitization substrate). See
`findings/openfrp74-source-disposition-2026-07-16.md` for the source
suitability assessment.
