"""
Module for UI Components
"""
import dearpygui.dearpygui as dpg
from tkinter import filedialog
from PIL import Image
import tkinter as tk
from glob import glob
import webbrowser
import asyncio
import os
from path_manager import *
import save_manager as save
from challenge_manager import challenge_manager
from code_evaluator import safe_eval, get_token_count, postprocessColor, uniform_color
from window_manager import place_window, window_close_callback, get_best_text_color


# For comparing user/challenge
user_colormap = {}
chall_colormap = {}

# Index for popups
_msgbox_idx = 0


def show_popup(title, content):
    """Open a popup"""
    global _msgbox_idx
    tag = f"_messagebox_{_msgbox_idx}"
    with dpg.window(tag=tag, no_title_bar=True, no_close=True, no_resize=True, no_collapse=True, no_scrollbar=True):
        _msgbox_idx += 1

        dpg.add_text(default_value=title)
        dpg.add_text(default_value=content, wrap=500)
        dpg.add_spacer(height=10)

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=250)
            dpg.add_button(label="OK", callback=lambda: dpg.delete_item(tag), width=30)


def setup_welcome_window():
    """Setup welcome window"""
    vp_width, vp_height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
    x = int((vp_width - 500) / 2)
    y = int((vp_height - 300) / 2)
    dpg.set_item_pos("welcome_window", [x, y])

    dpg.set_item_pos("welcome.close", [430, 235])
    dpg.set_item_pos("welcome.timeless", [280, 235])


def create_welcome_window():
    """Create welcome window"""
    if save.get("firstTime", True):
        with dpg.window(label="Welcome!", modal=True, width=500, height=300, tag="welcome_window", no_close=True, no_resize=True):
            with dpg.child_window(autosize_x=True, autosize_y=True):
                dpg.add_text(open(os.path.join(resource_path("docs"), os.path.join("001_Getting started","001_welcome.md")), "r", encoding="utf-8").read(), wrap=0)

                dpg.add_button(label="More about Timeless",
                                callback=lambda: webbrowser.open('https://timeless.hackclub.com/'),
                                tag="welcome.timeless")
                
                dpg.add_button(label="Close",
                                callback=lambda: dpg.hide_item("welcome_window"),
                                tag="welcome.close")


def resize_editor():
    """Trigger when editor is resized"""
    window_width = dpg.get_item_width("editor_window") - 75
    dpg.set_item_width("width-editor-slider", window_width)
    dpg.set_item_width("height-editor-slider", window_width)


def get_preview_size():
    """Get preview size (from user input or challenge)"""
    current_challenge = challenge_manager.get_current_challenge()
    if current_challenge is not None:
        return current_challenge['size']

    height = dpg.get_value("height-editor-slider")
    width = dpg.get_value("width-editor-slider")
    return (width, height)


def draw_usercode(sender, app_data, user_data):
    """Draw usercode in his window"""
    global user_colormap, chall_colormap
    
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

    # Define optimal size
    pixel_width = draw_width / preview_width
    pixel_height = draw_height / preview_height
    
    # Center the rectangle
    x_offset = (window_width - draw_width) // 2
    y_offset = (window_height - draw_height) // 2

    width, height = get_preview_size()
    code = dpg.get_value("userscript")

    try:
        for x in range(width):
            for y in range(height):
                color = safe_eval(code, x, y)
                user_colormap[f"{x},{y}"] = color
    except Exception as e:
        # If it can't eval a pixel, don't change the drawing
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
                    color=(0, 0, 0, 0),
                    fill=color
                )
    
    if dpg.does_item_exist("userpreview_popup"):
        dpg.delete_item("userpreview_popup")

    with dpg.popup("user_drawlist", no_move=True, min_size=[100,0], max_size=[100,100], tag="userpreview_popup"):
        dpg.add_button(
            label="Save as",
            width=-1,
            callback=save_userpreview
        )

    tokens = get_token_count(dpg.get_value("userscript"))
    dpg.set_value("editor_tokens", f"Tokens: {tokens}")

    # Verify if challenge is solved
    for pixel, value in user_colormap.items():
        if value != chall_colormap.get(pixel, None):
            return
        
    current_challenge = challenge_manager.get_current_challenge()
    if current_challenge is not None:
        name = current_challenge.get("title")
        challenge_id = current_challenge.get("id")

        if save.get(f"challenge.{challenge_id}.completed", False) == False:
            save.set(f"challenge.{challenge_id}.completed", True)
            save.set(f"challenge.{challenge_id}.tokens", tokens)
            show_popup("Challenge completed!", f"You've solved the '{name}' challenge with {tokens} tokens!")
        else:
            old_record = save.get(f"challenge.{challenge_id}.tokens", 99999999)
            if old_record > tokens:
                save.set(f"challenge.{challenge_id}.tokens", tokens)
                show_popup("Record beaten!", f"You've beat your past record for this challenge by {old_record-tokens} tokens ({old_record} -> {tokens})")


def draw_palette():
    drawlist = dpg.get_item_parent("palette_layer")
    dpg.delete_item("palette_layer")
    current_challenge = challenge_manager.get_current_challenge()

    if current_challenge == None:
        palette = []
    else:
        palette = current_challenge.get("palette", [])

    with dpg.draw_layer(parent=drawlist, tag="palette_layer"):
        i = len(palette)
        for color in palette:
            color = uniform_color(color)
            x = 500-(i*20)
            i -= 1
            idx = len(palette)-i

            dpg.draw_rectangle((x,0), (x+20, 20), fill=color, color=(0,0,0,0))

            dx = 2 if idx>=10 else 5
            dpg.draw_text((x+dx, 2.5), str(idx), color=get_best_text_color(color), size=15)


def toggle_editor():
    """Show/hide editor"""
    if dpg.does_item_exist("editor_window"):
        return dpg.delete_item("editor_window")

    with dpg.window(label='Editor', tag="editor_window", width=800, height=600, on_close=window_close_callback):
        dpg.add_input_text(
            width=-1,
            height=-70,
            tag="userscript",
            multiline=True,
            tab_input=True,
            callback=draw_usercode
        )

        current_challenge = challenge_manager.get_current_challenge()
        if current_challenge is None:
            dpg.set_value("userscript", "return (255,255,255)")
        else:
            dpg.set_value("userscript", current_challenge.get("starter", "return (255,255,255)"))

        with dpg.group(horizontal=True):
            dpg.add_text("Tokens: ???", tag="editor_tokens")
            
            dpg.add_spacer(width=203)
            with dpg.drawlist(width=500, height=20):
                with dpg.draw_layer(tag="palette_layer"):
                    pass

        draw_palette()

        with dpg.group(horizontal=True):
            dpg.add_text("Width :")
            dpg.add_slider_int(min_value=1, max_value=512, width=725, tag="width-editor-slider", default_value=16)

        with dpg.group(horizontal=True):
            dpg.add_text("Height:")
            dpg.add_slider_int(min_value=1, max_value=512, width=725, tag="height-editor-slider", default_value=16)

    place_window("editor_window")
    dpg.bind_item_handler_registry("editor_window", "editor_handler")
    draw_usercode(None, None, None)


def toggle_preview():
    """Show/hide user preview"""
    if dpg.does_item_exist("preview_window"):
        return dpg.delete_item("preview_window")
    
    with dpg.window(label="Code Preview", tag="preview_window", width=300, height=300, no_scrollbar=True, on_close=window_close_callback):
        with dpg.drawlist(width=265, height=265, tag="user_drawlist"):
            draw_usercode(None, None, None)
    
    place_window("preview_window")
    dpg.bind_item_handler_registry("preview_window", "preview_handler")
    draw_usercode(None, None, None)


def draw_challenge(sender, app_data, user_data):
    """Draw challenge preview"""
    global chall_colormap
    chall_colormap = {}
    
    current_challenge = challenge_manager.get_current_challenge()
    if current_challenge is None:
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

    # Define optimal size
    pixel_width = draw_width / preview_width
    pixel_height = draw_height / preview_height
    
    # Center the rectangle
    x_offset = (window_width - draw_width) // 2
    y_offset = (window_height - draw_height) // 2

    width, height = get_preview_size()

    for x in range(width):
        for y in range(height):
            color = current_challenge['run_func'](x, y)
            chall_colormap[f"{x},{y}"] = postprocessColor(color)

    dpg.delete_item("chall_drawlist")
    with dpg.drawlist(width=window_width, height=window_height, parent=window, tag="chall_drawlist"):
        # Draw
        async def draw_pixel(x, y):
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
                color=(0, 0, 0, 0),
                fill=color
            )

        for x in range(width):
            for y in range(height):
                asyncio.run(draw_pixel(x, y))

    draw_palette()


def open_challenge(cid):
    """Open a challenge"""
    challenge_manager.set_current_challenge(cid)

    if not dpg.does_item_exist("editor_window"):
        toggle_editor()

    if not dpg.does_item_exist("preview_window"):
        toggle_preview()

    dpg.delete_item("challenges_list")

    if cid is None:
        draw_palette()
        if dpg.does_item_exist("userscript"):
            dpg.set_value("userscript", "return 0xFFFFFF")
        if dpg.does_item_exist("chall_preview_window"):
            window_close_callback("chall_preview_window", None, None)
            dpg.delete_item("chall_preview_window")
        return 
    
    current_challenge = challenge_manager.get_current_challenge()

    if dpg.does_item_exist("userscript"):
        dpg.set_value("userscript", current_challenge.get("starter", "return (255,255,255)"))
    
    draw_usercode(None, None, None)

    if dpg.does_item_exist("chall_preview_window"):
        window_close_callback("chall_preview_window", None, None)
        dpg.delete_item("chall_preview_window")

    with dpg.window(label="Challenge Preview", tag="chall_preview_window", width=300, height=300, no_scrollbar=True, no_close=True):
        with dpg.drawlist(width=265, height=265, tag="chall_drawlist"):
            pass

    place_window("chall_preview_window")
    draw_challenge(None, None, None)


def make_chall_callback(challenge_id):
    """Create callback for opening a challenge"""
    return lambda: open_challenge(challenge_id)


def open_challenges_window():
    """Open challenges list"""
    if dpg.does_item_exist("challenges_list"):
        return dpg.delete_item("challenges_list")

    with dpg.window(
        label="Challenges",
        tag="challenges_list",
        width=200,
        height=300,
        on_close=window_close_callback):
        
        with dpg.theme() as completed_button_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (34, 173, 19, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (32, 148, 19, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (34, 173, 19, 255))

        challenges = challenge_manager.get_all_challenges()
        ordered_challenges = sorted(challenges.values(), key=lambda challenge: challenge.get("index", -1))

        button = dpg.add_button(label="Freeplay", width=-1, callback=make_chall_callback(None))

        for chall in ordered_challenges:
            cid = chall['id']

            button = dpg.add_button(label=chall['title'], width=-1, callback=make_chall_callback(cid))
            if save.get(f"challenge.{cid}.completed", False):
                dpg.bind_item_theme(button, completed_button_theme)

        userchallenges = challenge_manager.get_all_userchallenges().values()

        if len(userchallenges) != 0:
            dpg.add_text("Custom challenges")

        for chall in userchallenges:
            cid = chall['id']

            button = dpg.add_button(label=chall['title'], width=-1, callback=make_chall_callback("user."+cid))
            if save.get(f"challenge.{cid}.completed", False):
                dpg.bind_item_theme(button, completed_button_theme)

    place_window("challenges_list")


pages = {}

docs_folder = resource_path("docs")

for category in [d for d in glob(os.path.join(docs_folder, "*")) if os.path.isdir(d)]:
    cat_title = os.path.basename(category)[4:]
    
    pages[cat_title] = f"{cat_title}\n\n"
    for page in glob(os.path.join(category, "*.md")):
        content = open(page, "r", encoding="utf-8").readlines()

        title = "- "+content[0][2:-1]
        pages[title] = "".join(content[2:])
        pages[cat_title] += f"{title}\n"

"""
for page in glob("*_*.md", root_dir=resource_path("docs"), dir_fd=):
    content = open(os.path.join(resource_path("docs"), page), "r", encoding="utf-8").readlines()
    title = content[0][2:-1]

    pages[title] = "".join(content[2:])
"""

def _switch_docs_page(sender, app_data, user_data):
    content = pages[app_data]
    dpg.set_value("docs_content", content)

def toggle_docs():
    """Open documentation window"""
    if dpg.does_item_exist("documentation_window"):
        return dpg.delete_item("documentation_window")

    with dpg.window(
        label="Documentation",
        tag="documentation_window",
        width=700,
        height=560,
        no_resize=True,
        on_close=window_close_callback):

        with dpg.group(horizontal=True):
            dpg.add_listbox(
                list(pages.keys()),
                tag="docs_list",
                width=150,
                num_items=30,
                callback=_switch_docs_page
            )

            dpg.set_value("docs_list", "- Welcome")

            dpg.add_text("", tag="docs_content", wrap=500)

        _switch_docs_page(None, "- Welcome", None)


def save_userpreview():
    image = Image.new(mode="RGBA", size=get_preview_size())
    dpg.configure_item("userpreview_popup", show=False)

    for pos, pixel in user_colormap.items():
        x,y = pos.split(",")
        x,y = int(x), int(y)
        
        image.putpixel((x,y), pixel)

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.asksaveasfilename(
        title="Save Image As",
        defaultextension=".png",
        initialfile="image.png",
        filetypes=[("PNG Image", "*.png")]
    )

    root.destroy()

    if file_path:
        image.save(file_path)
        print(f"Image saved to: {file_path}")
