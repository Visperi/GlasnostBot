# GlasnostBot

**This project requires Python 3.9 or higher**

A bot that connects a Telegram bot to Discord bot and forwards messages from Telegram to Discord channels.

Simply put the bot listens to a Telegram channel, group or chat and forwards messages from there to configured Discord 
channels in Discord compatible format.

Variety of features are supported, including but not limited to:
- Sending files
- Text formatting
- Replies and edits to old messages
- Ignoring or listening specific users in Telegram

## Running the bot

1. Install the requirements to your environment
2. Generate a configuration file for the bot by executing `config.py`
3. Configure the bot as needed. See section [Configuration](#Configuration) for reference.
4. Start the bot by running `main.py`

Once started, the bot will listen to configured Telegram group, channel or discussion and forwards received messages 
to configured Discord channels. Discord and discord.py ratelimiting may affect the speed of message forwarding if they 
are sent rapidly.

### Bot permissions

The Discord bot must have permissions to send messages and read old messages in configured channels. The Telegram bot 
needs bot privacy setting turned off to receive messages from groups or direct messages. In channels this is not 
required, as bots are automatically admins in them.

## Configuration

Most of the bot behaviour can be controlled through configuration in `config.toml`. Discord command `reload` can be 
used to reload the configuration at runtime. Bot restart is required when changing API tokens.

Below is a list of config sections and their variables and values.

### General

|    variable     | value type | function                                                                                                                     |
|:---------------:|:----------:|------------------------------------------------------------------------------------------------------------------------------|
| `logging_level` |   String   | Sets the minimum level of messages logged. Must be capitalized.                                                              |
| `database_path` |   String   | Path to a sqlite3 database file used for storing the message references. If not found, a new file is created at bot startup. |

### Credentials

Remember to keep the tokens safe and never make them public. Anyone with the tokens has access to your bots.

Changing bot credentials require a complete restart for the bot.

|  variable  | value type | function           |
|:----------:|:----------:|--------------------|
| `telegram` |   String   | Telegram API token |
| `discord`  |   String   | Discord bot token  |

<details>
<summary>Click to open obtainment of API tokens</summary>

#### Obtaining Discord API token

1. Go to your application settings in Discord developer portal
2. The application token is found from menu Bot -> Token. Client secret in OAuth2 section is incorrect one.
3. Reset the token and copy it into `config.toml`

#### Obtaining Telegram API token

1. Open chat with the BotFather
2. Open the chat menu next to the text field
3. Select your bot and copy the token in spoilers and copy it into `config.toml`

</details>

### Channel IDs

> **Note** 
> 
>When adding the bot to groups (not channels), you need to turn bot privacy off from bot settings with BotFather. 
If the bot is already in a group when changing these settings, you need to kick the bot out and invite it again for them to take effect.

|  variable  |    value type    | function                                                                                                                                                          |
|:----------:|:----------------:|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `telegram` |     Integer      | ID of a Telegram channel, group or chat to listen to. Only one listened channel is currently supported.                                                           |
| `discord`  | List of integers | List of Discord channel IDs to forward the Telegram messages to. The Discord bot must have a permission to send messages and read old messages in these channels. |

### Users

User settings can be used to control whose messages are forwarded from Telegram to Discord. This section has no effect on channels posts, as they do not have a user as a sender.

|     variable     |    value type    | function                                                                                                                                                                           |
|:----------------:|:----------------:|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `ignored_users`  | List of integers | List of Telegram user IDs. Messages from these users will never be forwarded to Discord.                                                                                           |
| `listened_users` | List of integers | List of Telegram user IDs. Messages from these users will be forwarded to Discord. Leave as an empty list to forward messages from all users (except the ignored ones) to Discord. |

### Bot settings

Bot settings are used to control the bot presence and behaviour in Discord.

|      variable      |          value type           | function                                                                                                                                                                                                                                         |
|:------------------:|:-----------------------------:|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  `command_prefix`  | String or iterable of strings | Determines accepted command prefix(es) in Discord. For iterable prefixes, see the note in discord.py [documentation](https://discordpy.readthedocs.io/en/stable/ext/commands/api.html?highlight=prefix#discord.ext.commands.Bot.command_prefix). |
| `activity_status`  |            String             | Used to set the bot status message in Discord. Leave as an empty string for no Discord status.                                                                                                                                                   |
| `dm_only_commands` |            Boolean            | Accept bot commands in Discord only through direct messages. Otherwise the commands can be executed in any Discord channel the bot can read.                                                                                                     |

### Preferences

Preferences are used to control the Discord message forwarding behaviour.

|           variable            | value type | function                                                                                                                                                                                                                                                                                                                      |
|:-----------------------------:|:----------:|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  `prefer_telegram_usernames`  |  Boolean   | Prefer Telegram usernames over sender real name in forwarded Telegram messages if possible. If the original message sender does not have username set, their real name is used instead. This setting has no effect on forwarded channel posts and messages sent on behalf of a channel, as they do not have user as a sender. |
| `send_orphans_as_new_message` |  Boolean   | Send edits and replies not found in the bot database as completely new messages. Do note that e.g. short replies to very old messages can look out of place if enabled, and some context should perhaps be given.                                                                                                             |
|  `message_cleanup_threshold`  |  Integer   | Inclusive age in days for for Discord messages to be deleted from the database in 6 hour intervals. References at least this old in days will be deleted, and cannot be replied or edited in Discord anymore.                                                                                                                 |
|    `update_age_threshold`     |  Integer   | Inclusive maximum age in seconds for hanging Telegram messages to forward to Discord. Messages can be left hanging e.g. due to lag spikes or bot downtimes.                                                                                                                                                                   |

## Examples

Example of the fully supported nested text formatting:

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
