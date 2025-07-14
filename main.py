import dearpygui.dearpygui as dpg
import save_manager as save
import webbrowser

dpg.create_context()
dpg.create_viewport(title='Match my Shader', width=800, height=600)

if save.get("firstTime", True):
    with dpg.window(label="Welcome!", width=500, height=300, tag="welcome_window", no_close=True, no_resize=True) as main_window:
        with dpg.child_window(autosize_x=True, autosize_y=True):
            dpg.add_text("Hi! If you're seeing this it mean it's your first time launching 'Match my Shader' \n\nThis game was created in just 10 days for a game jam called Timeless, where the goal was to build a game that someone could enjoy for the next 10 years.\n\nIn Match My Shader, your challenge is to write code that draws a shader to match a target pixel-perfect result. It's creative, puzzling, and endlessly replayable. Enjoy!", wrap=0)

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

dpg.setup_dearpygui()
dpg.show_viewport()

if save.get("firstTime", True):
    setup_welcome_window()

dpg.start_dearpygui()
dpg.destroy_context()

save.set("firstTime", False)