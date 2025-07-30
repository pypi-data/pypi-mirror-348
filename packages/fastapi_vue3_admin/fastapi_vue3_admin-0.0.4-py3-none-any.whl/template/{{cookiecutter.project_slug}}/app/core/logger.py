import logging
import os
from logging.config import dictConfig

from rich.logging import RichHandler

from app.core.config import settings

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_LEVEL = "DEBUG" if settings.debug else "INFO"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "plain": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "level": LOG_LEVEL,
            "rich_tracebacks": True,
            "markup": True,
            "show_path": False
        },
        "file": {
            "class": "logging.FileHandler",
            "level": LOG_LEVEL,
            "filename": os.path.join(LOG_DIR, "app.log"),
            "formatter": "plain",
            "encoding": "utf8"
        },
    },
    "root": {
        "level": LOG_LEVEL,
        "handlers": ["console", "file"]
    },
}

def setup_logging():
    dictConfig(LOGGING_CONFIG)
    logging.getLogger(__name__).info("Logging initialized. Level=%s Debug=%s", LOG_LEVEL, settings.debug) 