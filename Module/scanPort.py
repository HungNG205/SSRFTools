import httpx
from Utils.runThread import run_threads
from Utils.makeRequest import make_request


def scanPort(request_info, params, network, port, url):
    try:
        method, _, header, body, verify = request_info
        payload = f"http://{network}:{port}"

        with httpx.Client(http2=True, verify=verify, timeout=3) as client:
            response = make_request(client, method, url, header, body, params, payload)

            if response.status_code == 200:
                print(f"Status Code {response.status_code} - Port {port} is open.")
    except httpx.RequestError as exc:
        return


def run(request_info, params, url):
    network_target = input("Network to scan: ").strip()
    with open("PayloadSSRF/Port.txt", "r") as f:
        ports = [int(port.strip()) for port in f.readlines()]

    def worker(port):
        scanPort(request_info, params, network_target, port, url)

    run_threads(ports, worker)
