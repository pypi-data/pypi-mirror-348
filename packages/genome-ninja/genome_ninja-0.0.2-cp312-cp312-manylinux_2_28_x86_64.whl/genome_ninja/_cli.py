# =============================================================================
#  Project       : GenomeNinja
#  File          : src/genome_ninja/_cli.py
#
#  Author        : Qinzhong Tian <tianqinzhong@qq.com>
#  Created       : 2025-04-28 17:30
#  Last Updated  : 2025-05-16 15:52
#
#  Description   : Command-line interface module that provides the main CLI
#                  functionality for GenomeNinja, including version info display,
#                  dynamic loading of built-in tools and plugins, and other
#                  core features.
#
#  Python        : Python 3.13.3
#  Version       : 0.1.3
#
#  Usage         : Can be used in the following ways:
#                  1. genome-ninja --help      # Show help information
#                  2. genome-ninja version     # Show version information
#                  3. genome-ninja <tool>      # Run specified tool
#                  4. genome-ninja -i          # Enter interactive mode
#
#  Copyright © 2025 Qinzhong Tian. All rights reserved.
#  License       : MIT – see LICENSE in project root for full text.
# =============================================================================
from __future__ import annotations

import datetime
import importlib
import importlib.metadata as md
import importlib.resources as res
import json
import pkgutil
import platform
import random
import sys
from importlib.metadata import entry_points, metadata
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

import typer

from genome_ninja import __version__

# ASCII Art Logo
ASCII_LOGO = r"""
   _____                                 _   _ _       _
  / ____|                               | \ | (_)     (_)
 | |  __  ___ _ __   ___  _ __ ___   ___|  \| |_ _ __  _  __ _
 | | |_ |/ _ \ '_ \ / _ \| '_ ` _ \ / _ \ . ` | | '_ \| |/ _` |
 | |__| |  __/ | | | (_) | | | | | |  __/ |\  | | | | | | (_| |
  \_____|\___|_| |_|\___/|_| |_| |_|\___|_| \_|_|_| |_| |\__,_|
                                                     _/ |
                                                    |__/
"""

# -----------------------------------------------------------------------------
# Typer app
# -----------------------------------------------------------------------------

app = typer.Typer(
    name="genome-ninja",
    help="GenomeNinja – a collection of tiny yet fast genome utilities.",
    invoke_without_command=True,
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)

# -----------------------------------------------------------------------------
# Helper utilities
# -----------------------------------------------------------------------------


def _format_time(iso_str: str) -> str:
    """Format ISO 8601 timestamp to human‑readable string."""
    try:
        dt = datetime.datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        return iso_str


def _sizeof_fmt(num: float) -> str:
    """Human‑readable bytes (binary prefixes)."""
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if num < 1024:
            return f"{num:.1f} {unit}"
        num /= 1024
    return f"{num:.1f} PiB"


def _get_pypi_info(pkg: str, ver: str) -> dict[str, str]:
    """Return PyPI info dict with release_date, latest_version, requires_python, total_size."""
    result = {
        "release_date": "Unknown",
        "latest_version": ver,
        "requires_python": "?",
        "total_size": "?",
    }
    url = f"https://pypi.org/pypi/{pkg}/json"
    try:
        with urlopen(
            Request(url, headers={"Accept": "application/json"}), timeout=3
        ) as resp:
            data = json.load(resp)
        # release date: latest upload in this version
        uploads = data["releases"].get(ver, [])
        if uploads:
            latest_upload = max(f["upload_time_iso_8601"] for f in uploads)
            result["release_date"] = _format_time(latest_upload)
            total_bytes = sum(f["size"] for f in uploads)
            result["total_size"] = _sizeof_fmt(total_bytes)
        # latest version info
        result["latest_version"] = data["info"].get("version", ver)
        result["requires_python"] = data["info"].get("requires_python", "?")
    except URLError:
        # offline or blocked – graceful degradation
        meta = metadata(pkg)
        if "Release-Date" in meta:
            result["release_date"] = meta["Release-Date"]
        dist = md.distribution(pkg)
        ts = Path(dist.locate_file("")).stat().st_mtime
        result["release_date"] = _format_time(
            datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).isoformat()
        )
    return result


# -----------------------------------------------------------------------------
# Root callback
# -----------------------------------------------------------------------------


@app.callback(invoke_without_command=True)
def _root(
    ctx: typer.Context,
    interactive: bool = typer.Option(
        False, "-i", "--interactive", help="Force interactive prompts"
    ),
):
    ctx.ensure_object(dict)
    ctx.obj["interactive"] = interactive
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.command.get_help(ctx))
        raise typer.Exit()


# -----------------------------------------------------------------------------
# Version command
# -----------------------------------------------------------------------------


@app.command("version", help="Show detailed GenomeNinja version info.")
def _version() -> None:
    try:
        from rich.align import Align
        from rich.console import Console
        from rich.panel import Panel
        from rich.table import Table

        console = Console()
        ver = __version__
        pypi = _get_pypi_info("genome-ninja", ver)

        meta = metadata("genome-ninja")
        install_cmd = "pip install genome-ninja"
        env_path = sys.prefix
        tools_pkg = importlib.import_module("genome_ninja.tools")
        tool_count = len(list(pkgutil.iter_modules(tools_pkg.__path__)))
        plugin_count = len(entry_points().select(group="genome_ninja.plugins"))

        author = (
            meta["Author"]
            if "Author" in meta
            else "Qinzhong Tian <tianqinzhong@qq.com>"
        )
        homepage = (
            meta["Home-page"]
            if "Home-page" in meta
            else "https://github.com/LoadStar822/GenomeNinja"
        )
        issues = homepage.rstrip("/") + "/issues"

        try:
            with (
                res.files("genome_ninja.data")
                .joinpath("quotes.txt")
                .open(encoding="utf-8")
            ) as f:
                quotes = [line.strip() for line in f if line.strip()]
                quote = random.choice(quotes)
        except Exception:
            quote = "Yeeeeart!"

        update_hint = (
            "(latest)"
            if pypi["latest_version"] == ver
            else f"→ {pypi['latest_version']}  (pip install -U genome-ninja)"
        )
        whats_new = f"What's new in v{ver}? Check the changelog on {homepage}/releases"

        table = Table(show_header=False, pad_edge=False, box=None)
        for key, val in [
            ("Version", f"{ver} {update_hint}"),
            ("Released", pypi["release_date"]),
            ("Requires Py", pypi["requires_python"]),
            ("Files", pypi["total_size"]),
            ("Python", platform.python_version()),
            ("Platform", f"{platform.system()} {platform.release()}"),
            ("Install", install_cmd),
            ("Env Path", env_path),
            ("Tools", f"{tool_count}"),
            ("Plugins", f"{plugin_count}"),
            ("Author", author),
            ("Homepage", homepage),
            ("Issues", issues),
            ("What's New", whats_new),
            ("Quote", quote),
        ]:
            table.add_row(f"[bold cyan]{key}[/]", str(val))

        console.print(Align.center(Panel(ASCII_LOGO, style="bold green")))
        console.print(
            Panel(table, title="[bold magenta]GenomeNinja Info[/]"), justify="center"
        )

    except ImportError:
        print(f"GenomeNinja {__version__}")
        return


# -----------------------------------------------------------------------------
# Dynamic discovery
# -----------------------------------------------------------------------------


def _discover_internal() -> None:
    mod_base = "genome_ninja.tools"
    try:
        for mod in pkgutil.iter_modules(importlib.import_module(mod_base).__path__):
            try:
                m = importlib.import_module(f"{mod_base}.{mod.name}")
                if hasattr(m, "register"):
                    m.register(app)
            except Exception as e:
                print(f"Warning: Failed to load built‑in tool {mod.name}: {e}")
    except Exception as e:
        print(f"Warning: Unable to load built‑in tools module: {e}")


def _discover_plugins() -> None:
    try:
        for ep in md.entry_points(group="genome_ninja.plugins"):
            try:
                mod = importlib.import_module(ep.module)
                getattr(mod, ep.attr)(app)
            except Exception as e:
                print(f"Warning: Failed to load plugin {ep.name}: {e}")
    except Exception as e:
        print(f"Warning: Unable to load plugins: {e}")


_discover_internal()
_discover_plugins()

# -----------------------------------------------------------------------------
# Main entry
# -----------------------------------------------------------------------------


def main() -> None:  # console script target
    app()


if __name__ == "__main__":
    main()
