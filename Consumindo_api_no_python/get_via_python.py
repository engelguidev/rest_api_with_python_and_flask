import json
import requests

hotel = input('Digiete o nome do hotel: ')

#Get /hoteis
URL = 'http://127.0.0.1:5000'
resposta_hoteis = requests.request('GET', URL + f'/hoteis/{hotel}')
print(resposta_hoteis)
print(resposta_hoteis.json())
seleciona_hotel = list(resposta_hoteis.json())
print(resposta_hoteis)
for hotel in resposta_hoteis:
    print(hotel)



