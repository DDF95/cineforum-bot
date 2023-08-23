from telegram import Update, constants
from telegram.ext import ContextTypes

from localization import *
from utils import load_movie_data, load_settings


async def generate_movie_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == constants.ChatType.PRIVATE:
        await update.message.reply_text(get_localized_message(update, "COMMAND_NOT_AVAILABLE_IN_PRIVATE"))
        return
    
    movie_data = load_movie_data()

    group_id = str(update.message.chat.id)
    if group_id not in movie_data:
        await update.message.reply_text(get_localized_message(update, "MOVIE_LIST_EMPTY"))
        return

    group_movies = movie_data[group_id]

    if not group_movies["users"]:
        await update.message.reply_text(get_localized_message(update, "MOVIE_LIST_EMPTY"))
        return

    message = get_localized_message(update, "MOVIE_LIST_HEADER")

    settings = load_settings(update.message.chat.id)
    movie_list_per_user = settings["movie_list_per_user"]

    movie_counter = 1
    for user_id, user_data in group_movies["users"].items():
        first_name = user_data["first_name"]
        movies = user_data["movies"]
        
        if movie_list_per_user == "✅":
            message += get_localized_message(update, "MOVIE_LIST_USERS", first_name=first_name)
        for movie in movies:
            message += f"{movie_counter}. {movie}\n"
            movie_counter += 1

    await update.message.reply_html(message)