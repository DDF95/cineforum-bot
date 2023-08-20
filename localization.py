MESSAGES = {
    "it": {
        # misc
        "COMMAND_NOT_AVAILABLE_IN_PRIVATE": "Questo comando è disponibile solo nei gruppi.",
        "ADMIN_ONLY": "Solo lx admin del gruppo possono usare questo comando.",
        "MOVIE_LIST_EMPTY": "La lista dei film del gruppo è vuota. Usa il comando /aggiungi per aggiungere film.",

        # /scegli
        "RANDOM_MOVIE_CHOSEN": "Film scelto casualmente: <i>{random_movie}</i>\n\n(aggiunto da <b>{user_name}</b>)",

        # /aggiungi
        "ADD_MOVIES_USAGE": "Inserisci almeno un film. Puoi inserirne più di uno separandoli con una nuova riga. Esempio:\n\n<code>/aggiungi Film 1\nFilm 2\nFilm 3</code>",
        "ADD_MOVIES_SUCCESS": "Fatto!",

        # /lista
        "MOVIE_LIST_HEADER": "<b>Lista dei film da vedere</b>\n",
        "MOVIE_LIST_USERS": "\nScelti da <b>{first_name}</b>:\n",

        # /cancella
        "DELETE_MOVIES_USAGE": (
            "Per eliminare un film dalla lista, usa il comando /cancella seguito dal numero del film. Esempio: <code>/cancella 5</code>\n\n"
            "Per eliminare tutti i film che hai aggiunto, usa il comando <code>/cancella tutti</code>"
        ),
        "DELETE_MOVIES_OWN_ONLY": "Puoi eliminare solo i tuoi film.",
        "DELETE_MOVIES_SUCCESS": "Il film <code>{movie}</code> è stato eliminato.",
        "DELETE_MOVIES_HEADER": "Film eliminati:\n\n<code>",
        "DELETE_MOVIES_EMPTY": "Non hai film da eliminare.",

        # help
        "HELP_COMMAND": (
            "<b>Comandi disponibili:</b>\n"
            "/aggiungi: Aggiunge uno o più film alla lista.\n"
            "/cancella: Cancella il film con il numero specificato, oppure tutti i film che hai aggiunto.\n"
            "/lista: Mostra la lista di tutti i film da vedere.\n"
            "/scegli: Sceglie casualmente un film dalla lista. (solo per admin del gruppo)\n"
            "/letterboxd: Mostra il link alla lista Letterboxd del gruppo.\n"
            "/setletterboxd: Imposta il link a Letterboxd per il gruppo. (solo per admin del gruppo)\n"
        ),
        "HELP_COMMAND_BOT_ADMIN": (
            "\n<b>Comandi del bot:</b>\n"
            "/riavvia: Riavvia il bot.\n"
            "/backup: Esegue il backup del database.\n"
        ),

        # /letterboxd
        "LETTERBOXD_LINK_NOT_SET": "Il link a Letterboxd per questo gruppo non è stato ancora impostato. Usa il comando /setletterboxd per impostarlo.",

        # /setletterboxd
        "SET_LETTERBOXD_LINK_ADMIN_ONLY": "Solo lx admin del gruppo possono impostare il link di Letterboxd.",
        "SET_LETTERBOXD_LINK_USAGE": "Inserisci il link a Letterboxd per il gruppo. Esempio: <code>/setletterboxd https://letterboxd.com/username/list/list-name/</code>",
        "SET_LETTERBOXD_LINK_SUCCESS": "Il link a Letterboxd è stato impostato.",

        # bot admin
        "BACKUP_ERROR": "Si è verificato un errore durante il backup del database.",
        "RESTARTING": "Riavvio in corso...",

        # config
        "CONFIG_FIRST_SETUP": "Se non lo hai già fatto, crea un bot con @BotFather e ottieni il token. Inoltre dovrai ottenere il tuo ID utente con @userinfobot (questo è necessario per comandi come /riavvia).",
        "CONFIG_TOKEN": "Inserisci il token del bot: ",
        "CONFIG_USER_ID": "Inserisci il tuo ID utente: ",
        "CONFIG_SUCCESS": "Configurazione completata! Il bot è ora attivo. Se riscontri problemi, elimina il file 'config.ini' e riavvia il bot.",
    },
    "en": {
        # misc
        "COMMAND_NOT_AVAILABLE_IN_PRIVATE": "This command is only available in groups.",
        "ADMIN_ONLY": "Inly group admins can use this command.",
        "MOVIE_LIST_EMPTY": "The group's movie list is empty. Use the /add command to add movies.",

        # /choose
        "RANDOM_MOVIE_CHOSEN": "Randomly chosen movie: <i>{random_movie}</i>\n\n(added by <b>{user_name}</b>)",

        # /add
        "ADD_MOVIES_USAGE": "Enter at least one movie. You can enter multiple movies by adding line breaks. Example:\n\n<code>/add Movie 1\nMovie 2\nMovie 3</code>",
        "ADD_MOVIES_SUCCESS": "Done!",

        # /list
        "MOVIE_LIST_HEADER": "<b>List of movies to watch</b>\n",
        "MOVIE_LIST_USERS": "\nChoosen by <b>{first_name}</b>:\n",

        # /delete
        "DELETE_MOVIES_USAGE": (
            "To delete a movie from the list, use the /delete command followed by the movie number. Example: <code>/delete 5</code>\n\n"
            "To delete all movies you added, use the command <code>/delete all</code>"
        ),
        "DELETE_MOVIES_OWN_ONLY": "You can only delete your own movies.",
        "DELETE_MOVIES_SUCCESS": "The movie <code>{movie}</code> has been deleted.",
        "DELETE_MOVIES_HEADER": "Deleted movies:\n\n<code>",
        "DELETE_MOVIES_EMPTY": "You don't have any movies to delete.",

        # help
        "HELP_COMMAND": (
            "<b>Available commands:</b>\n"
            "/add: Add one or more movies to the list.\n"
            "/delete: Delete the movie with the specified number, or all movies you added.\n"
            "/list: Show the list of all movies to watch.\n"
            "/choose: Choose a random movie from the list. (only for group admins)\n"
            "/letterboxd: Show the link to the group's Letterboxd list.\n"
            "/setletterboxd: Set the Letterboxd link for the group. (only for group admins)\n"
        ),
        "HELP_COMMAND_BOT_ADMIN": (
            "\n<b>Bot commands:</b>\n"
            "/restart: Restart the bot.\n"
            "/backup: Backup the database.\n"
        ),

        # /letterboxd
        "LETTERBOXD_LINK_NOT_SET": "The Letterboxd link for this group has not been set yet. Use the /setletterboxd command to set it.",

        # /setletterboxd
        "SET_LETTERBOXD_LINK_ADMIN_ONLY": "Only group admins can set the Letterboxd link.",
        "SET_LETTERBOXD_LINK_USAGE": "Enter the Letterboxd link for the group. Example: <code>/setletterboxd https://letterboxd.com/username/list/list-name/</code>",
        "SET_LETTERBOXD_LINK_SUCCESS": "The Letterboxd link has been set.",

        # bot admin
        "BACKUP_ERROR": "An error occurred while backing up the database.",
        "RESTARTING": "Restarting...",

        # config
        "CONFIG_FIRST_SETUP": "If you haven't already, create a bot with @BotFather and get your bot token. Also, you need to get your user ID with @userinfobot (this is needed for commands like /restart).)",
        "CONFIG_TOKEN": "Enter your bot token: ",
        "CONFIG_USER_ID": "Enter your user ID: ",
        "CONFIG_SUCCESS": "Configuration completed! The bot is now running. If you encounter any issues, delete the 'config.ini' file and restart the bot.",
    }
}

def get_localized_message(update, message_key, **kwargs):
    if update in ["it", "en"]:
        language_code = update
    else:
        language_code = update.effective_user.language_code
    try:
        return MESSAGES[language_code][message_key].format(**kwargs)
    except:
        return MESSAGES['en'][message_key].format(**kwargs)
