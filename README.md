## GlasnostBot

A bot made for forwarding Oulun Tietoteekkarit ry Telegram announcements from OTiT glasnost to their Discord server.

All text from shorter than 2000 character messages, including forwards, edits and replies, are supported and forwarded 
from Telegram channel/group/chat to an arbitrary amount of Discord channels.

The capability of editing and replying to old Discord messages depends solely on if they are found in the sqlite3 
database this bot uses. A cleanup background loop is automatically run every 6 hours and removes over 30 days old 
references.

The telegram library used in this bot is also made by me and has its own repository 
[telegram.py](https://github.com/Visperi/telegram.py).

For showcase images of the bot in action see section [Images](#Images).

## Running the bot

If you want to run this bot by yourself to whatever channels, you need `credentials.json` file in following format to 
the root of this repository:

```json
{
    "tokens": {
        "telegram": "TOKEN",
        "discord": "TOKEN"
    },
    "ids": {
        "telegram": -12345,
        "discord": [1, 2, 3]
    }
}
```

So before running the bot an application and token for both Telegram API and Discord API is needed.
There can currently be only one Telegram channel to listen and an arbitrary amount of listening Discord channels.
All IDs must be integers, and for Telegram they are always negative.

## TODO
Non-exhaustive list of features still needed for stable support:

- Support messages over length of 2000 characters
- Support attachments in messages
    - In edited messages support attachment deletion(?)
- Better bot configuration files

## Images

Once the bot is listening to a Telegram channel and has some Discord channels defined, it forwards all messages to 
Discord and serializes them into a sqlite3 database for possible edits and replies.

![Plain new message](img/plain_new.png)

Replied messages are also replied in Discord if message references are fround from the database.

![Reply message](img/reply.png)

Same goes for edited Telegram messages. Do note that edits into forwarded Telegram messages do not show in Telegram.

![Edited message](img/edit.png)

Forwarded messages include the name of the original message sender. For channels this means the channel title. 
For users this means their real name or username, depending on if `prefer_username` option is used.

![Forwarded message](img/forward.png)

## Licence

MIT Licence

Full licence: [LICENCE](LICENCE)
