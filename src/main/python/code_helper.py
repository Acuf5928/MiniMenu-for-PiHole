import json
import os
import requests

TIMEOUT = 1.000


def ricercaInfo(url):
    try:
        with requests.get(url=url, timeout=TIMEOUT) as status:
            json_string = status.content
            parsed_json = json.loads(json_string)
            status = parsed_json['status']

            if status == "enabled":
                return True
            elif status == "disabled":
                return False
            else:
                return None

    except Exception as es:
        print(es)
        return None


def readKey(filePosition):
    try:
        with open(filePosition + "\\key.json", "r") as read_file:
            data = json.load(read_file)
            return data["ip"], data["key"]

    except Exception:
        return "pi.hole", ""


def saveKey(ip, key, filePosition):
    data = {"ip": ip, "key": key}
    checkfolder(filePosition)

    with open(filePosition + "\\key.json", "w") as write_file:
        json.dump(data, write_file, indent=4)


# se la cartella data non esiste la crea
# la cartella madre deve esistere
def checkfolder(path):
    if not os.path.isdir(path):
        os.mkdir(path)
