HEADERS = {
    "title": "Circle",
    "starter": '# Draw a white circle in the center\n# Use the  Pythagoras\' theorem\n\nreturn (0, 0, 0)',
    "size": (15, 15),
    "index": 7,

    "_author": "@mathias"
}

import math

def run(x,y):
    cx, cy = 7, 7
    radius = 6
    
    distance = math.sqrt((x - cx)**2 + (y - cy)**2)
    
    if distance <= radius:
        return 0xFFFFFF
    else:
        return 0x000000