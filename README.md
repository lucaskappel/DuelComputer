# DuelComp
This is a discord bot designed for the purpose of aiding in content regarding Yu-Gi-Oh!

Support server: https://discord.gg/RdGZ42SWSA


# Setup

0) Make sure all the necessary libs are installed. Ideally make a venv with all the right stuff. Should just needs discord.py.

1) Run main.py once, this will generate your config and cache json files.

2) In the config.json, set the bot token to your bot, and set the owner to your discord id. Run the bot again, and then send the message "sync command tree now" on your server. It should print a response message letting you know the sync is complete.


## App Commands
- Read Q&A Entry -> Provided a link to a Q&A post from https://db.ygorganization.com/, can read the content and then allow users to also query and pull up the relevant cards within it from a select view.

## Slash Commands
- Display Card -> Queries and displays the card with the given ID.
- Resource -> Autocomplete query for content, various links, images, and writeups.
