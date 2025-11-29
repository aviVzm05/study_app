import logging
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_FILE = LOG_DIR / "app.log"

def setup_logging():
    """Configures application-wide logging."""
    if not LOG_DIR.exists():
        LOG_DIR.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
    # Suppress verbose logging from external libraries if needed
    logging.getLogger('google.api_core').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

    print(f"Logging configured. Log file: {LOG_FILE}")

# Initialize logger for the module
_logger = logging.getLogger(__name__)

def log_event(level: str, message: str):
    """Logs an event at the specified level."""
    if level == 'info':
        _logger.info(message)
    elif level == 'warning':
        _logger.warning(message)
    elif level == 'error':
        _logger.error(message)
    elif level == 'critical':
        _logger.critical(message)
    elif level == 'debug':
        _logger.debug(message)
    else:
        _logger.info(f"Unknown log level '{level}': {message}")


if __name__ == '__main__':
    setup_logging()
    _logger.info("Logging service initialized and tested.")
    log_event("info", "This is an info message via log_event.")
    log_event("debug", "This is a debug message via log_event.")
    log_event("warning", "This is a warning message via log_event.")
    log_event("error", "This is an error message via log_event.")
    log_event("critical", "This is a critical message via log_event.")
    log_event("unknown", "This is a message with an unknown level.")