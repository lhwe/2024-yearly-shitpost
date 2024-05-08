import requests

url = 'http://127.0.0.1:80/api/ban'

data = {
    "username": input('Username > '),
    "reason": input('Reason > ')
}

test = requests.post(url, json=data) 
if test.status_code == 200 or test.status_code == 201:
    formatted = test.json()["message"]
else:
    formatted = test.json()["error"]

print(formatted)