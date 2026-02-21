import httpx
from urllib.parse import urlparse
from Utils.runThread import threads
from Utils.makeRequest import make_request


def scanAPI(request_info, params, api, url):
    try:
        method, _, header, body, is_json, verify = request_info
        baseUrl = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        payload = f"{baseUrl}{api}"

        with httpx.Client(http2=True, verify=verify, timeout=3) as client:
            response = make_request(client, method, url, header, body, params, payload, is_json)

            print("-"*50)
            print(f"[API {api}] Status: {response.status_code}")
            if response.status_code == 200:
                print(f"API {api} is accessible.")
            else:
                print(f"API {api} is closed/filtered.")
            print("-"*50)
    except httpx.RequestError as exc:
        print(f"API {api} is not accessible/exist by (timeout).")


def run(request_info, params, url):
    with open("PayloadSSRF/ApiTesting.txt", "r") as f:
        api_list = [line.strip() for line in f if line.strip()]

    def worker(api):
        scanAPI(request_info, params, api, url)

    threads(api_list, worker)
