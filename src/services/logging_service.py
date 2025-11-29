import logging
from pathlib import Path
from datetime import datetime
import sys

LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_FILE = LOG_DIR / "app.log"

def setup_logging():
    """Sets up basic logging for the application."""
    if not LOG_DIR.exists():
        LOG_DIR.mkdir()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(sys.stdout) # Also log to console
        ]
    )

def log_event(level, message, *args, **kwargs):
    """Logs an application event."""
    logger = logging.getLogger(__name__)
    if level == 'info':
        logger.info(message, *args, **kwargs)
    elif level == 'warning':
        logger.warning(message, *args, **kwargs)
    elif level == 'error':
        logger.error(message, *args, **kwargs)
    elif level == 'critical':
        logger.critical(message, *args, **kwargs)
    else:
        logger.debug(message, *args, **kwargs)

if __name__ == '__main__':
    import sys
    setup_logging()
    log_event('info', "Application started.")
    log_event('warning', "Disk space low.")
    log_event('error', "Failed to load module %s.", "example_module")