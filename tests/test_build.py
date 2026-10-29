"""Verify that every sheet in sheets/ builds a valid, unbranded PDF."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pypdf
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from build import OUT_DIR, SHEETS_DIR, build_sheet, discover_sheets  # noqa: E402

SHEETS = discover_sheets()

BRAND_WORDS = re.compile(r"asdale|dylan", re.IGNORECASE)


# ---------------------------------------------------------------- fixtures

@pytest.fixture(scope="module")
def built_pdf_factory(tmp_path_factory):
    """Build each sheet on demand; cache by sheet name inside the session."""
    cache = {}

    def _build(name: str) -> Path:
        if name not in cache:
            out = tmp_path_factory.mktemp("pdfs") / name
            cache[name] = build_sheet(name, out)
        return cache[name]

    return _build


# ---------------------------------------------------------------- basics

def test_all_expected_sheets_exist():
    expected = {
        "blanket-layout", "price-signs", "price-stickers", "cash-tally",
        "change-card", "sold-tickets", "rain-plan", "load-sheet",
    }
    missing = expected - set(SHEETS)
    assert not missing, f"missing sheets: {sorted(missing)}"


def test_every_sheet_has_html_and_stylesheet_reference():
    for name in SHEETS:
        src = (SHEETS_DIR / f"{name}.html").with_suffix(".html")
        text = src.read_text(encoding="utf-8")
        assert 'rel="stylesheet"' in text or "stylesheet" in text, name


# ---------------------------------------------------------------- builds

@pytest.mark.parametrize("name", SHEETS)
def test_sheet_builds_nonempty_pdf(name, built_pdf_factory):
    pdf = built_pdf_factory(name)
    assert pdf.is_file()
    data = pdf.read_bytes()
    assert data.startswith(b"%PDF-"), f"{name}: not a PDF header"
    assert len(data) > 5_000, f"{name}: suspiciously small PDF ({len(data)} B)"


@pytest.mark.parametrize("name", SHEETS)
def test_sheet_pdf_has_pages_with_text(name, built_pdf_factory):
    pdf_path = built_pdf_factory(name)
    reader = pypdf.PdfReader(str(pdf_path))
    assert len(reader.pages) >= 1
    text = "".join((page.extract_text() or "") for page in reader.pages)
    assert len(text) >= 100, f"{name}: too little extractable text"


@pytest.mark.parametrize("name", SHEETS)
def test_sheet_pdf_is_letter_sized(name, built_pdf_factory):
    pdf_path = built_pdf_factory(name)
    reader = pypdf.PdfReader(str(pdf_path))
    for page in reader.pages:
        box = page.mediabox
        w, h = float(box.width), float(box.height)
        letter_ok = (
            (abs(w - 612) < 3 and abs(h - 792) < 3)          # portrait
            or (abs(w - 792) < 3 and abs(h - 612) < 3)        # landscape
        )
        assert letter_ok, f"{name}: mediabox {w}x{h} is not US Letter"


# ---------------------------------------------------------------- unbranded

@pytest.mark.parametrize("name", SHEETS)
def test_pdf_output_is_unbranded(name, built_pdf_factory):
    pdf_path = built_pdf_factory(name)
    reader = pypdf.PdfReader(str(pdf_path))
    text = "".join((page.extract_text() or "") for page in reader.pages)
    match = BRAND_WORDS.search(text)
    assert not match, f"{name}: PDF output contains branding ('{match.group(0)}')"


# ---------------------------------------------------------------- default build

def test_default_build_writes_into_printables_dir():
    for name in SHEETS:
        build_sheet(name, OUT_DIR)
    for name in SHEETS:
        pdf = OUT_DIR / f"{name}.pdf"
        assert pdf.is_file()
        reader = pypdf.PdfReader(str(pdf))
        assert len(reader.pages) >= 1
