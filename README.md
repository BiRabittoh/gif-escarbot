# EscarBot

Earthbound Café's custom delivery bot with other cool utilities built-in.

## Features
1. The bot's main feature is listening for posts in a channel and forwarding them to a group.
2. If the bot receives a private message, it will be forwarded to the bot's admin.
3. If the bot senses an Instagram, Twitter (X) or YouTube link, it will try to send a custom link with better thumbnail generation.

## How to use

Copy the `.env.example` file into `.env` and insert the following info:
* `token`: your Telegram Bot Token;
* `channel_id`: the channel the bot will listen to;
* `group_id`: the group that will receive the channel messages;
* `admin_id`: the user that will receive the bot's private messages.

Create a new virtual environment and install required packages:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then, start the bot by running:
```python main.py```
