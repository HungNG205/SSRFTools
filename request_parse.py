import json
import xml.etree.ElementTree as ET

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
            if key == "Content-Length":
                continue
            headers[key] = value
        body = file.read().strip()
        
    is_json = False
    is_xml = False
    body_dict = {}
    if body:
        try:
            body_dict = json.loads(body)
            is_json = True
        except json.JSONDecodeError:
            try:
                root = ET.fromstring(body)
                body_dict = {root.tag: _xml_to_dict(root)}
                is_xml = True
            except ET.ParseError:
                for item in body.split("&"):
                    if "=" in item:
                        key, value = item.split("=", 1)
                        body_dict[key] = value
    return method, api_path, headers, body_dict, is_json or is_xml

def _xml_to_dict(element):
    result = {}
    for child in element:
        child_data = _xml_to_dict(child)
        if child.tag in result:
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]
            result[child.tag].append(child_data)
        else:
            result[child.tag] = child_data
    return result if result else element.text or ""