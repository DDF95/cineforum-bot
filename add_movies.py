from telegram import Update, constants
from telegram.ext import ContextTypes

from localization import *
from utils import load_movie_data, save_movie_data


async def add_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == constants.ChatType.PRIVATE:
        await update.message.reply_text(get_localized_message(update, "COMMAND_NOT_AVAILABLE_IN_PRIVATE"))
        return
    
    if not context.args:
        await update.message.reply_html(get_localized_message(update, "ADD_MOVIES_USAGE"))
        return
    
    group_id = str(update.message.chat.id)
    user_id = str(update.message.from_user.id)
    first_name = update.message.from_user.first_name

    movies = update.message.text
    movies = movies.replace("/aggiungi \n", "")
    movies = movies.replace("/aggiungi" , "")
    movies = movies.replace("/aggiungi\n", "")
    movies = movies.replace("/add \n", "")
    movies = movies.replace("/add" , "")
    movies = movies.replace("/add\n", "")
    movies = movies.split("\n")
    movies = [movie.lstrip("- ") for movie in movies if movie.strip()]

    movie_data = load_movie_data()
    if group_id not in movie_data:
        movie_data[group_id] = {
            "letterboxd_link": "",
            "users": {}
        }
    if user_id not in movie_data[group_id]["users"]:
        movie_data[group_id]["users"][user_id] = {"first_name": first_name, "movies": []}
    
    movie_data[group_id]["users"][user_id]["movies"].extend(movies)

    save_movie_data(movie_data)
    await update.message.reply_text(get_localized_message(update, "ADD_MOVIES_SUCCESS"))