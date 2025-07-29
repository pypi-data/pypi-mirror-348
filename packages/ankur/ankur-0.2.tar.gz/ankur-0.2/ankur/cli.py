# ankur/cli.py
import argparse
from ankur import show_links, say_hello

def main():
    parser = argparse.ArgumentParser(description="Ankur's CLI Tool")
    parser.add_argument('--hello', action='store_true', help="Print a greeting")
    parser.add_argument('--links', action='store_true', help="Show social links")
    
    args = parser.parse_args()
    
    if args.hello:
        say_hello()
    if args.links:
        show_links()
    if not (args.hello or args.links):
        print("Usage: ankur-cli [--hello] [--links]")

if __name__ == "__main__":
    main()