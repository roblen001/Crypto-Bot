import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + 'news/all/4')
data = response.json()
print(data)
