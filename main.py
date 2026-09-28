from drivers.web import config as web_config
from drivers.cli import config as cli_config
import argparse
import logging
import os


def main():
    parser = argparse.ArgumentParser(
        prog='main',
        description='Run cli or web programs.',
        epilog='This is the epilog.'
    )
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Use this option to run cli programs.'
    )
    parser.add_argument(
        '--web',
        action='store_true',
        help='Use this option to run Web programs.'
    )
    parser.add_argument(
        '--log',
        nargs='+',
        default=[],
        help='Names of loggers to set to DEBUG.'
    )

    args = parser.parse_args()
    initlog(args.log)

    if args.cli and args.web:
        print("Two options cannot be used at the same time.")

    elif args.cli and not args.web:
        cli_config.Config().run_ui()

    elif not args.cli and args.web:
        web_config.Config().run_ui()

    else:
        print("No option has been passed.")


def initlog(debug_loggers):
    """INFO by default (LOG_LEVEL overrides it); the loggers named with
    --log are set to DEBUG."""
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())
    for name in debug_loggers:
        logging.getLogger(name).setLevel(logging.DEBUG)


if __name__ == "__main__":
    main()
