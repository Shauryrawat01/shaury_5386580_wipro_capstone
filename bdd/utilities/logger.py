import logging
import os
from datetime import datetime

# Global variable to store the log file name for the current session
_log_file = None

def setup_logger(name=None):
    global _log_file

    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logs_dir = os.path.join(project_root, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Use a custom attribute to check if we've already initialized our specific handlers
    if not hasattr(root_logger, "_automation_initialized"):
        if _log_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            _log_file = os.path.join(logs_dir, f"automation_{timestamp}.log")
        
        # File Handler (Session specific)
        file_handler = logging.FileHandler(_log_file)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

        # Latest Log (Always overwritten)
        latest_log = os.path.join(logs_dir, "latest.log")
        latest_handler = logging.FileHandler(latest_log, mode='w')
        latest_handler.setFormatter(file_formatter)
        root_logger.addHandler(latest_handler)

        # Console Handler (Only add if not already in a capture environment)
        # Note: Pytest -s allows seeing this.
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(file_formatter)
        root_logger.addHandler(console_handler)
        
        root_logger._automation_initialized = True

    if name:
        return logging.getLogger(name)
    return root_logger