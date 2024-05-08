import requests

url = 'http://127.0.0.1:80/api/check_ban'

data = {
    "username": input('Username > ')
}

test = requests.post(url, json=data) 
if test.status_code == 200:
    formatted = test.json()["ban_message"]
else:
    formatted = test.json()["error"]

print(formatted)