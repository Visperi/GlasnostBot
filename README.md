## telegram.py

An asynchronous python library for telegram API.

This is a very young and Work In Progress project. Even the name is subject to change. 
Lots of functionality is still missing, and documentation is nonexistent, 
although the structure and classes are solely based on the official API documentation.
Just converted to use pythonic coding style.

**Python 3.8 or higher is required**

## Usage

Basic usage:

```python
import telegram

client = telegram.Client()


@client.event
async def on_update(update: telegram.Update) -> None:
    print("Update received in main.py")

# Call this blocking call last!
client.start("YOUR SECRET HERE")
```

Multiple listeners are supported for each event, although currently limited by the listener names since they must be 
exact matches with the actual event. Listening events is also supported by subclassing `telegram.Client` and then 
overriding the event methods:

```python
import telegram


class TgBot(telegram.Client):

    def __init__(self):
        super().__init__()

    async def on_update(self, update: telegram.Update) -> None:
        print("Update received in TgBot overridden event")


bot = TgBot()


@bot.event
async def on_update(update: telegram.Update) -> None:
    print("Update received in event listener method")

bot.start("YOUR_TOKEN_HERE")
```

## Licence

MIT Licence

Full licence: [LICENCE](LICENCE)
