# Fernabschaltung

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

## google link
scopes_lesen=['https://www.googleapis.com/auth/spreadsheets.readonly']     
sheet_id_tachometer=''         # sheet_id
sheet_range_tachometer='Sheet1!A1'                                         # sheet_range
json='.json'                                        # Link vom google_sheet.json

## Netzwerkverbindung testen
try :
    socket.gethostbyname("google.com")
    internet_test="OK"
except socket.gaierror :
    internet_test="unterbrochen"

## einlesen Google Sheets
if internet_test=="OK" :
    #lesen_tachometer
    try :
        creds=Credentials.from_service_account_file(json, scopes=scopes_lesen)
        service=build('sheets','v4',credentials=creds, cache_discovery=False, num_retries=5)
        sheet=service.spreadsheets()
        result=sheet.values().get(spreadsheetId=sheet_id_tachometer, range=sheet_range_tachometer).execute()
        values=result.get('values', [])
        schalter=values[0][0]  
        internet_test="OK"
    except HttpError as e :
        internet_test="unterbrochen"
    except Exception as e :
        internet_test="unterbrochen"
