#!/usr/bin/env python3
"""Stage A, step 1 — split the 2-up source scan into single booklet pages.

Renders each PDF page at RENDER_DPI, splits spreads at a darkness-detected
gutter, writes per-booklet-page PNGs + the embedded-text-layer half (pass 1
of the dual-pass transcription), and emits a provenance manifest with
content hashes.

Outputs are DIGITIZATION INTERMEDIATES — gitignored, local-only (operator
ruling 2026-07-16). Only this script and the (hash-only) manifest schema are
public.

Usage:
    python3 tools/split_spreads.py [--source PATH] [--out DIR] [--dpi N]

Booklet layout (measured, findings/openfrp74-source-disposition-2026-07-16.md):
    V1 Men & Magic                       PDF  1-20
    V2 Monsters & Treasure               PDF 21-42
    V3 Underworld & Wilderness Adv.      PDF 43-63
Per booklet: cover (single page), then an unnumbered spread (inside front
cover | title page), then content spreads carrying booklet pages (2,3),
(4,5), ... Page-number labels from this arithmetic are CLAIMS to be
verified against the printed page numbers during the vision pass; the
manifest marks them `booklet_page_claimed`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass, asdict
from pathlib import Path

from PIL import Image

DEFAULT_SOURCE = "/Users/jon/dev/ai/reference/Dungeons & Dragons.pdf"
DEFAULT_OUT = Path(__file__).resolve().parent.parent / "OpenFRP74" / "digitization" / "pages"
RENDER_DPI = 300

# Booklet definitions: (id, title, first_pdf_page, last_pdf_page).
# A first==last entry is a single-leaf artifact (no cover/title structure).
# PDF p63 is the Correction Sheet errata insert shipped with early printings
# — its own work, NOT V3 p38 (discovered at first split run; the aspect-
# ratio self-check flagged it).
BOOKLETS = [
    ("v1", "Men & Magic", 1, 20),
    ("v2", "Monsters & Treasure", 21, 42),
    ("v3", "The Underworld & Wilderness Adventures", 43, 62),
    ("errata", "Correction Sheet (single-leaf insert)", 63, 63),
]

# A page is a spread iff it is wider than tall (covers scanned single).
# Gutter search is confined to this central fraction of the width.
GUTTER_BAND = 0.24


@dataclass
class PageRecord:
    id: str                      # e.g. "v1-p07", "v2-cover", "v3-title"
    booklet: str                 # v1 | v2 | v3
    label: str                   # cover | ifc | title | pNN
    booklet_page_claimed: int | None  # arithmetic claim; vision pass verifies
    pdf_page: int                # 1-indexed source PDF page
    side: str                    # single | left | right
    image: str                   # path relative to out dir
    image_sha256: str
    width_px: int
    height_px: int
    split_x_px: int | None       # gutter x in the rendered spread (spreads only)
    pass1_text: str | None       # path relative to out dir, embedded-OCR half
    pass1_sha256: str | None


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def render_page(source: Path, pdf_page: int, dpi: int, tmpdir: Path) -> Path:
    """Render one PDF page to PNG via pdftoppm; returns the PNG path."""
    stem = tmpdir / f"render-{pdf_page:03d}"
    subprocess.run(
        ["pdftoppm", "-png", "-r", str(dpi), "-f", str(pdf_page), "-l", str(pdf_page),
         str(source), str(stem)],
        check=True, capture_output=True,
    )
    hits = sorted(tmpdir.glob(f"render-{pdf_page:03d}*.png"))
    if len(hits) != 1:
        raise RuntimeError(f"expected 1 rendered file for pdf page {pdf_page}, got {hits}")
    return hits[0]


def find_gutter(img: Image.Image) -> int:
    """Darkest-column scan in the central band — the book spine shadow.

    Falls back to the exact midpoint if the darkness signal is flat
    (< 8 gray levels of spread), so a spine-less scan still splits sanely.
    """
    gray = img.convert("L")
    # Downsample rows for speed; keep full x resolution.
    w, h = gray.size
    band_lo = int(w * (0.5 - GUTTER_BAND / 2))
    band_hi = int(w * (0.5 + GUTTER_BAND / 2))
    small = gray.resize((w, 256))
    px = small.load()
    best_x, best_mean = w // 2, 255.0
    means = []
    for x in range(band_lo, band_hi):
        s = 0
        for y in range(256):
            s += px[x, y]
        m = s / 256.0
        means.append(m)
        if m < best_mean:
            best_mean, best_x = m, x
    if max(means) - min(means) < 8.0:
        return w // 2
    return best_x


def pdf_page_points(source: Path, pdf_page: int) -> tuple[float, float]:
    """(width, height) of the PDF page in points, via pypdf."""
    from pypdf import PdfReader
    reader = PdfReader(str(source))
    box = reader.pages[pdf_page - 1].mediabox
    return float(box.width), float(box.height)


# Inset applied to the TEXT crop on the gutter side only (fraction of page
# width). The image crop keeps everything; the text crop pulls back from the
# cut so facing-page character slivers don't inject phantom tokens into
# pass 1 (verified noise source: v1-p19 pilot diff).
GUTTER_TEXT_INSET_FRAC = 0.012

# Bleed applied to the IMAGE crop on the gutter side (fraction of spread
# width): each half keeps a sliver of the other side so glyphs can never be
# lost to the cut (verified defect: v1-p03's first character column was
# clipped — its text runs tight to the gutter). Facing-page slivers are
# already ignorable by transcription convention; lost glyphs are not
# recoverable.
GUTTER_IMAGE_BLEED_FRAC = 0.012


def extract_half_text(source: Path, pdf_page: int, half: str,
                      split_frac: float | None) -> str:
    """Embedded-text-layer extraction for one half of a spread (or a full
    single page), via pdftotext -layout with a crop box in 72-dpi units."""
    w_pt, h_pt = pdf_page_points(source, pdf_page)
    inset = int(w_pt * GUTTER_TEXT_INSET_FRAC)
    if half == "single":
        x, wid = 0, int(w_pt)
    elif half == "left":
        x, wid = 0, int(w_pt * (split_frac or 0.5)) - inset
    else:
        x = int(w_pt * (split_frac or 0.5)) + inset
        wid = int(w_pt) - x
    out = subprocess.run(
        ["pdftotext", "-layout", "-r", "72",
         "-f", str(pdf_page), "-l", str(pdf_page),
         "-x", str(x), "-y", "0", "-W", str(wid), "-H", str(int(h_pt)),
         str(source), "-"],
        check=True, capture_output=True,
    )
    return out.stdout.decode("utf-8", errors="replace")


def labels_for_booklet(first: int, last: int):
    """Yield (pdf_page, [(side, label, booklet_page_claimed), ...])."""
    if first == last:  # single-leaf artifact (e.g. the Correction Sheet)
        yield first, [("single", "sheet", None)]
        return
    yield first, [("single", "cover", None)]
    yield first + 1, [("left", "ifc", None), ("right", "title", None)]
    page = 2
    for pdf_page in range(first + 2, last + 1):
        yield pdf_page, [
            ("left", f"p{page:02d}", page),
            ("right", f"p{page + 1:02d}", page + 1),
        ]
        page += 2


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=DEFAULT_SOURCE)
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--dpi", type=int, default=RENDER_DPI)
    args = ap.parse_args()

    source = Path(args.source)
    out_root = Path(args.out)
    if not source.exists():
        print(f"source not found: {source}", file=sys.stderr)
        return 1

    records: list[PageRecord] = []
    warnings: list[str] = []

    with tempfile.TemporaryDirectory() as td:
        tmpdir = Path(td)
        for bk_id, bk_title, first, last in BOOKLETS:
            bk_dir = out_root / bk_id
            bk_dir.mkdir(parents=True, exist_ok=True)
            for pdf_page, sides in labels_for_booklet(first, last):
                rendered = render_page(source, pdf_page, args.dpi, tmpdir)
                img = Image.open(rendered)
                w, h = img.size
                is_spread = w > h
                expected_spread = sides[0][0] != "single"
                if is_spread != expected_spread:
                    warnings.append(
                        f"{bk_id} pdf p{pdf_page}: aspect says "
                        f"{'spread' if is_spread else 'single'}, layout map says "
                        f"{'spread' if expected_spread else 'single'} — following aspect"
                    )
                    if not is_spread:
                        sides = [("single", sides[0][1], sides[0][2])]

                split_x = find_gutter(img) if is_spread else None
                split_frac = (split_x / w) if split_x is not None else None

                bleed = int(w * GUTTER_IMAGE_BLEED_FRAC) if is_spread else 0
                for side, label, claimed in sides:
                    if side == "single":
                        half_img = img
                    elif side == "left":
                        half_img = img.crop((0, 0, min(w, split_x + bleed), h))
                    else:
                        half_img = img.crop((max(0, split_x - bleed), 0, w, h))

                    rec_id = f"{bk_id}-{label}"
                    img_rel = f"{bk_id}/{rec_id}.png"
                    img_path = out_root / img_rel
                    half_img.save(img_path)

                    txt = extract_half_text(source, pdf_page, side, split_frac)
                    txt_rel = f"{bk_id}/{rec_id}.pass1.txt"
                    (out_root / txt_rel).write_text(txt, encoding="utf-8")

                    records.append(PageRecord(
                        id=rec_id, booklet=bk_id, label=label,
                        booklet_page_claimed=claimed, pdf_page=pdf_page,
                        side=side, image=img_rel,
                        image_sha256=sha256_file(img_path),
                        width_px=half_img.size[0], height_px=half_img.size[1],
                        split_x_px=split_x,
                        pass1_text=txt_rel,
                        pass1_sha256=hashlib.sha256(txt.encode()).hexdigest(),
                    ))
                img.close()
                rendered.unlink()

    manifest = {
        "source": {
            "file": source.name,
            "sha256": sha256_file(source),
            "render_dpi": args.dpi,
        },
        "booklets": [
            {"id": b[0], "title": b[1], "pdf_pages": [b[2], b[3]]} for b in BOOKLETS
        ],
        "note": ("booklet_page_claimed values are arithmetic claims from the "
                 "spread layout; the vision pass verifies them against printed "
                 "page numbers before anything downstream trusts them"),
        "warnings": warnings,
        "pages": [asdict(r) for r in records],
    }
    (out_root / "pages-manifest.json").write_text(
        json.dumps(manifest, indent=1), encoding="utf-8")

    spreads = sum(1 for r in records if r.side in ("left", "right")) // 2
    singles = sum(1 for r in records if r.side == "single")
    print(f"wrote {len(records)} page records ({singles} singles, {spreads} spreads split) "
          f"→ {out_root}")
    for w in warnings:
        print(f"WARNING: {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
