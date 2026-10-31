# Größ_Rücktauschkurs  B -----> A (intern)

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
    ### rechnung_id
    rechnung_ID=rechnung_id.rechnung_ID_BA
    
    PUTZEN="P" ; KV="V" ; zeit=datetime.now()

## Offene Order-ID ermitteln
if internet_test=="OK" :
    verkaufen_gross_filtered=rechnung_BA[(rechnung_BA['PUTZEN']=="-")&(rechnung_BA['K/V']=="K")]
else :
    verkaufen_gross_filtered=pd.DataFrame()

## Offene Order mit den höchsten Kosten ermitteln
if verkaufen_gross_filtered.empty or pd.isna(verkaufen_gross_filtered["rechnung-ID"].max()) or internet_test=="unterbrochen" :
    pass
else :
    verkaufen_gross_filtered=verkaufen_gross_filtered[verkaufen_gross_filtered[ pair+"-preise"]==min(verkaufen_gross_filtered[ pair+"-preise"])]
    verkaufen_gross_rechnung=verkaufen_gross_filtered[(verkaufen_gross_filtered['rechnung-ID']==min(verkaufen_gross_filtered['rechnung-ID']))]
    B_fee=B_profit=B_A_profit=0
    B_A=float(verkaufen_gross_rechnung[Apair].iloc[0])
    B_prokaufen=float(verkaufen_gross_rechnung[Bpair].iloc[0])
    B_A_fee=B_A*A_fee_prozent
    B_A_B=(B_A-B_A_fee)/preise
    B_A_B_earn=float(B_A_B-B_prokaufen)
    kaufen_ID=float(verkaufen_gross_rechnung['rechnung-ID'].iloc[0])
    EM="M"

### Order platzieren (intern)
if verkaufen_gross_filtered.empty or pd.isna(verkaufen_gross_filtered["rechnung-ID"].max()) or float(verkaufen_gross_rechnung[Bpair].iloc[0])==0 or internet_test=="unterbrochen" :
    pass
#### Gewinnmitnahme
elif B_A_B_earn >=0 :
    B_prokaufen=B_A_B_zuruck=B_A_B_putzen=B_A_B_putzen_fee=B_A_B_B_putzen=0
    B_A_B_enden=float(B_A_B+B_A_B_zuruck+B_A_B_B_putzen)
    rechnung_verkaufen_neu=pd.DataFrame([[rechnung_ID,PUTZEN,KV,float(B_prokaufen),float(B_fee),float(B_profit),float(B_A),float(B_A_fee),float(B_A_profit),float(B_A_B),float(B_A_B_earn),float(B_A_B_zuruck),float(B_A_B_putzen),float(B_A_B_putzen_fee),float(B_A_B_B_putzen),float(B_A_B_enden),float(preise),richtung,str(z),str(zeit),kaufen_ID,EM]],columns=rechnung_column_names_BA)
#### Verlustschließung
elif abs(B_A_B_earn/B_prokaufen)>=putzen_prozent :
    B_A_B_zuruck=min(abs(B_A_B_earn),B_sparen)
    ##### Verlustschließung mit Token B
    if B_A_B_earn+B_A_B_zuruck >=0 :
        B_prokaufen=B_A_B_putzen=B_A_B_putzen_fee=B_A_B_B_putzen=0
        B_A_B_enden=float(B_A_B+B_A_B_zuruck+B_A_B_B_putzen)
        rechnung_verkaufen_neu=pd.DataFrame([[rechnung_ID,PUTZEN,KV,float(B_prokaufen),float(B_fee),float(B_profit),float(B_A),float(B_A_fee),float(B_A_profit),float(B_A_B),float(B_A_B_earn),float(B_A_B_zuruck),float(B_A_B_putzen),float(B_A_B_putzen_fee),float(B_A_B_B_putzen),float(B_A_B_enden),float(preise),richtung,str(z),str(zeit),kaufen_ID,EM]],columns=rechnung_column_names_BA)
    ##### Verlustschließung mit Token B und A
    else :
        B_prokaufen=0
        B_A_B_all_putzen=(A_sparen-A_sparen*A_fee_prozent)/preise
        B_A_B_B_putzen=min(abs(B_A_B_earn+B_A_B_zuruck),B_A_B_all_putzen)
        B_A_B_putzen=B_A_B_B_putzen*preise/(1-A_fee_prozent)
        B_A_B_putzen_fee=B_A_B_putzen*A_fee_prozent
        B_A_B_enden=float(B_A_B+B_A_B_zuruck+B_A_B_B_putzen)
        rechnung_verkaufen_neu=pd.DataFrame([[rechnung_ID,PUTZEN,KV,float(B_prokaufen),float(B_fee),float(B_profit),float(B_A),float(B_A_fee),float(B_A_profit),float(B_A_B),float(B_A_B_earn),float(B_A_B_zuruck),float(B_A_B_putzen),float(B_A_B_putzen_fee),float(B_A_B_B_putzen),float(B_A_B_enden),float(preise),richtung,str(z),str(zeit),kaufen_ID,EM]],columns=rechnung_column_names_BA)
else :
    B_prokaufen=B_A_B_zuruck=B_A_B_putzen=B_A_B_putzen_fee=B_A_B_B_putzen=0
    B_A_B_enden=float(B_A_B+B_A_B_zuruck+B_A_B_B_putzen)
    rechnung_verkaufen_neu=pd.DataFrame([[rechnung_ID,PUTZEN,KV,float(B_prokaufen),float(B_fee),float(B_profit),float(B_A),float(B_A_fee),float(B_A_profit),float(B_A_B),float(B_A_B_earn),float(B_A_B_zuruck),float(B_A_B_putzen),float(B_A_B_putzen_fee),float(B_A_B_B_putzen),float(B_A_B_enden),float(preise),richtung,str(z),str(zeit),kaufen_ID,EM]],columns=rechnung_column_names_BA)

if internet_test=="OK" :
    try :
        socket.gethostbyname("google.com")
        internet_test="OK"
    except socket.gaierror :
        internet_test="unterbrochen"

### Handelsstatus 
if verkaufen_gross_filtered.empty or pd.isna(verkaufen_gross_filtered["rechnung-ID"].max()) or float(verkaufen_gross_rechnung[Bpair].iloc[0])==0 or internet_test=="unterbrochen" :
    machen="warten"
elif B_A_B_earn+B_A_B_zuruck+B_A_B_B_putzen>=0 and pd.notna(verkaufen_gross_filtered["rechnung-ID"].max()) and B_A_B_B_putzen>0 :
    machen="putzen"
elif B_A_B_earn+B_A_B_zuruck+B_A_B_B_putzen>=0 and pd.notna(verkaufen_gross_filtered["rechnung-ID"].max()) :
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
        request = service.spreadsheets().values().append(spreadsheetId=sheet_id_BA,range=sheet_range_BA,valueInputOption="USER_ENTERED",body={"values":[rechnung]}).execute()
        internet_test="OK"
    except HttpError as e :
        internet_test="unterbrochen"
    except Exception as e :
        internet_test="unterbrochen"
    if internet_test=="OK" :
        try :
            request = service.spreadsheets().values().update(spreadsheetId=sheet_id_BA,range='Sheet1!B'+str(int(verkaufen_gross_filtered.index[0])+2),valueInputOption="USER_ENTERED",body={"values":[['P']]}).execute()
            internet_test="OK"
        except HttpError as e :
            internet_test="unterbrochen"
        except Exception as e :
            internet_test="unterbrochen"

