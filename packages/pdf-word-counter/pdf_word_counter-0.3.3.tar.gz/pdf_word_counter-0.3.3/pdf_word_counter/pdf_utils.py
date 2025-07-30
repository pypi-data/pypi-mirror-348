"""
Wrapper functions around PyPDF2 and pdfminer.six for text extraction.
"""
from __future__ import annotations

import io
from pathlib import Path
from typing import List, Optional, Sequence

import PyPDF2

try:
    from pdfminer.high_level import extract_text, extract_text_to_fp
    from pdfminer.pdfpage import PDFPage

    HAS_PDFMINER = True
except ImportError:  # pragma: no cover
    HAS_PDFMINER = False  # pdfminer is strictly optional


def count_pages_with_pdfminer(pdf_path: str) -> int:
    """Count the number of pages in a PDF using pdfminer."""
    with open(pdf_path, "rb") as f:
        return sum(1 for _ in PDFPage.get_pages(f))


def extract_with_pypdf2(pdf: str | Path, page_numbers: Sequence[int] | None = None) -> List[str]:
    """Return a list of page texts using PyPDF2."""
    reader = PyPDF2.PdfReader(str(pdf), strict=False)
    pages = range(len(reader.pages)) if page_numbers is None else page_numbers
    return [reader.pages[p].extract_text() or "" for p in pages]


def extract_with_pdfminer(pdf: str | Path, page_numbers: Sequence[int] | None = None) -> str:
    """Return concatenated text of selected pages (or whole doc) via pdfminer.six."""
    if not HAS_PDFMINER:  # pragma: no cover
        raise RuntimeError("pdfminer.six not installed")

    if page_numbers is None:
        return extract_text(str(pdf))  # type: ignore[arg-type]

    text_chunks: List[str] = []
    with open(pdf, "rb") as fh:
        for page in page_numbers:
            buf = io.StringIO()
            extract_text_to_fp(fh, buf, page_numbers=[page])  # type: ignore[arg-type]
            text_chunks.append(buf.getvalue())
            fh.seek(0)
    return "".join(text_chunks)

