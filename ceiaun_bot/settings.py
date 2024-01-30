import logging.config
import os.path
from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent

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

# Bot
BOT_TOKEN = config("BOT_TOKEN")

# Excel files
EXCEL_BASE_TEMPLATE = BASE_DIR / "data/base/report.xlsx"
EXCEL_GENERATED_FILES_DIR = BASE_DIR / "data/generated_files"
EXCEL_TEMP_FILE = EXCEL_GENERATED_FILES_DIR / "temp.xlsx"

if not os.path.exists(EXCEL_GENERATED_FILES_DIR):
    os.makedirs(EXCEL_GENERATED_FILES_DIR)

# TODO: Set in .env
# File ids
FILE_SE_CHARTS = [
    "BQACAgQAAx0Edz5chAADA2W34cxmn7EW_DTt--kiUPL3WPmlAAIJEAACi4zBUU3kLcvAvafGNAQ",  # SE List
    "BQACAgQAAx0Edz5chAADBWW34lzgzLL287tXKHGMZav4Omf_AAILEAACi4zBUaBr4xU4RUdINAQ",  # SE Chart
]
FILE_IT_CHARTS = [
    "BQACAgQAAx0Edz5chAADBGW34ileWM0Tg0cbAAF8xXR1ig7mSwACChAAAouMwVEy3dkOwcKm_DQE",  # IT List
    "BQACAgQAAx0Edz5chAADBmW34pXyzuUw9KQUw9bCIUM4I-BjAAIMEAACi4zBUf6IfhfsqxqiNAQ"  # IT Chart
]
FILE_HOME_IMAGE = "BQACAgQAAx0Edz5chAADCWW340mbGOmLl-WAtkCOFxEm1L5kAAIPEAACi4zBUS36-Kc0q-JeNAQ"
FILE_CONVERT_NAME = "BQACAgQAAx0Edz5chAADCmW3440_ebd_3XPYwfxkoCpz8TYnAAIQEAACi4zBUfXtf4Z0LyMsNAQ"
FILE_COURSE_REQUEST = "BQACAgQAAx0Edz5chAADB2W34uUd86Q7EG8SNB8-jRtiPMZsAAINEAACi4zBURJXGMOkPaRENAQ"
