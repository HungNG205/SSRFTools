import httpx
from Utils.runThread import threads
from Utils.makeRequest import make_request


def scanPort(request_info, params, network, port, url):
    try:
        method, _, header, body, is_json, verify = request_info
        payload = f"http://{network}:{port}"

        with httpx.Client(http2=True, verify=verify, timeout=3) as client:
            response = make_request(client, method, url, header, body, params, payload, is_json)
            
            print("-"*50)
            print(f"[Port {port}] Status: {response.status_code}")
            if response.status_code == 200:
                print(f"Port {port} is open.")
            else:
                print(response.text)
                print(f"Port {port} is closed/filtered.")
            print("-"*50)
    except httpx.RequestError as exc:
        print(f"Port {port} is closed by (timeout).")


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
        scanPort(request_info, params, network_target, port, url)

    threads(ports, worker)
