import argparse
from .core import FBH

def main():
    parser = argparse.ArgumentParser(description="FBH: File Encryption Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Hide command
    hide_parser = subparsers.add_parser("hide", help="Encrypt a file")
    hide_parser.add_argument("password", nargs="?", default=None, help="Password or '-' for no password")
    hide_parser.add_argument("file", help="File to encrypt")

    # Decode command
    decode_parser = subparsers.add_parser("decode", help="Decrypt a file")
    decode_parser.add_argument("password", help="Password for decryption")
    decode_parser.add_argument("file", help="Encrypted file")

    args = parser.parse_args()
    fbh = FBH()

    if args.command == "hide":
        output_file = args.file + ".fbh"
        if args.password == "-":
            fbh.hide_file(args.file, output_file, password=None)
        else:
            fbh.hide_file(args.file, output_file, password=args.password)
    elif args.command == "decode":
        output_file = args.file.replace(".fbh", ".dec")
        fbh.decode_file(args.file, output_file, args.password)

if __name__ == "__main__":
    main()