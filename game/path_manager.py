import platformdirs
import os
import sys

appname="match_my_shader"
appauthor="mathias"

data_dir = platformdirs.user_data_dir(appname, appauthor)
chall_dir = os.path.join(data_dir, "challenges")

os.makedirs(data_dir, exist_ok=True)
os.makedirs(chall_dir, exist_ok=True)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def get_userchallenges_directory():
    return chall_dir

def get_settings_path():
    return os.path.join(data_dir, "settings.json")