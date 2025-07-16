import platformdirs
import json
import os

appname="match_my_shader"
appauthor="mathias"
datadir = platformdirs.user_data_dir(appname, appauthor)

os.makedirs(datadir, exist_ok=True)

def getall():
    try:
        with open(os.path.join(datadir, "settings.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def get(key:str, default:str):
    data = getall()
    return data.get(key, default)

def set(key:str, value):
    data = getall()
    old = data.get(key)
    data[key] = value

    with open(os.path.join(datadir, "settings.json"), "w+", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    return old
