import requests
from Utils.runThread import threads


def scanport(request_info, params, network, port, url):
    try:
        method, _, header, body, is_json, verify = request_info

        if method == "POST" or method == "PUT":
            body_data = body.copy()
            if params in body_data:
                body_data[params] = f"http://{network}:{port}"

            if is_json:
                response = requests.request(method, url, headers=header, json=body_data, timeout=3, verify=verify)
            else:
                body_str = "&".join([f"{k}={v}" for k, v in body_data.items()])
                response = requests.request(method, url, headers=header, data=body_str, timeout=3, verify=verify)
        elif method == "GET":
            response = requests.request(method, url, headers=header, params={params: f"http://{network}:{port}"}, timeout=3, verify=verify)
        print(f"[Port {port}] Status: {response.status_code}")

        if response.status_code == 200:
            print(f"Port {port} is open.")
        else:
            print(response.text)
            print(f"Port {port} is closed/filtered.")
    except requests.exceptions.RequestException as exc:
        print(f"Port {port} is closed. Error: {exc}")


def parse_ports(value):
    if not value.strip():
        return [1]

    if "-" in value:
        start, end = value.split("-")
        return list(range(int(start), int(end) + 1))

    if "," in value:
        return [int(p.strip()) for p in value.split(",")]

    return [int(value)]


def run(request_info, params, url):
    network_target = input("Network to scan: ").strip()
    ports = parse_ports(input("Ports (ex: 80 / 80,443 / 1-1024): ").strip())

    def worker(port):
        scanport(request_info, params, network_target, port, url)

    threads(ports, worker)
