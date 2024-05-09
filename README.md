# DiscoDJ: 

DiscoDJ is a Discord bot that utilizes the Spotify Web API to look up, play, and suggest songs. By using DiscoDJ, users will be able to play curated tracks based on all users' song history, adding an element of convenience not seen in most other mainstream Discord music bots.

# Product Architecture

![team35Graph](https://github.com/CS222-UIUC-SP24/group-project-team-35/assets/115494515/b52e4edc-8ee2-454f-a204-f03f1211a4ef)

Our graph shows the architecture of our product from user input back to a song response, and is elaborated on within our presentation.


# Developers:
Darren: Discord bot API/features

Jason: SQLite Database and data integration

Jack: Spotify/SpotiPy Web API integration

Chris: Virtual Environment, GitHub Workflow


# Download and Setup

after launching a virtual environment (whether that be locally through Python or externally through something like Docker), run 
```
pip install -r requirements.txt
```
to download all required libraries

then, invite the bot to your server of choice with the invite link: https://discord.com/oauth2/authorize?client_id=1209407473203810324&permissions=8&scope=bot

after getting the bot in your server, run ```FFMpeg test/main.py``` to start up the bot locally in your enviornment 

Afterwords, you'll be able to run commands using '!' as a prefix. To see all commands available, run ```!help``` inside of your command channel (whichever text channel(s) you designate for bot commands) to get a list of all commands with a short description of their functions

Have fun!






