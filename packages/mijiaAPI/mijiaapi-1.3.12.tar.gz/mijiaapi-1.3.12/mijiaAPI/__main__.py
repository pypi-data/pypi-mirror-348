import argparse
import sys

from .login import mijiaLogin

def parse_args(args):
    parser = argparse.ArgumentParser(description="Mijia API CLI")
    parser.add_argument(
        '-i', '--login',
        action='store_true',
        help="Login by QR code and save cookies to file",
    )
    parser.add_argument(
        '-c', '--cookie_path',
        type=str,
        help="Path to the cookies file",
    )
    return parser.parse_args(args)

def main(args):
    args = parse_args(args)
    if args.login:
        api = mijiaLogin(save_path=args.cookie_path)
        auth = api.QRlogin()

if __name__ == "__main__":
    main(sys.argv[1:])
