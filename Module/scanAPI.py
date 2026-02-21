import requests
from urllib.parse import urlparse
from Utils.runThread import threads

def scanAPI(request_info, params, api, url):
    try:
        method, api_path , header, body, is_json, verify = request_info
        parsed = urlparse(url)
        baseUrl = f"{parsed.scheme}://{parsed.netloc}"
        if method == "POST" or method == "PUT":
            body_data = body.copy()
            if params in body_data:
                body_data[params] = f"{baseUrl}{api}"
            if is_json:
                response = requests.request(method, url, headers=header, json=body_data, timeout=3, verify=verify)
            else:
                response = requests.request(method, url, headers=header, data=body_data, timeout=3, verify=verify)

        elif method == "GET":
            response = requests.request(method, url, headers=header, params={params: f"{baseUrl}{api}"}, timeout=3, verify=verify)
        
        print(f"[API {api}] Status: {response.status_code}")

        if response.status_code == 200:
            print(f"API {api} is accessible.")
        else:
            print(f"API {api} is closed/filtered.")
    except requests.exceptions.RequestException as exc:
        print(f"API {api} is closed. Error: {exc}")

def run(request_info, params, url):
    with open("Dict/API_dict.txt", "r") as f:
        api_list = [line.strip() for line in f if line.strip()]
    def worker(api):
        scanAPI(request_info, params, api, url)

    threads(api_list, worker)