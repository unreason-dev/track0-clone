#!/usr/bin/env python3
"""Grind checkpoint: stamp image hashes into transcripts from the pages
manifest, validate all transcripts against the schema, run the differ,
and print progress (transcribed / total pages)."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "OpenFRP74" / "digitization" / "pages"
TRANS = ROOT / "OpenFRP74" / "digitization" / "transcripts"


def main() -> int:
    manifest = json.loads((PAGES / "pages-manifest.json").read_text())
    by_id = {r["id"]: r for r in manifest["pages"]}

    stamped = 0
    for p in TRANS.glob("*.pass2.json"):
        doc = json.loads(p.read_text())
        rec = by_id[doc["id"]]
        if doc["source"].get("image_sha256") != rec["image_sha256"]:
            doc["source"]["image_sha256"] = rec["image_sha256"]
            p.write_text(json.dumps(doc, indent=1, ensure_ascii=False))
            stamped += 1

    done = {p.name[:-len(".pass2.json")] for p in TRANS.glob("*.pass2.json")}
    todo = [r["id"] for r in manifest["pages"] if r["id"] not in done]
    print(f"stamped {stamped}; progress {len(done)}/{len(manifest['pages'])} "
          f"({len(todo)} remaining)")
    if todo:
        print("next:", ", ".join(todo[:12]), "…" if len(todo) > 12 else "")

    rc1 = subprocess.run([sys.executable, str(ROOT / "tools" / "transcribe_pages.py"),
                          "--validate"]).returncode
    rc2 = subprocess.run([sys.executable, str(ROOT / "tools" / "diff_passes.py")]).returncode
    return rc1 or rc2


if __name__ == "__main__":
    sys.exit(main())
