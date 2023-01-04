## GlasnostBot

A bot forwarding broadcast Telegram channel posts to Discord channels. The main purpose of this bot is to provide a
one-way connection from Telegram announcements to Discord announcements for Oulun Tietoteekkarit ry 
(University of Oulu CSE student guild).

New messages, edits, replies and forwards are all supported from one Telegram channel/group/chat to an arbitrary amount 
of Discord channels. Only attachments are yet to be supported.

The telegram library used in this bot is also made by me and has its own repository 
[telegram.py](https://github.com/Visperi/telegram.py).

For images of the features see section [Images](#Images).

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

Example of message with different kind of markdown texts:

![Basic markdown example](img/basic_example.png)

Messages can of course also be edited:

![Edit example](img/edit_example.png)

...And replied to:

![Reply example](img/reply_example.png)

The maximum length for messages is 4096 characters like in free Telegram version:

![Lorem ipsum](img/lorem_ipsum.PNG)

## Licence

MIT Licence

Full licence: [LICENCE](LICENCE)
