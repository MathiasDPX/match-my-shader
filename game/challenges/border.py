HEADERS = {
    "title": "Border",
    "starter": 'return (255, 255, 255)',
    "size": (12, 12),
    "index": 8,

    "_author": "@mathias"
}

def run(x,y):
    if x == 0 or x == 11 or y == 0 or y == 11:
        return 0xFFFFFF
    else:
        return 0x000000