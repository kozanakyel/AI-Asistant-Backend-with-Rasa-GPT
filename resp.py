import requests

url: str = 'http://0.0.0.0:5005/webhooks/rest/webhook'

data = {
    "sender": 1,
    "message": "i want to buy a pizza"
}

result = requests.post(url=url, json=data)
print(result.json()[0]['text'])
