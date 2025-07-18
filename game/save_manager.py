from path_manager import *
import json

def getall():
    try:
        with open(get_settings_path(), "r", encoding="utf-8") as f:
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

    with open(get_settings_path(), "w+", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    return old
