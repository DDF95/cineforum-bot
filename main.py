import json
import os
import random
import sys
from pathlib import Path

from telegram import Update, constants
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from localization import *


application = ApplicationBuilder().token("INSERT BOT TOKEN HERE").build()

main_directory = Path(__file__).absolute().parent
json_file_path = main_directory / "movie_data.json"


def is_admin(user_id: int):
    if user_id == 14770193:
        return True
    else:
        return False


def load_movie_data():
    if json_file_path.exists():
        with open(json_file_path, "r") as file:
            return json.load(file)
    return {}


def save_movie_data(data):
    with open(json_file_path, "w") as file:
        json.dump(data, file, indent=4)


async def random_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == constants.ChatType.PRIVATE:
        await update.message.reply_text(get_localized_message(update, "COMMAND_NOT_AVAILABLE_IN_PRIVATE"))
        return
    
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

    save_movie_data(movie_data)
    await update.message.reply_html(get_localized_message(update, "RANDOM_MOVIE", random_movie=random_movie, user_name=user_name))


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

    movie_counter = 1
    for user_id, user_data in group_movies["users"].items():
        first_name = user_data["first_name"]
        movies = user_data["movies"]
        
        message += get_localized_message(update, "MOVIE_LIST_USERS", first_name=first_name)
        for movie in movies:
            message += f"{movie_counter}. {movie}\n"
            movie_counter += 1

    await update.message.reply_html(message)


async def delete_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == constants.ChatType.PRIVATE:
        await update.message.reply_text(get_localized_message(update, "COMMAND_NOT_AVAILABLE_IN_PRIVATE"))
        return
    
    help_text = get_localized_message(update, "DELETE_MOVIES_USAGE")

    movie_data = load_movie_data()

    group_id = str(update.message.chat.id)
    user_id = str(update.message.from_user.id)
    is_group_admin = update.message.from_user.id in [admin.user.id for admin in await context.bot.get_chat_administrators(update.message.chat.id)]

    if not context.args:
        await update.message.reply_html(help_text)
    else:
        if context.args[0].isdigit():
            movie_number = int(context.args[0])

            movie_list = []
            for user_id, user_data in movie_data.get(group_id, {}).get("users", {}).items():
                movies = user_data["movies"]
                movie_list.append((user_id, movies))

            movie_counter = 1
            for user_id, movies in movie_list:
                for movie in movies:
                    if movie_counter == movie_number:
                        if is_group_admin or user_id == str(update.message.from_user.id):
                            movies.remove(movie)
                            save_movie_data(movie_data)
                            await update.message.reply_html(get_localized_message(update, "DELETE_MOVIES_SUCCESS", movie=movie))
                        else:
                            await update.message.reply_text(get_localized_message(update, "DELETE_MOVIES_OWN_ONLY"))
                        return
                    movie_counter += 1
        else:
            if context.args[0] == "tutti" or context.args[0] == "all":
                if group_id in movie_data and user_id in movie_data[group_id]["users"]:
                    deleted_movies = movie_data[group_id]["users"][user_id]["movies"]

                    del movie_data[group_id]["users"][user_id]

                    if not movie_data[group_id]:
                        del movie_data[group_id]

                    save_movie_data(movie_data)

                    message = get_localized_message(update, "DELETE_MOVIES_HEADER")
                    for movie in deleted_movies:
                        message += f"{movie}\n"
                    await update.message.reply_html(message + "</code>")
                else:
                    await update.message.reply_text(get_localized_message(update, "DELETE_MOVIES_EMPTY"))
            else:
                await update.message.reply_html(help_text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = get_localized_message(update, "HELP_COMMAND")

    if is_admin(update.message.from_user.id):
        help_text += get_localized_message(update, "HELP_COMMAND_BOT_ADMIN")
        
    await update.message.reply_html(help_text)


async def letterboxd_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_data = load_movie_data()
    group_id = str(update.message.chat.id)
    
    letterboxd_link = movie_data.get(group_id, {}).get("letterboxd_link", "")

    if letterboxd_link:
        await update.message.reply_text(f"{letterboxd_link}")
    else:
        await update.message.reply_text(get_localized_message(update, "LETTERBOXD_LINK_NOT_SET"))


async def set_letterboxd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == constants.ChatType.PRIVATE:
        await update.message.reply_text(get_localized_message(update, "COMMAND_NOT_AVAILABLE_IN_PRIVATE"))
        return
    
    if not update.message.from_user.id in [admin.user.id for admin in await context.bot.get_chat_administrators(update.message.chat.id)]: 
        await update.message.reply_text(get_localized_message(update, "SET_LETTERBOXD_LINK_ADMIN_ONLY"))
        return

    if not context.args:
        await update.message.reply_html(get_localized_message(update, "SET_LETTERBOXD_LINK_USAGE"))
        return
    
    group_id = str(update.message.chat.id)
    letterboxd_link = context.args[0]
    
    movie_data = load_movie_data()
    if group_id not in movie_data:
        movie_data[group_id] = {}
    
    movie_data[group_id]["letterboxd_link"] = letterboxd_link
    save_movie_data(movie_data)
    
    await update.message.reply_text(get_localized_message(update, "SET_LETTERBOXD_LINK_SUCCESS"))


async def send_backup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_admin(update.message.from_user.id):
        backup_file_path = main_directory / "movie_data.json"

        try:
            with open(backup_file_path, "rb") as file:
                await context.bot.send_document(chat_id=update.message.from_user.id, document=file)
        except Exception as e:
            await update.message.reply_text(get_localized_message(update, "BACKUP_ERROR"))


async def restart_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_admin(update.message.from_user.id):
        await update.message.reply_text(get_localized_message(update, "RESTARTING"))
        args = sys.argv[:]
        args.insert(0, sys.executable)
        os.chdir(os.getcwd())
        os.execv(sys.executable, args)


if __name__ == '__main__':
    random_movie_handler = CommandHandler(('scegli', 'choose'), random_movie)
    application.add_handler(random_movie_handler, 0)

    add_movies_handler = CommandHandler(('aggiungi', 'add'), add_movies)
    application.add_handler(add_movies_handler, 1)

    generate_movie_list_handler = CommandHandler(('lista', 'list'), generate_movie_list)
    application.add_handler(generate_movie_list_handler, 2)

    delete_movies_handler = CommandHandler(('cancella', 'delete'), delete_movies)
    application.add_handler(delete_movies_handler, 3)

    help_command_handler = CommandHandler(('start', 'aiuto', 'help'), help_command)
    application.add_handler(help_command_handler, 4)

    letterboxd_list_handler = CommandHandler('letterboxd', letterboxd_list)
    application.add_handler(letterboxd_list_handler, 5)

    set_letterboxd_handler = CommandHandler('setletterboxd', set_letterboxd)
    application.add_handler(set_letterboxd_handler, 6)

    send_backup_handler = CommandHandler('backup', send_backup)
    application.add_handler(send_backup_handler, 98)

    restart_handler = CommandHandler(('riavvia', 'restart'), restart_bot)
    application.add_handler(restart_handler, 99)

    application.run_polling(drop_pending_updates=True)
