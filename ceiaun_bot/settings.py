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
BOT_DATABASE_DIR = BASE_DIR / "data/bot"
BOT_DATABASE_UPDATE_INTERVAL = config("BOT_DATABASE_UPDATE_INTERVAL", cast=int, default=60)

make_dir(BOT_DATABASE_DIR)

# Excel files
EXCEL_BASE_TEMPLATE = BASE_DIR / "data/base/report.xlsx"
EXCEL_GENERATED_FILES_DIR = BASE_DIR / "data/generated_files"
make_dir(EXCEL_GENERATED_FILES_DIR)
EXCEL_TEMP_FILE = EXCEL_GENERATED_FILES_DIR / "temp.xlsx"

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
FILE_CONVERT_NAME = "BQACAgQAAx0Edz5chAADDmW5YEX63_VhYtRaQdrZJVLro0g2AAJMEwACtPPIUcTrhInm9kklNAQ"
FILE_COURSE_REQUEST = "BQACAgQAAx0Edz5chAADB2W34uUd86Q7EG8SNB8-jRtiPMZsAAINEAACi4zBURJXGMOkPaRENAQ"
