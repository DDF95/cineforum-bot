import random

from telegram import Update, constants
from telegram.ext import ContextTypes

from localization import *
from utils import load_movie_data, load_settings, save_movie_data


async def random_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == constants.ChatType.PRIVATE:
        await update.message.reply_text(get_localized_message(update, "COMMAND_NOT_AVAILABLE_IN_PRIVATE"))
        return
    
    settings = load_settings(update.message.chat.id)
    choose_admin_only = settings["choose_admin_only"]
    movie_list_per_user = settings["movie_list_per_user"]

    if choose_admin_only == "✅":
        if not update.message.from_user.id in [admin.user.id for admin in await context.bot.get_chat_administrators(update.message.chat.id)]:
            await update.message.reply_text(get_localized_message(update, "ADMIN_ONLY"))
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

    if movie_list_per_user == "✅":
        all_users = list(group_movies["users"].keys())
        if not all_users:
            await update.message.reply_text(get_localized_message(update, "MOVIE_LIST_EMPTY"))
            return
        
        random_user_id = random.choice(all_users)
        user_data = group_movies["users"][random_user_id]
        user_name = user_data["first_name"]
        user_movies = user_data["movies"]

        random_movie = random.choice(user_movies)
        user_movies.remove(random_movie)
        if len(user_movies) == 0:
            del group_movies["users"][random_user_id]
    else:
        all_movies = [movie for user_data in group_movies["users"].values() for movie in user_data["movies"]]
        if not all_movies:
            await update.message.reply_text(get_localized_message(update, "MOVIE_LIST_EMPTY"))
            return
        
        random_movie = random.choice(all_movies)
        for user_data in group_movies["users"].values():
            if random_movie in user_data["movies"]:
                user_name = user_data["first_name"]
                user_data["movies"].remove(random_movie)
                break
            
    save_movie_data(movie_data)

    await update.message.reply_html(get_localized_message(update, "RANDOM_MOVIE_CHOSEN", random_movie=random_movie, user_name=user_name))