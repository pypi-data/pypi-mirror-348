# =============================================================================
#  Project       : GenomeNinja
#  File          : src/genome_ninja/__init__.py
#
#  Author        : Qinzhong Tian <tianqinzhong@qq.com>
#  Created       : 2025-04-28 17:29
#  Last Updated  : 2025-04-29 17:53
#
#  Description   : Entry file for GenomeNinja package
#                 Implements the following features:
#                 1. Define package version number
#                 2. Dynamically import submodules via lazy loading
#                 3. Provide type hint support
#                 4. Define public package interface
#
#  Python        : Python 3.13.3
#  Version       : 0.1.0
#
#  Usage         : import genome_ninja
#                 genome_ninja.test  # Import submodules on demand
#
#  Copyright © 2025 Qinzhong Tian. All rights reserved.
#  License       : MIT – see LICENSE in project root for full text.
# =============================================================================
from __future__ import annotations

from importlib import import_module, metadata
from types import ModuleType
from typing import TYPE_CHECKING, Any

# --------------------------------------------------------------------------- #
# Version number
# --------------------------------------------------------------------------- #
__version__: str = metadata.version("genome-ninja")

# --------------------------------------------------------------------------- #
# Lazy loading of submodules
# --------------------------------------------------------------------------- #
_SUBMODULE_MAP: dict[str, str] = {
    "test": "genome_ninja._gninja_test",
    # "io":    "genome_ninja._gninja_io",
    # "core":  "genome_ninja._gninja_core",
}


def __getattr__(name: str) -> ModuleType:  # noqa: D401
    """
    When user accesses ``genome_ninja.<name>``, dynamically import corresponding C++ extension and return it.
    Attributes not in _SUBMODULE_MAP are handled with regular AttributeError.
    """
    if name in _SUBMODULE_MAP:
        mod = import_module(_SUBMODULE_MAP[name])
        globals()[name] = mod  # Cache in module namespace to avoid reimporting
        return mod
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


# --------------------------------------------------------------------------- #
# Make submodule symbols visible to IDE / Mypy
# --------------------------------------------------------------------------- #
if TYPE_CHECKING:  # pragma: no cover
    from genome_ninja import _gninja_test as test  # type: ignore

    # from genome_ninja import _gninja_io   as io      # type: ignore
    # from genome_ninja import _gninja_core as core    # type: ignore

# --------------------------------------------------------------------------- #
# Explicit exports
# --------------------------------------------------------------------------- #
__all__: list[str] = ["__version__", *(_SUBMODULE_MAP.keys())]
