import logging
from fsa.settings import log_dir

logger = logging.getLogger(__name__)


def delete_log_files():
    logs = log_dir.rglob("*.log")
    counter = 0
    for log in logs:
        counter += 1
        log.unlink()

    logger.debug(f"removed {counter} log file(s)")
