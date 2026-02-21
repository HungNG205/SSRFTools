import json

def parse_request(request_file):
    headers = {}
    with open(request_file, "r", encoding="utf-8") as f:
        reqLine = next(f, "").strip().split(" ")
        method = reqLine[0].upper()
        api_path = reqLine[1]
        for line in f:
            if not line.strip():
                break
            key, value = line.strip().split(": ", 1)
            if key == "Content-Length" or key == "Accept-Encoding":
                continue
            headers[key] = value
        body = f.read().strip()
        
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
