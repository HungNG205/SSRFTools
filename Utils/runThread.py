from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
console = Console()

def run_threads(items, worker, max_threads=40):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("[cyan]Processing...", total=len(items))

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [executor.submit(worker, item) for item in items]
            for future in as_completed(futures):
                progress.advance(task)
                try:
                    future.result()
                except Exception as e:
                    progress.console.print(f"[bold red]Thread error:[/bold red] {e}")
