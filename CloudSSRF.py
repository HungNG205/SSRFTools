import argparse
from request_parse import parse_request

def main():
    parser = argparse.ArgumentParser(description="Cloud SSRF",
                                     epilog="Example usage: python CloudSSRF.py -f request_exam.txt -p url -s http -o scanNet")
    parser.add_argument("-f", "--file", required=True, help="Header request file path")
    parser.add_argument("-p", "--params", required=True, help="Parameter to test SSRF")
    parser.add_argument("-s", "--scheme", required=True, help="Protocol scheme (http or https)")
    parser.add_argument("-o", "--option", required=True, choices=["scanNet", "scanPort", "scanAPI", "exploitMetadata"], help="option of scan/exploit")
    args = parser.parse_args()
    file_path = args.file
    params = args.params
    scheme = args.scheme
    method, api_path, header, body, is_json = parse_request(file_path)
    if scheme == "https":
        header["Verify"] = "False"
    url = f"{scheme}://{header['Host'].strip()}{api_path.split('?')[0]}"
    try:
        module_name = f"Module.{args.option}"
        mod = __import__(module_name, fromlist=['run'])
        mod.run((method, api_path, header, body, is_json), args.params, url)
    except ImportError as e:
        print(f"[!] Error loading module {args.option}: {e}")
    except Exception as e:
        print(f"[!] Runtime error: {e}")
    
if __name__ == "__main__":
    main()
