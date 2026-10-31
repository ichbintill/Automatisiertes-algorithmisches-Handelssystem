# Wash-Trading vermeiden und die Reihenfolge der Handelsstrategien festlegen

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

## google link
scopes_schreiben=['https://www.googleapis.com/auth/spreadsheets']                      
scopes_lesen=['https://www.googleapis.com/auth/spreadsheets.readonly']            
sheet_id_tachometer='1ttLnVhqSVZI4URvsiXKxrMeQy_wyD8MgN3muFVv0otM'                 # sheet_id

sheet_range_Taktik='Taktik!A2:L326'                                                # sheet_range
sheet_range_order='order!A2:R3'                                                    # sheet_range

json='./rcallput-7922e8a588bd.json'                                                # Link vom google_sheet.json

## Netzwerkverbindung testen
try :
    socket.gethostbyname("google.com")
    internet_test="OK"
except socket.gaierror :
    internet_test="unterbrochen"

## Handelsentscheidungstabelle einlesen (ob eine Order an der Börse platziert werden muss)
if internet_test=="OK" :
    try :
        creds=Credentials.from_service_account_file(json, scopes=scopes_lesen)
        service=build('sheets','v4',credentials=creds)
        sheet=service.spreadsheets()
        result=sheet.values().get(spreadsheetId=sheet_id_tachometer, range=sheet_range_Taktik).execute()
        values=result.get('values', [])
        taktik=pd.DataFrame(values[1:], columns=values[0])  
    except HttpError as e :
        internet_test="unterbrochen"
    except Exception as e :
        internet_test="unterbrochen"
        
## Systemunterprogramme und Variablen importieren
if internet_test=="OK" :
    import umgebung
    internet_test=umgebung.internet_test

if internet_test=="OK" :
    import range
    importlib.reload(range)
    internet_test=range.internet_test
    
if internet_test=="OK" :
    #umgebung
    exchange=umgebung.exchange
    Apair=umgebung.Apair ; Bpair=umgebung.Bpair ; pair=Apair+Bpair
    spread_prozent=umgebung.spread_prozent
    A_buget=umgebung.A_buget ; B_buget=umgebung.B_buget
    A_fee_prozent=umgebung.A_fee_prozent ; B_fee_prozent=umgebung.B_fee_prozent
    A_profit_prozent=umgebung.A_profit_prozent ; B_profit_prozent=umgebung.B_profit_prozent
    A_prokaufen=umgebung.A_prokaufen
    #range
    richtung=range.A_richtung
    range_ausreiss_data=range.range_ausreiss_data_AB
    andern=range_ausreiss_data.iloc[len(range_ausreiss_data)-1]['andern']

if internet_test=="OK" :
    if richtung=="fallen" :
        import verhandeln_sequenz_AB
        internet_test=verhandeln_sequenz_AB.internet_test
        if internet_test=="OK" :
            gross_verkaufen_AB_machen=verhandeln_sequenz_AB.gross_verkaufen_AB_machen
            gross_verkaufen_BA_machen=verhandeln_sequenz_AB.gross_verkaufen_BA_machen
            klein_verkaufen_AB_machen=verhandeln_sequenz_AB.klein_verkaufen_AB_machen
            klein_verkaufen_BA_machen=verhandeln_sequenz_AB.klein_verkaufen_BA_machen
            kaufen_AB_machen=verhandeln_sequenz_AB.kaufen_AB_machen
            kaufen_BA_machen=verhandeln_sequenz_AB.kaufen_BA_machen
            gross_verkaufen_AB_rechung_id=verhandeln_sequenz_AB.gross_verkaufen_AB_rechung_id
            gross_verkaufen_BA_rechung_id=verhandeln_sequenz_AB.gross_verkaufen_BA_rechung_id
            klein_verkaufen_AB_rechung_id=verhandeln_sequenz_AB.klein_verkaufen_AB_rechung_id
            klein_verkaufen_BA_rechung_id=verhandeln_sequenz_AB.klein_verkaufen_BA_rechung_id
            kaufen_AB_rechung_id=verhandeln_sequenz_AB.kaufen_AB_rechung_id
            kaufen_BA_rechung_id=verhandeln_sequenz_AB.kaufen_BA_rechung_id
            Down_AB=verhandeln_sequenz_AB.Down_AB
            Up_AB=verhandeln_sequenz_AB.Up_AB
            Down_BA=verhandeln_sequenz_AB.Down_BA
            Up_BA=verhandeln_sequenz_AB.Up_BA
    elif richtung=="eben" and andern>0 :
        import verhandeln_sequenz_AB
        internet_test=verhandeln_sequenz_AB.internet_test
        if internet_test=="OK" :
            gross_verkaufen_AB_machen=verhandeln_sequenz_AB.gross_verkaufen_AB_machen
            gross_verkaufen_BA_machen=verhandeln_sequenz_AB.gross_verkaufen_BA_machen
            klein_verkaufen_AB_machen=verhandeln_sequenz_AB.klein_verkaufen_AB_machen
            klein_verkaufen_BA_machen=verhandeln_sequenz_AB.klein_verkaufen_BA_machen
            kaufen_AB_machen=verhandeln_sequenz_AB.kaufen_AB_machen
            kaufen_BA_machen=verhandeln_sequenz_AB.kaufen_BA_machen
            gross_verkaufen_AB_rechung_id=verhandeln_sequenz_AB.gross_verkaufen_AB_rechung_id
            gross_verkaufen_BA_rechung_id=verhandeln_sequenz_AB.gross_verkaufen_BA_rechung_id
            klein_verkaufen_AB_rechung_id=verhandeln_sequenz_AB.klein_verkaufen_AB_rechung_id
            klein_verkaufen_BA_rechung_id=verhandeln_sequenz_AB.klein_verkaufen_BA_rechung_id
            kaufen_AB_rechung_id=verhandeln_sequenz_AB.kaufen_AB_rechung_id
            kaufen_BA_rechung_id=verhandeln_sequenz_AB.kaufen_BA_rechung_id
            Down_AB=verhandeln_sequenz_AB.Down_AB
            Up_AB=verhandeln_sequenz_AB.Up_AB
            Down_BA=verhandeln_sequenz_AB.Down_BA
            Up_BA=verhandeln_sequenz_AB.Up_BA
    else :
        import verhandeln_sequenz_BA
        internet_test=verhandeln_sequenz_BA.internet_test
        if internet_test=="OK" :
            gross_verkaufen_AB_machen=verhandeln_sequenz_BA.gross_verkaufen_AB_machen
            gross_verkaufen_BA_machen=verhandeln_sequenz_BA.gross_verkaufen_BA_machen
            klein_verkaufen_AB_machen=verhandeln_sequenz_BA.klein_verkaufen_AB_machen
            klein_verkaufen_BA_machen=verhandeln_sequenz_BA.klein_verkaufen_BA_machen
            kaufen_AB_machen=verhandeln_sequenz_BA.kaufen_AB_machen
            kaufen_BA_machen=verhandeln_sequenz_BA.kaufen_BA_machen
            gross_verkaufen_AB_rechung_id=verhandeln_sequenz_BA.gross_verkaufen_AB_rechung_id
            gross_verkaufen_BA_rechung_id=verhandeln_sequenz_BA.gross_verkaufen_BA_rechung_id
            klein_verkaufen_AB_rechung_id=verhandeln_sequenz_BA.klein_verkaufen_AB_rechung_id
            klein_verkaufen_BA_rechung_id=verhandeln_sequenz_BA.klein_verkaufen_BA_rechung_id
            kaufen_AB_rechung_id=verhandeln_sequenz_BA.kaufen_AB_rechung_id
            kaufen_BA_rechung_id=verhandeln_sequenz_BA.kaufen_BA_rechung_id
            Down_AB=verhandeln_sequenz_BA.Down_AB
            Up_AB=verhandeln_sequenz_BA.Up_AB
            Down_BA=verhandeln_sequenz_BA.Down_BA
            Up_BA=verhandeln_sequenz_BA.Up_BA

## Handelsentscheidungen hochladen
if internet_test=="OK" :
    taktik=taktik[(taktik['GV-AB']==gross_verkaufen_AB_machen)]
    taktik=taktik[(taktik['GV-BA']==gross_verkaufen_BA_machen)]
    taktik=taktik[(taktik['KV-AB']==klein_verkaufen_AB_machen)]
    taktik=taktik[(taktik['KV-BA']==klein_verkaufen_BA_machen)]
    taktik=taktik[(taktik['K-AB']==kaufen_AB_machen)]
    taktik=taktik[(taktik['K-BA']==kaufen_BA_machen)]
    taktik.insert(0,'GV-AB-ID',gross_verkaufen_AB_rechung_id)
    taktik.insert(1,'GV-BA-ID',gross_verkaufen_BA_rechung_id)
    taktik.insert(2,'KV-AB-ID',klein_verkaufen_AB_rechung_id)
    taktik.insert(3,'KV-BA-ID',klein_verkaufen_BA_rechung_id)
    taktik.insert(4,'K-AB-ID',kaufen_AB_rechung_id)
    taktik.insert(5,'K-BA-ID',kaufen_BA_rechung_id)
    try :
        creds=Credentials.from_service_account_file(json, scopes=scopes_schreiben)
        service=build('sheets','v4',credentials=creds, cache_discovery=False, num_retries=5)
        taktik=[taktik.columns.tolist()]+taktik.values.tolist()
        request=service.spreadsheets().values().update(spreadsheetId=sheet_id_tachometer,range=sheet_range_order,valueInputOption="USER_ENTERED",body={"values":taktik}).execute()
        internet_test="OK"
    except HttpError as e :
        internet_test="unterbrochen"
    except Exception as e :
        internet_test="unterbrochen"

