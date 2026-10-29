#!/usr/bin/env python3
"""Build the flea-market booth printable pack.

Converts HTML/CSS source sheets in sheets/ into print-ready PDF files in
printables/ using WeasyPrint. Fully local, no network access needed.

Usage:
    python3 build.py            build every sheet
    python3 build.py <name>...  build only the named sheets (no extension)
    python3 build.py --clean    delete generated PDFs first
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from weasyprint import HTML

ROOT = Path(__file__).resolve().parent
SHEETS_DIR = ROOT / "sheets"
OUT_DIR = ROOT / "printables"

# Fallback order matters: it is also the order the README lists the sheets.
SHEET_ORDER = [
    "blanket-layout",
    "price-signs",
    "price-stickers",
    "cash-tally",
    "change-card",
    "sold-tickets",
    "rain-plan",
    "load-sheet",
]


def discover_sheets() -> list[str]:
    """Get sheet names from sheets/*.html in SHEET_ORDER, then any extras."""
    found = {p.stem for p in SHEETS_DIR.glob("*.html") if p.stem != "template"}
    ordered = [name for name in SHEET_ORDER if name in found]
    extras = sorted(found - set(SHEET_ORDER))
    return ordered + extras


def build_sheet(name: str, out_dir: Path) -> Path:
    src = SHEETS_DIR / f"{name}.html"
    if not src.is_file():
        raise FileNotFoundError(f"no sheet named '{name}' ({src})")
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / f"{name}.pdf"
    # base_url lets relative <link> stylesheets resolve.
    HTML(filename=str(src), base_url=str(SHEETS_DIR)).write_pdf(str(dest))
    return dest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build printable PDFs")
    parser.add_argument("names", nargs="*", help="sheet names (no .html)")
    parser.add_argument("--clean", action="store_true", help="remove printables/ first")
    parser.add_argument("--out", type=Path, default=OUT_DIR, help="output directory")
    args = parser.parse_args(argv)

    if args.clean and args.out.is_dir():
        shutil.rmtree(args.out)

    names = args.names or discover_sheets()
    for name in names:
        try:
            dest = build_sheet(name, args.out)
        except FileNotFoundError as exc:
            print(f"error: {exc}", file=sys.stderr)
            all_names = discover_sheets()
            print(f"available sheets: {', '.join(all_names)}", file=sys.stderr)
            return 1
        except Exception as exc:  # noqa: BLE001 - report, keep building others
            print(f"error: {name}: {exc}", file=sys.stderr)
            continue
        print(f"built {dest}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
