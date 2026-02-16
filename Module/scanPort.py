import requests

<<<<<<< HEAD
=======
from Module.runThread import threads
>>>>>>> 3c7d22bfb8026b3b49a150a14419db5d0046f2de

def scanPort(request_info,  network, port, url):
    try:
<<<<<<< HEAD
        method, path , header, body = request_info
        body_data = body.copy()
        if 'profilePicture' in body_data:
            body_data['profilePicture'] = f"http://{network}:{port}"
=======
        method, _ , header, body, is_json = request_info

        if method == "POST" or method == "PUT":
            body_data = body.copy()
            if params in body_data:
                body_data[params] = f"http://{network}:{port}"

            if is_json:
                response = requests.request(method, url, headers=header, json=body_data, timeout=3)
            else:
                body_str = "&".join([f"{k}={v}" for k, v in body_data.items()])
                response = requests.request(method, url, headers=header, data=body_str, timeout=3)
        elif method == "GET":
            response = requests.request(method, url, headers=header, params={params: f"http://{network}:{port}"}, timeout=3)        
        print(f"[Port {port}] Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"Port {port} is open.")
>>>>>>> 3c7d22bfb8026b3b49a150a14419db5d0046f2de
        else:
            body_data['coverImage'] = f"http://{network}:{port}"
        response = requests.request(method, f"{url}{path}", headers=header, json=body_data, timeout=30)
        # print(f"[Port {port}] Status: {response.status_code}")
        if response.status_code == 200:
            # print(f"Port {port} is open.")
            return True
        else:
            # print(response.text)
            # print(f"Port {port} is closed/filtered.")
            return False
    except requests.exceptions.RequestException as exc:
        # print(f"Port {port} is closed. Error: {exc}")
        return False



<<<<<<< HEAD
=======
def run(request_info, params, url):
    network_target = input("Network to scan: ").strip()
    ports = parse_ports(input("Ports (ex: 80 / 80,443 / 1-1024): ").strip())
    def worker(port):
        scanPort(request_info, params, network_target, port, url)
        
    threads(ports, worker)
>>>>>>> 3c7d22bfb8026b3b49a150a14419db5d0046f2de
