from fastapi.testclient import TestClient
from multiprocessing import cpu_count
from app import response, config
from app import app
#
client = TestClient(app)

def test_healtcheck():
    response = client.get("/api/v1/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"message":f"{config.APP_NAME} app is alive", "total_cpu_count":cpu_count()}

def test_sentiment():
    body = {"data": [{"txt":"Alo xin lỗi cho em hỏi phải số mấy chị cung không ạ", "lang": "vi","id":1},{"txt":"Selamat sore dengan Pak Budianto","lang": "id","id":2}]}
    response = client.post("/api/v1/sentiment", json=body)

    sentiment_resp = {
        "result": [
            {
                "id": 1,
                "txt": "Alo xin lỗi cho em hỏi phải số mấy chị cung không ạ",
                "language_code": "vi",
                "neg": 0.49998750031249223,
                "neu": 0.69230236690487,
                "pos": 0.49998750031249223
            },
            {
                "id": 2,
                "txt": "Selamat sore dengan Pak Budianto",
                "language_code": "id",
                "neg": 0.9999000099990001,
                "neu": 0.7999840003199936,
                "pos": 0.0
            }
        ],
        "message": "success"
    }
    assert response.status_code == 200
    assert response.json() == sentiment_resp