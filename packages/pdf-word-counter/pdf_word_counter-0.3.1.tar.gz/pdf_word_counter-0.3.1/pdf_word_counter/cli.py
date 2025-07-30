"""
Command-line interface (argparse) + entry-point ``main()``.
"""
from __future__ import annotations

import argparse
import ast
import logging
import sys
from typing import List, Sequence

from . import version, output
from .search import search_pdfs
from .utils import parse_page_range


# ---------------------------------------------------------------------
def _parse_cli() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="pdf-word-counter",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Search PDFs for words and build a statistics table",
        epilog=f"pdf-word-counter version {version.__version__}",
    )

    p.add_argument("words", help="Words to find (comma-separated)")
    p.add_argument("pdfs", nargs="*", help="PDF files or glob patterns")

    # Search behaviour -------------------------------------------------
    s = p.add_argument_group("Search options")
    s.add_argument("--case", action="store_true", help="Case-sensitive search")
    s.add_argument("--pages", help="Pages to include, e.g. '1,3-5'")
    s.add_argument("--miner", action="store_true", help="Use pdfminer.six backend")
    s.add_argument("--pprint", type=int, metavar="N",
                   help="Progress log every N pages (PyPDF2 only)")
    s.add_argument("--unicode", action="store_true", help="Normalise Unicode text")
    s.add_argument("--form", choices=["NFC", "NFD", "NFKC", "NFKD"],
                   default="NFKC", help="Unicode normalisation form")

    # Output / formatting ----------------------------------------------
    o = p.add_argument_group("Output control")
    o.add_argument("--outfile", help="Write output table to this file")
    o.add_argument("--show", action="store_true", help="Print table to stdout")
    o.add_argument("--sort", help="Sort by these columns (comma-separated)")

    # Filename derived columns -----------------------------------------
    f = p.add_argument_group("Filename parsing")
    f.add_argument("--ext", action="store_true", help="Keep file extension")
    f.add_argument("--year", action="store_true", help="Add 'year' column")
    f.add_argument("--dsep", type=str,
                   help="Separators dict literal, e.g. \"{'_': {'cat': 0}}\"")

    # Column toggles ----------------------------------------------------
    c = p.add_argument_group("Column toggles")
    c.add_argument("--nfile", action="store_true", help="Omit filename column")
    c.add_argument("--npages", action="store_false",
                   dest="include_pages", help="Omit pages column")

    # Performance -------------------------------------------------------
    p.add_argument("--workers", type=int, default=1, help="Thread workers")
    p.add_argument("--backend", choices=["pandas", "astropy"],
                   help="Force output backend")
    p.add_argument("--ppdf", type=int, metavar="N",
                   help="Log progress every N files (serial mode)")
    p.add_argument("--log-level", default="INFO",
                   choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                   help="Logging threshold")

    return p.parse_args()


# ---------------------------------------------------------------------
def main(cli_args: Sequence[str] | None = None) -> None:
    args = _parse_cli() if cli_args is None else _parse_cli(cli_args)

    logging.basicConfig(format="%(levelname)s | %(message)s",
                        level=getattr(logging, args.log_level))

    # Load backend
    output.load_backend(args.backend)

    words: List[str] = [w.strip() for w in args.words.split(",")]
    sort_cols = [c.strip() for c in args.sort.split(",")] if args.sort else None
    pages = parse_page_range(args.pages)

    separators = None
    if args.dsep:
        try:
            separators = ast.literal_eval(args.dsep)
            if not isinstance(separators, dict):
                raise ValueError
        except Exception:
            logging.error("--dsep must be a valid Python dict literal.")
            sys.exit(1)

    # Kick off search --------------------------------------------------
    search_pdfs(
        args.pdfs or ["*.pdf"],
        words,
        outfile=args.outfile,
        show=args.show,
        sort_cols=sort_cols,
        workers=args.workers,
        ppdf=args.ppdf,
        ignore_case=not args.case,
        pages=pages,
        use_pdfminer=args.miner,
        include_pages=args.include_pages,
        include_filename=not args.nfile,
        keep_extension=args.ext,
        separators=separators,
        include_year=args.year,
        normalise_unicode=args.unicode,
        unicode_form=args.form,
        progress_interval=args.pprint,
    )


__all__ = ["main"]

