from configparser import ConfigParser
from pathlib import Path

from localization import *


MAIN_DIRECTORY = Path(__file__).absolute().parent

cfg = ConfigParser(interpolation=None)

if not Path(MAIN_DIRECTORY / "config.ini").exists():
    language = input("Enter your language (type 'it' or 'en'): ").strip()
    if language not in ["it", "en"]:
        print("Invalid language. Defaulting to English.")
        language = "en"

    print(get_localized_message(language, "CONFIG_FIRST_SETUP"))
    bot_token = input(get_localized_message(language, "CONFIG_TOKEN")).strip()
    user_id = input(get_localized_message(language, "CONFIG_USER_ID")).strip()

    cfg['bot'] = {'bot_token': bot_token}
    cfg['bot_admins'] = {'admin_1': user_id}

    with open(MAIN_DIRECTORY / "config.ini", "w") as configfile:
        cfg.write(configfile)
    
    print(get_localized_message(language, "CONFIG_SUCCESS"))

cfg.read(MAIN_DIRECTORY / "config.ini")

BOT_TOKEN = cfg.get("bot", "bot_token")
BOT_ADMINS = [int(admin) for admin in cfg["bot_admins"].values()]

JSON_FILE_PATH = MAIN_DIRECTORY / "movie_data.json"