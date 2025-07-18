HEADERS = {
    "title": "Simon",
    "starter": '# We <3 if trees\n\nreturn (0, 0, 0)',
    "size": (8, 8),
    "index": 5,
    "palette": [0xDD4B3E, 0x3EDD4B, 0x4B3EDD, 0xFFEA37],

    "_author": "@mathias"
}

def run(x,y):
    if x < 4:
        if y >= 4:
            return 3
        else:
            return 1
    else:
        if y >= 4:
            return 4
        else:
            return 2