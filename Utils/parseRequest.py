import json
from urllib.parse import parse_qsl

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
            if key.lower() in ["content-length", "accept-encoding"]:
                continue
            headers[key] = value
        body = f.read().strip()
        
    body_dict = {}
    if body:
        try:
            body_dict = json.loads(body)
        except json.JSONDecodeError:
            body_dict = dict(parse_qsl(body, keep_blank_values=True))
    return method, api_path, headers, body_dict
    