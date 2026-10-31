# Klein_Rücktauschkurs A -----> B (intern)

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

## Netzwerkverbindung testen
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
    import rechnung_id
    importlib.reload(rechnung_id)
    internet_test=rechnung_id.internet_test

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
    putzen_prozent=range.A_putzen_prozent
    z=range.A_z
    ### sparen
    A_sparen=sparen.A_sparen
    B_sparen=sparen.B_sparen
    ### rechnung
    rechnung_AB=rechnung.rechnung_AB
    scopes_schreiben=rechnung.scopes_schreiben
    sheet_id_AB=rechnung.sheet_id_AB
    sheet_range_AB=rechnung.sheet_range_AB
    json=rechnung.json
    rechnung_column_names_AB=rechnung_AB.columns
    ### rechnung_id
    rechnung_ID=rechnung_id.rechnung_ID_AB
    
    PUTZEN="P" ; KV="V" ; zeit=datetime.now()

## Offene Order-ID ermitteln    
if internet_test=="OK" :
    verkaufen_klein_filtered=rechnung_AB[(rechnung_AB['PUTZEN']=="-")&(rechnung_AB['K/V']=="K")]
else :
    verkaufen_klein_filtered=pd.DataFrame()
    kaufen_klein_filtered=pd.DataFrame()

## Offene Order mit den niedrigsten Kosten ermitteln
if verkaufen_klein_filtered.empty or pd.isna(verkaufen_klein_filtered["rechnung-ID"].max()) or internet_test=="unterbrochen" :
    pass
else :
    verkaufen_klein_filtered=verkaufen_klein_filtered[(verkaufen_klein_filtered[ pair+"-preise"]==max(verkaufen_klein_filtered[ pair+"-preise"]))]
    verkaufen_klein_rechnung=verkaufen_klein_filtered[(verkaufen_klein_filtered['rechnung-ID']==min(verkaufen_klein_filtered['rechnung-ID']))]
    A_fee=A_profit=A_B_profit=0
    A_B=float(verkaufen_klein_rechnung[Bpair].iloc[0])
    
    A_B_fee=A_B*B_fee_prozent
    A_B_A=(A_B-A_B_fee)/preise
    A_B_A_earn=float(A_B_A-A_prokaufen)
    kaufen_ID=float(verkaufen_klein_rechnung['rechnung-ID'].iloc[0])
    EM="M"

### Order platzieren (intern)
if verkaufen_klein_filtered.empty or pd.isna(verkaufen_klein_filtered["rechnung-ID"].max()) or internet_test=="unterbrochen" :
    pass
#### Gewinnmitnahme
elif A_B_A_earn >=0 :
    A_prokaufen=A_B_A_zuruck=A_B_A_putzen=A_B_A_putzen_fee=A_B_A_A_putzen=0
    A_B_A_enden=float(A_B_A+A_B_A_zuruck+A_B_A_A_putzen)
    rechnung_verkaufen_neu=pd.DataFrame([[rechnung_ID,PUTZEN,KV,float(A_prokaufen),float(A_fee),float(A_profit),float(A_B),float(A_B_fee),float(A_B_profit),float(A_B_A),float(A_B_A_earn),float(A_B_A_zuruck),float(A_B_A_putzen),float(A_B_A_putzen_fee),float(A_B_A_A_putzen),float(A_B_A_enden),float(preise),richtung,str(z),str(zeit),kaufen_ID,EM]],columns=rechnung_column_names_AB)
#### Verlustschließung
elif abs(A_B_A_earn/A_prokaufen)>=putzen_prozent :
    A_B_A_zuruck=min(abs(A_B_A_earn),A_sparen)
    ##### Verlustschließung mit Token A
    if A_B_A_earn+A_B_A_zuruck >=0 :
        A_prokaufen=A_B_A_putzen=A_B_A_putzen_fee=A_B_A_A_putzen=0
        A_B_A_enden=float(A_B_A+A_B_A_zuruck+A_B_A_A_putzen)
        rechnung_verkaufen_neu=pd.DataFrame([[rechnung_ID,PUTZEN,KV,float(A_prokaufen),float(A_fee),float(A_profit),float(A_B),float(A_B_fee),float(A_B_profit),float(A_B_A),float(A_B_A_earn),float(A_B_A_zuruck),float(A_B_A_putzen),float(A_B_A_putzen_fee),float(A_B_A_A_putzen),float(A_B_A_enden),float(preise),richtung,str(z),str(zeit),kaufen_ID,EM]],columns=rechnung_column_names_AB)
    ##### Verlustschließung mit Token A und B
    else :
        A_prokaufen=0
        A_B_A_all_putzen=(B_sparen-B_sparen*B_fee_prozent)/preise
        A_B_A_A_putzen=min(abs(A_B_A_earn+A_B_A_zuruck),A_B_A_all_putzen)
        A_B_A_putzen=A_B_A_A_putzen*preise/(1-B_fee_prozent)
        A_B_A_putzen_fee=A_B_A_putzen*B_fee_prozent
        A_B_A_enden=float(A_B_A+A_B_A_zuruck+A_B_A_A_putzen)
        rechnung_verkaufen_neu=pd.DataFrame([[rechnung_ID,PUTZEN,KV,float(A_prokaufen),float(A_fee),float(A_profit),float(A_B),float(A_B_fee),float(A_B_profit),float(A_B_A),float(A_B_A_earn),float(A_B_A_zuruck),float(A_B_A_putzen),float(A_B_A_putzen_fee),float(A_B_A_A_putzen),float(A_B_A_enden),float(preise),richtung,str(z),str(zeit),kaufen_ID,EM]],columns=rechnung_column_names_AB)
else :
    A_prokaufen=A_B_A_zuruck=A_B_A_putzen=A_B_A_putzen_fee=A_B_A_A_putzen=0
    A_B_A_enden=float(A_B_A+A_B_A_zuruck+A_B_A_A_putzen)
    rechnung_verkaufen_neu=pd.DataFrame([[rechnung_ID,PUTZEN,KV,float(A_prokaufen),float(A_fee),float(A_profit),float(A_B),float(A_B_fee),float(A_B_profit),float(A_B_A),float(A_B_A_earn),float(A_B_A_zuruck),float(A_B_A_putzen),float(A_B_A_putzen_fee),float(A_B_A_A_putzen),float(A_B_A_enden),float(preise),richtung,str(z),str(zeit),kaufen_ID,EM]],columns=rechnung_column_names_AB)

#print(A_B_A_earn,A_B_A_zuruck,A_B_A_A_putzen,A_B_A_earn+A_B_A_zuruck+A_B_A_A_putzen)
if internet_test=="OK" :
    try :
        socket.gethostbyname("google.com")
        internet_test="OK"
    except socket.gaierror :
        internet_test="unterbrochen"

### Handelsstatus 
if verkaufen_klein_filtered.empty or pd.isna(verkaufen_klein_filtered["rechnung-ID"].max()) or internet_test=="unterbrochen" :
    machen="warten"
elif A_B_A_earn+A_B_A_zuruck+A_B_A_A_putzen>=0 and pd.notna(verkaufen_klein_filtered["rechnung-ID"].max()) and A_B_A_A_putzen>0 :
    machen="putzen"
elif A_B_A_earn+A_B_A_zuruck+A_B_A_A_putzen>=0 and pd.notna(verkaufen_klein_filtered["rechnung-ID"].max()) :
    machen="verkaufen"
else :
    machen="warten"

### Order platzieren (intern)
if machen=="verkaufen" or machen=="putzen" :
    creds=Credentials.from_service_account_file(json, scopes=scopes_schreiben)
    service=build('sheets','v4',credentials=creds, cache_discovery=False, num_retries=5)
    rechnung=rechnung_verkaufen_neu.where(pd.notnull(rechnung_verkaufen_neu), None)
    rechnung=rechnung.astype(object).values.tolist()[0]
    try :
        request=service.spreadsheets().values().append(spreadsheetId=sheet_id_AB,range=sheet_range_AB,valueInputOption="USER_ENTERED",body={"values":[rechnung]}).execute()
        internet_test="OK"
    except HttpError as e :
        internet_test="unterbrochen"
    except Exception as e :
        internet_test="unterbrochen"
    if internet_test=="OK" :
        try :
            request=service.spreadsheets().values().update(spreadsheetId=sheet_id_AB,range='Sheet1!B'+str(int(verkaufen_klein_filtered.index[0])+2),valueInputOption="USER_ENTERED",body={"values":[['P']]}).execute()
            internet_test="OK"
        except HttpError as e :
            internet_test="unterbrochen"
        except Exception as e :
            internet_test="unterbrochen"

