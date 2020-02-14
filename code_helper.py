import requests
import json
import time
import sys
import os

def aprifile(percorso):
    try:
        with open(percorso, "r") as ptrfile:
            settings = ptrfile.readlines()

            for a in range(0, len(settings)):
                if settings[a][-1] == "\n":
                    settings[a] = settings[a][:-1]

            return (settings)

    except Exception:
        return(["pi.hole", ""])

def scrivifile(text, percorso):
    try:
        with open(percorso, "w") as ptrfile:
            ptrfile.write(text)

    except Exception as er:
        print("Impossibile scrivere file " + str(er))

def ricercaInfo(url):
        try:
            with requests.get(url = url, timeout= 0.700) as status:
                json_string = status.content
                parsed_json = json.loads(json_string)
                status = parsed_json['status']
                
                if(status == "enabled"):
                    return True
                elif(status == "disabled"):
                    return False
                else:
                    return None

        except Exception as es:
            print(es)
            return None

def readKey():
    try:
        data = aprifile("data.txt")
        return(data[0], data[1])

    except Exception:
        return("pi.hole", "")

def saveKey(ip, key, path):
    scrivifile(ip + "\n" + key, path)

#def resource_path(relative_path):
#    if hasattr(sys, '_MEIPASS'):
#        return os.path.join(sys._MEIPASS, relative_path)
#    return os.path.join(os.path.abspath("."), relative_path)