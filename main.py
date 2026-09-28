from drivers.web import config as web_config
import argparse
import logging
import os


def main():
    parser = argparse.ArgumentParser(
        prog='main',
        description='Run the web application.'
    )
    parser.add_argument(
        '--web',
        action='store_true',
        help='Run the web application (the only interface).'
    )
    parser.add_argument(
        '--log',
        nargs='+',
        default=[],
        help='Names of loggers to set to DEBUG.'
    )

    args = parser.parse_args()
    initlog(args.log)
    web_config.Config().run_ui()


def initlog(debug_loggers):
    """INFO by default (LOG_LEVEL overrides it); the loggers named with
    --log are set to DEBUG."""
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())
    for name in debug_loggers:
        logging.getLogger(name).setLevel(logging.DEBUG)


if __name__ == "__main__":
    main()
