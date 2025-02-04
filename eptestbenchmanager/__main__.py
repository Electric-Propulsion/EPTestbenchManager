import argparse
import logging
import os
from datetime import datetime
from .app import app_root


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
    parser.add_argument(
        "--log-dir", default="program_logs", help="Set the logging directory"
    )

    args = parser.parse_args()

    logdir = os.path.join(os.path.dirname(__file__), "program_logs")
    logfile = os.path.join(
        logdir, f'EPTestbenchManager {datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.log'
    )
    os.makedirs(os.path.dirname(logfile), exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.FileHandler(logfile, "w", "utf-8"), logging.StreamHandler()],
    )
    logger = logging.getLogger(__name__)
    logger.info("Logging to %s", logfile)
    logger.info(
        "Starting Testbench Manager with log level %s and log directory %s",
        args.log_level,
        args.log_dir,
    )
    logger.info("Logging level set to %s", args.log_level)

    app_root.start_app()


if __name__ == "__main__":
    main()
