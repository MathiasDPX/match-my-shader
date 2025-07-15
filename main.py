import dearpygui.dearpygui as dpg
from io import BytesIO
from glob import glob
import webbrowser
import importlib
import tokenize
import save_manager as save

dpg.create_context()
dpg.create_viewport(title='Match my Shader', width=1600, height=1000)

# Load challenges
challenges = {}

# Used to compare user and challenge
user_colormap={}
chall_colormap={}

for challenge in glob("*.py", root_dir="challenges"):
    module = importlib.import_module(f"challenges.{challenge[:-3]}")

    if not hasattr(module, "HEADERS"):
        print(f"Missing HEADERS dict for {challenge}")
        continue

    if not hasattr(module, "run"):
        print(f"Missing run() functio for {challenge}")
        continue

    headers = getattr(module, "HEADERS")
    headers['run_func'] = getattr(module, "run")
    headers['id'] = challenge[:-3]

    challenges[headers['id']] = headers

# Welcome window
if save.get("firstTime", True):
    with dpg.window(label="Welcome!", width=500, height=300, tag="welcome_window", no_close=True, no_resize=True) as main_window:
        with dpg.child_window(autosize_x=True, autosize_y=True):
            dpg.add_text("Hi! If you're seeing this it mean it's your first time launching 'Match my Shader' \n\nThis game was created in just 10 days for a game jam called Timeless, where the goal was to build a game that someone could enjoy for the next 10 years.\n\nIn Match My Shader, your challenge is to write code that draws a shader to match a target pixel-perfect result. It's creative, puzzling, and endlessly replayable.\n\nThere is two gamemodes: Freeplay, where you just code to ", wrap=0)

            dpg.add_button(label="More about Timeless",
                            callback=lambda:webbrowser.open('https://timeless.hackclub.com/'),
                            tag="welcome.timeless")
            
            dpg.add_button(label="Close",
                            callback=lambda:dpg.hide_item("welcome_window"),
                            tag="welcome.close")

def setup_welcome_window():
    vp_width, vp_height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
    x = int((vp_width - 500) / 2)
    y = int((vp_height - 300) / 2)
    dpg.set_item_pos("welcome_window", [x, y])

    # spooky spooky hardcoded values
    dpg.set_item_pos("welcome.close", [430, 235])
    dpg.set_item_pos("welcome.timeless", [280, 235])

def convertHexToRGB(hex):
    r = (hex >> 16) & 0xFF
    g = (hex >> 8) & 0xFF
    b = hex & 0xFF
    return (r, g, b, 255)

def postprocessColor(color):
    if type(color) == int:
        color = convertHexToRGB(color)
    elif type(color) == tuple:
        if len(color) == 3:
            color = (color[0], color[1], color[2], 255)

    if any(x > 255 for x in color):
        return (255, 255, 255, 255)

    return color

def safe_eval(usercode, x,y):
    wrapped_code = f"def _user_func(x,y):\n"
    for line in usercode.splitlines():
        wrapped_code += f"    {line}\n"

    # Restricted global/local environment
    safe_globals = {
        "__builtins__": {
            "abs": abs, "min": min, "max": max, "sum": sum,
            "range": range, "len": len,  # whitelist safe builtins
        }
    }

    safe_locals = {}
    exec(wrapped_code, safe_globals, safe_locals)
    return postprocessColor(safe_locals["_user_func"](x,y))

def get_token_count(code):
    tokens = list(tokenize.tokenize(BytesIO(code.encode('utf-8')).readline))
    real_tokens = [tok for tok in tokens if tok.type not in (tokenize.ENCODING, tokenize.ENDMARKER, tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE)]

    print(real_tokens)

    return len(real_tokens)

_msgbox_idx = 0
def show_popup(title, content):
    global _msgbox_idx
    tag = f"_messagebox_{_msgbox_idx}"
    with dpg.window(tag=tag, no_title_bar=True, no_close=True, no_resize=True, no_collapse=True, no_scrollbar=True):
        _msgbox_idx += 1

        dpg.add_text(default_value=title)
        dpg.add_text(default_value=content, wrap=500)
        dpg.add_spacer(height=10)

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=250)
            dpg.add_button(label="OK", callback=lambda:dpg.delete_item(tag), width=30)
        
# Editor window
def resize_editor():
    window_width = dpg.get_item_width("editor_window")-75

    dpg.set_item_width("width-editor-slider", window_width)
    dpg.set_item_width("height-editor-slider", window_width)

def toggle_editor():
    if dpg.does_item_exist("editor_window"):
        return dpg.delete_item("editor_window")

    with dpg.window(label='Editor', tag="editor_window", width=800, height=600):
        dpg.add_input_text(
            width=-1,
            height=-50,
            tag="userscript",
            multiline=True,
            tab_input=True,
            callback=draw_usercode
        )

        if challenge == None:
            dpg.set_value("userscript", "return (255,255,255)")
        else:
            dpg.set_value("userscript", challenge.get("starter", "return (255,255,255)"))

        with dpg.group(horizontal=True):
            dpg.add_text("Width :")
            dpg.add_slider_int(min_value=1, max_value=512, width=725, tag="width-editor-slider", default_value=16)

        with dpg.group(horizontal=True):
            dpg.add_text("Height:")
            dpg.add_slider_int(min_value=1, max_value=512, width=725, tag="height-editor-slider", default_value=16)

    dpg.bind_item_handler_registry("editor_window", "editor_handler")
    draw_usercode(None, None, None)

# Preview window
def get_preview_size():
    if challenge != None:
        return challenge['size']

    height = dpg.get_value("height-editor-slider")
    width = dpg.get_value("width-editor-slider")
    return (width, height)

def draw_usercode(sender, app_data, user_data):
    if not dpg.does_item_exist("preview_window"):
        return

    preview_width, preview_height = get_preview_size()

    if None in [preview_height, preview_width]:
        return

    aspect_ratio = preview_width / preview_height

    window_width = dpg.get_item_width("preview_window") - 17.5
    window_height = dpg.get_item_height("preview_window") - 35
    window = dpg.get_item_parent("user_drawlist")

    if window_width / window_height > aspect_ratio:
        # Fit to height
        draw_height = window_height
        draw_width = int(draw_height * aspect_ratio)
    else:
        # Fit to width
        draw_width = window_width
        draw_height = int(draw_width / aspect_ratio)

    # Calculate pixel size to maximize preview
    pixel_width = draw_width / preview_width
    pixel_height = draw_height / preview_height
    
    # Center the rectangle
    x_offset = (window_width - draw_width) // 2
    y_offset = (window_height - draw_height) // 2

    global user_colormap
    width, height = get_preview_size()
    code = dpg.get_value("userscript")

    try:
        for x in range(width):
            for y in range(height):
                color = safe_eval(code, x,y)
                user_colormap[f"{x},{y}"] = color
    except Exception as e:
        # if it can generate a pixel it will return without changing the last image
        return

    dpg.delete_item("user_drawlist")
    with dpg.drawlist(width=window_width, height=window_height, parent=window, tag="user_drawlist"):
        # Draw
        for x in range(width):
            for y in range(height):
                color = user_colormap[f"{x},{y}"]
                dpg.draw_rectangle(
                    (
                        x_offset + (x * pixel_width),
                        y_offset + (y * pixel_height)
                    ),
                    (
                        x_offset + ((x + 1) * pixel_width),
                        y_offset + ((y + 1) * pixel_height)
                    ),
                    color=(0,0,0,0),
                    fill=color
                )

    for pixel, value in user_colormap.items():
        if value != chall_colormap.get(pixel, None):
            return
        
    if challenge != None:
        name = challenge.get("title")
        id = challenge.get("id")
        tokens = get_token_count(dpg.get_value("userscript"))

        if save.get(f"challenge.{id}.completed", False) == False:
            save.set(f"challenge.{id}.completed", True)
            save.set(f"challenge.{id}.tokens", tokens)
            show_popup("Challenge completed!", f"You've solved the '{name}' challenge with {tokens} tokens!")

def toggle_preview():
    if dpg.does_item_exist("preview_window"):
        return dpg.delete_item("preview_window")
    
    with dpg.window(label="Code Preview", tag="preview_window", width=300, height=300, no_scrollbar=True):
        with dpg.drawlist(width=265, height=265, tag="user_drawlist"):
            draw_usercode(None, None, None)

    dpg.bind_item_handler_registry("preview_window", "preview_handler")
    draw_usercode(None, None, None)

# Challenges
challenge = None
def open_challenge(cid):
    global challenge

    if not dpg.does_item_exist("editor_window"):
        toggle_editor()

    if not dpg.does_item_exist("preview_window"):
        toggle_preview()

    dpg.delete_item("challenges_list")

    if cid == None:
        challenge = None

        if dpg.does_item_exist("userscript"):
            dpg.set_value("userscript", "return 0xFFFFFF")
        if dpg.does_item_exist("chall_preview_window"):
            dpg.delete_item("chall_preview_window")
        return 
    
    challenge = challenges.get(cid)

    if dpg.does_item_exist("userscript"):
        dpg.set_value("userscript", challenge.get("starter", "return (255,255,255)"))
    
    draw_usercode(None, None, None)

    if dpg.does_item_exist("chall_preview_window"):
        dpg.delete_item("chall_preview_window")

    with dpg.window(label="Challenge Preview", tag="chall_preview_window", width=300, height=300, no_scrollbar=True, no_close=True):
        with dpg.drawlist(width=265, height=265, tag="chall_drawlist"):
            pass

    draw_challenge(None, None, None)

def draw_challenge(sender, app_data, user_data):
    global chall_colormap
    chall_colormap = {}
    if challenge == None:
        return

    preview_width, preview_height = get_preview_size()

    if None in [preview_height, preview_width]:
        return

    aspect_ratio = preview_width / preview_height

    window_width = dpg.get_item_width("chall_preview_window") - 17.5
    window_height = dpg.get_item_height("chall_preview_window") - 35
    window = dpg.get_item_parent("chall_drawlist")

    if window_width / window_height > aspect_ratio:
        # Fit to height
        draw_height = window_height
        draw_width = int(draw_height * aspect_ratio)
    else:
        # Fit to width
        draw_width = window_width
        draw_height = int(draw_width / aspect_ratio)

    # Calculate pixel size to maximize preview
    pixel_width = draw_width / preview_width
    pixel_height = draw_height / preview_height
    
    # Center the rectangle
    x_offset = (window_width - draw_width) // 2
    y_offset = (window_height - draw_height) // 2

    chall_colormap = {}
    width, height = get_preview_size()

    for x in range(width):
        for y in range(height):
            color = challenge['run_func'](x,y)
            chall_colormap[f"{x},{y}"] = postprocessColor(color)

    dpg.delete_item("chall_drawlist")
    with dpg.drawlist(width=window_width, height=window_height, parent=window, tag="chall_drawlist"):
        # Draw
        for x in range(width):
            for y in range(height):
                color = chall_colormap[f"{x},{y}"]
                dpg.draw_rectangle(
                    (
                        x_offset + (x * pixel_width),
                        y_offset + (y * pixel_height)
                    ),
                    (
                        x_offset + ((x + 1) * pixel_width),
                        y_offset + ((y + 1) * pixel_height)
                    ),
                    color=(0,0,0,0),
                    fill=color
                )

def make_chall_callback(challenge_id):
    return lambda: open_challenge(challenge_id)

def open_challenges_window():
    if dpg.does_item_exist("challenges_list"):
        return dpg.delete_item("challenges_list")

    with dpg.window(label="Challenges", tag="challenges_list", width=200, height=300):
        with dpg.theme() as completed_button_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (34, 173, 19,255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (32, 148, 19,255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (34, 173, 19,255))

        ordered_challenges = sorted(challenges.values(), key=lambda challenge: challenge.get("index", -1))

        button = dpg.add_button(label="Freeplay", width=-1, callback=make_chall_callback(None))

        for chall in ordered_challenges:
            cid = chall['id']

            button = dpg.add_button(label=chall['title'], width=-1, callback=make_chall_callback(cid))
            if save.get(f"challenge.{cid}.completed", False):
                dpg.bind_item_theme(button, completed_button_theme)

# Menu bar
with dpg.viewport_menu_bar():
    dpg.add_menu_item(label="Challenges", callback=open_challenges_window)
    
    with dpg.menu(label="Views"):
        dpg.add_menu_item(label="Editor", callback=toggle_editor)
        dpg.add_menu_item(label="Code preview", callback=toggle_preview)

dpg.setup_dearpygui()
dpg.show_viewport()

with dpg.item_handler_registry(tag="preview_handler"):
    dpg.add_item_resize_handler(callback=draw_usercode, user_data="preview_window")

with dpg.item_handler_registry(tag="editor_handler"):
    dpg.add_item_resize_handler(callback=resize_editor, user_data="editor_window")

if save.get("firstTime", True):
    setup_welcome_window()

dpg.start_dearpygui()
dpg.destroy_context()

save.set("firstTime", False)