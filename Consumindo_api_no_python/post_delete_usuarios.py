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


'''#logout - Para deletar um usuario, não pode fazer logout...
endpoint_logout = URL + '/logout'
body_logout = {
    'login': 'Guiteste',
    'senha': 'abc2'
}

headers_logout = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token['acess_token']
}

resposta_logout = requests.request('POST', endpoint_logout, json=body_logout, headers=headers_logout)
print('Logout efetivado!','Status Code:', resposta_logout.status_code)
print(resposta_logout)
#print(resposta_logout.json())'''

#Delete usuario
endpoint_delete_user = URL + '/usuarios/2'
body_delete_user = {
    'login': 'Guiteste',
    'senha': 'abc2'
}

headers_delete_user = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token['acess_token']
}

resposta_delete_user = requests.request('DELETE', endpoint_delete_user, json=body_delete_user, headers=headers_delete_user)
print(resposta_delete_user.status_code)
print(resposta_delete_user.json())



