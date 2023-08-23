from telegram import Update, constants
from telegram.ext import ContextTypes

from localization import *
from utils import load_movie_data, load_settings, save_movie_data


async def delete_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == constants.ChatType.PRIVATE:
        await update.message.reply_text(get_localized_message(update, "COMMAND_NOT_AVAILABLE_IN_PRIVATE"))
        return
    
    help_text = get_localized_message(update, "DELETE_MOVIES_USAGE")

    movie_data = load_movie_data()

    settings = load_settings(update.message.chat.id)
    delete_admin_only = settings["delete_admin_only"]

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
                        if delete_admin_only == "✅":
                            if is_group_admin or user_id == str(update.message.from_user.id):
                                movies.remove(movie)
                                save_movie_data(movie_data)
                                await update.message.reply_html(get_localized_message(update, "DELETE_MOVIES_SUCCESS", movie=movie))
                            else:
                                await update.message.reply_text(get_localized_message(update, "DELETE_MOVIES_OWN_ONLY"))
                            return
                        else:
                            movies.remove(movie)
                            save_movie_data(movie_data)
                            await update.message.reply_html(get_localized_message(update, "DELETE_MOVIES_SUCCESS", movie=movie))
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