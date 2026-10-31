#  Bedingungen festlegen

import requests
import json
from datetime import datetime
import socket

## Systemstartdatum 
anfangen_zeit=datetime(2025,5,5)

## API und Exchange
exchange="MEXC"
exchange_link="https://api.mexc.com/api/v3/klines?symbol="
exchange_api="https://api.mexc.com/api/v3/ticker/price?symbol="
kosten_api="https://api.mexc.com/api/v3/exchangeInfo"

## Handelseinstellungen
### Handelspaar
Apair="EURI" ; Bpair="USDT"
### Gewinneinstellungen
A_profit_prozent=0.025/100 ; B_profit_prozent=0.025/100
### Anfangsbestand
A_buget=1500 ; B_buget=1500
### Handelsbetrag pro Trade
A_prokaufen=1 ; B_prokaufen=1
### Verlustbegrenzung und Positionsschließung
A_zuruck_prozent=0.025/100 ; B_zuruck_prozent=0.025/100
A_putzen_prozent=0.05/100 ; B_putzen_prozent=0.05/100
### Slippage-Einstellungen
spread_prozent=0.05/100
### Standardabweichungsbereichs-Einstellungen
A_ausreiss_z=1.25 ; B_ausreiss_z=1.25

## Netzwerkverbindung testen
try:
    socket.gethostbyname("google.com")
    internet_test="OK"
except socket.gaierror:
    internet_test="unterbrochen"

## API-Gebühren abfragen
if internet_test=="OK" :
    response=requests.get(kosten_api,params={"symbol": Apair + Bpair},timeout=15)
    kosten_data=response.json()
    for data in kosten_data.get("symbols",[]):
        if data["symbol"]==Apair+Bpair:
            A_fee_prozent=B_fee_prozent=float(data['takerCommission'])
            break




