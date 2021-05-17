import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + 'all_transaction_history/4')
data = response.json()
print(data)
