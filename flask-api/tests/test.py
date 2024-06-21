import requests

# BASE = add created ip address here

response = requests.put(
    BASE + 'botFeederAddData', {'amount': 111, 'timestamp': '2017-10-11 8:32 am'})
data = response.json()
print(data)
