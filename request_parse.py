import json

def parse_request(file_path):
    headers = {}
    with open(file_path, "r", encoding="utf-8") as file:
        line0 = next(file, "").strip().split(" ")
        method = line0[0].upper()
        api_path = line0[1]
        for line in file:
            if line == "\n":
                break
            key, value = line.strip().split(": ", 1)
            if key == "Content-Length" or key == "Accept-Encoding":
                continue
            headers[key] = value
        body = file.read().strip()
        
    is_json = False
    body_dict = {}
    if body:
        try:
            body_dict = json.loads(body)
            is_json = True
        except json.JSONDecodeError:
            for item in body.split("&"):
                if "=" in item:
                    key, value = item.split("=", 1)
                    body_dict[key] = value
    return method, api_path, headers, body_dict, is_json