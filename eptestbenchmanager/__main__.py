import argparse
import logging
import os
from datetime import datetime
from .app import app_root
from .runtime.runtimemanager import RuntimeManager

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the Testbench Manager application.

    Parses command-line arguments and starts the application with the specified options.
    """

    parser = argparse.ArgumentParser(description="Testbench Manager")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
    )
    parser.add_argument("--app-data-dir", default=None)

    args = parser.parse_args()

    runtimeManager = RuntimeManager(args.app_data_dir)
    runtimeManager.configure_logging(args.log_level)
    logger.info("Starting EPTestbenchManager...")

    app_root.start_app(runtimeManager)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("An error occurred: %s", e)
        raise
