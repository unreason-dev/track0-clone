#!/usr/bin/env python3
"""Stage A, step 1 (single-leaf sources) — render a 1-page-per-scan PDF.

The sibling of split_spreads.py for sources scanned one leaf per PDF page
(e.g. OpenFRP77b / Holmes Basic): no gutter detection, no halving. Renders
each page at RENDER_DPI, extracts the embedded-text layer per page (pass 1
of the dual-pass transcription), and emits the same provenance manifest
shape split_spreads.py produces, so checkpoint.py works unchanged via
--work.

Outputs are DIGITIZATION INTERMEDIATES — gitignored, local-only.

Usage:
    python3 tools/render_singles.py --source PATH --work OpenFRP77b \
        --booklet hb [--dpi 300]

Labels are hb-p01..hb-pNN by PDF order; printed page numbers are recorded
independently during the vision pass (the label is a CLAIM, per the 74
convention).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RENDER_DPI = 300


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--booklet', default='hb')
    ap.add_argument('--dpi', type=int, default=RENDER_DPI)
    a = ap.parse_args()

    out = ROOT / 'digitization' / a.work / 'pages'
    bdir = out / a.booklet
    bdir.mkdir(parents=True, exist_ok=True)

    n_pages = 0
    for line in subprocess.run(['pdfinfo', a.source], capture_output=True,
                               text=True, check=True).stdout.splitlines():
        if line.startswith('Pages:'):
            n_pages = int(line.split()[1])
    assert n_pages, 'pdfinfo gave no page count'

    pages = []
    with tempfile.TemporaryDirectory() as td:
        for p in range(1, n_pages + 1):
            label = f'p{p:02d}'
            pid = f'{a.booklet}-{label}'
            png = bdir / f'{pid}.png'
            subprocess.run(['pdftoppm', '-png', '-r', str(a.dpi),
                            '-f', str(p), '-l', str(p),
                            a.source, str(Path(td) / 'pg')], check=True)
            rendered = sorted(Path(td).glob('pg*.png'))[-1]
            rendered.replace(png)
            txt = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p),
                                  a.source, '-'], capture_output=True,
                                 text=True, check=True).stdout
            p1 = bdir / f'{pid}.pass1.txt'
            p1.write_text(txt)
            pages.append({
                'id': pid, 'booklet': a.booklet, 'label': label,
                'pdf_page': p, 'side': 'single',
                'image': f'{a.booklet}/{pid}.png',
                'image_sha256': sha256_file(png),
                # pass-1 (embedded OCR half) — the differ reads this pointer.
                'pass1_text': f'{a.booklet}/{pid}.pass1.txt',
                'pass1_sha256': sha256_file(p1),
                'booklet_page_claimed': None,
            })
            if p % 8 == 0:
                print(f'  rendered {p}/{n_pages}')

    manifest = {
        'work': a.work, 'source_pdf': a.source,
        'source_sha256': sha256_file(Path(a.source)),
        'render_dpi': a.dpi, 'mode': 'single-leaf',
        'booklets': [{'id': a.booklet, 'title': None,
                      'pdf_pages': [1, n_pages]}],
        'pages': pages,
    }
    (out / 'pages-manifest.json').write_text(
        json.dumps(manifest, indent=1) + '\n')
    print(f'{n_pages} pages rendered -> {out}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
