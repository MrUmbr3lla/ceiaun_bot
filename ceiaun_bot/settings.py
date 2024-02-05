import logging.config
import os.path
from pathlib import Path

from decouple import config


def make_dir(path: Path) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


BASE_DIR = Path(__file__).resolve().parent

# Logging
make_dir(BASE_DIR / "logs")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s - %(funcName)s(): %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "none": {
            "format": "%(message)s",
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
        "log_request": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/requests.log",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "none",
        },
        "log_bad_request": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/bad_requests.log",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
            "formatter": "none",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "log_file"],
            "level": "INFO",
            "propagate": False,
        },
        "request_log": {
            "handlers": ["console", "log_request"],
            "level": "INFO",
            "propagate": False,
        },
        "bad_request_log": {
            "handlers": ["console", "log_bad_request"],
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

# Bot
BOT_TOKEN = config("BOT_TOKEN")
BOT_DATABASE_DIR = BASE_DIR / "data/bot"
BOT_DATABASE_UPDATE_INTERVAL = config("BOT_DATABASE_UPDATE_INTERVAL", cast=int, default=60)
ADMIN_IDS = [int(i) for i in config("ADMIN_IDS").split(",")]

make_dir(BOT_DATABASE_DIR)

# Excel files
EXCEL_BASE_TEMPLATE = BASE_DIR / "data/base/report.xlsx"
EXCEL_GENERATED_FILES_DIR = BASE_DIR / "data/generated_files"
make_dir(EXCEL_GENERATED_FILES_DIR)
EXCEL_TEMP_FILE = EXCEL_GENERATED_FILES_DIR / "temp.xlsx"

# File ids
FILE_SE_CHARTS = (config("FILE_SE_LIST"), config("FILE_SE_CHART"))
FILE_IT_CHARTS = (config("FILE_IT_LIST"), config("FILE_IT_CHART"))
FILE_HOME_IMAGE = config("FILE_HOME_IMAGE")
FILE_CONVERT_NAME = config("FILE_CONVERT_NAME")
FILE_COURSE_REQUEST = config("FILE_COURSE_REQUEST")
