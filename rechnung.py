# Historische Handelsdaten einlesen (Google Sheets)

import pandas as pd
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

### umgebung

import umgebung
internet_test= umgebung.internet_test
if internet_test=="OK" :
    exchange=umgebung.exchange
    Apair=umgebung.Apair ; Bpair=umgebung.Bpair ; pair=Apair+Bpair
    spread_prozent=umgebung.spread_prozent
    A_buget=umgebung.A_buget ; B_buget=umgebung.B_buget
    A_fee_prozent=umgebung.A_fee_prozent ; B_fee_prozent=umgebung.B_fee_prozent
    A_profit_prozent=umgebung.A_profit_prozent ; B_profit_prozent=umgebung.B_profit_prozent
    A_prokaufen=umgebung.A_prokaufen ; B_prokaufen=umgebung.B_prokaufen

### google link
scopes_schreiben=['https://www.googleapis.com/auth/spreadsheets']
scopes_lesen=['https://www.googleapis.com/auth/spreadsheets.readonly']

sheet_id_AB='1ijogqYh7Fr9TAsm_sBJ3DiVp78F4iWTgGATOEGR5jtI'                 # sheet_id
sheet_id_BA='1MdbieD-ERzC0vouKCyFxGYaIs42v7xJE132hZqX5reA'                 # sheet_id
# sheet_id_tachometer='1ttLnVhqSVZI4URvsiXKxrMeQy_wyD8MgN3muFVv0otM'

sheet_range_AB='Sheet1'                                                    # sheet_range
sheet_range_BA='Sheet1'                                                    # sheet_range
# sheet_range_tachometer='Sheet1!A2'                                       # sheet_range

json='./rcallput-7922e8a588bd.json'                                        # Link vom google_sheet.json

## Netzwerkverbindung testen 
if internet_test=="OK" :
    try:
        socket.gethostbyname("google.com")
        internet_test="OK"
    except socket.gaierror :
        internet_test="unterbrochen"
else:
    internet_test="unterbrochen"

## Historische Handelsdaten einlesen (Google Sheets)
if internet_test=="OK" :
    ### lesen_rechnung_AB
    try :
        creds = Credentials.from_service_account_file(json, scopes=scopes_lesen)
        service= build('sheets','v4',credentials=creds, cache_discovery=False, num_retries=5)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id_AB, range=sheet_range_AB).execute()
        values = result.get('values', [])
        rechnung_AB = pd.DataFrame(values[1:], columns=values[0])  # 第一行作為列名
        columns_to_float=["rechnung-ID", Apair, Apair+"-Fee", Apair+"-Tax",Bpair, Bpair+"-Fee", Bpair+"-Tax", Apair+".1", Apair+"-eran", Apair+"-zuruck",Bpair+"-PZ", Bpair+"-PZ_Fee",Apair+"-PZ", "END-"+Apair, pair+"-preise","Z","kaufen-ID"]
        rechnung_AB[columns_to_float] = rechnung_AB[columns_to_float].apply(pd.to_numeric, errors='coerce')
        internet_test="OK"
    except HttpError as e :
        internet_test="unterbrochen"
    except Exception as e :
        internet_test="unterbrochen"
    #print(rechnung_AB)

## Historische Handelsdaten einlesen (Google Sheets)
if internet_test=="OK" :
    ### lesen_rechnung_BA
    try :
        creds = Credentials.from_service_account_file(json, scopes=scopes_lesen)
        service= build('sheets','v4',credentials=creds, cache_discovery=False, num_retries=5)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id_BA, range=sheet_range_BA).execute()
        values = result.get('values', [])
        rechnung_BA = pd.DataFrame(values[1:], columns=values[0])  # 第一行作為列名
        columns_to_float=["rechnung-ID", Bpair, Bpair+"-Fee", Bpair+"-Tax",Apair, Apair+"-Fee", Apair+"-Tax", Bpair+".1", Bpair+"-eran", Bpair+"-zuruck",Apair+"-PZ", Apair+"-PZ_Fee",Bpair+"-PZ", "END-"+Bpair, pair+"-preise","Z","kaufen-ID"]
        rechnung_BA[columns_to_float] = rechnung_BA[columns_to_float].apply(pd.to_numeric, errors='coerce')
        internet_test="OK"
    except HttpError as e :
        internet_test="unterbrochen"
    except Exception as e :
        internet_test="unterbrochen"
    #print(rechnung_BA)

