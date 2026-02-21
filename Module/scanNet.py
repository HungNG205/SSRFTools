import ipaddress
import httpx
from Utils.runThread import threads


def scanNet(request_info, params, ip, url):
    try:
        method, _, header, body, is_json, verify = request_info

        with httpx.Client(http2=True, verify=verify, timeout=3) as client:
            if method == "POST" or method == "PUT":
                body_data = body.copy()
                if params in body_data:
                    body_data[params] = f"http://{ip}"

                if is_json:
                    response = client.request(method, url, headers=header, json=body_data)
                else:
                    body_str = "&".join([f"{k}={v}" for k, v in body_data.items()])
                    response = client.request(method, url, headers=header, data=body_str)
            elif method == "GET":
                response = client.request(method, url, headers=header, params={params: f"http://{ip}"})

            print(f"[{ip}] Status: {response.status_code}")

            if response.status_code == 200:
                print(f"Network {ip} is open.")
            else:
                body_res = response.text
                if "ECONNREFUSED" in body_res:
                    print(f"Network {ip} is open but connection refused.")
                else:
                    print(f"Network {ip} is closed/filtered.")
    except httpx.RequestError as exc:
        print(f"Network {ip} does not exist by (timeout).")


def run(request_info, params, url):
    target_subnet = input("Target IP/CIDR (e.g., 192.168.0.1/20): ").strip()
    network = ipaddress.ip_network(target_subnet, strict=False)
    networks = list(network.hosts())

    def worker(ip):
        scanNet(request_info, params, ip, url)

    threads(networks, worker)
