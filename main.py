from Module import scanAPI, scanNet, scanPort
from request_parse import parse_request

def main():
    print("Select function:\n1) scanNet\n2) scanPort\n3) scanAPI\n4) exploitMetadata")
    choice = input("Enter choice (1-4): ").strip()
    file_path = input("Enter request file (default request_exam.txt): ").strip() or "request_exam.txt"
    method, api_path, header, body, is_json = parse_request(file_path)
    if "?" in api_path:
        params = api_path.split("?")[1].split("=")[0] 
    else:
        print(body)
        params = input(f"Enter parameter to test: ").strip()
    if not params:
        raise ValueError("Parameter required.")
    scheme = input("Enter scheme (http/https, default http): ").strip().lower() or "http"
    if scheme == "https":
        header["Verify"] = "False"
    url = f"{scheme}://{header['Host'].strip()}{api_path.split('?')[0]}"
    if choice == "1":
        scanNet.run((method, api_path, header, body, is_json), params, url)
    elif choice == "2":
        scanPort.run((method, api_path, header, body, is_json), params, url)
    elif choice == "3":
        scanAPI.run((method, api_path, header, body, is_json), params, url)
    elif choice == "4":
        exploitMetaData.run((method, api_path, header, body, is_json), params, url)
if __name__ == "__main__":
    main()
