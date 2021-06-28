import logging
import os
from fastapi import FastAPI
from polyglot.downloader import downloader
from app.utils.logs import CustomizeLogger
from app import config

from app.routers import sentiments

logger = logging.getLogger(__name__)
config_path= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config_path = config.LOG_CONFIG

def create_app() -> FastAPI:
    app = FastAPI(title='Sentiment app', debug=False)
    logger = CustomizeLogger.make_logger(config_path)
    # print(logger)
    app.logger = logger
    return app

app = create_app()

app.include_router(sentiments.router, prefix="/api/v1", tags=["Sentiment Docs"])

app.logger.info("Starting downloading languages packages for polyglot.....")
# print("Starting downloading languages packages for polyglot.....")
polyglot_languages = ["en", "vi", "id"]
try:
    for lang in polyglot_languages:
        downloader.download(f"embeddings2.{lang}")
        downloader.download(f"sentiment2.{lang}")
        downloader.download(f"ner2.{lang}")
    app.logger.info(f"Languages packages {polyglot_languages} have been successfully downloaded")
except Exception as e:
    app.logger.error(f"Something went wrong: {e}")
