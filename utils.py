import json

import config


def is_admin(user_id: int):
    if user_id in config.BOT_ADMINS:
        return True
    else:
        return False


def load_movie_data():
    if config.MOVIE_DATA_FILE_PATH.exists():
        with open(config.MOVIE_DATA_FILE_PATH, "r") as file:
            return json.load(file)
    return {}


def save_movie_data(data):
    with open(config.MOVIE_DATA_FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)


# settings
DEFAULT_SETTINGS = {
    "toggle_welcome_message": "❌",
    "movie_list_per_user": "✅",
    "choose_admin_only": "✅",
    "delete_admin_only": "✅",
    "welcome_message": "",
}


def load_settings(chat_id):
    try:
        with open(config.SETTINGS_FILE_PATH, "r") as file:
            settings = json.load(file)
            return settings.get(str(chat_id), DEFAULT_SETTINGS)
    except FileNotFoundError:
        save_settings(chat_id, DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS


def save_settings(chat_id, settings):
    try:
        with open(config.SETTINGS_FILE_PATH, "r") as file:
            all_settings = json.load(file)
    except FileNotFoundError:
        all_settings = {}
    
    all_settings[str(chat_id)] = settings
    
    with open(config.SETTINGS_FILE_PATH, "w") as file:
        json.dump(all_settings, file, indent=4)