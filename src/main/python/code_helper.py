import json

import requests

FILE_POSITION = "../../../key"
TIMEOUT = 1.000


def ricercaInfo(url):
    try:
        with requests.get(url=url, timeout=TIMEOUT) as status:
            json_string = status.content
            parsed_json = json.loads(json_string)
            status = parsed_json['status']

            if (status == "enabled"):
                return True
            elif (status == "disabled"):
                return False
            else:
                return None

    except Exception as es:
        print(es)
        return None


def readKey():
    try:
        with open(FILE_POSITION, "r") as read_file:
            data = json.load(read_file)
            return (data["ip"], data["key"])

    except Exception:
        return ("pi.hole", "")


def saveKey(ip, key):
    data = {"ip": ip, "key": key}

    with open(FILE_POSITION, "w") as write_file:
        json.dump(data, write_file, indent=4)

# def resource_path(relative_path):
#    if hasattr(sys, '_MEIPASS'):
#        return os.path.join(sys._MEIPASS, relative_path)
#    return os.path.join(os.path.abspath("."), relative_path)
