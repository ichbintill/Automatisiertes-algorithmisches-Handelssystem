#  Markt-Preisdaten herunterladen

import requests
import json
import socket

## Systemunterprogramm
import umgebung
### umgebung
exchange_api=umgebung.exchange_api
Apair=umgebung.Apair
Bpair=umgebung.Bpair
pair=Apair+Bpair

## Netzwerkverbindung testen und API-Markt-Preisdaten
try :
    socket.gethostbyname("google.com")
    #API
    price_api=exchange_api+pair
    response=requests.get(price_api)
    response.raise_for_status()
    internet_test="OK"
except socket.gaierror :
    internet_test="unterbrochen"
except requests.exceptions.RequestException as e :
    internet_test="unterbrochen"

## API-Markt-Preisdaten
if internet_test=="OK" :
    if response.status_code==200 :
        data=response.json()
        preise_AB=float(data['price'])
        preise_BA=float(1/float(data['price']))
        #print(preise_AB)
    else :
        print("Error")

