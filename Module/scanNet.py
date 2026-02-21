import ipaddress
import requests
from Utils.runThread import threads


def scanNet(request_info, params, ip, url):
    try:
        method, _, header, body, is_json, verify = request_info
        if method == "POST" or method == "PUT":
            body_data = body.copy()
            if params in body_data:
                body_data[params] = f"http://{ip}"

            if is_json:
                response = requests.request(method, url, headers=header, json=body_data, timeout=3, verify=verify)
            else:
                body_str = "&".join([f"{k}={v}" for k, v in body_data.items()])
                response = requests.request(method, url, headers=header, data=body_str, timeout=3, verify=verify)
        elif method == "GET":
            response = requests.request(method, url, headers=header, params={params: f"http://{ip}"}, timeout=3, verify=verify)

        print(f"[{ip}] Status: {response.status_code}")

        if response.status_code == 200:
            print(f"Network {ip} is open.")
        else:
            body_res = response.text
            if "ECONNREFUSED" in body_res:
                print(f"Network {ip} is open but connection refused.")
            else:
                print(body_res[:100])
                print(f"Network {ip} is closed/filtered.")
    except requests.exceptions.RequestException as exc:
        print(f"Network {ip} error: {exc}")


def run(request_info, params, url):
    target_subnet = input("Target IP/CIDR (e.g., 192.168.0.1/20): ").strip()
    network = ipaddress.ip_network(target_subnet, strict=False)
    networks = list(network.hosts())

    def worker(ip):
        scanNet(request_info, params, ip, url)

    threads(networks, worker)
