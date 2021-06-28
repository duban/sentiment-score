from starlette.requests import Request
from starlette.responses import JSONResponse
from app.transformers import SentimentTransformer
from multiprocessing import cpu_count
from app import response, config
import json

class SentimentController:
    @staticmethod
    async def get_sentiment(request: Request) -> JSONResponse:
        try:
            request_data = request.json()
            data = json.loads(request_data)
            body = data["data"]
            resp = SentimentTransformer.sentiment_process_v2(body)
            # print(data.get('data'))
            # print(resp)
            # print(json.dumps(request_data))
            return response.ok(resp,"success")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def get_healthcheck() -> JSONResponse:
        data = {
            'message': f"{config.APP_NAME} app is alive",
            "total_cpu_count": cpu_count()
        }
        return response.info(data)

    # @staticmethod
    # async def get_items(request: Request) -> JSONResponse:
    #     request_data = request.json()
    #     # body = request_data["data"]
    #     # request_data = json.loads(request_data)
    #     # print(request_data)
    #     return response.ok(request_data,"success")




