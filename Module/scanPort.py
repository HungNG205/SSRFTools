import requests
from threading import Thread

def scanPort(request_info, params, port, url):
    try:
        method, _ , header, body, is_json = request_info

        if method == "POST" or method == "PUT":
            body_data = body.copy()
            if params in body_data:
                body_data[params] = f"http://{header['Host'].split(':')[0].strip()}:{port}"

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
                params={params: f"http://{header['Host'].split(':')[0].strip()}:{port}"},
                timeout=3,
            )
        
        print(f"[Port {port}] Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Port {port} is open.")
        else:
            print(f"Port {port} is closed/filtered.")
    except requests.exceptions.RequestException:
        print(f"Port {port} is closed.")

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
    threads = []
    ports = parse_ports(input("Ports (ex: 80 / 80,443 / 1-1024): ").strip())
    for port in ports:
        t = Thread(target=scanPort, args=(request_info, params, port, url))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
