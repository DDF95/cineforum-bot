# cineforum-bot
`cineforum-bot` is a Telegram bot designed to help manage a cineforum group. It allows users to create a list of movies they want to watch together, choose random movies, and more.

## Usage
1. Start a chat with the bot or invite it to your cineforum group.
2. The following commands are available:
   - `/add <movie>`: Add one or more movies to your list.
   - `/delete`: Delete the movie associated to a number in the list, or delete all your movies.
   - `/choose`: Choose a random movie from the entire list (Admin only).
   - `/list`: Generate a list of all movies.
   - `/letterboxd`: Show the group's Letterboxd link.
   - `/setletterboxd`: Set the group's Letterboxd link.
   - `/welcome`: Show the group's welcome message.
   - `/settings`: Adjust the bot's settings.
   - `/setwelcome`: Set the group's welcome message.
   - `/deletewelcome`: Delete the group's welcome message.
   - `/restart`: Restart the bot.
   - `/help`: Get information about available commands.

## Installation
1. Clone this repository: `git clone https://github.com/DDF95/cineforum-bot.git`
2. Install the required dependencies: `pip install -r requirements.txt`.
3. Run the bot: `python3 main.py`.
4. Follow the on-screen instructions to input your bot token and your user ID.
5. You're good to go! :)

## Dependencies
- [python-telegram-bot](https://python-telegram-bot.readthedocs.io/): Python wrapper for the Telegram Bot API.

## Contribution
Contributions to the project are welcome! If you have any suggestions, bug reports, or improvements, please open an issue or submit a pull request.

## To-do
1. Some sort of integration with JustWatch.
2. Data management overhaul (as of now it's messy, with two `JSONs` and a `config.ini`).
3. Some code must be simplified (looking at you, `delete_movies.py`).