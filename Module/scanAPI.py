import requests
from Module.runThread import threads

def scanPort(request_info, params, api, url):
    try:
        method, _ , header, body, is_json = request_info

        if method == "POST" or method == "PUT":
            pass
        #em chưa biết viết cái này ntn nên tạm thời để pass, nếu có ý tưởng thì có thể viết sau
        elif method == "GET":
            response = requests.request(
                method,
                url,
                headers=header,
                params={params: f"http://{header['Host'].strip()}{api}"},
                timeout=3,
            )
        
        print(f"[API {api}] Status: {response.status_code}")
        if response.status_code == 200:
            print(f"API {api} is access.")
        else:
            print(f"API {api} is closed/filtered.")
    except requests.exceptions.RequestException as exc:
        print(f"API {api} is closed. Error: {exc}")

def run(request_info, params, url):
    with open("Dict/api_dict.txt", "r") as f:
        api_list = [line.strip() for line in f if line.strip()]
    def worker(api):
        scanPort(request_info, params, api, url)
    threads(api_list, worker)
