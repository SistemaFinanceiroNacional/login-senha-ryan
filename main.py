from drivers.Web import server

import argparse


def main():
    parser = argparse.ArgumentParser(prog='main', description='Run cli or web programs.', epilog='This is the epilog.')
    parser.add_argument('--cli', action='store_true', help='Use this option to run cli programs.')
    parser.add_argument('--web', action='store_true', help='Use this option to run Web programs.')

    args = parser.parse_args()
    if args.cli and args.web:
        print("Two options cannot be used at the same time.")

    elif args.cli and not args.web:
        print("OK, but --cli is not implemented yet.")

    elif not args.cli and args.web:
        server.main()

    else:
        print("No option has been passed.")


if __name__ == "__main__":
    main()