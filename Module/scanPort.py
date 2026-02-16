import requests


def scanPort(request_info,  network, port, url):
    try:
        method, path , header, body = request_info
        body_data = body.copy()
        if 'profilePicture' in body_data:
            body_data['profilePicture'] = f"http://{network}:{port}"
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



