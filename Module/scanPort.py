import httpx
from Utils.runThread import run_threads
from Utils.makeRequest import make_request

def scanPort(request_info, params, network, port, url):
    try:
        method, _, header, body, verify = request_info
        payload = f"http://{network}:{port}"

        with httpx.Client(http2=True, verify=verify, timeout=10) as client:
            response = make_request(client, method, url, header, body, params, payload)
            if response.status_code == 200:
                return f"[+] Port {port} is open."

    except httpx.RequestError as exc:
        return


def read_port():
    try:
        with open("PayloadSSRF/Port.txt", "r") as f:
            port_list = [int(line.strip()) for line in f.readlines()]
        return port_list
    except FileNotFoundError:
        print("Error: PayloadSSRF/Port.txt not found.")
        return []


def run(request_info, params, url):
    network_target = input("Network to scan (e.g., 127.0.0.1): ").strip()
    ports = read_port()
    if not ports:
        return

    print(f"\nScanning {len(ports)} ports on {network_target}...")

    def worker(port):
        return scanPort(request_info, params, network_target, port, url)

    run_threads(ports, worker)
    print("Port scan completed.")
