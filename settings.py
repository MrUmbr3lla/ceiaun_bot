import logging.config
import os.path
from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent

# Bot
BOT_TOKEN = config("BOT_TOKEN")

# Excel files
EXCEL_BASE_TEMPLATE = BASE_DIR / "data/base/report.xlsx"
EXCEL_GENERATED_FILES_DIR = BASE_DIR / "data/generated_files"
EXCEL_TEMP_FILE = EXCEL_GENERATED_FILES_DIR / "temp.xlsx"

if not os.path.exists(EXCEL_GENERATED_FILES_DIR):
    os.makedirs(EXCEL_GENERATED_FILES_DIR)

# Logging
if not os.path.exists("logs"):
    os.makedirs("logs")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s - %(funcName)s(): %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "log_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/info.log",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "standard",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "log_file"],
            "level": "INFO",
            "propagate": False,
        },
        "httpx": {
            "handlers": ["console", "log_file"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

logging.config.dictConfig(LOGGING)
