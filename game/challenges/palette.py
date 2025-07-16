HEADERS = {
    "title": "Palette breton",
    "starter": '# Sometimes, 16.777.216 colors may be overwhelming,\n# Palette allow you to restrain how many colors you can use for a better harmony :rainbow:\n\nreturn x',
    "palette": [0x000000, 0x1D2B53, 0x7E2553, 0x008751, 0xAB5236, 0x5F574F, 0xC2C3C7, 0xFFF1E8, 0xFF004D, 0xFFA300, 0xFFEC27, 0x00E436, 0x29ADFF, 0x83769C, 0xFF77A8, 0xFFCCAA], #pico8 palette
    "size": (16, 16),
    "index": 4,

    "_author": "@mathias"
}

def run(x,y):
    return (x+y)%16
