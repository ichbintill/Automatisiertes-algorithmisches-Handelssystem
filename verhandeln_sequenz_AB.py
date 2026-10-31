# Status interner Orders und zentrale Unterprogrammvariablen zusammenfassen

import pandas as pd
import math
from datetime import datetime
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

## Systemunterprogramme und Variablen importieren
## Netzwerkverbindung testen
import umgebung
internet_test=umgebung.internet_test
if internet_test=="OK" :
    exchange=umgebung.exchange
    Apair=umgebung.Apair ; Bpair=umgebung.Bpair ; pair=Apair+Bpair
    spread_prozent=umgebung.spread_prozent
    A_buget=umgebung.A_buget ; B_buget=umgebung.B_buget
    A_fee_prozent=umgebung.A_fee_prozent ; B_fee_prozent=umgebung.B_fee_prozent
    A_profit_prozent=umgebung.A_profit_prozent ; B_profit_prozent=umgebung.B_profit_prozent
    A_prokaufen=umgebung.A_prokaufen

if internet_test=="OK" :
    import gross_verkaufen_AB
    internet_test_gross_verkaufen_AB=gross_verkaufen_AB.internet_test
    if internet_test_gross_verkaufen_AB=="unterbrochen":
        internet_test="unterbrochen"
        gross_verkaufen_AB_machen="warten"
    elif pd.isna(gross_verkaufen_AB.verkaufen_gross_filtered['rechnung-ID'].max()) :
        gross_verkaufen_AB_rechung_id=0
        gross_verkaufen_AB_machen="warten"
    else:
        gross_verkaufen_AB_rechung_id= gross_verkaufen_AB.rechnung_verkaufen_neu['rechnung-ID'].iloc[0]
        gross_verkaufen_AB_machen=gross_verkaufen_AB.machen

if internet_test=="OK" :
    import gross_verkaufen_BA
    internet_test_gross_verkaufen_BA=gross_verkaufen_BA.internet_test
    if internet_test_gross_verkaufen_BA=="unterbrochen" :
        internet_test="unterbrochen"
        gross_verkaufen_BA_machen="warten"
    elif pd.isna(gross_verkaufen_BA.verkaufen_gross_filtered['rechnung-ID'].max()) :
        gross_verkaufen_BA_rechung_id=0
        gross_verkaufen_BA_machen="warten"
    else:
        gross_verkaufen_BA_rechung_id= gross_verkaufen_BA.rechnung_verkaufen_neu['rechnung-ID'].iloc[0]
        gross_verkaufen_BA_machen=gross_verkaufen_BA.machen
else:
    gross_verkaufen_BA_machen="warten"

if internet_test=="OK" :
    import klein_verkaufen_AB
    internet_test_klein_verkaufen_AB=klein_verkaufen_AB.internet_test
    if internet_test_klein_verkaufen_AB=="unterbrochen" :
        internet_test="unterbrochen"
        klein_verkaufen_AB_machen="warten"
    elif pd.isna(klein_verkaufen_AB.verkaufen_klein_filtered['rechnung-ID'].max()) :
        klein_verkaufen_AB_rechung_id=0
        klein_verkaufen_AB_machen="warten"
    else:
        klein_verkaufen_AB_rechung_id= klein_verkaufen_AB.rechnung_verkaufen_neu['rechnung-ID'].iloc[0]
        klein_verkaufen_AB_machen=klein_verkaufen_AB.machen
else:
    klein_verkaufen_AB_machen="warten"
     
if internet_test=="OK" :
    import klein_verkaufen_BA
    internet_test_klein_verkaufen_BA=klein_verkaufen_BA.internet_test
    if internet_test_klein_verkaufen_BA=="unterbrochen" :
        internet_test="unterbrochen"
        klein_verkaufen_BA_machen="warten"
    elif pd.isna(klein_verkaufen_BA.verkaufen_klein_filtered['rechnung-ID'].max()) :
        klein_verkaufen_BA_rechung_id=0
        klein_verkaufen_BA_machen="warten"
    else:
        klein_verkaufen_BA_rechung_id= klein_verkaufen_BA.rechnung_verkaufen_neu['rechnung-ID'].iloc[0]
        klein_verkaufen_BA_machen=klein_verkaufen_BA.machen
else:
    klein_verkaufen_BA_machen="warten"

if internet_test=="OK" :
    import kaufen_AB
    internet_test_kaufen_AB=kaufen_AB.internet_test
    if internet_test_kaufen_AB=="unterbrochen" :
        internet_test="unterbrochen"
        kaufen_AB_machen="warten"
    elif kaufen_AB.machen=="warten" :
        kaufen_AB_rechung_id=0
        kaufen_AB_machen="warten"
        Down_AB=kaufen_AB.down
        Up_AB=kaufen_AB.up
    else :
        kaufen_AB_rechung_id= kaufen_AB.rechnung_kaufen_neu['rechnung-ID'].iloc[0]
        kaufen_AB_machen=kaufen_AB.machen
        Down_AB=kaufen_AB.down
        Up_AB=kaufen_AB.up
#else:
#    kaufen_AB_machen="warten"
#    import kaufen_AB
#    Down_AB=kaufen_AB.down
#    Up_AB=kaufen_AB.up

if internet_test=="OK" :
    import kaufen_BA
    internet_test_kaufen_BA=kaufen_BA.internet_test
    if internet_test_kaufen_BA=="unterbrochen" :
        internet_test="unterbrochen"
        kaufen_BA_machen="warten"
    elif kaufen_BA.machen=="warten" :
        kaufen_BA_rechung_id=0
        kaufen_BA_machen="warten"
        Down_BA=kaufen_BA.down
        Up_BA=kaufen_BA.up
    else :
        kaufen_BA_rechung_id= kaufen_BA.rechnung_kaufen_neu['rechnung-ID'].iloc[0]
        kaufen_BA_machen=kaufen_BA.machen
        Down_BA=kaufen_BA.down
        Up_BA=kaufen_BA.up
#else:
#    kaufen_BA_machen="warten"
#    import kaufen_BA
#    Down_BA=kaufen_BA.down
#    Up_BA=kaufen_BA.up
