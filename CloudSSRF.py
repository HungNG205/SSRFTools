
import argparse
from Utils.parseRequest import parse_request
import importlib
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def print_banner():
    banner_text = r"""
        __   _
    __(  )_( )_
   (_   _    _)_
  / /(_) (__)   
 ____  ____  ____  _____ 
/ ___|/ ___||  _ \|  ___|
\___ \\___ \| |_) | |_   
 ___) |___) |  _ <|  _|  
|____/|____/|_| \_\_|    
"""
    usage_text = """
[bold green]Usage Options:[/bold green]
  [cyan]-f, --file[/cyan]     Request file path (required)
  [cyan]-p, --params[/cyan]   Parameter to test SSRF (required)
  [cyan]-s, --scheme[/cyan]   Protocol scheme: http or https (required)
  [cyan]-m, --module[/cyan]   Module to run: scanNet, scanPort, exploitCloud (required)

[bold magenta]Example:[/bold magenta]
  python CloudSSRF.py -f request_exam.txt -p url -s http -m scanNet
"""
    title = Text("Cloud SSRF v1.0", style="bold yellow")
    panel = Panel(
        Text.from_markup(f"[bold cyan]{banner_text}[/bold cyan]\n{usage_text}"), 
        title=title, 
        border_style="blue", 
        expand=False
    )
    console.print(panel)


def main():
    print_banner()
    try:
        parser = argparse.ArgumentParser(
            description="Cloud SSRF",
            epilog="Example usage: python CloudSSRF.py -f request_exam.txt -p url -s http -m scanNet",
        )
        parser.add_argument("-f", "--file", required=True, help="Request file path")
        parser.add_argument("-p", "--params", required=True, help="Parameter to test SSRF")
        parser.add_argument("-s", "--scheme", required=True, help="Protocol scheme (http or https)")     
        parser.add_argument("-m", "--module", required=True, choices=["scanNet", "scanPort", "exploitCloud"], help="option of scan/exploit")
       
        args = parser.parse_args()
        file_path = args.file
        scheme = args.scheme.lower()
        verify = True
        method, api_path, headers, body = parse_request(file_path)
        if scheme == "https":
            verify = False

        host = headers.get("Host")
        if not host:
            console.print("[bold red]Error:[/bold red] Missing required Host header in request file.")
            return

        url = f"{scheme}://{host.strip()}{api_path.split('?')[0]}"
        module_name = f"Module.{args.module}"
        module = importlib.import_module(module_name)
        module.run((method, api_path, headers, body, verify), args.params, url)
    except SystemExit as e:
        if e.code in (0, None):
            return
        console.print("[bold red]Error:[/bold red] Invalid command-line arguments. Use -h for help.")
    except FileNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] Request file not found: {e}")
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] Invalid request file format: {e}")
    except ImportError as e:
        console.print(f"[bold red]Error:[/bold red] Failed to load module: {e}")
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Operation cancelled by user.[/bold yellow]")
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/bold red] {e}")


if __name__ == "__main__":
    main()
