HEADERS = {
    "title": "Diagonal",
    "starter": '# Think in 2D\n\nreturn (255, 255, 255)',
    "size": (8, 8),
    "index": 6,

    "_author": "@mathias"
}

def run(x,y):
    if x == y:
        return (255, 255, 255)
    else:
        return (0, 0, 0)