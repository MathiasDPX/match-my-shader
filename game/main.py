"""
Entrypoint for 'Match my Shader'
"""

import dearpygui.dearpygui as dpg
import save_manager as save
from path_manager import *
from ui_components import (
    create_welcome_window, 
    setup_welcome_window, 
    open_challenges_window,
    toggle_editor, 
    toggle_preview,
    toggle_docs,
    draw_usercode,
    resize_editor
)


def main():
    dpg.create_context()
    dpg.create_viewport(
        title='Match my Shader',
        width=1600,
        height=1000,
        small_icon=resource_path("icon.ico"),
        large_icon=resource_path("icon.ico")
    )

    create_welcome_window()

    # Menu bar
    with dpg.viewport_menu_bar():
        dpg.add_menu_item(label="Challenges", callback=open_challenges_window)
        
        with dpg.menu(label="Views"):
            dpg.add_menu_item(label="Editor", callback=toggle_editor)
            dpg.add_menu_item(label="Code preview", callback=toggle_preview)

        dpg.add_menu_item(label="Help", callback=toggle_docs)

    dpg.setup_dearpygui()
    dpg.show_viewport()

    # Register events handlers
    with dpg.item_handler_registry(tag="preview_handler"):
        dpg.add_item_resize_handler(callback=draw_usercode, user_data="preview_window")

    with dpg.item_handler_registry(tag="editor_handler"):
        dpg.add_item_resize_handler(callback=resize_editor, user_data="editor_window")

    if save.get("firstTime", True):
        setup_welcome_window()

    dpg.start_dearpygui()
    dpg.destroy_context()

    save.set("firstTime", False)


if __name__ == "__main__":
    main()
