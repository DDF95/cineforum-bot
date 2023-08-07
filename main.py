import json
import os
import random
import sys
from pathlib import Path

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


application = ApplicationBuilder().token("INSERT BOT TOKEN HERE").build()

main_directory = Path(__file__).absolute().parent
json_file_path = main_directory / "movie_data.json"


def is_admin(user_id: int):
    if user_id == 14770193:
        return True
    else:
        return False


async def random_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_admin(update.message.from_user.id):
        movie_data = load_movie_data()

        all_movies = []
        movie_users = {}
        for user_id, user_data in movie_data.items():
            for movie in user_data["movies"]:
                all_movies.append(movie)
                movie_users[movie] = user_data["first_name"]

        if not all_movies:
            await update.message.reply_text("Nessun film nella lista.")
            return

        random_movie = random.choice(all_movies)
        user_who_added = movie_users.get(random_movie, "Sconosciuto")
        
        for user_id, user_data in movie_data.items():
            if random_movie in user_data["movies"]:
                user_data["movies"].remove(random_movie)
        
        save_movie_data(movie_data)
        await update.message.reply_html(f"Film scelto casualmente: <i>{random_movie}</i>\n\n(aggiunto da <b>{user_who_added}</b>)")


def load_movie_data():
    if json_file_path.exists():
        with open(json_file_path, "r") as file:
            return json.load(file)
    return {}


def save_movie_data(data):
    with open(json_file_path, "w") as file:
        json.dump(data, file, indent=4)


async def add_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_html("Inserisci almeno un film. Se vuoi puoi inserirne più di uno andando a capo. Esempio:\n\n<code>/aggiungi Film 1\nFilm 2\nFilm 3</code>")
        return

    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    
    movies = update.message.text
    movies = movies.replace("/aggiungi \n", "")
    movies = movies.replace("/aggiungi" , "")
    movies = movies.replace("/aggiungi\n", "")
    movies = movies.split("\n")
    movies = [movie.lstrip("- ") for movie in movies if movie.strip()]

    movie_data = load_movie_data()
    if str(user_id) not in movie_data:
        movie_data[str(user_id)] = {"first_name": first_name, "movies": []}
    movie_data[str(user_id)]["movies"].extend(movies)

    save_movie_data(movie_data)
    await update.message.reply_text("Fatto!")


async def generate_movie_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_data = load_movie_data()

    if not movie_data:
        await update.message.reply_text("La lista è vuota. Usa il comando /aggiungi per aggiungere dei film.")
        return

    movie_list = []
    for user_id, user_data in movie_data.items():
        first_name = user_data["first_name"]
        movies = user_data["movies"]
        movie_list.append((first_name, movies))

    movie_list.sort(key=lambda x: x[0])
    message = "<b>Lista dei film da vedere</b>\n"
    
    movie_counter = 1
    for first_name, movies in movie_list:
        message += f"\nScelti da <b>{first_name}</b>:\n"
        for movie in movies:
            message += f"{movie_counter}. {movie}\n"
            movie_counter += 1
    message += f"\n<i>Per aggiungere un film alla lista usa il comando /aggiungi</i>"
            
    await update.message.reply_html(message)


async def delete_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_data = load_movie_data()

    user_id = str(update.message.from_user.id)
    if user_id in movie_data:
        deleted_movies = movie_data.pop(user_id)["movies"]
        save_movie_data(movie_data)

        message = "Film eliminati:\n"
        for idx, movie in enumerate(deleted_movies, start=1):
            message += f"{idx}. {movie}\n"
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("Non hai film da eliminare")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "<b>Comandi disponibili:</b>\n"
        "/aggiungi: Aggiunge uno o più film alla lista.\n"
        "/cancella: Elimina tutti i film che hai aggiunto.\n"
        "/lista: Mostra la lista di tutti i film da vedere.\n"
        "/scegli: Sceglie casualmente un film dalla lista. (Admin only)\n"
        "/letterboxd: Link alla lista di film che abbiamo visto in passato.\n"
    )
    await update.message.reply_html(help_text)


async def letterboxd_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Questi sono i film che abbiamo visto in passato: https://letterboxd.com/alannadi/list/every-night-is-movie-night-cineforum/")


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

    send_backup_handler = CommandHandler('backup', send_backup)
    application.add_handler(send_backup_handler, 98)

    restart_handler = CommandHandler('restart', restart_bot)
    application.add_handler(restart_handler, 99)

    application.run_polling(drop_pending_updates=True)
