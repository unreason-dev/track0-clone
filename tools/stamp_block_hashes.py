#!/usr/bin/env python3
"""Compute per-block content hashes for pass-2 transcripts.

Completes the provenance unit {work, booklet, page, block_index, content_hash}
promised by the pipeline methodology (Stage A). Hashes are COMPUTED here, never
model-emitted, and live in a sidecar manifest rather than inside the transcripts
so the page-transcript schema stays closed (additionalProperties: false) and
transcripts remain pure transcriber output.

Hash input per block: the content-bearing fields only —
  type, text, level, underlined, items, columns, caption, rows
serialized as canonical JSON (sorted keys, no whitespace, UTF-8). Excluded:
transcriber_note (transcriber commentary, not source content), continuation
flags and index (structural bookkeeping), and all source/provenance fields
(already covered by image_sha256 in the transcript itself).

Output: digitization/<work>/transcripts/block-hashes.json
  { "<page id>": {"work":…, "booklet":…, "label":…, "image_sha256":…,
                   "blocks": [{"block_index": n, "content_sha256": …}, …]}, … }

Deterministic: re-running on unchanged transcripts yields byte-identical output.
"""

import hashlib
import json
from pathlib import Path

import argparse
_ap = argparse.ArgumentParser()
_ap.add_argument("--work", default="OpenFRP74")
_ARGS, _ = _ap.parse_known_args()
ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPTS = ROOT / "digitization" / _ARGS.work / "transcripts"
OUT = TRANSCRIPTS / "block-hashes.json"

CONTENT_FIELDS = ("type", "text", "level", "underlined", "items", "columns", "caption", "rows")


def block_hash(block: dict) -> str:
    payload = {k: block.get(k) for k in CONTENT_FIELDS}
    canon = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def main() -> None:
    manifest = {}
    for path in sorted(TRANSCRIPTS.glob("*.pass2.json")):
        doc = json.loads(path.read_text())
        src = doc["source"]
        manifest[doc["id"]] = {
            "work": src["work"],
            "booklet": src["booklet"],
            "label": src["label"],
            "image_sha256": src["image_sha256"],
            "blocks": [
                {"block_index": b["index"], "content_sha256": block_hash(b)}
                for b in doc["blocks"]
            ],
        }
    OUT.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")
    n_blocks = sum(len(p["blocks"]) for p in manifest.values())
    print(f"stamped {n_blocks} block hashes across {len(manifest)} pages -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
