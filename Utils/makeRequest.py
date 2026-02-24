def make_request(client, method, url, headers, body, params, payload):
    body_data = body.copy()
    
    if method in ["POST", "PUT"]:
        body_data[params] = payload
        content_type = headers.get("Content-Type", "")
        if "json" in content_type:
            return client.request(method, url, headers=headers, json=body_data)
        else:
            body_str = "&".join([f"{k}={v}" for k, v in body_data.items()])
            return client.request(method, url, headers=headers, data=body_str)
    elif method == "GET":
        return client.request(method, url, headers=headers, params={params: payload})
    
    raise ValueError(f"Unsupported HTTP method: {method}")


