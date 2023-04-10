import config
import requests

uri = config.APP_SERVER + '/rasatext'

data = {
    "username":"ali",
    "text":"hello"
}

result = requests.post(url=uri, json=data)
print(result.json())