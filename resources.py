"""Locate bundled resource files, working both from source and from the
PyInstaller onefile build (which unpacks data under sys._MEIPASS)."""

from __future__ import annotations

import os
import sys


def resource_path(*parts: str) -> str:
    if getattr(sys, "frozen", False):
        base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    else:
        base = os.path.dirname(os.path.abspath(__file__))  # project root
    return os.path.join(base, *parts)
