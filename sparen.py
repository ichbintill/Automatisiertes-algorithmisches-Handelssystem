# Überschussgewinnreserve

import pandas as pd
import math
import importlib
import os
import time
import hmac
import hashlib
import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import socket

##  Netzwerkverbindung testen
import umgebung
internet_test=umgebung.internet_test

if internet_test=="OK" :
    import preise
    importlib.reload(preise)
    internet_test=preise.internet_test

if internet_test=="OK" :
    import rechnung
    importlib.reload(rechnung)
    internet_test=rechnung.internet_test

## Systemunterprogramme und Variablen importieren
   
if internet_test=="OK" :
    ### umgebung
    exchange=umgebung.exchange
    Apair=umgebung.Apair ; Bpair=umgebung.Bpair ; pair=Apair+Bpair
    spread_prozent=umgebung.spread_prozent
    A_buget=umgebung.A_buget ; B_buget=umgebung.B_buget
    A_zuruck_prozent=umgebung.A_zuruck_prozent ; B_zuruck_prozent=umgebung.B_zuruck_prozent
    A_putzen_prozent=umgebung.A_putzen_prozent ; B_putzen_prozent=umgebung.B_putzen_prozent
    A_fee_prozent=umgebung.A_fee_prozent ; B_fee_prozent=umgebung.B_fee_prozent
    A_profit_prozent=umgebung.A_profit_prozent ; B_profit_prozent=umgebung.B_profit_prozent
    A_prokaufen=umgebung.A_prokaufen ; B_prokaufen=umgebung.B_prokaufen
    ### preise
    preise=float(preise.preise_AB)
    ### rechnung
    rechnung_AB=rechnung.rechnung_AB
    rechnung_BA=rechnung.rechnung_BA


## sparen
if  internet_test=="OK" :
    BA_A_sparen=-1*float(sum(rechnung_BA[Apair+'-PZ']))+float(rechnung_BA[rechnung_BA['E/M']=='M'][Apair+'-PZ_Fee'].sum())
    BA_B_sparen=float(sum(rechnung_BA[Bpair+'-eran'])+sum(rechnung_BA[Bpair+'-PZ'])+rechnung_BA[rechnung_BA['E/M']=='M'][Bpair+'-Fee'].sum())
    AB_A_sparen=float(sum(rechnung_AB[Apair+'-eran'])+sum(rechnung_AB[Apair+'-PZ'])+rechnung_AB[rechnung_AB['E/M']=='M'][Apair+'-Fee'].sum())
    AB_B_sparen=-1*float(sum(rechnung_AB[Bpair+'-PZ']))+float(rechnung_AB[rechnung_AB['E/M']=='M'][Bpair+'-PZ_Fee'].sum())
    A_sparen=AB_A_sparen+BA_A_sparen
    B_sparen=AB_B_sparen+BA_B_sparen
#print(A)
#print(A_sparen,B_sparen)
