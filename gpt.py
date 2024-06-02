import requests
idcm = "bt1vpbph6bfjm2f4d2ue" #id-дообученной модели
IAM =  "AQVN3uisVvr7XhoXVLyvk90b8HFUp9wkGcB9i0WO" #значение IAM-токена сервисного аккаунта.
folderId = "b1g72uajlds114mlufqi" #идентификаторкаталога
def generate_message(query):
    req = {
            "modelUri": f"ds://{idcm}", #подключение к дообученной модели yandexgpt на датасете
            "completionOptions": {
                "stream": False,
                "temperature": 0.1,
                "maxTokens": "2000"
            },
            "messages": [
                {
                "role": "user",
                "text": query
                }
            ]
    }
    headers = {"Authorization" : "Api-Key " + IAM,
            "x-folder-id": folderId, }
    response = requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
        headers=headers, json=req)
    if response.status_code == 200:
        return response.text
    return "bad request"