from fastapi import APIRouter,Body
from app.controllers.SentimentController import SentimentController as controller
from typing import List
from pydantic import BaseModel

router = APIRouter()

class Data(BaseModel):
    txt: str
    lang: str
    id:int

class Item(BaseModel):
    data: List[Data] = None



# @router.post("/items/", tags=["items"])
# async def create_item(item: Item):
#     return await controller.get_items(item)

@router.get("/healthcheck")
async def get_info():
    return await controller.get_healthcheck()


@router.post("/sentiment", response_model=Item)
async def sentiment_value(item: Item = Body(default=None, example={
    "data": [
        {
            "txt": "Alo xin lỗi cho em hỏi phải số mấy chị cung không ạ",
            "lang": "vi",
            "id":1
        },
        {
            "txt": "Selamat sore dengan Pak Budianto",
            "lang": "id",
            "id":2
        }
    ]
})):
    return await controller.get_sentiment(item)



