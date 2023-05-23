from drivers.Web import config as web_config
from drivers.Cli import config as cli_config
import argparse
import logging


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
        help='Use this to activate a log.'
    )

    args = parser.parse_args()
    initlog(args.log)

    if args.cli and args.web:
        print("Two options cannot be used at the same time.")

    elif args.cli and not args.web:
        cli_config.Config().run_ui()

    elif not args.cli and args.web:
        web_config.config().run_ui()

    else:
        print("No option has been passed.")


def initlog(logs):
    logging.basicConfig(level=logging.DEBUG)
    allLogs = [
        "drivers.Web.server",
        "drivers.Web.httpRequest",
        "drivers.Web.httpConnection"
    ]

    for log in allLogs:
        logger = logging.getLogger(log)
        logger.disabled = True

    for log in logs:
        logger = logging.getLogger(log)
        logger.disabled = False


if __name__ == "__main__":
    main()
