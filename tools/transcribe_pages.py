#!/usr/bin/env python3
"""Stage A, step 2 — pass-2 vision transcription of split booklet pages.

Sends each page image to Claude (vision) and stores a block-model JSON
transcript per page (schema: tools/page-transcript.schema.json). Transcripts
are DIGITIZATION INTERMEDIATES — gitignored, local-only.

Modes:
    --pilot v2-p03,v1-p19      synchronous transcription of named pages
    --submit [--pages ...]     submit a Message Batch for all/named pages
    --poll                     check batch status
    --collect                  fetch batch results -> per-page transcripts
    --validate                 validate all transcripts against the schema

Requires ANTHROPIC_API_KEY (or an `ant auth login` profile) and
`pip install anthropic jsonschema`.

Design notes (durable, see docs/retroclone-pipeline-methodology.md §A.3):
- Verbatim fidelity: source typos preserved; cells as printed strings;
  uncertainty flagged, never guessed silently.
- The transcriber is NEVER shown the arithmetic page-number claim — its
  printed_page_number observation independently verifies the split.
- Batches API for full runs (50% cost, not latency-sensitive).
"""

from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / "OpenFRP74" / "digitization" / "pages"
OUT_DIR = ROOT / "OpenFRP74" / "digitization" / "transcripts"
SCHEMA_PATH = Path(__file__).resolve().parent / "page-transcript.schema.json"
BATCH_STATE = OUT_DIR / "batch-state.json"

MODEL = "claude-opus-4-8"
MAX_TOKENS = 16000

SYSTEM_PROMPT = """\
You are transcribing a scanned page from a 1974 tabletop-wargame rules \
booklet into structured JSON. This is archival transcription, not editing:

- Transcribe VERBATIM, preserving the source's own spellings, typos, \
punctuation, and capitalization exactly as printed. Do not correct anything. \
Historic typos are data.
- Table cells are strings exactly as printed (e.g. "30 - 300", "1-1/1/2", \
"4 +1"). Do not interpret, normalize, or split them.
- When a printed value spans multiple columns (e.g. "All variable - - - -"), \
put the full text in the FIRST spanned cell and leave the remaining spanned \
cells as empty strings. When one cell's content wraps across printed lines, \
join the lines with a newline character.
- If a glyph or token is unclear, give your best reading in place and record \
it in uncertain_tokens with the reason. Never silently guess.
- Describe illustrations as figure blocks; do not omit them.
- Mark inline print emphasis with lightweight markup: __underlined span__, \
~~struck-through span~~. Underlines in these booklets are often semantic \
(corrected readings, emphasis) — preserve them. Handwritten ink annotations \
are NOT printed text: describe them in transcriber_note instead.
- Record the printed page number exactly as it appears, or null if none.
- Reading order: top to bottom; note blocks that visibly continue from the \
previous page or onto the next.
- Faint mirrored text is ink bleed-through from the reverse side: ignore it.
- Character slivers at the extreme bound edge are spillover from the FACING \
page across the binding: ignore them (they are transcribed with their own \
page). Note their presence in transcriber_note on the first block only.
- A header spanning several table columns goes in the table's `caption` \
field, verbatim.
"""

USER_PROMPT = """\
Transcribe this page ({context}) into the required JSON structure. \
Every visible content element belongs to exactly one block, in reading order.\
"""


def load_manifest() -> dict:
    return json.loads((PAGES_DIR / "pages-manifest.json").read_text())


def page_records(manifest: dict, only: list[str] | None) -> list[dict]:
    recs = manifest["pages"]
    if only:
        wanted = set(only)
        recs = [r for r in recs if r["id"] in wanted]
        missing = wanted - {r["id"] for r in recs}
        if missing:
            sys.exit(f"unknown page ids: {sorted(missing)}")
    return recs


def output_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text())


def request_params(rec: dict) -> dict:
    """Messages API params for one page (shared by sync + batch paths)."""
    img_path = PAGES_DIR / rec["image"]
    data = base64.standard_b64encode(img_path.read_bytes()).decode()
    context = f"booklet {rec['booklet']}, one page of a scanned three-booklet set"
    return {
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "system": SYSTEM_PROMPT,
        "output_config": {"format": {"type": "json_schema", "schema": output_schema()}},
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image",
                 "source": {"type": "base64", "media_type": "image/png", "data": data}},
                {"type": "text", "text": USER_PROMPT.format(context=context)},
            ],
        }],
    }


def write_transcript(rec: dict, payload: dict, meta: dict) -> Path:
    out = {
        "id": rec["id"],
        "source": {
            "work": "OpenFRP74",
            "booklet": rec["booklet"],
            "label": rec["label"],
            "pdf_page": rec["pdf_page"],
            "side": rec["side"],
            "image": rec["image"],
            "image_sha256": rec["image_sha256"],
        },
        "transcription": meta,
        **payload,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{rec['id']}.pass2.json"
    path.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    return path


def parse_response_text(text: str) -> dict:
    return json.loads(text)


def cmd_pilot(ids: list[str]) -> int:
    import anthropic
    client = anthropic.Anthropic()
    manifest = load_manifest()
    for rec in page_records(manifest, ids):
        print(f"transcribing {rec['id']} …", flush=True)
        params = request_params(rec)
        with client.messages.stream(**params) as stream:
            resp = stream.get_final_message()
        if resp.stop_reason == "refusal":
            print(f"  REFUSAL on {rec['id']} — check stop_details; skipping")
            continue
        text = next(b.text for b in resp.content if b.type == "text")
        payload = parse_response_text(text)
        meta = {"pass": 2, "model": resp.model, "mode": "pilot-sync",
                "usage": {"input_tokens": resp.usage.input_tokens,
                          "output_tokens": resp.usage.output_tokens}}
        path = write_transcript(rec, payload, meta)
        print(f"  → {path.relative_to(ROOT)}  "
              f"(blocks: {len(payload['blocks'])}, "
              f"printed page: {payload['printed_page_number']!r}, "
              f"uncertain: {len(payload['uncertain_tokens'])})")
    return 0


def cmd_submit(ids: list[str] | None) -> int:
    import anthropic
    client = anthropic.Anthropic()
    manifest = load_manifest()
    recs = page_records(manifest, ids)
    requests = [{"custom_id": rec["id"], "params": request_params(rec)}
                for rec in recs]
    batch = client.messages.batches.create(requests=requests)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    BATCH_STATE.write_text(json.dumps(
        {"batch_id": batch.id, "submitted": len(requests),
         "page_ids": [r["id"] for r in recs]}, indent=1))
    print(f"submitted batch {batch.id} with {len(requests)} pages; "
          f"state → {BATCH_STATE.relative_to(ROOT)}")
    return 0


def cmd_poll() -> int:
    import anthropic
    client = anthropic.Anthropic()
    state = json.loads(BATCH_STATE.read_text())
    batch = client.messages.batches.retrieve(state["batch_id"])
    print(f"batch {batch.id}: {batch.processing_status}  counts={batch.request_counts}")
    return 0 if batch.processing_status == "ended" else 2


def cmd_collect() -> int:
    import anthropic
    client = anthropic.Anthropic()
    state = json.loads(BATCH_STATE.read_text())
    manifest = load_manifest()
    by_id = {r["id"]: r for r in manifest["pages"]}
    ok, failed = 0, []
    for result in client.messages.batches.results(state["batch_id"]):
        rec = by_id.get(result.custom_id)
        if rec is None:
            failed.append((result.custom_id, "unknown page id"))
            continue
        if result.result.type != "succeeded":
            failed.append((result.custom_id, result.result.type))
            continue
        msg = result.result.message
        if msg.stop_reason == "refusal":
            failed.append((result.custom_id, "refusal"))
            continue
        text = next((b.text for b in msg.content if b.type == "text"), None)
        if text is None:
            failed.append((result.custom_id, "no text block"))
            continue
        try:
            payload = parse_response_text(text)
        except json.JSONDecodeError as e:
            failed.append((result.custom_id, f"bad json: {e}"))
            continue
        meta = {"pass": 2, "model": msg.model, "mode": "batch",
                "batch_id": state["batch_id"],
                "usage": {"input_tokens": msg.usage.input_tokens,
                          "output_tokens": msg.usage.output_tokens}}
        write_transcript(rec, payload, meta)
        ok += 1
    print(f"collected {ok} transcripts; {len(failed)} failures")
    for cid, why in failed:
        print(f"  FAILED {cid}: {why}")
    (OUT_DIR / "collect-report.json").write_text(json.dumps(
        {"ok": ok, "failed": failed}, indent=1))
    return 0 if not failed else 1


def cmd_validate() -> int:
    import jsonschema
    schema = output_schema()
    # The stored transcript wraps the model payload with id/source/transcription.
    n, bad = 0, 0
    for path in sorted(OUT_DIR.glob("*.pass2.json")):
        doc = json.loads(path.read_text())
        payload = {k: doc[k] for k in ("printed_page_number", "blocks", "uncertain_tokens")}
        try:
            jsonschema.validate(payload, schema)
            n += 1
        except jsonschema.ValidationError as e:
            bad += 1
            print(f"INVALID {path.name}: {e.message}")
    print(f"validated {n} transcripts OK, {bad} invalid")
    return 0 if bad == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--pilot", help="comma-separated page ids, transcribed synchronously")
    g.add_argument("--submit", action="store_true", help="submit a Message Batch")
    g.add_argument("--poll", action="store_true")
    g.add_argument("--collect", action="store_true")
    g.add_argument("--validate", action="store_true")
    ap.add_argument("--pages", help="comma-separated page ids to limit --submit")
    args = ap.parse_args()
    if args.pilot:
        return cmd_pilot(args.pilot.split(","))
    if args.submit:
        return cmd_submit(args.pages.split(",") if args.pages else None)
    if args.poll:
        return cmd_poll()
    if args.collect:
        return cmd_collect()
    if args.validate:
        return cmd_validate()
    return 1


if __name__ == "__main__":
    sys.exit(main())
