# =============================================================================
#  Project       : GenomeNinja
#  File          : src/genome_ninja/tools/seq_gc.py
#
#  Author        : Qinzhong Tian <tianqinzhong@qq.com>
#  Created       : 2025-04-29 16:38
#  Last Updated  : 2025-05-06 15:59
#
#  Description   : GC Content Calculator
#                 Supports FASTA/FASTQ input
#                 Multiple running modes and output formats
#                 Optional additional statistics
#
#  Python        : Python 3.13.3
#  Version       : 0.1.16
#
#  Usage         : genome-ninja seq-gc <fasta/fastq file>
#                 Optional arguments:
#                   --format/-f: Output format (table/csv/json)
#                   --modes: Running mode (quick/accurate/auto)
#                   --extra/-e: Run additional statistics
#
#  Copyright © 2025 Qinzhong Tian. All rights reserved.
#  License       : MIT – see LICENSE in project root for full text.
# =============================================================================
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.panel import Panel

from genome_ninja import test as gn_test  # demo pybind11 GC util
from genome_ninja.core.interactive import interactive_cmd
from genome_ninja.core.interactive import ps as P

console = Console()

# -----------------------------------------------------------------------------
# Typer registration
# -----------------------------------------------------------------------------


def register(cli: typer.Typer) -> None:
    """Register the seq‑gc demo command to the Typer CLI."""

    @cli.command(
        "seq-gc",
        help="Calculate GC content and echo test parameters",
        rich_help_panel="misc",
    )
    @interactive_cmd(
        P(
            "path",
            "FASTA/FASTQ file path",
            validate=lambda v: Path(v).exists()  # type: ignore
            or "File does not exist, please try again",
            rule="Please enter a valid file path",
            required=True,
        ),
        P(
            "format",
            "Output format",
            choices=["table", "csv", "json"],
            rule="Single selection (table/csv/json)",
            required=False,
            input_type="select",
        ),
        P(
            "modes",
            "Select running modes (multiple choice)",
            choices=["quick", "accurate", "auto"],
            input_type="multiselect",
            required=False,
        ),
        P(
            "run_extra",
            "Run additional statistics",
            required=False,
            input_type="confirm",
        ),
    )
    def seq_gc(
        ctx: typer.Context,
        path: Optional[str] = typer.Argument(None, help="FASTA/FASTQ file path"),
        format: Optional[str] = typer.Option(None, "--format", "-f"),
        modes: Optional[List[str]] = typer.Option(None, "--modes"),
        run_extra: bool = typer.Option(False, "--extra", "-e"),
    ) -> None:
        """
        GC Content Analysis Interactive Mode:

        • Input a single FASTA/FASTQ file path
        • Select output format (optional)
        • Multiple running modes selection
        • Optional additional statistics

        The tool will calculate GC% and echo your choices for UI testing.
        """

        # ------------------------------------------------------------------
        # Validate + compute GC
        # ------------------------------------------------------------------
        fp = Path(path)  # type: ignore
        if not fp.exists():
            console.print(Panel(f"[red]File not found: {fp}[/]", border_style="red"))
            raise typer.Exit(1)

        try:
            gc_pct = gn_test.gc_percent(str(fp))  # type: ignore
        except Exception as exc:  # noqa: BLE001
            console.print(
                Panel(f"[red]Calculation failed: {exc}[/]", border_style="red")
            )
            raise typer.Exit(1)

        console.print(
            Panel(
                f"[bold cyan]{fp.name}[/] GC content: [green]{gc_pct:.2f}%[/]",
                title="GC Result",
                border_style="green",
            )
        )

        # Echo testing parameters -------------------------------------------
        console.print(
            Panel(
                f"[yellow]Test parameters echo:[/]\n"
                f"Output format = [bold]{format or 'None'}[/]\n"
                f"Running modes = [bold]{', '.join(modes) if modes else 'None'}[/]\n"
                f"Additional stats = [bold]{'Yes' if run_extra else 'No'}[/]",
                title="Parameter Echo",
                border_style="blue",
            )
        )


# -----------------------------------------------------------------------------
# Stand‑alone execution
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    app = typer.Typer()
    register(app)
    app()
