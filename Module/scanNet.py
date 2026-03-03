import ipaddress
import httpx
from Utils.runThread import run_threads
from Utils.makeRequest import make_request

def scanNet(request_info, params, ip, url):
    try:
        method, _, header, body= request_info
        payload = f"http://{ip}"

        with httpx.Client(http2=True, verify=False, timeout=10) as client:
            response = make_request(client, method, url, header, body, params, payload)

            if response.status_code == 200:
                return f"[+] Network {ip} is open."
            else:
                body_res = response.text
                if "ECONNREFUSED" in body_res:
                    return f"[+] Network {ip} is open."

    except httpx.RequestError as exc:
        return


def run(request_info, params, url):
    target_subnet = input("Target IP/CIDR (e.g., 192.168.0.1/20): ").strip()
    try:
        network = ipaddress.ip_network(target_subnet, strict=False)
        networks = list(network.hosts())[:40]
    except ValueError as e:
        print(f"Invalid IP/CIDR: {e}")
        return

    print(f"\nScanning {len(networks)} hosts in {network}...")

    def worker(ip):
        return scanNet(request_info, params, ip, url)

    run_threads(networks, worker)
    print("Network scan completed.")
