import json
import os
import random
import sys
from pathlib import Path

from telegram import Update, constants
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


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
        await update.message.reply_text("Questo comando è disponibile solo nei gruppi.")
        return
    
    if not update.message.from_user.id in [admin.user.id for admin in await context.bot.get_chat_administrators(update.message.chat.id)]:
        await update.message.reply_text("Solo gli amministratori del gruppo possono usare questo comando.")
        return
    
    movie_data = load_movie_data()

    group_id = str(update.message.chat.id)
    if group_id not in movie_data:
        await update.message.reply_text("La lista del gruppo è vuota. Usa il comando /aggiungi per aggiungere dei film.")
        return

    group_movies = movie_data[group_id]

    if not group_movies["users"]:
        await update.message.reply_text("La lista del gruppo è vuota. Usa il comando /aggiungi per aggiungere dei film.")
        return

    all_users = list(group_movies["users"].keys())
    if not all_users:
        await update.message.reply_text("La lista del gruppo è vuota. Usa il comando /aggiungi per aggiungere dei film.")
        return

    random_user_id = random.choice(all_users)
    user_data = group_movies["users"][random_user_id]
    user_name = user_data["first_name"]
    user_movies = user_data["movies"]

    if not user_movies:
        await update.message.reply_text(f"Nessun film aggiunto da {user_name}.")
        return

    random_movie = random.choice(user_movies)
    user_movies.remove(random_movie)
    if len(user_movies) == 0:
        del group_movies["users"][random_user_id]

    save_movie_data(movie_data)
    await update.message.reply_html(f"Film scelto casualmente: <i>{random_movie}</i>\n\n(aggiunto da <b>{user_name}</b>)")


async def add_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == constants.ChatType.PRIVATE:
        await update.message.reply_text("Questo comando è disponibile solo nei gruppi.")
        return
    
    if not context.args:
        await update.message.reply_html("Inserisci almeno un film. Se vuoi puoi inserirne più di uno andando a capo. Esempio:\n\n<code>/aggiungi Film 1\nFilm 2\nFilm 3</code>")
        return
    
    group_id = str(update.message.chat.id)
    user_id = str(update.message.from_user.id)
    first_name = update.message.from_user.first_name

    movies = update.message.text
    movies = movies.replace("/aggiungi \n", "")
    movies = movies.replace("/aggiungi" , "")
    movies = movies.replace("/aggiungi\n", "")
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
    await update.message.reply_text("Fatto!")



async def generate_movie_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == constants.ChatType.PRIVATE:
        await update.message.reply_text("Questo comando è disponibile solo nei gruppi.")
        return
    
    movie_data = load_movie_data()

    group_id = str(update.message.chat.id)
    if group_id not in movie_data:
        await update.message.reply_text("La lista del gruppo è vuota. Usa il comando /aggiungi per aggiungere dei film.")
        return

    group_movies = movie_data[group_id]

    if not group_movies["users"]:
        await update.message.reply_text("La lista del gruppo è vuota. Usa il comando /aggiungi per aggiungere dei film.")
        return

    message = "<b>Lista dei film da vedere</b>\n"

    movie_counter = 1
    for user_id, user_data in group_movies["users"].items():
        first_name = user_data["first_name"]
        movies = user_data["movies"]
        
        message += f"\nScelti da <b>{first_name}</b>:\n"
        for movie in movies:
            message += f"{movie_counter}. {movie}\n"
            movie_counter += 1

    await update.message.reply_html(message)


async def delete_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == constants.ChatType.PRIVATE:
        await update.message.reply_text("Questo comando è disponibile solo nei gruppi.")
        return
    
    help_text = (
        "Per eliminare un film dalla lista, usa il comando /cancella seguito dal numero del film. Esempio: <code>/cancella 5</code>\n\n"
        "Per eliminare tutti i film che hai aggiunto, usa il comando <code>/cancella tutti</code>"
    )

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
                            await update.message.reply_html(f"Il film <code>{movie}</code> è stato eliminato.")
                        else:
                            await update.message.reply_text("Puoi eliminare solo i tuoi film.")
                        return
                    movie_counter += 1
        else:
            if context.args[0] == "tutti":
                if group_id in movie_data and user_id in movie_data[group_id]["users"]:
                    deleted_movies = movie_data[group_id]["users"][user_id]["movies"]

                    del movie_data[group_id]["users"][user_id]

                    if not movie_data[group_id]:
                        del movie_data[group_id]

                    save_movie_data(movie_data)

                    message = "Film eliminati:\n\n<code>"
                    for movie in deleted_movies:
                        message += f"{movie}\n"
                    await update.message.reply_html(message + "</code>")
                else:
                    await update.message.reply_text("Non hai film da eliminare.")
            else:
                await update.message.reply_html(help_text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "<b>Comandi disponibili:</b>\n"
        "/aggiungi: Aggiunge uno o più film alla lista.\n"
        "/cancella: Cancella il film con il numero specificato, oppure tutti i film che hai aggiunto.\n"
        "/lista: Mostra la lista di tutti i film da vedere.\n"
        "/scegli: Sceglie casualmente un film dalla lista. (solo per admin del gruppo)\n"
        "/letterboxd: Link alla lista di film che abbiamo visto in passato.\n"
    )
    await update.message.reply_html(help_text)


async def letterboxd_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_data = load_movie_data()
    group_id = str(update.message.chat.id)
    
    letterboxd_link = movie_data.get(group_id, {}).get("letterboxd_link", "")

    if letterboxd_link:
        await update.message.reply_text(f"{letterboxd_link}")
    else:
        await update.message.reply_text("Il link a Letterboxd non è stato impostato per questo gruppo.")


async def set_letterboxd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == constants.ChatType.PRIVATE:
        await update.message.reply_text("Questo comando è disponibile solo nei gruppi.")
        return
    
    if not context.args:
        await update.message.reply_text("Per utilizzare questo comando, inserisci il link di Letterboxd.")
        return
    
    group_id = str(update.message.chat.id)
    letterboxd_link = context.args[0]  # Assuming the link is provided as the first argument
    
    movie_data = load_movie_data()
    if group_id not in movie_data:
        movie_data[group_id] = {}
    
    movie_data[group_id]["letterboxd_link"] = letterboxd_link
    save_movie_data(movie_data)
    
    await update.message.reply_text("Il link di Letterboxd è stato impostato correttamente.")



async def send_backup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_admin(update.message.from_user.id):
        backup_file_path = main_directory / "movie_data.json"

        try:
            with open(backup_file_path, "rb") as file:
                await context.bot.send_document(chat_id=update.message.from_user.id, document=file)
        except Exception as e:
            await update.message.reply_text("An error occurred while sending the backup.")


async def restart_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_admin(update.message.from_user.id):
        await update.message.reply_text("Restarting...")
        args = sys.argv[:]
        args.insert(0, sys.executable)
        os.chdir(os.getcwd())
        os.execv(sys.executable, args)


if __name__ == '__main__':
    random_movie_handler = CommandHandler('scegli', random_movie)
    application.add_handler(random_movie_handler, 0)

    add_movies_handler = CommandHandler('aggiungi', add_movies)
    application.add_handler(add_movies_handler, 1)

    generate_movie_list_handler = CommandHandler('lista', generate_movie_list)
    application.add_handler(generate_movie_list_handler, 2)

    delete_movies_handler = CommandHandler('cancella', delete_movies)
    application.add_handler(delete_movies_handler, 3)

    help_command_handler = CommandHandler(('help', 'start'), help_command)
    application.add_handler(help_command_handler, 4)

    letterboxd_list_handler = CommandHandler('letterboxd', letterboxd_list)
    application.add_handler(letterboxd_list_handler, 5)

    set_letterboxd_handler = CommandHandler('setletterboxd', set_letterboxd)
    application.add_handler(set_letterboxd_handler, 6)

    send_backup_handler = CommandHandler('backup', send_backup)
    application.add_handler(send_backup_handler, 98)

    restart_handler = CommandHandler('restart', restart_bot)
    application.add_handler(restart_handler, 99)

    application.run_polling(drop_pending_updates=True)
