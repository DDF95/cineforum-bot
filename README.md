# cineforum-bot
`cineforum-bot` is a Telegram bot designed to help manage a cineforum group. It allows users to create a list of movies they want to watch together, choose random movies, and more.

## Usage
1. Start a chat with the bot or invite it to your cineforum group.
2. The following commands are available:
   - `/aggiungi <film>`: Add one or more movies to your list.
   - `/cancella`: Delete the movie associated to a number in the list, or delete all your movies.
   - `/scegli`: Choose a random movie from the entire list (Admin only).
   - `/lista`: Generate a list of all movies.
   - `/letterboxd`: Show the group's Letterboxd link.
   - `/setletterboxd`: Set the group's Letterboxd link.
   - `/restart`: Restarts the bot.
   - `/help`: Get information about available commands.

## Installation
1. Clone this repository.
2. Install the required dependencies: `pip install -U python-telegram-bot`.
3. Replace the placeholder token in `main.py` with your own Telegram Bot API token.
4. Run the bot: `python3 main.py`.

## Dependencies
- [python-telegram-bot](https://python-telegram-bot.readthedocs.io/): Python wrapper for the Telegram Bot API.

## Contribution
Contributions to the project are welcome! If you have any suggestions, bug reports, or improvements, please open an issue or submit a pull request.

## To-do
- ~~Add /setletterboxd to set a group-specific Letterboxd link. It should be saved in the JSON;~~
- Localized strings in Italian and English;
- Settings (toggleable welcome message?);
- ~~A way to delete specific movies from the list;~~
- Some sort of integration with JustWatch.
