HEADERS = {
    "title": "Valuable Values",
    "starter": '# A shader is a bit of code that run for every pixel, but each pixel gets\n# different x and y values based on its position.\n# You can use x to make effects like gradients.\n#\n# Tip: The challenge use values in steps of 16 for gradients\n\nreturn (x,x,x)',
    "size": (16, 16),
    "index": 2,

    "_author": "@mathias"
}

def run(x,y):
    return (x*16, x*16, x*16)