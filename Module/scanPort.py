import httpx
from Utils.runThread import run_threads
from Utils.makeRequest import make_request
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def scanPort(request_info, params, network, port, url):
    try:
        method, _, header, body, verify = request_info
        payload = f"http://{network}:{port}"

        with httpx.Client(http2=True, verify=verify, timeout=3) as client:
            response = make_request(client, method, url, header, body, payload, params)
            if response.status_code == 200:
                console.print(f"[bold green][+][/bold green] Port [cyan]{port}[/cyan] is open.")
            else:
                pass
    except httpx.RequestError as exc:
        pass


def read_port():
    try:
        with open("PayloadSSRF/PortList.txt", "r") as f:
            port_list = [int(line.strip()) for line in f.readlines()]
        return port_list
    except FileNotFoundError:
        console.print("[bold red]Error:[/bold red] PayloadSSRF/PortList.txt not found.")
        return []


def run(request_info, params, url):
    network_target = Prompt.ask("[bold blue]Network to scan[/bold blue] (e.g., 127.0.0.1)").strip()
    ports = read_port()
    if not ports:
        return

    console.print(f"[bold yellow]Scanning {len(ports)} ports on {network_target}...[/bold yellow]")

    def worker(port):
        scanPort(request_info, params, network_target, port, url)

    run_threads(ports, worker)
    console.print("[bold green]Port scan completed.[/bold green]")
