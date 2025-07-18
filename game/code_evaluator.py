"""
Module for evaluating code
"""
import math
import tokenize
from io import BytesIO
from challenge_manager import challenge_manager

def convertHexToRGB(hex):
    """Convert HEX to RGBA"""
    r = (hex >> 16) & 0xFF
    g = (hex >> 8) & 0xFF
    b = hex & 0xFF
    return (r, g, b, 255)

def uniform_color(color):
    """Convert colors to RGBA"""
    if color is None:
        return (0,)*4 # transparent black
    if type(color) == int:
        color = convertHexToRGB(color)
    elif type(color) == tuple:
        if len(color) == 3:
            color = (color[0], color[1], color[2], 255)

    if any(x > 255 for x in color):
        return (255, 255, 255, 255)

    return color


def postprocessColor(color):
    """Post-process color for converting everything to RGBA"""
    cur_chall = challenge_manager.get_current_challenge()

    if cur_chall != None:
        palette = cur_chall.get("palette")
        if palette != None:
            try:
                return uniform_color(palette[color-1])
            except Exception as e:
                return (0,0,0,0)
    
    return uniform_color(color)

def safe_eval(usercode, x, y):
    """Safely eval usercode"""
    wrapped_code = f"def _user_func(x,y):\n"
    for line in usercode.splitlines():
        wrapped_code += f"    {line}\n"

    safe_math = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
    safe_globals = {
        "__builtins__": {
            "abs": abs, "min": min, "max": max, "sum": sum,
            "range": range, "len": len,
            **safe_math
        }
    }

    safe_locals = {}
    exec(wrapped_code, safe_globals, safe_locals)
    return postprocessColor(safe_locals["_user_func"](x, y))


def get_token_count(code):
    """Count tokens"""
    tokens = list(tokenize.tokenize(BytesIO(code.encode('utf-8')).readline))
    real_tokens = [tok for tok in tokens if tok.type not in (tokenize.ENCODING, tokenize.ENDMARKER, tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE)]
    return len(real_tokens)
