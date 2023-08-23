from configparser import ConfigParser
from pathlib import Path

from localization import *


MAIN_DIRECTORY = Path(__file__).absolute().parent

if not Path(MAIN_DIRECTORY / "Data").exists():
    Path(MAIN_DIRECTORY / "Data").mkdir()

cfg = ConfigParser(interpolation=None)

if not Path(MAIN_DIRECTORY / "Data" / "config.ini").exists():
    language = input("Enter your language (type 'it' or 'en'): ").strip()
    if language not in ["it", "en"]:
        print("Invalid language. Defaulting to English.")
        language = "en"

    print(get_localized_message(language, "CONFIG_FIRST_SETUP"))
    bot_token = input(get_localized_message(language, "CONFIG_TOKEN")).strip()
    user_id = input(get_localized_message(language, "CONFIG_USER_ID")).strip()

    cfg['bot'] = {'bot_token': bot_token}
    cfg['bot_admins'] = {'admin_1': user_id}

    with open(MAIN_DIRECTORY / "Data" / "config.ini", "w") as configfile:
        cfg.write(configfile)
    
    print(get_localized_message(language, "CONFIG_SUCCESS"))

cfg.read(MAIN_DIRECTORY / "Data" / "config.ini")

BOT_TOKEN = cfg.get("bot", "bot_token")
BOT_ADMINS = [int(admin) for admin in cfg["bot_admins"].values()]

MOVIE_DATA_FILE_PATH = MAIN_DIRECTORY / "Data" / "movie_data.json"
SETTINGS_FILE_PATH = MAIN_DIRECTORY / "Data" / "settings.json"