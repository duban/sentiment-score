from pathlib import Path
from loguru import logger
import logging
from datetime import datetime
import json
import sys
from app.config import FastConfig

class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG',
        0: 'NOTSET',
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id='app')
        log.opt(
            depth=depth,
            exception=record.exc_info
        ).log(level,record.getMessage())


class CustomizeLogger:

    @classmethod
    def make_logger(cls,config_path: Path):
        now = datetime.now()

        config = cls.load_logging_config(config_path)
        logging_config = config['logger']
        path = logging_config.get('path')
        date_now = now.strftime("%Y%m%d")
        filename = '{}_{}{}'.format(FastConfig.APP_NAME.upper(),date_now,logging_config['ext'])
        # print(path)
        # print(filename)
        log_file = '{}{}'.format(FastConfig.APP_DIR+'/var/', filename)
        print(log_file)

        logger = cls.customize_logging(
            log_file ,
            level=logging_config.get('level'),
            retention=logging_config.get('retention'),
            rotation=logging_config.get('rotation'),
            format=logging_config.get('format')
        )
        # print(sys.stdout)
        return logger

    @classmethod
    def customize_logging(cls,
            filepath: Path,
            level: str,
            rotation: str,
            retention: str,
            format: str
    ):

        logger.remove()
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format
        )
        logger.add(
            str(filepath),
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format
        )
        # print('cek:',logger)
        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ['uvicorn',
                     'uvicorn.error',
                     'fastapi'
                     ]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)


    @classmethod
    def load_logging_config(cls, config_path):
        config = None
        with open(config_path) as config_file:
            config = json.load(config_file)
        # print(config)
        return config

