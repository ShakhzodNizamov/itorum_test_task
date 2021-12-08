import base64
import requests
from requests.auth import HTTPBasicAuth

usrPass = "admin:1".encode('ascii')
base64_bytes = base64.b64encode(usrPass)
base64_message = base64_bytes.decode('ascii')
# b64Val = base64.b64encode(usrPass)
print()
json_data = '''
[
    {
        client_id: 3,
        date: '07.12.2021',
        sum: 210
    },
    {
        client_id: 2,
        date: '02.12.2021',
        sum: 210
    },
    {
        client_id: 1,
        date: '08.12.2021',
        sum: 210
    },
]
'''
URL = 'http://127.0.0.1:8000/export/'
headers = {
    # "Authorization": f"Basic {base64_message}",
    "Content-Type":"application/json",
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}

r = requests.post(URL, auth=HTTPBasicAuth('admin', '1'),
                  data=json_data,
                  headers=headers)

print(r.status_code)
# print(r.text)