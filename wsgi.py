import logging
import os
from datetime import datetime
from eptestbenchmanager.app import app_root

# Configure logging
logdir = os.path.join(os.path.dirname(__file__), "program_logs")
logfile = os.path.join(
    logdir, f'EPTestbenchManager {datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.log'
)
os.makedirs(os.path.dirname(logfile), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler(logfile, "w", "utf-8"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
logger.info("Logging to %s", logfile)

app = app_root.app
