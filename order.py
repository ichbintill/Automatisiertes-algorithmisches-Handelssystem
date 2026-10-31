# Handelsentscheidungen herunterladen

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

sheet_id_tachometer=''                 # sheet_id

sheet_range_order='order!A2:R3'                                                    # sheet_range 

json='.json'                                                # Link vom google_sheet.json

## Netzwerkverbindung testen 
try :
    socket.gethostbyname("google.com")
    internet_test="OK"
except socket.gaierror :
    internet_test="unterbrochen"

## Handelsentscheidungen herunterladen
if internet_test=="OK" :
    try :
        creds=Credentials.from_service_account_file(json, scopes=scopes_lesen)
        service=build('sheets','v4',credentials=creds, cache_discovery=False, num_retries=5)
        sheet=service.spreadsheets()
        result=sheet.values().get(spreadsheetId=sheet_id_tachometer, range=sheet_range_order).execute()
        values=result.get('values', [])
        order= pd.DataFrame(values[1:], columns=values[0])  
        columns_to_float=["GV-AB-ID", "GV-BA-ID", "KV-AB-ID", "KV-BA-ID","K-AB-ID", "K-BA-ID"]
        order[columns_to_float] = order[columns_to_float].apply(pd.to_numeric, errors='coerce')
        internet_test="OK"
    except HttpError as e :
        internet_test="unterbrochen"
    except Exception as e :
        internet_test="unterbrochen"
