def make_request(client, method, url, headers, body, params, payload, is_json):
    body_data = body.copy()
    body_data[params] = payload
    
    if method in ["POST", "PUT"]:
        if is_json:
            return client.request(method, url, headers=headers, json=body_data)
        else:
            body_str = "&".join([f"{k}={v}" for k, v in body_data.items()])
            return client.request(method, url, headers=headers, data=body_str)
    elif method == "GET":
        return client.request(method, url, headers=headers, params={params: payload})
    
    raise ValueError(f"Unsupported HTTP method: {method}")


