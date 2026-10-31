# Zeitgesteuerter Ausführer

import subprocess
import time
import importlib
import socket

processes=[]

## Netzwerkverbindung testen
def machen():
    try:
        socket.gethostbyname("google.com")
        internet="OK"
    except socket.gaierror:
        internet="unterbrochen"
    ## Fernsteuerungsschalter
    if internet=='OK' :
        import schalter
        importlib.reload(schalter)
        schalter= schalter.schalter
        if schalter== 'AN':
            ## Hauptprogramm starten
            process=subprocess.Popen(["python3","tachometer_ausreiss.py"])
            process.wait()
            processes.append(process)
        else :
            print("warten")
    else:
        print("unterbrochen")

## Programmausführungsintervall      
try:
    while True:
        machen()
        time.sleep(60)
except KeyboardInterrupt:
    for process in processes:
        process.terminate()
    print("enden")
