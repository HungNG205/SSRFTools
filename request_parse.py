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
    body = json.loads(body)
    return method, api_path, headers, body
