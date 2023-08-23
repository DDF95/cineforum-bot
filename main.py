import os
import sys

from telegram import Update, constants
from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          ChatMemberHandler, CommandHandler, ContextTypes)

import config
from add_movies import add_movies
from delete_movies import delete_movies
from generate_movie_list import generate_movie_list
from localization import *
from random_movie import random_movie
from settings import settings_button, show_settings
from utils import is_admin, load_movie_data, save_movie_data
from welcome_message import (delete_welcome_message, send_welcome_message,
                             set_welcome_message, show_welcome_message)


application = ApplicationBuilder().token(config.BOT_TOKEN).build()


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
        

async def show_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("https://github.com/DDF95/cineforum-bot")


async def send_backup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_admin(update.message.from_user.id):
        try:
            with open(config.MOVIE_DATA_FILE_PATH, "rb") as file:
                await context.bot.send_document(chat_id=update.message.from_user.id, document=file)
            with open(config.SETTINGS_FILE_PATH, "rb") as file:
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

    set_welcome_message_handler = CommandHandler(('setwelcome', 'setbenvenuto'), set_welcome_message)
    application.add_handler(set_welcome_message_handler, 7)

    send_welcome_message_handler = ChatMemberHandler(send_welcome_message, ChatMemberHandler.CHAT_MEMBER)
    application.add_handler(send_welcome_message_handler, 8)

    show_welcome_message_handler = CommandHandler(('benvenuto', 'welcome'), show_welcome_message)
    application.add_handler(show_welcome_message_handler, 9)

    delete_welcome_message_handler = CommandHandler(('cancellabenvenuto', 'deletewelcome'), delete_welcome_message)
    application.add_handler(delete_welcome_message_handler, 10)

    show_about_handler = CommandHandler(('info', 'about'), show_about)
    application.add_handler(show_about_handler, 95)

    show_settings_handler = CommandHandler(('impostazioni', 'settings'), show_settings)
    application.add_handler(show_settings_handler, 96)

    settings_button_handler = CallbackQueryHandler(settings_button)
    application.add_handler(settings_button_handler, 97)

    send_backup_handler = CommandHandler('backup', send_backup)
    application.add_handler(send_backup_handler, 98)

    restart_handler = CommandHandler(('riavvia', 'restart'), restart_bot)
    application.add_handler(restart_handler, 99)

    allowed_updates = [Update.MESSAGE, Update.CALLBACK_QUERY, Update.CHAT_MEMBER]
    application.run_polling(drop_pending_updates=True, allowed_updates=allowed_updates)