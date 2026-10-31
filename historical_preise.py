# Historische Preisdaten

from datetime import datetime
import requests
import json
import pandas as pd
import socket

## Systemunterprogramm
import umgebung
### umgebung
exchange=umgebung.exchange
exchange_link=umgebung.exchange_link
Apair=umgebung.Apair
Bpair=umgebung.Bpair
pair=Apair+Bpair
interval="1d"        #1m  5m  15m 30m  1h  4h  1d  1w
limit=365

## Netzwerkverbindung testen und API-Historische Preisdaten
try :
    socket.gethostbyname("google.com")
    # API
    mexc_historical_preise_api=exchange_link+pair+"&interval="+interval+"&limit="+str(limit)
    response=requests.get(mexc_historical_preise_api)
    response.raise_for_status()
    internet_test="OK"
except socket.gaierror :
    internet_test="unterbrochen"
except requests.exceptions.RequestException as e :
    internet_test="unterbrochen"

## Erstellung historischer Daten und API-Historische Preisdaten
if internet_test=="OK" :
    # historical_preise_AB
    historical_preise_AB=[]
    if response.status_code==200 :
        data=response.json()
        for item in data :
            timestamp=datetime.utcfromtimestamp(int(item[0])/1000).date()
            open_price=float(item[1])
            high_price=float(item[2])
            low_price=float(item[3])
            close_price=float(item[4])
            volume=float(item[5])
            historical_preise_AB.append([timestamp,open_price,high_price,low_price,close_price,volume])   
        historical_preise_AB_formular= pd.DataFrame(historical_preise_AB,columns=["data","open","high","low","close","volume"])
        historical_preise_AB_formular=historical_preise_AB_formular.sort_values(by="data",ascending=False)
    else:
        print(response.status_code)
    
    # historical_preise_BA
    historical_preise_BA=[]
    if response.status_code==200 :
        data=response.json()
        for item in data:
            timestamp=datetime.utcfromtimestamp(int(item[0])/1000).date()
            open_price=1/float(item[1])
            high_price=1/float(item[2])
            low_price=1/float(item[3])
            close_price=1/float(item[4])
            volume=float(item[5])
            historical_preise_BA.append([timestamp,open_price,high_price,low_price,close_price,volume])   
        historical_preise_BA_formular= pd.DataFrame(historical_preise_BA,columns=["data","open","high","low","close","volume"])
        historical_preise_BA_formular=historical_preise_BA_formular.sort_values(by="data",ascending=False)
    else:
        print(response.status_code)

