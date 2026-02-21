import argparse
from Utils.parseRequest import parse_request


def print_banner():
    banner = r"""
    [96m        __   _
         __(  )_( )_
        (_   _    _)_
       / /(_) (__)   [0m
    [91m ____  ____  ____  _____ 
    / ___|/ ___||  _ \|  ___|
    \___ \\___ \| |_) | |_   
     ___) |___) |  _ <|  _|  
    |____/|____/|_| \_\_|    [0m
    [93m[ Cloud SSRF v1.0 ][0m
    """
    print(banner)


def main():
    print_banner()
    try:
        parser = argparse.ArgumentParser(
            description="Cloud SSRF",
            epilog="Example usage: python CloudSSRF.py -f request_exam.txt -p url -s http -o scanNet",
        )
        parser.add_argument("-f", "--file", required=True, help="Request file path")
        parser.add_argument("-p", "--params", required=True, help="Parameter to test SSRF")
        parser.add_argument("-s", "--scheme", required=True, help="Protocol scheme (http or https)")     
        parser.add_argument("-m", "--module", required=True, choices=["scanNet", "scanPort", "scanAPI", "exploitCloud"], help="option of scan/exploit")
       
        args = parser.parse_args()
        file_path = args.file
        scheme = args.scheme.lower()
        verify = True
        method, api_path, headers, body, is_json = parse_request(file_path)
        if scheme == "https":
            verify = False

        host = headers.get("Host")
        if not host:
            print("Error: Missing required Host header in request file.")
            return

        url = f"{scheme}://{host.strip()}{api_path.split('?')[0]}"
        module_name = f"Module.{args.module}"
        module = __import__(module_name, fromlist=["run"])
        module.run((method, api_path, headers, body, is_json, verify), args.params, url)
    except SystemExit:
        print("Error: Invalid command-line arguments. Use -h for help.")
    except FileNotFoundError as e:
        print(f"Error: Request file not found: {e}")
    except ValueError as e:
        print(f"Error: Invalid request file format: {e}")
    except ImportError as e:
        print(f"Error: Failed to load module: {e}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
