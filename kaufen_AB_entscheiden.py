# Währungswechsel A -----> B (Live-Order platzieren)

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

if internet_test=="OK" :
    import umgebung
    internet_test=umgebung.internet_test

if internet_test=="OK" :
    import range
    importlib.reload(range)
    internet_test=range.internet_test

if internet_test=="OK" :
    import sparen
    importlib.reload(sparen)
    internet_test=sparen.internet_test

if internet_test=="OK" :
    import order
    importlib.reload(order)
    internet_test=order.internet_test

if internet_test=="OK" :
    import rechnung
    importlib.reload(rechnung)
    internet_test=rechnung.internet_test

#if internet_test=="OK" :
#    import rechnung_id
#    importlib.reload(rechnung_id)
#    internet_test=rechnung_id.internet_test

## Systemunterprogramme und Variablen importieren
if internet_test=="OK" :
    ### preise
    preise=float(preise.preise_AB)
    ### umgebung
    exchange=umgebung.exchange
    Apair=umgebung.Apair ; Bpair=umgebung.Bpair ; pair=Apair+Bpair
    spread_prozent=umgebung.spread_prozent
    A_buget=umgebung.A_buget ; B_buget=umgebung.B_buget
    A_fee_prozent=umgebung.A_fee_prozent ; B_fee_prozent=umgebung.B_fee_prozent
    A_profit_prozent=umgebung.A_profit_prozent ; B_profit_prozent=umgebung.B_profit_prozent
    A_prokaufen=umgebung.A_prokaufen ; B_prokaufen=umgebung.B_prokaufen
    
    ### range
    richtung=range.A_richtung
    sparen_proz=abs(range.A_sparen_prozent)
    std=range.A_std
    average_z=range.A_average_z
    mean=range.A_mean
    ausreiss_z=range.A_ausreiss_z
    z=range.A_z
    ### sparen
    A_sparen=sparen.A_sparen
    B_sparen=sparen.B_sparen
    A_sparen_proz=A_sparen/A_buget
    B_sparen_proz=B_sparen/B_buget
    ### order
    kaufen_rechnung_ID=order.order['K-AB-ID'].iloc[0]


if internet_test=="OK" :
    ### richtung
    if A_sparen_proz>=sparen_proz :
        if richtung=="eben":
            up=mean+std*average_z
            down=mean-std*average_z
        elif richtung=="fallen":
            up=mean
            down=mean-ausreiss_z*std
        else :
            up=mean+ausreiss_z*std
            down=mean-ausreiss_z*std
    elif internet_test=="OK":
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
    if  kaufen_rechnung_ID>0 :
        ### rechnung
        rechnung_AB=rechnung.rechnung_AB
        scopes_schreiben=rechnung.scopes_schreiben
        sheet_id_AB=rechnung.sheet_id_AB
        sheet_range_AB=rechnung.sheet_range_AB
        json=rechnung.json
        rechnung_column_names_AB=rechnung_AB.columns
        kaufen_filtered=rechnung_AB[(rechnung_AB['rechnung-ID']==kaufen_rechnung_ID)]
        ### buget
        if float(rechnung_AB.loc[(rechnung_AB['PUTZEN']=="-")&(rechnung_AB['K/V']=="K"),Apair].sum())/A_buget <1 and internet_test=="OK" :
            A_buget_prozent="OK"
        else:
            A_buget_prozent="-"

    ### Order erstellen (Live-Order platzieren)   
    if preise>=down and preise<=up :
        # kaufen_rechnen
        ## kaufen rechnung_neu
        PUTZEN="-"
        KV="K"
        A_fee=float(A_prokaufen*A_fee_prozent)
        A_profit=float(A_prokaufen*A_profit_prozent)
        A_B=float((A_prokaufen-A_fee-A_profit)*preise)
        A_B_fee=A_B_profit=A_B_A=A_B_A_earn=A_B_A_zuruck=A_B_A_putzen=A_B_A_putzen_fee=A_B_A_A_putzen=A_B_A_enden=0
        zeit=datetime.now()
        kaufen_ID=kaufen_rechnung_ID
        EM="E"
        
        rechnung_kaufen_neu=pd.DataFrame([[kaufen_rechnung_ID,PUTZEN,KV,float(A_prokaufen),float(A_fee),float(A_profit),float(A_B),float(A_B_fee),float(A_B_profit),float(A_B_A),float(A_B_A_earn),float(A_B_A_zuruck),float(A_B_A_putzen),float(A_B_A_putzen_fee),float(A_B_A_A_putzen),float(A_B_A_enden),float(preise),richtung,str(z),str(zeit),kaufen_ID,EM]],columns=rechnung_column_names_AB)

if internet_test=="OK" :
    try :
        socket.gethostbyname("google.com")
        internet_test="OK"
    except socket.gaierror :
        internet_test="unterbrochen"

## Handelsstatus    
if internet_test=="unterbrochen" :
    machen="warten"
elif preise>=down and preise<=up and A_buget_prozent=="OK" :
    machen="einkaufen"
else:
    machen="absagen"

## Order platzieren (Live-Order platzieren)
if machen=="einkaufen" :
    creds=Credentials.from_service_account_file(json, scopes=scopes_schreiben)
    service=build('sheets','v4',credentials=creds, cache_discovery=False, num_retries=5)
    rechnung=rechnung_kaufen_neu.where(pd.notnull(rechnung_kaufen_neu), None)
    rechnung=rechnung.astype(object).values.tolist()[0]
    try :
        request=service.spreadsheets().values().update(spreadsheetId=sheet_id_AB,range='Sheet1!A'+str(int(kaufen_filtered.index[0])+2),valueInputOption="USER_ENTERED",body={"values":[rechnung]}).execute()
        internet_test="OK"
    except HttpError as e :
        internet_test="unterbrochen"
    except Exception as e :
        internet_test="unterbrochen"
## Ursprüngliche interne Order stornieren 
elif machen=="absagen" :
    creds = Credentials.from_service_account_file(json, scopes=scopes_schreiben)
    service= build('sheets','v4',credentials=creds, cache_discovery=False, num_retries=5)
    request_body={"requests":[{"deleteDimension":{"range":{"sheetId":0,"dimension":"ROWS","startIndex":int(kaufen_filtered.index[0]+1),"endIndex":int(kaufen_filtered.index[0])+2}}}]}
    try :
        request = service.spreadsheets().batchUpdate(spreadsheetId=sheet_id_AB,body=request_body).execute()
        internet_test="OK"
    except HttpError as e :
        internet_test="unterbrochen"
    except Exception as e :
        internet_test="unterbrochen"   

#print(machen)
#print(rechnung_kaufen_neu)
#print('kaufen_AB_ausreiss')
