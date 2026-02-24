import ipaddress
import httpx
from Utils.runThread import run_threads
from Utils.makeRequest import make_request
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def scanNet(request_info, params, ip, url):
    try:
        method, _, header, body, verify = request_info
        payload = f"http://{ip}"

        with httpx.Client(http2=True, verify=verify, timeout=30) as client:
            response = make_request(client, method, url, header, body, params, payload)

            if response.status_code == 200:
                console.print(f"[bold green][+][/bold green] Network [cyan]{ip}[/cyan] is open. [dim](Status: {response.status_code})[/dim]")
            else:
                body_res = response.text
                if "ECONNREFUSED" in body_res:
                    console.print(f"[bold green][+][/bold green] Network [cyan]{ip}[/cyan] is open. [dim](Status: {response.status_code})[/dim]")
                else:
                    pass
    except httpx.RequestError as exc:
        pass


def run(request_info, params, url):
    target_subnet = Prompt.ask("[bold blue]Target IP/CIDR[/bold blue] (e.g., 192.168.0.1/20)").strip()
    try:
        network = ipaddress.ip_network(target_subnet, strict=False)
        networks = list(network.hosts())[:40]
    except ValueError as e:
        console.print(f"[bold red]Invalid IP/CIDR:[/bold red] {e}")
        return

    console.print(f"[bold yellow]Scanning {len(networks)} hosts in {network}...[/bold yellow]")

    def worker(ip):
        scanNet(request_info, params, ip, url)

    run_threads(networks, worker)
    console.print("[bold green]Network scan completed.[/bold green]")
