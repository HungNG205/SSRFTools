from Module.exploitMetaData import explotMetadata
from Module.scanNet import scanNet
from Module.scanPort import scanPort
from request_parse import parse_request

import argparse
import os
import sys
import threading
import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, MofNCompleteColumn
from rich.rule import Rule
from rich import box

console = Console()

# ── Banner ───────────────────────────────────────────────────────────────────
BANNER = r"""
[bold cyan]  ██████  ██████  ██████  ███████   ████████  ██████   ██████  ██      
 ██      ██      ██   ██ ██           ██    ██    ██ ██    ██ ██      
  █████   █████  ██████  █████        ██    ██    ██ ██    ██ ██      
      ██      ██ ██   ██ ██           ██    ██    ██ ██    ██ ██      
 ██████  ██████  ██   ██ ██           ██     ██████   ██████  ███████[/bold cyan]
"""


def print_banner():
    console.print(BANNER)
    console.print(Panel(
        "[bold white]v1.0.0[/bold white]  •  [dim]Server-Side Request Forgery Exploitation Toolkit[/dim]",
        border_style="cyan", padding=(0, 2),
    ))
    console.print()


def show_request_info(method, api_path, headers, body):
    """Hiển thị thông tin HTTP request đã parse dưới dạng bảng Rich."""
    table = Table(
        title="[bold yellow]📋 Parsed HTTP Request[/bold yellow]",
        box=box.ROUNDED, border_style="yellow", show_lines=True, title_justify="left",
    )
    table.add_column("Field", style="bold cyan", width=22)
    table.add_column("Value", style="white", overflow="fold")

    table.add_row("Method", f"[bold green]{method}[/bold green]")
    table.add_row("API Path", f"[bold]{api_path}[/bold]")

    for key, value in headers.items():
        display = value
        if key.lower() == "cookie" and len(value) > 60:
            display = value[:60] + "…"
        elif key.lower() == "auth-token" and len(value) > 40:
            display = value[:40] + "… [dim](truncated)[/dim]"
        table.add_row(f"[dim]{key}[/dim]", display)

    body_keys = ", ".join(body.keys()) if body else "(empty)"
    table.add_row("Body", f"[magenta]{body_keys}[/magenta]")

    console.print(table)


# ═════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="SSRF Exploitation Toolkit",
        usage="python main.py -r request.txt [-ip IP] [-port PORT] [-metadata FILE] [--full]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py -r request_exam.txt
  python main.py -r request_exam.txt -ip 10.132.0.3 -port 1-1024
  python main.py -r request_exam.txt -ip 10.132.0.0/28
  python main.py -r request_exam.txt -metadata Dict/API_metadata.txt
  python main.py -r request_exam.txt --full -ip 10.132.0.0/28 -port 1-1024
        """,
    )

    parser.add_argument("-r", metavar="REQFILE", dest="rqfile", help="Path to HTTP request file (required)", required=True)
    parser.add_argument("-ip", metavar="IP", dest="ip", help="Target IP or CIDR network (e.g. 10.132.0.3 or 10.132.0.0/28)", required=False)
    parser.add_argument("-port", metavar="PORT", dest="port", help="Port or port range (e.g. 80, 1-1024, 80,443,8080)", required=False)
    parser.add_argument("-metadata", metavar="FILE", dest="metadata", help="Custom metadata endpoints file (default: Dict/API_metadata.txt)", required=False)
    parser.add_argument("--full", action="store_true", help="Scan all ports and networks", required=False)
    args = parser.parse_args()

    # ── Banner ───────────────────────────────────────────────────────────────
    print_banner()

    # ── Parse request ────────────────────────────────────────────────────────
    rqfile = getattr(args, "rqfile")
    if not os.path.isfile(rqfile):
        console.print(f"[bold red]✗ Error:[/bold red] File không tồn tại: [bold]{rqfile}[/bold]")
        sys.exit(1)

    with console.status("[bold cyan]Đang parse request file…[/bold cyan]", spinner="dots"):
        request_info = parse_request(rqfile)

    method, api_path, headers, body = request_info
    origin = headers.get("Origin")

    show_request_info(method, api_path, headers, body)
    console.print(f"\n  [dim]🔗 Base URL:[/dim] [bold cyan]{origin}[/bold cyan]\n")

    # ── Xử lý từng module theo argument ──────────────────────────────────────

    # --- Network Scan (ip) ---
    if args.ip:
        ip = args.ip
        console.print(Rule("[bold blue]🌐 NETWORK SCAN[/bold blue]", style="blue"))
        console.print(f"  [dim]Target:[/dim] [bold]{ip}[/bold]\n")
        scanNet(request_info, ip, origin)
        console.print()

    # --- Port Scan ---
    if args.port:
        port = args.port
        console.print(Rule("[bold red]🔍 PORT SCAN[/bold red]", style="red"))
        console.print(f"  [dim]Target IP:[/dim] [bold]{args.ip or 'N/A'}[/bold]  [dim]Port:[/dim] [bold]{port}[/bold]\n")
        # scanPort cần: request_info, network, port, url
        if args.ip:
            result = scanPort(request_info, args.ip, port, origin)
            if result:
                console.print(f"  [bold green]✔ Port {port} is OPEN[/bold green]")
            else:
                console.print(f"  [bold red]✗ Port {port} is CLOSED/FILTERED[/bold red]")
        else:
            console.print("[bold yellow]⚠ Cần chỉ định -ip để scan port[/bold yellow]")
        console.print()

    # --- Metadata Extraction ---
    if args.metadata:
        metadata_file = args.metadata
        console.print(Rule("[bold magenta]☁️  METADATA EXTRACTION[/bold magenta]", style="magenta"))

        if not os.path.isfile(metadata_file):
            console.print(f"[bold red]✗ Metadata file not found:[/bold red] {metadata_file}")
        else:
            with open(metadata_file, "r", encoding="utf-8") as f:
                raw = f.read()
            endpoints = [line.strip() for line in raw.split("\n") if line.strip()]

            console.print(f"  [dim]Endpoints:[/dim] [bold]{len(endpoints)}[/bold]  [dim]File:[/dim] [bold]{os.path.basename(metadata_file)}[/bold]\n")

            # Bảng danh sách endpoint
            ep_table = Table(box=box.SIMPLE_HEAVY, border_style="magenta", show_lines=False)
            ep_table.add_column("#", style="dim", justify="center", width=5)
            ep_table.add_column("Endpoint", style="cyan")
            for idx, ep in enumerate(endpoints, 1):
                ep_table.add_row(str(idx), ep)
            console.print(ep_table)
            console.print()

            # Chạy exploit với progress bar
            with Progress(
                SpinnerColumn("dots12", style="magenta"),
                TextColumn("[bold magenta]{task.description}[/bold magenta]"),
                BarColumn(bar_width=40, style="magenta", complete_style="green"),
                MofNCompleteColumn(),
                TimeElapsedColumn(),
                console=console,
            ) as progress:
                task = progress.add_task("Exploiting metadata…", total=len(endpoints))
                for ep in endpoints:
                    progress.update(task, description=f"Trying [cyan]{ep[:50]}[/cyan]")
                    try:
                        explotMetadata(request_info, ep, origin)
                    except Exception as exc:
                        console.print(f"  [red]✗ {ep}[/red] — [dim]{exc}[/dim]")
                    progress.advance(task)

            console.print(Panel(
                "[bold green]✅ Metadata extraction hoàn tất.[/bold green]",
                border_style="green", padding=(0, 2),
            ))

    # --- Full Scan ---
    if args.full:
        console.print(Panel(
            "[bold yellow]🚀 FULL SCAN MODE[/bold yellow]\n"
            "[dim]Chạy tất cả module: Network → Port → Metadata[/dim]",
            border_style="yellow", padding=(1, 2),
        ))
        console.print("[dim]Full scan mode đang được phát triển…[/dim]")

    # ── Kết thúc ─────────────────────────────────────────────────────────────
    console.print()
    console.print(Panel(
        "[bold green]✅ Hoàn tất tất cả tác vụ.[/bold green]",
        border_style="green", padding=(0, 2),
    ))