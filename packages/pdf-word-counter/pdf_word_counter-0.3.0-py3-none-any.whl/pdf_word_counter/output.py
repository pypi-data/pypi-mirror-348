"""
Backend-agnostic helpers: choose Astropy or pandas at runtime.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, Sequence

_BACKEND = "astropy"  # default
_funcs: Dict[str, Any] = {}  # populated by `load_backend`


def load_backend(name: str | None = None) -> None:  # noqa: C901  (intentional branching)
    global _BACKEND, _funcs

    if name != "pandas":
        try:
            from astropy.table import Table, vstack

            _BACKEND = "astropy"

            def make_table(data: Dict[str, Iterable]) -> Table:  # type: ignore
                return Table({k: list(v) for k, v in data.items()})

            def stack_tables(tbls):  # type: ignore
                return vstack(tbls, metadata_conflicts="silent")

            def sort_table(tbl, cols):  # type: ignore
                tbl.sort(cols)
                return tbl

            def write_table(tbl, path):  # type: ignore
                tbl.write(path, format="ascii.fixed_width", bookend=False,
                          delimiter=",", overwrite=True)

            _funcs = dict(make_table=make_table,
                          stack_tables=stack_tables,
                          sort_table=sort_table,
                          write_table=write_table)
            return
        except ImportError:
            if name == "astropy":
                print(">>> astropy not installed; using pandas")

    import pandas as pd  # fallback
    _BACKEND = "pandas"

    def make_table(data: Dict[str, Iterable]) -> pd.DataFrame:  # type: ignore
        return pd.DataFrame(data)

    def stack_tables(tbls):  # type: ignore
        return pd.concat(tbls, ignore_index=True)

    def sort_table(tbl, cols):  # type: ignore
        return tbl.sort_values(cols, ignore_index=True)

    def write_table(tbl, path):  # type: ignore
        tbl.to_csv(path, index=False)

    _funcs = dict(make_table=make_table,
                  stack_tables=stack_tables,
                  sort_table=sort_table,
                  write_table=write_table)


# Initialise with default backend when module is imported
load_backend()

# Public re-exports ----------------------------------------------------
make_table = lambda *a, **k: _funcs["make_table"](*a, **k)
stack_tables = lambda *a, **k: _funcs["stack_tables"](*a, **k)
sort_table = lambda *a, **k: _funcs["sort_table"](*a, **k)
write_table = lambda *a, **k: _funcs["write_table"](*a, **k)
__all__ = ["load_backend", "make_table", "stack_tables", "sort_table", "write_table"]

