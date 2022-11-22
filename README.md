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

secret = "YOUR SECRET HERE"
client = telegram.Client(secret)


@client.event
async def on_update(update: telegram.Update) -> None:
    print("Update received in main.py")

# Call this blocking call last!
client.start()
```

Multiple listeners are supported for each event, although currently limited by the listener names since they must be 
exact matches with the actual event. Listening events is also supported by subclassing `telegram.Client` and then 
overriding the event methods.

## Licence

MIT Licence

Full licence: [LICENCE](LICENCE)
