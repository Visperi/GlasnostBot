## GlasnostBot

A bot forwarding broadcast Telegram channel posts to Discord channels. The main purpose of this bot is to provide a
one-way connection from Telegram announcements to Discord announcements for Oulun Tietoteekkarit ry 
(University of Oulu CSE student guild).

New messages, edits, replies and forwards are all supported from one Telegram channel/group/chat to an arbitrary amount 
of Discord channels. Only restriction is that they currently must be less than 2000 characters long for Discord.

The telegram library used in this bot is also made by me and has its own repository 
[telegram.py](https://github.com/Visperi/telegram.py).

For images of the bot in action see section [Images](#Images).

## Running the bot

Before running the bot an application and API tokens for both Telegram API and Discord API are needed.

To run an instance of this bot by yourself, all that is required is to configure the `config.toml` file. 
A prefilled template can be found from `config_example.toml`. There can currently be only one Telegram channel to listen
and an arbitrary amount of Discord channels where the 
messages are forwarded.

The capability of editing and replying to old Discord messages depends solely on if they are found in the bots' 
database. This can be adjusted with variable `message_cleanup_threshold` in preferences.

IDs for both Discord and Telegram are always integers, and for Telegram they start with `-100`. 
IDs can be edited in the configuration file and then reloaded in runtime by using command `reload` through Discord.

### Preferences

Preferences can be used to control the bot behaviour in more readable way and in runtime without restarting the whole 
bot. All that is needed to adjust the configuration values and then use command `reload` through Discord. 
Following preferences are currently available:

1. `prefer_telegram_usernames`: Boolean value. In forwarded user messages prefer their username over their real name(s)
if possible. Has no effect for forwarded channel posts.

2. `send_orphans_as_new_message`: Boolean value. Send edits and replies not found from the database as completely new 
messages. Do note that e.g. short replies to old messages can look out of place this way, and some context should 
perhaps be given.

3. `message_cleanup_threshold`: Integer value. Inclusive age in days for Discord message references to be deleted from 
the database in 6 hour intervals. References at least this old will be deleted, and cannot be replied or edited in 
Discord anymore.

4. `update_age_threshold`: Integer value. Inclusive maximum age in seconds for hanging Telegram messages to forward to 
Discord, due to e.g. lag spikes or bot downtimes.

5. `database_path`: String value. Path to the sqlite3 database file used for storing message references.

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
