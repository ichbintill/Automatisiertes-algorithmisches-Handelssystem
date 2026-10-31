# Standardabweichung und Ausreißergrenzen berechnen

import numpy as np
import pandas as pd
from datetime import datetime

# A_ausreiss_z=1.25 ; B_ausreiss_z=1.25

## Netzwerkverbindung testen
import historical_preise
internet_test=historical_preise.internet_test

if internet_test=="OK" :
    import umgebung
    internet_test=umgebung.internet_test
  
if internet_test=="OK" :
    import preise
    internet_test=preise.internet_test

## Systemunterprogramme und Variablen importieren
if internet_test=="OK" :
    ### umgebung
    A_putzen_prozent_max=umgebung.B_fee_prozent+umgebung.A_fee_prozent+umgebung.A_profit_prozent
    B_putzen_prozent_max=umgebung.A_fee_prozent+umgebung.B_fee_prozent+umgebung.B_profit_prozent
    A_ausreiss_z=umgebung.A_ausreiss_z
    B_ausreiss_z=umgebung.B_ausreiss_z
    heute_datum= datetime.today().date()
    ### preise
    preise_AB=preise.preise_AB
    preise_BA=preise.preise_BA


## Standardabweichung
if internet_test=="OK" :
    ### range_AB
    #### Nicht benötigte Spalten entfernen
    histprocal_AB_data=historical_preise.historical_preise_AB_formular.drop(columns=["open","high","low","volume"])
    histprocal_AB_data=histprocal_AB_data.sort_values(by="data",ascending=True)
    #### Aktuelle Tageskurse aktualisieren
    if heute_datum==histprocal_AB_data.iloc[len(histprocal_AB_data)-1]['data'] :
        heute_preise_AB={'data':heute_datum,'close':preise_AB}
        histprocal_AB_data[len(histprocal_AB_data)]=heute_preise_AB
    else :
        pass
    #### Liquidations-Referenztabelle erstellen
    preise=histprocal_AB_data["close"]
    datum=histprocal_AB_data["data"]
    row=len(histprocal_AB_data)
    range_ausreiss_data_AB=[]
    t=0
    for i in range(0,row) :
        data=datum[i]
        close=preise[i]
        preise_data=preise[0+t:i+1]
        mean=np.mean(preise_data)
        andern=close/preise[t]-1
        if i==0 :
            std=0
            z=0
            andern=0
        else :
            std=np.std(preise_data,ddof=1)
            if pd.isna(std) or std==0 :
                std=0
                z=0
            else :
                z=abs((close-mean)/std)
        
        if z >= A_ausreiss_z :
            ausreiss="J"
            t=i
        else :
            ausreiss="N"
        
        if ausreiss=="J" or andern==0 :
            richtung="eben"
        elif andern >0 :
            richtung="fallen"
        else :
            richtung="steigen"
        range_row=[data,close,mean,std,z,ausreiss,andern,richtung]
        range_ausreiss_data_AB.append(range_row)
    range_ausreiss_data_AB=pd.DataFrame(range_ausreiss_data_AB,columns=["data","close","mean","std","z","ausreiss","andern","richtung"])

    #### Verlustbegrenzung und Positionsschließung
    A_sparen_prozent=range_ausreiss_data_AB.iloc[t]['andern']
    A_std=range_ausreiss_data_AB.iloc[len(histprocal_AB_data)-1]['std']
    A_z=range_ausreiss_data_AB.iloc[len(histprocal_AB_data)-1]['z']
    A_average_z=range_ausreiss_data_AB[range_ausreiss_data_AB['ausreiss']=='J']['z'].mean()
    A_richtung=range_ausreiss_data_AB.iloc[len(histprocal_AB_data)-1]['richtung']
    A_mean=range_ausreiss_data_AB.iloc[len(histprocal_AB_data)-1]['mean']
    if range_ausreiss_data_AB.iloc[len(histprocal_AB_data)-1]['ausreiss']=="J" :
        A_putzen_prozent=max(abs(range_ausreiss_data_AB.iloc[len(histprocal_AB_data)-1]['andern']),A_putzen_prozent_max)
    elif range_ausreiss_data_AB.iloc[len(histprocal_AB_data)-2]['ausreiss']=="J" :
        A_putzen_prozent=max(abs(range_ausreiss_data_AB.iloc[len(histprocal_AB_data)-1]['andern']),A_putzen_prozent_max)
    else :
        A_putzen_prozent=min(abs((A_mean-A_ausreiss_z*A_std)/range_ausreiss_data_AB.iloc[t]['close']-1),abs((A_mean+A_ausreiss_z*A_std)/range_ausreiss_data_AB.iloc[t]['close']-1))+A_putzen_prozent_max
    #print(range_ausreiss_data_AB)
    
    ### range_BA
    #### Nicht benötigte Spalten entfernen
    histprocal_BA_data=historical_preise.historical_preise_BA_formular.drop(columns=["open","high","low","volume"])
    histprocal_BA_data=histprocal_BA_data.sort_values(by="data",ascending=True)
    #### Aktuelle Tageskurse aktualisieren
    if heute_datum==histprocal_BA_data.iloc[len(histprocal_BA_data)-1]['data'] :
        heute_preise_BA={'data':heute_datum,'close':preise_BA}
        histprocal_BA_data[len(histprocal_BA_data)]=heute_preise_BA
    else :
        pass
    #### Liquidations-Referenztabelle erstellen
    preise=histprocal_BA_data["close"]
    datum=histprocal_BA_data["data"]
    row=len(histprocal_BA_data)
    range_ausreiss_data_BA=[]
    t=0
    for i in range(0,row) :
        data=datum[i]
        close=preise[i]
        preise_data=preise[0+t:i+1]
        mean=np.mean(preise_data)
        andern=close/preise[t]-1
        if i==0 :
            std=0
            z=0
            andern=0
        else :
            std=np.std(preise_data,ddof=1)
            if pd.isna(std) or std==0 :
                std=0
                z=0
            else :
                z=abs((close-mean)/std)
        
        if z >= B_ausreiss_z :
            ausreiss="J"
            t=i
        else :
            ausreiss="N"
        
        if ausreiss=="J" or andern==0 :
            richtung="eben"
        elif andern >0 :
            richtung="fallen"
        else :
            richtung="steigen"
        
        range_row=[data,close,mean,std,z,ausreiss,andern,richtung]
        range_ausreiss_data_BA.append(range_row)
    range_ausreiss_data_BA=pd.DataFrame(range_ausreiss_data_BA,columns=["data","close","mean","std","z","ausreiss","andern","richtung"])
    
    #### Verlustbegrenzung und Positionsschließung
    B_sparen_prozent=range_ausreiss_data_BA.iloc[t]['andern']
    B_std=range_ausreiss_data_BA.iloc[len(histprocal_BA_data)-1]['std']
    B_z=range_ausreiss_data_BA.iloc[len(histprocal_BA_data)-1]['z']
    B_average_z=range_ausreiss_data_BA[range_ausreiss_data_BA['ausreiss']=='J']['z'].mean()
    B_richtung=range_ausreiss_data_BA.iloc[len(histprocal_BA_data)-1]['richtung']
    B_mean=range_ausreiss_data_BA.iloc[len(histprocal_BA_data)-1]['mean']
    if range_ausreiss_data_BA.iloc[len(histprocal_BA_data)-1]['ausreiss']=="J" :
        B_putzen_prozent=max(abs(range_ausreiss_data_BA.iloc[len(histprocal_BA_data)-1]['andern']),B_putzen_prozent_max)
    elif range_ausreiss_data_BA.iloc[len(histprocal_BA_data)-2]['ausreiss']=="J" :
        B_putzen_prozent=max(abs(range_ausreiss_data_BA.iloc[len(histprocal_BA_data)-1]['andern']),B_putzen_prozent_max)
    else :
        B_putzen_prozent=min(abs((B_mean-B_ausreiss_z*B_std)/range_ausreiss_data_BA.iloc[t]['close']-1),abs((B_mean+B_ausreiss_z*B_std)/range_ausreiss_data_BA.iloc[t]['close']-1))+B_putzen_prozent_max
    # print(range_ausreiss_data_BA)
    # print('range_ausreiss')
