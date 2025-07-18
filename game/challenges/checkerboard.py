HEADERS = {
    "title": "Checkerboard",
    "starter": '# When a palette is used (you can it under the editor\n# You simply need to return the index of the color\n# Do you know this checkerboard ??\n\nreturn None',
    "palette": [0xC66100, 0x632000],
    "size": (4, 4),
    "index": 4,

    "_author": "@mathias"
}

def run(x,y):
    return (x+y)%2
