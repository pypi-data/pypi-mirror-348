"""
High-level search functions (`search_pdf` and `search_pdfs`).
"""
from __future__ import annotations

import concurrent.futures as cf
import logging
import math
import unicodedata
from collections import OrderedDict
from glob import glob
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

from tqdm import tqdm

from . import output as _out
from .pdf_utils import (
    count_pages_with_pdfminer,
    extract_with_pdfminer,
    extract_with_pypdf2,
    HAS_PDFMINER,
)
from .utils import apply_separators, compile_words, dict_to_lists, find_year

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------
def search_pdf(
    pdf: str | Path,
    words: Sequence[str],
    *,
    ignore_case: bool = True,
    pages: Sequence[int] | None = None,
    include_pages: bool = True,
    include_year: bool = False,
    default_year: str | None = None,
    include_filename: bool = True,
    keep_extension: bool = False,
    separators: Dict[str, Dict[str, int]] | None = None,
    progress_interval: int | None = None,
    use_pdfminer: bool = False,
    normalise_unicode: bool = False,
    unicode_form: str = "NFKC",
):
    """
    Search *pdf* for *words* and return a one-row Astropy Table or pandas DataFrame.
    """
    pdf = Path(pdf)
    flags = 0 if ignore_case else 0
    if ignore_case:
        import re

        flags = re.IGNORECASE
    regexes = compile_words(words, flags)

    fname_full = pdf.name
    fname = fname_full if keep_extension else pdf.stem

    # Result row -------------------------------------------------------
    row: Dict[str, Iterable] = OrderedDict()
    if include_filename:
        row["file"] = fname
    if include_year:
        row["year"] = find_year(fname_full, default_year)
    if separators:
        row.update(apply_separators(fname_full if keep_extension else fname, separators))
    if include_pages:
        row["pages"] = 0

    for w in words:
        row[w] = 0

    # Choose extraction backend ---------------------------------------
    if use_pdfminer and HAS_PDFMINER:
        if include_pages:
            row["pages"] = count_pages_with_pdfminer(str(pdf)) 
        text = extract_with_pdfminer(str(pdf), pages)
        if normalise_unicode:
            text = unicodedata.normalize(unicode_form, text)
        for w, pat in regexes.items():
            row[w] = len(pat.findall(text))
        return _out.make_table(dict_to_lists(row))

    # Fallback to PyPDF2 (page by page) -------------------------------
    page_texts = extract_with_pypdf2(str(pdf), pages)

    if include_pages:
        row["pages"] = len(page_texts) if pages is None else len(pages)

    for i, txt in enumerate(page_texts, 1):
        if progress_interval and i % progress_interval == 0:
            log.info("[%s] page %d/%d", fname, i, len(page_texts))
        if normalise_unicode:
            txt = unicodedata.normalize(unicode_form, txt)
        for w, pat in regexes.items():
            row[w] += len(pat.findall(txt))

    return _out.make_table(dict_to_lists(row))


# ---------------------------------------------------------------------
def search_pdfs(
    pdfs: Sequence[str] | str,
    words: Sequence[str],
    *,
    outfile: str | None = None,
    show: bool = False,
    sort_cols: Sequence[str] | None = None,
    workers: int = 1,
    ppdf: int | None = None,
    tqdm_desc: str = "PDFs",
    **kwargs,
):
    """
    Wrapper over :pyfunc:`search_pdf` for many files (serial or threaded).
    """
    if isinstance(pdfs, str):
        pdfs = glob(pdfs) if "*" in pdfs else [pdfs]
    pdfs = sorted(pdfs)

    if not pdfs:
        raise FileNotFoundError("No PDF files matched the given pattern(s).")

    tables = []

    # Threaded branch --------------------------------------------------
    if workers > 1:
        with cf.ThreadPoolExecutor(max_workers=workers) as ex, tqdm(
            total=len(pdfs), desc=tqdm_desc, unit="pdf", ascii=True
        ) as bar:
            futs = {ex.submit(search_pdf, pdf, words, **kwargs): pdf for pdf in pdfs}
            for fut in cf.as_completed(futs):
                tables.append(fut.result())
                bar.update(1)
    # Serial branch ----------------------------------------------------
    else:
        if ppdf:
            stride = max(1, math.ceil(len(pdfs) / ppdf))
            for i, pdf in enumerate(pdfs, 1):
                if (i - 1) % stride == 0:
                    log.info("%02d/%02d [%s]", i, len(pdfs), Path(pdf).name)
                tables.append(search_pdf(pdf, words, **kwargs))
        else:
            for pdf in tqdm(pdfs, desc=tqdm_desc, unit="pdf", ascii=True):
                tables.append(search_pdf(pdf, words, **kwargs))

    table = _out.stack_tables(tables)

    if sort_cols:
        sort_cols = [c for c in sort_cols if c in table.columns]
        if sort_cols:
            table = _out.sort_table(table, sort_cols)

    if show:
        print(table)

    if outfile:
        _out.write_table(table, outfile)
        log.info("Results saved to %s", outfile)

    return table

