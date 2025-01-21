import argparse
from .app import app_root


def main():
    """Main entry point for the Testbench Manager application.

    Parses command-line arguments and starts the application with the specified options.
    """
    parser = argparse.ArgumentParser(description="Testbench Manager")
    parser.add_argument(
        "--delay-apparatus-load",
        action="store_true",
        help="Delay the loading of the apparatus.",
    )
    parser.add_argument(
        "--delay-experiment-load",
        action="store_true",
        help="Delay the loading of the experiment.",
    )
    args = parser.parse_args()

    app_root.start_app(args.delay_apparatus_load, args.delay_experiment_load)


if __name__ == "__main__":
    main()
