import ipaddress
import httpx
from Utils.runThread import run_threads
from Utils.makeRequest import make_request


def scanNet(request_info, params, ip, url):
    try:
        method, _, header, body, is_json, verify = request_info
        payload = f"http://{ip}"

        with httpx.Client(http2=True, verify=verify, timeout=3) as client:
            response = make_request(client, method, url, header, body, params, payload, is_json)

            print("-"*50)
            print(f"[{ip}] Status: {response.status_code}")
            if response.status_code == 200:
                print(f"Network {ip} is open.")
            else:
                body_res = response.text
                if "ECONNREFUSED" in body_res:
                    print(f"Network {ip} is open but connection refused.")
                else:
                    print(f"Network {ip} is closed/filtered.")
            print("-"*50)
    except httpx.RequestError as exc:
        print(f"Network {ip} does not exist by (timeout).")


def run(request_info, params, url):
    target_subnet = input("Target IP/CIDR (e.g., 192.168.0.1/20): ").strip()
    network = ipaddress.ip_network(target_subnet, strict=False)
    networks = list(network.hosts())

    def worker(ip):
        scanNet(request_info, params, ip, url)

    run_threads(networks, worker)
