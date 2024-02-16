import requests

URL = 'http://127.0.0.1:5000'
#Criando Cadastro
endpoint_cadastro = URL + '/cadastro'
print(endpoint_cadastro)
body_cadastro = {
    'login': 'Guiteste',
    'senha': 'abc2'
}
headers_cadastro = {
    'Content-Type': 'application/json'
}
resposta_cadastro = requests.request('POST', endpoint_cadastro, json=body_cadastro, headers=headers_cadastro)
print(f'Cadastro efetivado!', 'Status Code:', resposta_cadastro.status_code)
print(resposta_cadastro.json())

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

#Post hotel
endpoint_hotel_id = URL + '/hoteis/meuhotel'

body_hotel_id = {
   "nome": "Meu Hotel",
   "estrelas": 4,
   "diaria": 230,
   "cidade": "Carapicuiba",
   "site_id": 2
}
headers_hotel_id = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token['acess_token']
}
resposta_hotel_id = requests.request('POST', endpoint_hotel_id, json=body_hotel_id, headers=headers_hotel_id)
print(resposta_hotel_id)
print(resposta_hotel_id.json())


