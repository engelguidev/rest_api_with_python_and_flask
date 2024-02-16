import requests
import json

URL = 'http://127.0.0.1:5000'

#Login
endpoint_login = URL + '/login'
body_login = {
    'login': 'Guiteste',
    'senha': 'abc2'
}

headers_login = {
    'Content-Type': 'application/json'
}

resposta_login = requests.request('POST', endpoint_login, json=body_login, headers=headers_login)
print('Login efetivado!','Status Code:', resposta_login.status_code)
token = resposta_login.json()
token['acess_token']
print(token)

#Put hotel
endpoint_hotel_id = URL + '/hoteis/meuhotel2'

body_hotel_id = {
   "nome": "Balalaika Hotel",
   "estrelas": 2,
   "diaria": 230,
   "cidade": "São Paulo",
   "site_id": 2
}

headers_hotel_id = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token['acess_token']
}
resposta_hotel_id = requests.request('PUT', endpoint_hotel_id, json=body_hotel_id, headers=headers_hotel_id)
print(resposta_hotel_id)
print(resposta_hotel_id.json())


