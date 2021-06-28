import os
import uvicorn
import logging
import sys
from pathlib import Path
from loguru import logger
import json
from datetime import datetime

LOG_CONFIG = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/app/logging_config.json'
ENV = os.environ.get('ENV', 'local')
APP_NAME = os.environ.get("APP_NAME", "sentiment")
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(APP_DIR, "data")


class FastConfig(object):
    APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ENV = os.environ.get('ENV', 'local')

    APP_NAME = APP_NAME
    APP_VERSION = "1.0"
    APP_HOST = os.environ.get('APP_HOST', '0.0.0.0')
    APP_PORT = os.environ.get('APP_PORT', 8000)
    # SECRET_KEY = os.environ.get('SECRET_KEY', 'SECRET')
    RELOAD = False