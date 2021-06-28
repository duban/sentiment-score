import uvicorn
from app.config import FastConfig
from app import app

app.logger.info(f"* {FastConfig.APP_NAME.upper()} microservice is starting....")

if __name__ == '__main__':

    uvicorn.run(app, host=FastConfig.APP_HOST, port=int(FastConfig.APP_PORT))
