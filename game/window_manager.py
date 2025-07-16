"""
Module for window management
"""
import dearpygui.dearpygui as dpg
import save_manager as save


def place_window(id):
    """Place a window based of his saved position and size"""
    pos = save.get(f"window.{id}.pos", [0, 0])
    current_w, current_h = dpg.get_item_width(id), dpg.get_item_height(id)
    size = save.get(f"window.{id}.size", [current_w, current_h])
    vw, vh = dpg.get_viewport_width(), dpg.get_viewport_height()

    clamped_x = max(0, min(pos[0], vw - size[0]))
    clamped_y = max(0, min(pos[1], vh - size[1]))

    dpg.set_item_pos(id, [clamped_x, clamped_y])
    dpg.set_item_width(id, size[0])
    dpg.set_item_height(id, size[1])


def window_close_callback(sender, app_data, user_data):
    """Callback for saving a window pos & size"""
    if dpg.does_item_exist(sender):
        save.set(f"window.{sender}.pos", dpg.get_item_pos(sender))
        save.set(f"window.{sender}.size", [dpg.get_item_width(sender), dpg.get_item_height(sender)])
        dpg.delete_item(sender)


def exit_callback():
    """Callback when the viewport is closed"""
    #window_close_callback("challenges_list", None, None)
    #window_close_callback("editor_window", None, None)
    #window_close_callback("preview_window", None, None)
    #window_close_callback("chall_preview_window", None, None)


def get_best_text_color(background):
    r, g, b, a = background
    brightness = (r * 299 + g * 587 + b * 114) / 1000  # perceived brightness
    if brightness > 128:
        return (0,0,0,255)
    else:
        return (255,)*4
