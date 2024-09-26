import argparse
from .app import app_root

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Testbench Manager")
    parser.add_argument(
        "--delay-apparatus-load",
        action="store_true",
    )
    parser.add_argument(
        "--delay-experiment-load",
        action="store_true",
    )
    args = parser.parse_args()

    app_root.start_app(args.delay_apparatus_load, args.delay_experiment_load)
