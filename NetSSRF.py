import argparse
import importlib

from Utils.parseRequest import parse_request


def print_banner():
    banner_text = """
    \x1b[96m _   _      _    ____ ____  ____  _____ \x1b[0m
    \x1b[96m| \\ | | ___| |_ / ___/ ___||  _ \\|  ___|\x1b[0m
    \x1b[96m|  \\| |/ _ \\ __|\\___ \\___ \\| |_) | |_   \x1b[0m
    \x1b[96m| |\\  |  __/ |_  ___) |__) |  _ <|  _|  \x1b[0m
    \x1b[96m|_| \\_|\\___|\\__||____/____/|_| \\_\\_|    \x1b[0m
    \x1b[93m[ NetSSRF - Internal Recon CLI ]\x1b[0m
    """
    print(banner_text)


def main():
    print_banner()
    try:
        parser = argparse.ArgumentParser(
            description="NetSSRF - Internal network reconnaissance for SSRF testing",
            epilog="Example usage: python NetSSRF.py -f request_exam.txt -p url -s http -m scanNet",
        )
        parser.add_argument("-f", "--file", required=True, help="Request file path")
        parser.add_argument("-p", "--params", required=True, help="Parameter to test SSRF")
        parser.add_argument("-s", "--scheme", required=True, choices=["http", "https"], help="Protocol scheme")
        parser.add_argument(
            "-m",
            "--module",
            required=True,
            choices=["scanNet", "scanPort"],
            help="Recon module: scanNet or scanPort",
        )

        args = parser.parse_args()
        file_path = args.file
        scheme = args.scheme.lower()
        method, api_path, headers, body = parse_request(file_path)

        host = headers.get("Host")
        if not host:
            print("Error: Missing required Host header in request file.")
            return

        url = f"{scheme}://{host.strip()}{api_path.split('?')[0]}"
        module_name = f"Module.{args.module}"
        module = importlib.import_module(module_name)
        module.run((method, api_path, headers, body), args.params, url)
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