"""
pyvfp64.connection
------------------
A *minimal* DB-API-style wrapper around pyvfp64.to_dataframe.

Only SELECT queries are supported – good enough for all the read-only
reporting code that used to rely on pyodbc/adodbapi.

Public API
~~~~~~~~~~
- connect(connection_string)   -> VFPConnection
- opera_connection(conn_str)   # context-manager helper
"""

from __future__ import annotations

import contextlib
from typing import List, Tuple

import pandas as pd
from .pyvfp import to_dataframe


# ────────────────────────────────────────────────────────────────────
# Cursor
# ────────────────────────────────────────────────────────────────────
class VFPCursor:
    """Implements just the pieces the legacy code touches."""

    def __init__(self, conn_str: str):
        self._conn_str = conn_str
        self._df: pd.DataFrame | None = None
        self.description: List[Tuple[str, None]] | None = None

    # --- DB-API methods --------------------------------------------
    def execute(self, sql: str, params: tuple | None = None):
        if params:  # parameterised queries not required in legacy code
            raise NotImplementedError("Parameterised queries are not supported.")

        self._df = to_dataframe(self._conn_str, sql)
        self.description = [(col, None) for col in self._df.columns]

    def fetchall(self):
        if self._df is None:
            raise RuntimeError("execute() must be called before fetchall().")
        return [tuple(row) for row in self._df.itertuples(index=False, name=None)]

    def fetchone(self):
        if self._df is None:
            raise RuntimeError("execute() must be called before fetchone().")
        if self._df.empty:
            return None
        return tuple(self._df.iloc[0].tolist())

    @property
    def rowcount(self):
        return -1 if self._df is None else len(self._df)

    # --- housekeeping ---------------------------------------------
    def close(self):
        self._df = None
        self.description = None


# ────────────────────────────────────────────────────────────────────
# Connection
# ────────────────────────────────────────────────────────────────────
class VFPConnection:
    """Hands out VFPCursors and supports the ‘with’ statement."""

    def __init__(self, conn_str: str):
        self._conn_str = conn_str
        self.closed = False

    # --- DB-API methods --------------------------------------------
    def cursor(self) -> VFPCursor:
        if self.closed:
            raise RuntimeError("Connection already closed.")
        return VFPCursor(self._conn_str)

    def close(self):
        self.closed = True

    # --- context-manager sugar -------------------------------------
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# ────────────────────────────────────────────────────────────────────
# Convenience helpers
# ────────────────────────────────────────────────────────────────────
def connect(connection_string: str) -> VFPConnection:
    """Factory function mirroring other DB drivers (pyodbc.connect, etc.)."""
    return VFPConnection(connection_string)


@contextlib.contextmanager
def opera_connection(connection_string: str, *, use_odbc: bool = False):
    """
    Legacy-compat context manager.

    `use_odbc` is ignored – it’s here purely so old signatures still work.
    """
    conn = VFPConnection(connection_string)
    try:
        yield conn
    finally:
        conn.close()