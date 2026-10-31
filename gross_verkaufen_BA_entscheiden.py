# Größ_Rücktauschkurs  B -----> A (Live-Order platzieren)

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
    import rechnung
    importlib.reload(rechnung)
    internet_test=rechnung.internet_test

if internet_test=="OK" :
    import order
    importlib.reload(order)
    internet_test=order.internet_test

#if internet_test=="OK" :
#    import rechnung_id
#    importlib.reload(rechnung_id)
#    internet_test=rechnung_id.internet_test

## Systemunterprogramme und Variablen importieren
if internet_test=="OK" :
    ### preise
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
    putzen_prozent=range.B_putzen_prozent
    z=range.B_z
    ### sparen
    A_sparen=sparen.A_sparen
    B_sparen=sparen.B_sparen
    ### rechnung
    rechnung_BA=rechnung.rechnung_BA
    scopes_schreiben=rechnung.scopes_schreiben
    sheet_id_BA=rechnung.sheet_id_BA
    sheet_range_BA=rechnung.sheet_range_BA
    json=rechnung.json
    rechnung_column_names_BA=rechnung_BA.columns
    ### order
    verkaufen_rechnung_ID=order.order['GV-BA-ID'].iloc[0]
    
    PUTZEN="P" ; KV="V" ; zeit=datetime.now()

## Zielorder ermitteln
if internet_test=="OK" :
    verkaufen_gross_filtered=rechnung_BA[(rechnung_BA['rechnung-ID']==verkaufen_rechnung_ID)]
    kaufen_gross_filtered=rechnung_BA[(rechnung_BA['rechnung-ID']==verkaufen_gross_filtered["kaufen-ID"].iloc[0])]
else :
    verkaufen_gross_filtered=pd.DataFrame()
    kaufen_gross_filtered=pd.DataFrame()

## Handelsgewinn und -verlust berechnen
if verkaufen_gross_filtered.empty or pd.isna(verkaufen_gross_filtered["rechnung-ID"].iloc[0]) or internet_test=="unterbrochen" :
    pass
else :
    verkaufen_gross_rechnung=rechnung_BA[(rechnung_BA['rechnung-ID']==verkaufen_gross_filtered['kaufen-ID'].iloc[0])]
    B_fee=B_profit=B_A_profit=0
    B_A=float(verkaufen_gross_rechnung[Apair].iloc[0])
    B_prokaufen=float(verkaufen_gross_rechnung[Bpair].iloc[0])
    B_A_fee=B_A*A_fee_prozent
    B_A_B=(B_A-B_A_fee)/preise
    B_A_B_earn=float(B_A_B-B_prokaufen)
    kaufen_ID=verkaufen_gross_filtered['kaufen-ID'].iloc[0]
    EM="E"

## Order platzieren (Live-Order platzieren)
if verkaufen_gross_filtered.empty or pd.isna(verkaufen_gross_filtered["rechnung-ID"].iloc[0]) or float(verkaufen_gross_rechnung[Bpair].iloc[0])==0 or internet_test=="unterbrochen" :
    pass
### Gewinnmitnahme
elif B_A_B_earn >=0 :
    B_prokaufen=B_A_B_zuruck=B_A_B_putzen=B_A_B_putzen_fee=B_A_B_B_putzen=0
    B_A_B_enden=float(B_A_B+B_A_B_zuruck+B_A_B_B_putzen)
    rechnung_verkaufen_neu=pd.DataFrame([[verkaufen_rechnung_ID,PUTZEN,KV,float(B_prokaufen),float(B_fee),float(B_profit),float(B_A),float(B_A_fee),float(B_A_profit),float(B_A_B),float(B_A_B_earn),float(B_A_B_zuruck),float(B_A_B_putzen),float(B_A_B_putzen_fee),float(B_A_B_B_putzen),float(B_A_B_enden),float(preise),richtung,str(z),str(zeit),kaufen_ID,EM]],columns=rechnung_column_names_BA)
### Verlustschließung
elif abs(B_A_B_earn/B_prokaufen)>=putzen_prozent :
    B_A_B_zuruck=min(abs(B_A_B_earn),B_sparen+verkaufen_gross_filtered[Bpair+'-zuruck'].iloc[0])
    #### Verlustschließung mit Token A
    if B_A_B_earn+B_A_B_zuruck >=0 :
        B_prokaufen=B_A_B_putzen=B_A_B_putzen_fee=B_A_B_B_putzen=0
        B_A_B_enden=float(B_A_B+B_A_B_zuruck+B_A_B_B_putzen)
        rechnung_verkaufen_neu=pd.DataFrame([[verkaufen_rechnung_ID,PUTZEN,KV,float(B_prokaufen),float(B_fee),float(B_profit),float(B_A),float(B_A_fee),float(B_A_profit),float(B_A_B),float(B_A_B_earn),float(B_A_B_zuruck),float(B_A_B_putzen),float(B_A_B_putzen_fee),float(B_A_B_B_putzen),float(B_A_B_enden),float(preise),richtung,str(z),str(zeit),kaufen_ID,EM]],columns=rechnung_column_names_BA)
    #### Verlustschließung mit Token A und B
    else :
        B_prokaufen=0
        B_A_B_all_putzen=((A_sparen+verkaufen_gross_filtered[Apair+'-PZ'].iloc[0])*(1-A_fee_prozent))/preise
        B_A_B_B_putzen=min(abs(B_A_B_earn+B_A_B_zuruck),B_A_B_all_putzen)
        B_A_B_putzen=B_A_B_B_putzen*preise/(1-A_fee_prozent)
        B_A_B_putzen_fee=B_A_B_putzen*A_fee_prozent
        B_A_B_enden=float(B_A_B+B_A_B_zuruck+B_A_B_B_putzen)
        rechnung_verkaufen_neu=pd.DataFrame([[verkaufen_rechnung_ID,PUTZEN,KV,float(B_prokaufen),float(B_fee),float(B_profit),float(B_A),float(B_A_fee),float(B_A_profit),float(B_A_B),float(B_A_B_earn),float(B_A_B_zuruck),float(B_A_B_putzen),float(B_A_B_putzen_fee),float(B_A_B_B_putzen),float(B_A_B_enden),float(preise),richtung,str(z),str(zeit),kaufen_ID,EM]],columns=rechnung_column_names_BA)
else :
    B_prokaufen=B_A_B_zuruck=B_A_B_putzen=B_A_B_putzen_fee=B_A_B_B_putzen=0
    B_A_B_enden=float(B_A_B+B_A_B_zuruck+B_A_B_B_putzen)
    rechnung_verkaufen_neu=pd.DataFrame([[verkaufen_rechnung_ID,PUTZEN,KV,float(B_prokaufen),float(B_fee),float(B_profit),float(B_A),float(B_A_fee),float(B_A_profit),float(B_A_B),float(B_A_B_earn),float(B_A_B_zuruck),float(B_A_B_putzen),float(B_A_B_putzen_fee),float(B_A_B_B_putzen),float(B_A_B_enden),float(preise),richtung,str(z),str(zeit),kaufen_ID,EM]],columns=rechnung_column_names_BA)
#print(B_A_B_earn,B_A_B_zuruck,B_A_B_B_putzen,B_A_B_earn+B_A_B_zuruck+B_A_B_B_putzen)

if internet_test=="OK" :
    try :
        socket.gethostbyname("google.com")
        internet_test="OK"
    except socket.gaierror :
        internet_test="unterbrochen"

## Handelsstatus 
if verkaufen_gross_filtered.empty or pd.isna(verkaufen_gross_filtered["rechnung-ID"].iloc[0]) or float(verkaufen_gross_rechnung[Bpair].iloc[0])==0 or internet_test=="unterbrochen" :
    machen="warten"
elif B_A_B_earn+B_A_B_zuruck+B_A_B_B_putzen>=0 and pd.notna(verkaufen_gross_filtered["rechnung-ID"].max()):
    machen="verkaufen"
else :
    machen="absagen"

## Order platzieren (Live-Order platzieren)
if machen=="verkaufen" :
    creds=Credentials.from_service_account_file(json, scopes=scopes_schreiben)
    service=build('sheets','v4',credentials=creds, cache_discovery=False, num_retries=5)
    rechnung=rechnung_verkaufen_neu.where(pd.notnull(rechnung_verkaufen_neu), None)
    rechnung=rechnung.astype(object).values.tolist()[0]
    try :
        request=service.spreadsheets().values().update(spreadsheetId=sheet_id_BA,range='Sheet1!A'+str(int(verkaufen_gross_filtered.index[0])+2),valueInputOption="USER_ENTERED",body={"values":[rechnung]}).execute()
        internet_test="OK"
    except HttpError as e :
        internet_test="unterbrochen"
    except Exception as e :
        internet_test="unterbrochen"
## Ursprüngliche interne Order stornieren 
elif machen=="absagen" :
    creds=Credentials.from_service_account_file(json, scopes=scopes_schreiben)
    service=build('sheets','v4',credentials=creds, cache_discovery=False, num_retries=5)
    request_body={"requests":[{"deleteDimension":{"range":{"sheetId":0,"dimension":"ROWS","startIndex":int(verkaufen_gross_filtered.index[0]+1),"endIndex":int(verkaufen_gross_filtered.index[0])+2}}}]}
    try :
        request=service.spreadsheets().batchUpdate(spreadsheetId=sheet_id_BA,body=request_body).execute()
        internet_test="OK"
    except HttpError as e :
        internet_test="unterbrochen"
    except Exception as e :
        internet_test="unterbrochen"
    if  internet_test=="OK" :
        try :
            request=service.spreadsheets().values().update(spreadsheetId=sheet_id_BA,range='Sheet1!B'+str(int(kaufen_gross_filtered.index[0])+2),valueInputOption="USER_ENTERED",body={"values":[['-']]}).execute()
            internet_test="OK"
        except HttpError as e :
            internet_test="unterbrochen"
        except Exception as e :
            internet_test="unterbrochen"

#print(machen)
#print(rechnung_verkaufen_neu)
