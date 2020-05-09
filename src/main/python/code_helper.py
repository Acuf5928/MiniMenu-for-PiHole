import json

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
        with open(filePosition, "r") as read_file:
            data = json.load(read_file)
            return data["ip"], data["key"]

    except Exception:
        return "pi.hole", ""


def saveKey(ip, key, filePosition):
    data = {"ip": ip, "key": key}

    with open(filePosition, "w") as write_file:
        json.dump(data, write_file, indent=4)
