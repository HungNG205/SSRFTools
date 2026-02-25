
import argparse
from Utils.parseRequest import parse_request
import importlib


def print_banner():
    banner_text = r"""
        __   _
    __(  )_( )_
   (_   _    _)_
  / /(_) (__)   
 ____  ____  ____  _____ 
/ ___|/ ___||  _ \|  ___|
\___ \\___ \| |_) | |_   
 ___) |___) |  _ <|  _|  
|____/|____/|_| \_\_|    
"""
    usage_text = """
Usage Options:
    -f, --file     Request file path (required)
    -p, --params   Parameter to test SSRF (required)
    -s, --scheme   Protocol scheme: http or https (required)
    -m, --module   Module to run: scanNet, scanPort, exploitCloud (required)

Example:
    python CloudSSRF.py -f request_exam.txt -p url -s http -m scanNet
"""
    print("Cloud SSRF v1.0")
    print(banner_text)
    print(usage_text)


def main():
    print_banner()
    try:
        parser = argparse.ArgumentParser(
            description="Cloud SSRF",
            epilog="Example usage: python CloudSSRF.py -f request_exam.txt -p url -s http -m scanNet",
        )
        parser.add_argument("-f", "--file", required=True, help="Request file path")
        parser.add_argument("-p", "--params", required=True, help="Parameter to test SSRF")
        parser.add_argument("-s", "--scheme", required=True, help="Protocol scheme (http or https)")     
        parser.add_argument("-m", "--module", required=True, choices=["scanNet", "scanPort", "exploitCloud"], help="option of scan/exploit")
       
        args = parser.parse_args()
        file_path = args.file
        scheme = args.scheme.lower()
        verify = True
        method, api_path, headers, body = parse_request(file_path)
        if scheme == "https":
            verify = False

        host = headers.get("Host")
        if not host:
            print("Error: Missing required Host header in request file.")
            return

        url = f"{scheme}://{host.strip()}{api_path.split('?')[0]}"
        module_name = f"Module.{args.module}"
        module = importlib.import_module(module_name)
        module.run((method, api_path, headers, body, verify), args.params, url)
    except SystemExit as e:
        if e.code in (0, None):
            return
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
