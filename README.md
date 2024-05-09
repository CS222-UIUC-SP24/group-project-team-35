# DiscoDJ: 

DiscoDJ is a Discord bot that utilizes the Spotify Web API to look up, play, and suggest songs. By using DiscoDJ, users will be able to play curated tracks based on all users' song history, adding an element of convenience not seen in most other mainstream Discord music bots.

# Product Architecture

(https://keep.google.com/u/1/media/v2/165Ut3xueVzMaMkn5kIIErYFWv_p7G0bgo9LtinIHjmewtXOltZ056oIVkfnhkHer/1TTUaKUXJ1DOK-3EoiuUgluiuNFiq41X7agMe5u2_MZgjNEZQjpSLy6VbOVW5XFxn?sz=512&accept=image%2Fgif%2Cimage%2Fjpeg%2Cimage%2Fjpg%2Cimage%2Fpng%2Cimage%2Fwebp)

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






