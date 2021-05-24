import requests

BASE = "http://127.0.0.1:5000/"

response = requests.put(
    BASE + 'botFeederAddData', {'amount': 111, 'timestamp': '2017-10-11 8:32 am'})
data = response.json()
print(data)
