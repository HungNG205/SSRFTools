from Module import scanNet, scanPort
from request_parse import parse_request

def main():
    print("Select function:\n1) scanNet\n2) scanPort")
    choice = input("Enter choice (1-2): ").strip()
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
        network = input("Network to scan (e.g., 192.168.1): ").strip()
        port = int(input("Port (default 8080): ").strip() or "8080")
        scanNet.run((method, api_path, header, body, is_json), params, network, port, url)
    elif choice == "2":
        ports = scanPort.parse_ports(input("Ports (ex: 80 / 80,443 / 1-1024): ").strip())
        scanPort.run((method, api_path, header, body, is_json), params, ports, url)

if __name__ == "__main__":
    main()
