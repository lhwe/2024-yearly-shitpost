import requests

url = 'http://127.0.0.1:80/api/login'

data = {
    "username": input('Username > '),
    "password": input('Password > ')
}

test = requests.post(url, json=data) 
if test.status_code == 200:
    formatted = test.json()["message"]
else:
    formatted = test.json()["error"]

print(formatted)