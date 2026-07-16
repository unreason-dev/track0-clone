#!/usr/bin/env python3
"""Stage A, step 3 — the numeric disagreement queue between passes.

For every page with both a pass-1 text half (embedded OCR layer) and a
pass-2 transcript (vision), compare the multisets of NUMERIC tokens and
queue the disagreements. Per the dual-pass discipline no numeric value is
trusted on one pass alone; agreement clears a token, disagreement queues it
for adjudication (operator decision D-3 governs who adjudicates).

Numeric token = maximal digit-run within the text. Digit-runs rather than
formatted tokens keep the comparison robust to pass-1's known mangling
("20%" vs "2()0A," still compares 20 vs 2,0 and FIRES, which is correct —
pass-1 corrupted the token).

Expected behavior on known pass-1 defects (validated on v2-p03): silent
cell dropouts and range-bound losses surface as pass2-only tokens.

Usage:
    python3 tools/diff_passes.py [--gold] [--pages id1,id2]

--gold compares *.gold.json instead of *.pass2.json (format-validation runs).
Output: digitization/transcripts/disagreements.json + console summary.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / "OpenFRP74" / "digitization" / "pages"
TRANSCRIPTS_DIR = ROOT / "OpenFRP74" / "digitization" / "transcripts"

DIGIT_RUN = re.compile(r"\d+")


def digit_runs(text: str) -> Counter:
    return Counter(DIGIT_RUN.findall(text))


def transcript_text(doc: dict) -> str:
    """Flatten every text-bearing surface of a pass-2 transcript."""
    parts: list[str] = []
    if doc.get("printed_page_number"):
        parts.append(str(doc["printed_page_number"]))
    for b in doc["blocks"]:
        if b.get("type") == "figure":
            continue  # figure descriptions are transcriber prose, not page text
        if b.get("text"):
            parts.append(b["text"])
        for item in b.get("items") or []:
            parts.append(item)
        for col in b.get("columns") or []:
            parts.append(col)
        for row in b.get("rows") or []:
            parts.extend(row)
    return "\n".join(parts)


def diff_page(page_id: str, pass1_path: Path, pass2_doc: dict) -> dict | None:
    p1 = digit_runs(pass1_path.read_text(encoding="utf-8"))
    p2 = digit_runs(transcript_text(pass2_doc))
    only1 = p1 - p2
    only2 = p2 - p1
    if not only1 and not only2:
        return None
    return {
        "page": page_id,
        "pass1_only": sorted(only1.elements()),
        "pass2_only": sorted(only2.elements()),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", action="store_true",
                    help="diff *.gold.json instead of *.pass2.json")
    ap.add_argument("--pages", help="comma-separated page ids to limit")
    args = ap.parse_args()

    suffix = ".gold.json" if args.gold else ".pass2.json"
    manifest = json.loads((PAGES_DIR / "pages-manifest.json").read_text())
    by_id = {r["id"]: r for r in manifest["pages"]}
    only = set(args.pages.split(",")) if args.pages else None

    queue, clean, missing = [], 0, 0
    for tpath in sorted(TRANSCRIPTS_DIR.glob(f"*{suffix}")):
        page_id = tpath.name[: -len(suffix)]
        if only and page_id not in only:
            continue
        rec = by_id.get(page_id)
        if rec is None or rec.get("pass1_text") is None:
            missing += 1
            continue
        doc = json.loads(tpath.read_text())
        d = diff_page(page_id, PAGES_DIR / rec["pass1_text"], doc)
        if d is None:
            clean += 1
        else:
            queue.append(d)

    out = TRANSCRIPTS_DIR / "disagreements.json"
    out.write_text(json.dumps(
        {"mode": "gold" if args.gold else "pass2",
         "clean_pages": clean, "queued_pages": len(queue), "queue": queue},
        indent=1))
    print(f"{clean} pages clean, {len(queue)} pages queued, {missing} skipped "
          f"(no pass1) → {out.relative_to(ROOT)}")
    for d in queue[:20]:
        print(f"  {d['page']}: pass1-only {d['pass1_only'][:12]} "
              f"| pass2-only {d['pass2_only'][:12]}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
