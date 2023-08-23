from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Update,
                      constants)
from telegram.ext import ContextTypes

from localization import *
from utils import load_settings, save_settings


SETTING_KEYS = {
    "toggle_welcome_message": "SETTINGS_TOGGLE_WELCOME_MESSAGE",
    "movie_list_per_user": "SETTINGS_MOVIE_LIST_PER_USER",
    "choose_admin_only": "SETTINGS_CHOOSE_ADMIN_ONLY",
    "delete_admin_only": "SETTINGS_DELETE_ADMIN_ONLY",
}


async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == constants.ChatType.PRIVATE:
        await update.message.reply_text(get_localized_message(update, "COMMAND_NOT_AVAILABLE_IN_PRIVATE"))
        return

    if not update.message.from_user.id in [admin.user.id for admin in await context.bot.get_chat_administrators(update.message.chat.id)]:
        await update.message.reply_text(get_localized_message(update, "ADMIN_ONLY"))
        return
    
    chat_id = update.message.chat.id
    settings = load_settings(chat_id)

    keyboard = []
    for key, message_key in SETTING_KEYS.items():
        setting_value = settings[key]
        keyboard.append([InlineKeyboardButton(get_localized_message(update, message_key) + ": " + setting_value, callback_data=key)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_html(get_localized_message(update, "SETTINGS_HEADER"), reply_markup=reply_markup)


async def settings_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    query_data = query.data

    if not query.from_user.id in [admin.user.id for admin in await context.bot.get_chat_administrators(query.message.chat_id)]:
        await query.answer(get_localized_message(update, "ADMIN_ONLY"))
        return
    
    if query_data in SETTING_KEYS:
        chat_id = query.message.chat_id
        key = query_data
        settings = load_settings(chat_id)
        settings[key] = "❌" if settings[key] == "✅" else "✅"

        save_settings(chat_id, settings)

        await query.answer(get_localized_message(update, "SETTINGS_SAVED"))

    await update_settings_message(update, context)


async def update_settings_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    keyboard = []
    for key, message_key in SETTING_KEYS.items():
        setting_value = load_settings(query.message.chat_id)[key]
        keyboard.append([InlineKeyboardButton(get_localized_message(update, message_key) + ": " + setting_value, callback_data=key)])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=get_localized_message(update, "SETTINGS_HEADER"),
        reply_markup=reply_markup,
        parse_mode=constants.ParseMode.HTML
    )