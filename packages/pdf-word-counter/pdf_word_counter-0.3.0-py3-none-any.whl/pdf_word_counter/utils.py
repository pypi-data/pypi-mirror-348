"""
Utility helpers (filename parsing, page-range parsing, etc.).
"""
from __future__ import annotations

import os
import re
from typing import Dict, Iterable, List, Optional, Sequence


def find_year(fname: str, default: str | None = None) -> str | None:
    """Return the first 4-digit number found in *fname* (commonly a year)."""
    m = re.findall(r"\d{4}", os.path.basename(fname))
    return m[0] if m else default


def dict_to_lists(d: Dict[str, Iterable]) -> Dict[str, List]:
    """Ensure every value is a *list* to satisfy Astropy / pandas constructors."""
    return {k: list(v if isinstance(v, (list, tuple)) else [v]) for k, v in d.items()}


def compile_words(words: Sequence[str], flags: int):
    """Pre-compile regex patterns for faster repeated use."""
    import re

    return {w: re.compile(w, flags=flags) for w in words}


def apply_separators(fname: str, mapping: Dict[str, Dict[str, int]]) -> Dict[str, str]:
    """
    Split *fname* on each separator in *mapping* and populate extra columns.

    Example
    -------
    >>> apply_separators('2023_report.final.pdf',
    ...                  {'_': {'category': -2}, '.': {'ext': -1}})
    {'category': 'report', 'ext': 'pdf'}
    """
    out: Dict[str, str] = {}
    for sep, cols in mapping.items():
        parts = fname.split(sep)
        for col, idx in cols.items():
            if -len(parts) <= idx < len(parts):
                out[col] = parts[idx].strip()
    return out


def parse_page_range(spec: str | None) -> Optional[List[int]]:
    """
    Turn ``"1,3-5,-1"`` into a list of page indices (0-based, negatives allowed).

    Returns ``None`` for an empty / ``None`` spec.
    """
    if not spec or not spec.strip():
        return None

    pages: List[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = map(int, part.split("-"))
            pages.extend(range(start, end + 1))
        else:
            pages.append(int(part))
    return pages

