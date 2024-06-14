import logging.config
import os.path
from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent

# Logging
os.makedirs(BASE_DIR / "logs", exist_ok=True)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s - %(funcName)s(): %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
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
            "formatter": "standard",
        },
        "log_bad_request": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/bad_requests.log",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
            "formatter": "standard",
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
BACKUP_CH_ID = config("BACKUP_CH_ID")
REQUEST_CLOSE = config("REQUEST_CLOSE", cast=bool, default=False)
SUMMER_REQUEST_CLOSE = config("SUMMER_REQUEST_CLOSE", cast=bool, default=False)

os.makedirs(BOT_DATABASE_DIR, exist_ok=True)

# Excel files
EXCEL_BASE_TEMPLATE = BASE_DIR / "data/base/report.xlsx"
EXCEL_BASE_SUMMER_TEMPLATE = BASE_DIR / "data/base/summer_report.xlsx"
EXCEL_GENERATED_FILES_DIR = BASE_DIR / "data/generated_files"
os.makedirs(EXCEL_GENERATED_FILES_DIR, exist_ok=True)
EXCEL_TEMP_FILE = EXCEL_GENERATED_FILES_DIR / "temp.xlsx"

# File ids
FILE_SE_CHARTS = (config("FILE_SE_LIST"), config("FILE_SE_CHART"))
FILE_IT_CHARTS = (config("FILE_IT_LIST"), config("FILE_IT_CHART"))
FILE_HOME_IMAGE = config("FILE_HOME_IMAGE")
FILE_CONVERT_NAME = config("FILE_CONVERT_NAME")
FILE_COURSE_REQUEST = config("FILE_COURSE_REQUEST")
