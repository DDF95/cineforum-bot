from typing import Optional, Tuple

from telegram import ChatMember, ChatMemberUpdated, Update, constants
from telegram.ext import ContextTypes

from localization import *
from utils import load_settings, save_settings


async def set_welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == constants.ChatType.PRIVATE:
        await update.message.reply_text(get_localized_message(update, "COMMAND_NOT_AVAILABLE_IN_PRIVATE"))
        return
    
    if not update.message.from_user.id in [admin.user.id for admin in await context.bot.get_chat_administrators(update.message.chat.id)]:
        await update.message.reply_text(get_localized_message(update, "ADMIN_ONLY"))
        return

    if not context.args:
        await update.message.reply_html(get_localized_message(update, "SET_WELCOME_MESSAGE_USAGE"))
        return
    
    chat_id = str(update.message.chat.id)
    welcome_message = update.message.text
    welcome_message = welcome_message.replace("/setbenvenuto ", "")
    welcome_message = welcome_message.replace("/setwelcome", "")

    settings = load_settings(chat_id)
    settings["welcome_message"] = welcome_message
    save_settings(chat_id, settings)

    await update.message.reply_html(get_localized_message(update, "SETTINGS_WELCOME_MESSAGE_SET"))


def extract_status_change(chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = old_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (old_status == ChatMember.RESTRICTED and old_is_member is True)
    is_member = new_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (new_status == ChatMember.RESTRICTED and new_is_member is True)

    return was_member, is_member


async def send_welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    settings = load_settings(update.effective_chat.id)
    toggle_welcome_message = settings["toggle_welcome_message"]

    if toggle_welcome_message == "✅":
        result = extract_status_change(update.chat_member)
        if result is None:
            return

        was_member, is_member = result

        if not was_member and is_member:
            if ":name:" in settings["welcome_message"]:
                await update.effective_chat.send_message(settings["welcome_message"].replace(":name:", update.effective_user.first_name), parse_mode=constants.ParseMode.HTML)
            else:
                await update.effective_chat.send_message(settings["welcome_message"], parse_mode=constants.ParseMode.HTML)


async def show_welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == constants.ChatType.PRIVATE:
        await update.message.reply_text(get_localized_message(update, "COMMAND_NOT_AVAILABLE_IN_PRIVATE"))
        return
    
    if not update.message.from_user.id in [admin.user.id for admin in await context.bot.get_chat_administrators(update.message.chat.id)]:
        await update.message.reply_text(get_localized_message(update, "ADMIN_ONLY"))
        return
    
    settings = load_settings(update.message.chat.id)
    welcome_message = settings["welcome_message"]
    
    if welcome_message == "":
        await update.message.reply_text(get_localized_message(update, "SETTINGS_WELCOME_MESSAGE_NOT_SET"))
    else:
        await update.message.reply_text(welcome_message)


async def delete_welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == constants.ChatType.PRIVATE:
        await update.message.reply_text(get_localized_message(update, "COMMAND_NOT_AVAILABLE_IN_PRIVATE"))
        return
    
    if not update.message.from_user.id in [admin.user.id for admin in await context.bot.get_chat_administrators(update.message.chat.id)]:
        await update.message.reply_text(get_localized_message(update, "ADMIN_ONLY"))
        return
    
    settings = load_settings(update.message.chat.id)
    settings["welcome_message"] = ""
    save_settings(update.message.chat.id, settings)
    
    await update.message.reply_text(get_localized_message(update, "SETTINGS_WELCOME_MESSAGE_DELETED"))