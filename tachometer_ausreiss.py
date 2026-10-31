# Hauptprogramm

from datetime import datetime
import pandas as pd
import importlib
import time
import hmac
import hashlib
import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import socket

## Netzwerkverbindung testen
import umgebung
internet_test=umgebung.internet_test
if internet_test=="OK" :
    import taktik
    internet_test=taktik.internet_test

## Systemunterprogramme und Variablen importieren
if internet_test=="OK" :
    ### umgebung
    Apair=umgebung.Apair
    Bpair=umgebung.Bpair
    A_buget=umgebung.A_buget
    B_buget=umgebung.B_buget
    anfangen_zeit=umgebung.anfangen_zeit
    zeit=datetime.today()
    if zeit-anfangen_zeit==0 :
        jahre=1/365
    else :
        jahre=(zeit-anfangen_zeit).days/365
    ### taktik
    Down_AB=taktik.Down_AB
    Up_AB=taktik.Up_AB
    Down_BA=taktik.Down_BA
    Up_BA=taktik.Up_BA
    taktik_machen=taktik.taktik
    taktik_machen=pd.DataFrame(taktik_machen[1:], columns=taktik_machen[0])
    machen_gross_verkaufen_AB=taktik_machen["GV-AB"].iloc[0]
    machen_gross_verkaufen_BA=taktik_machen["GV-BA"].iloc[0]
    machen_klein_verkaufen_AB=taktik_machen["KV-AB"].iloc[0]
    machen_klein_verkaufen_BA=taktik_machen["KV-BA"].iloc[0]
    machen_kaufen_AB=taktik_machen["K-AB"].iloc[0]
    machen_kaufen_BA=taktik_machen["K-BA"].iloc[0]

## Netzwerkverbindung testen und Systemunterprogramme und Variablen importieren
if  internet_test=="OK" :
    if taktik_machen["GV-AB-ENT"].iloc[0]=="E" :
        import gross_verkaufen_AB_entscheiden
        internet_test=gross_verkaufen_AB_entscheiden.internet_test
        if internet_test=="OK" :
            machen_gross_verkaufen_AB=gross_verkaufen_AB_entscheiden.machen
    
    if taktik_machen["GV-BA-ENT"].iloc[0]=="E" :
        import gross_verkaufen_BA_entscheiden
        internet_test=gross_verkaufen_BA_entscheiden.internet_test
        if internet_test=="OK" :
            machen_gross_verkaufen_BA=gross_verkaufen_BA_entscheiden.machen
    
    if taktik_machen["KV-AB-ENT"].iloc[0]=="E" :
        import klein_verkaufen_AB_entscheiden
        internet_test=klein_verkaufen_AB_entscheiden.internet_test
        if internet_test=="OK" :
            machen_klein_verkaufen_AB=klein_verkaufen_AB_entscheiden.machen
    
    if taktik_machen["KV-BA-ENT"].iloc[0]=="E" :
        import klein_verkaufen_BA_entscheiden
        internet_test=klein_verkaufen_BA_entscheiden.internet_test
        if internet_test=="OK" :
            machen_klein_verkaufen_BA=klein_verkaufen_BA_entscheiden.machen
    
    if taktik_machen["K-AB-ENT"].iloc[0]=="E" :
        import kaufen_AB_entscheiden
        internet_test=kaufen_AB_entscheiden.internet_test
        if  internet_test=="OK" :
            machen_kaufen_AB=kaufen_AB_entscheiden.machen
            Down_AB=kaufen_AB_entscheiden.down
            Up_AB=kaufen_AB_entscheiden.up
    
    if taktik_machen["K-BA-ENT"].iloc[0]=="E" :
        import kaufen_BA_entscheiden
        internet_test=kaufen_BA_entscheiden.internet_test
        if internet_test=="OK" :
            machen_kaufen_BA=kaufen_BA_entscheiden.machen
            Down_BA=kaufen_BA_entscheiden.down
            Up_BA=kaufen_BA_entscheiden.up    
else :
    pass

## Echtzeitdaten aktualisieren
if internet_test=="OK" :
    import rechnung
    importlib.reload(rechnung)
    internet_test=rechnung.internet_test

if internet_test=="OK" :
    import range
    importlib.reload(range)
    internet_test=range.internet_test

if internet_test=="OK" :
    import preise
    importlib.reload(preise)
    internet_test=preise.internet_test

if internet_test=="OK" :
    import sparen
    importlib.reload(sparen)
    internet_test=sparen.internet_test

## google link
scopes_schreiben=['https://www.googleapis.com/auth/spreadsheets']

sheet_id_tachometer=''          # sheet_id

sheet_range_tachometer='Sheet1!A2'                                          # sheet_range

json='.json'                                         # Link vom google_sheet.json

## Handelsstatus und Bestandsgewinn/-verlust zusammenfassen
if internet_test=="OK" :
    ### rechnung
    rechnung_AB=rechnung.rechnung_AB
    A_Buget=float(rechnung_AB.loc[(rechnung_AB['PUTZEN']=="-")&(rechnung_AB['K/V']=="K"),Apair].sum())
    A_Buget_proz=f"{A_Buget/A_buget*100:.2f}%"
    rechnung_BA=rechnung.rechnung_BA
    B_Buget=float(rechnung_BA.loc[(rechnung_BA['PUTZEN']=="-")&(rechnung_BA['K/V']=="K"),Bpair].sum())
    B_Buget_proz=f"{B_Buget/B_buget*100:.2f}%"
    A_Profit_proz=f"{(float(sum(rechnung_AB[Apair+'-Tax']))+float(sum(rechnung_BA[Apair+'-Tax']))+float(rechnung_BA[rechnung_BA['E/M']=='M'][Apair+'-Fee'].sum()))/A_buget:.2f}%"
    A_Profit_Jproz=f"{(float(sum(rechnung_AB[Apair+'-Tax']))+float(sum(rechnung_BA[Apair+'-Tax']))+float(rechnung_BA[rechnung_BA['E/M']=='M'][Apair+'-Fee'].sum()))/A_buget/jahre*100:.2f}%"
    B_Profit_proz=f"{(float(sum(rechnung_AB[Bpair+'-Tax']))+float(sum(rechnung_BA[Bpair+'-Tax']))+float(rechnung_AB[rechnung_AB['E/M']=='M'][Bpair+'-Fee'].sum()))/B_buget:.2f}%"
    B_Profit_Jproz=f"{(float(sum(rechnung_AB[Bpair+'-Tax']))+float(sum(rechnung_BA[Bpair+'-Tax']))+float(rechnung_AB[rechnung_AB['E/M']=='M'][Bpair+'-Fee'].sum()))/B_buget/jahre*100:.2f}%"
    ### range
    A_richtung=range.A_richtung
    B_richtung=range.B_richtung
    A_z=range.A_z
    B_z=range.B_z
    ### preise
    preise_AB=preise.preise_AB
    preise_BA=preise.preise_BA
    ### sparen
    A_sparen=sparen.A_sparen
    A_sparen_proz=f"{float(A_sparen/A_buget)*100:.2f}%"
    B_sparen=sparen.B_sparen
    B_sparen_proz=f"{float(B_sparen/B_buget)*100:.2f}%"
    
    print(Apair+"<---------->"+Bpair,datetime.now())
    Tachometer_column_names=["A<->B", "Sparen","Sparen(%)", "Buget", "Buget(%)","Profit(%)", "Profit(J%)", "Kaufen","G-Verkaufen", "K-Verkaufen","Down","Preise","Up","richtung","z"]
    Tachometer=pd.DataFrame(
        [
            [ 
                Apair, A_sparen, A_sparen_proz, A_Buget, A_Buget_proz, A_Profit_proz, A_Profit_Jproz, machen_kaufen_AB, machen_gross_verkaufen_AB, machen_klein_verkaufen_AB, Down_AB, preise_AB, Up_AB, A_richtung, A_z
            ],
            [ 
                Bpair, B_sparen, B_sparen_proz, B_Buget, B_Buget_proz, B_Profit_proz, B_Profit_Jproz, machen_kaufen_BA, machen_gross_verkaufen_BA, machen_klein_verkaufen_BA, Down_BA, preise_BA, Up_BA, B_richtung, B_z
            ]
        ]
        ,columns=Tachometer_column_names)
    print(Tachometer)

## Handelsstatus und Bestandsgewinn/-verlust hochladen
if  internet_test=="OK" :
    try :
        socket.gethostbyname("google.com")
        internet_test="OK"
    except socket.gaierror :
        internet_test="unterbrochen"
if  internet_test=="OK" :
    try :
        creds = Credentials.from_service_account_file(json, scopes=scopes_schreiben)
        service= build('sheets','v4',credentials=creds, cache_discovery=False, num_retries=5)
        Tachometer = [Tachometer.columns.tolist()]+Tachometer.values.tolist()
        request = service.spreadsheets().values().update(spreadsheetId=sheet_id_tachometer,range=sheet_range_tachometer,valueInputOption="USER_ENTERED",body={"values":Tachometer}).execute()
    except HttpError as e :
        internet_test="unterbrochen"
    except Exception as e :
        internet_test="unterbrochen"

