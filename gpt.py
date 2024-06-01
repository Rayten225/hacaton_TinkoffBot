import requests
def generate_message(query):
    req = {
            "modelUri": "gpt://b1g72uajlds114mlufqi/yandexgpt/latest",
            # "modelUri": "ds://bt1aij3mg7k5iflurk8n",
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
    headers = {"Authorization" : "Api-Key " + 'AQVN3uisVvr7XhoXVLyvk90b8HFUp9wkGcB9i0WO',
            "x-folder-id": "b1g72uajlds114mlufqi", }
    response = requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
        headers=headers, json=req)
    if response.status_code == 200:
        return response.text
    return "Bad request"
