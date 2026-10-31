# Währungswechsel B -----> A (Live-Order platzieren)

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

## Echtzeitdaten aktualisieren und Netzwerkverbindung testen
import preise
importlib.reload(preise)
internet_test=preise.internet_test

if internet_test=="OK":
    import umgebung
    internet_test=umgebung.internet_test

if internet_test=="OK":
    import range
    importlib.reload(range)
    internet_test=range.internet_test

if internet_test=="OK":
    import sparen
    importlib.reload(sparen)
    internet_test=sparen.internet_test

if internet_test=="OK":
    import order
    importlib.reload(order)
    internet_test=order.internet_test
    
if internet_test=="OK":
    import rechnung
    importlib.reload(rechnung)
    internet_test=rechnung.internet_test

#if internet_test=="OK":
#    import rechnung_id
#    importlib.reload(rechnung_id)
#    internet_test=rechnung_id.internet_test

## Systemunterprogramme und Variablen importieren
if internet_test=="OK":
    ### preise
    B_prokaufen=float(preise.preise_AB)
    preise=float(preise.preise_BA)
    ### umgebung
    exchange=umgebung.exchange
    Apair=umgebung.Apair ; Bpair=umgebung.Bpair ; pair=Apair+Bpair
    spread_prozent=umgebung.spread_prozent
    A_buget=umgebung.A_buget ; B_buget=umgebung.B_buget
    A_fee_prozent=umgebung.A_fee_prozent ; B_fee_prozent=umgebung.B_fee_prozent
    A_profit_prozent=umgebung.A_profit_prozent ; B_profit_prozent=umgebung.B_profit_prozent
    A_prokaufen=umgebung.A_prokaufen
    ### range
    richtung=range.B_richtung
    sparen_proz=abs(range.B_sparen_prozent)
    std=range.B_std
    average_z=range.B_average_z
    mean=range.B_mean
    ausreiss_z=range.B_ausreiss_z
    z=range.B_z
    ### sparen
    A_sparen=sparen.A_sparen
    B_sparen=sparen.B_sparen
    A_sparen_proz=A_sparen/A_buget
    B_sparen_proz=B_sparen/B_buget
    ### order
    kaufen_rechnung_ID=order.order['K-BA-ID'].iloc[0]

if internet_test=="OK":
    ### richtung
    if B_sparen_proz>=sparen_proz :
        if richtung=="eben":
            up=mean+std*average_z
            down=mean-std*average_z
        elif richtung=="fallen":
            up=mean
            down=mean-ausreiss_z*std
        else :
            up=mean+ausreiss_z*std
            down=mean-ausreiss_z*std
    elif  internet_test=="OK":
        if richtung=="eben":
            up=mean+ausreiss_z*std
            down=mean-ausreiss_z*std
        elif richtung=="fallen":
            up=mean
            down=mean-ausreiss_z*std
        else :
            up=mean+1*std
            down=mean-ausreiss_z*std
    ### Verbleibendes Investitionsbudget 
    if  kaufen_rechnung_ID>0:
        #rechnung
        rechnung_BA=rechnung.rechnung_BA
        scopes_schreiben=rechnung.scopes_schreiben
        sheet_id_BA=rechnung.sheet_id_BA
        sheet_range_BA=rechnung.sheet_range_BA
        json=rechnung.json
        rechnung_column_names_BA=rechnung_BA.columns
        kaufen_filtered=rechnung_BA[(rechnung_BA['rechnung-ID']==kaufen_rechnung_ID)]
        # buget
        if float(rechnung_BA.loc[(rechnung_BA['PUTZEN']=="-")&(rechnung_BA['K/V']=="K"),Bpair].sum())/B_buget <1 and internet_test=="OK":
            B_buget_prozent="OK"
        else:
            B_buget_prozent="-"

    ### Order erstellen (Live-Order platzieren)        
    if preise>=down and preise<up :
        # kaufen_rechnen
        ## kaufen rechnung_neu
        PUTZEN="-"
        KV="K"
        B_fee=float(B_prokaufen*B_fee_prozent)
        B_profit=float(B_prokaufen*B_profit_prozent)
        B_A=float((B_prokaufen-B_fee-B_profit)*preise)
        B_A_fee=B_A_profit=B_A_B=B_A_B_earn=B_A_B_zuruck=B_A_B_putzen=B_A_B_putzen_fee=B_A_B_B_putzen=B_A_B_enden=0
        zeit=datetime.now()
        kaufen_ID=kaufen_rechnung_ID
        EM="E"
        
        rechnung_kaufen_neu=pd.DataFrame([[kaufen_rechnung_ID,PUTZEN,KV,float(B_prokaufen),float(B_fee),float(B_profit),float(B_A),float(B_A_fee),float(B_A_profit),float(B_A_B),float(B_A_B_earn),float(B_A_B_zuruck),float(B_A_B_putzen),float(B_A_B_putzen_fee),float(B_A_B_B_putzen),float(B_A_B_enden),float(preise),richtung,str(z),str(zeit),kaufen_ID,EM]],columns=rechnung_column_names_BA)

if internet_test=="OK":
    try:
        socket.gethostbyname("google.com")
        internet_test="OK"
    except socket.gaierror:
        internet_test="unterbrochen"

## Handelsstatus 
if internet_test=="unterbrochen":
    machen="warten"
elif preise>=down and preise<up and B_buget_prozent=="OK":
    machen="einkaufen"
else:
    machen="absagen"

## Order platzieren (Live-Order platzieren)
if machen=="einkaufen":
    creds = Credentials.from_service_account_file(json, scopes=scopes_schreiben)
    service= build('sheets','v4',credentials=creds, cache_discovery=False, num_retries=5)
    rechnung = rechnung_kaufen_neu.where(pd.notnull(rechnung_kaufen_neu), None)
    rechnung = rechnung.astype(object).values.tolist()[0]
    try :
        request = service.spreadsheets().values().update(spreadsheetId=sheet_id_BA,range='Sheet1!A'+str(int(kaufen_filtered.index[0])+2),valueInputOption="USER_ENTERED",body={"values":[rechnung]}).execute()
        internet_test="OK"
    except HttpError as e:
        internet_test="unterbrochen"
    except Exception as e:
        internet_test="unterbrochen"
## Ursprüngliche interne Order stornieren 
elif machen=="absagen":
    creds = Credentials.from_service_account_file(json, scopes=scopes_schreiben)
    service= build('sheets','v4',credentials=creds, cache_discovery=False, num_retries=5)
    request_body={"requests":[{"deleteDimension":{"range":{"sheetId":0,"dimension":"ROWS","startIndex":int(kaufen_filtered.index[0]+1),"endIndex":int(kaufen_filtered.index[0])+2}}}]}
    try :
        request = service.spreadsheets().batchUpdate(spreadsheetId=sheet_id_BA,body=request_body).execute()
        internet_test="OK"
    except HttpError as e:
        internet_test="unterbrochen"
    except Exception as e:
        internet_test="unterbrochen"
    
#print(machen)
#print(rechnung_kaufen_neu)
#print('kaufen_BA_ausreiss')
