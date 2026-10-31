# Handels-ID generieren

import pandas as pd
import math
from datetime import datetime
import importlib

## Netzwerkverbindung testen
import umgebung
internet_test=umgebung.internet_test

if internet_test=="OK" :
    import rechnung
    internet_test=rechnung.internet_test

## Systemunterprogramme und Variablen importieren
if internet_test=="OK" :
    #umgebung
    exchange=umgebung.exchange
    Apair=umgebung.Apair ; Bpair=umgebung.Bpair ; pair=Apair+Bpair
    spread_prozent=umgebung.spread_prozent
    A_buget=umgebung.A_buget ; B_buget=umgebung.B_buget
    A_zuruck_prozent=umgebung.A_zuruck_prozent ; B_zuruck_prozent=umgebung.B_zuruck_prozent
    A_putzen_prozent=umgebung.A_putzen_prozent ; B_putzen_prozent=umgebung.B_putzen_prozent
    A_fee_prozent=umgebung.A_fee_prozent ; B_fee_prozent=umgebung.B_fee_prozent
    A_profit_prozent=umgebung.A_profit_prozent ; B_profit_prozent=umgebung.B_profit_prozent
    A_prokaufen=umgebung.A_prokaufen ; B_prokaufen=umgebung.B_prokaufen
    #rechnung
    rechnung_AB=rechnung.rechnung_AB
    rechnung_BA=rechnung.rechnung_BA

# Handels-ID generieren
if internet_test=="OK" :
    # rechnung-ID  A----->B
    if pd.isna(rechnung_AB["rechnung-ID"].max()) :
        rechnung_ID_AB=1
    else :
        rechnung_ID_AB=rechnung_AB["rechnung-ID"].max()+1
    PUTZEN="P" ; KV="V" ; zeit=datetime.now()
    # rechnung-ID  B----->A
    if pd.isna(rechnung_BA["rechnung-ID"].max()) :
        rechnung_ID_BA=1
    else :
        rechnung_ID_BA=rechnung_BA["rechnung-ID"].max()+1
        
#print(rechnung_ID_AB,rechnung_ID_BA)
