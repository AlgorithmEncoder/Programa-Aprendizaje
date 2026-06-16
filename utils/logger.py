import logging
from pathlib import Path

from config.settings import (
    LOG_LEVEL,
    LOG_TO_FILE,
    LOG_PATH
)


def setup_logging():

    log_level = getattr(
        logging,
        LOG_LEVEL.upper(),
        logging.INFO
    )

    handlers = [
        logging.StreamHandler()
    ]

    if LOG_TO_FILE:

        log_file = Path(LOG_PATH)

        log_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        handlers.append(
            logging.FileHandler(
                log_file,
                encoding="utf-8"
            )
        )

    logging.basicConfig(
        level=log_level,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        handlers=handlers,
        force=True
    )


def get_logger(name):
    return logging.getLogger(name)