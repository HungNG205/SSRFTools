import httpx
from Utils.runThread import run_threads
from Utils.makeRequest import make_request


def scanPort(request_info, params, network, port, url):
    try:
        method, _, header, body, verify = request_info
        payload = f"http://{network}:{port}"

        with httpx.Client(http2=True, verify=verify, timeout=3) as client:
            response = make_request(client, method, url, header, body, params, payload)
            
            print("-"*50)
            print(f"[Port {port}] Status: {response.status_code}")
            if response.status_code == 200:
                print(f"Port {port} is open.")
            print("-"*50)
    except httpx.RequestError as exc:
        return


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
    with open("PayloadSSRF/Port.txt", "r") as f:
        ports = [int(port.strip()) for port in f.readlines()]

    def worker(port):
        scanPort(request_info, params, network_target, port, url)

    run_threads(ports, worker)
