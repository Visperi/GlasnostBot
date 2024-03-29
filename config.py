import toml
from typing import TypeVar, Any


Missing = TypeVar("Missing", Any, None)


class __ConfigSection:

    __slots__ = ()

    def __init__(self, section_dict: dict):
        for key, value in section_dict.items():
            setattr(self, key, value)

    def as_dict(self) -> dict:
        d = {}
        for attr_name in self.__slots__:
            attr_value = getattr(self, attr_name)
            d[attr_name] = attr_value

        return d

    def __str__(self):
        return str(self.as_dict())

class _Preferences(__ConfigSection):

    __slots__ = (
        "prefer_telegram_usernames",
        "send_orphans_as_new_message",
        "message_cleanup_threshold",
        "update_age_threshold",
        "database_path"
    )

    def __init__(self, preferences_dict: dict):
        super().__init__(preferences_dict)


class _BotSettings(__ConfigSection):

    __slots__ = (
        "command_prefix",
        "activity_status",
        "dm_only_commands"
    )

    def __init__(self, settings_dict: dict):
        super().__init__(settings_dict)


class _Tokens(__ConfigSection):

    __slots__ = (
        "discord",
        "telegram"
    )

    def __init__(self, tokens_dict: dict):
        super().__init__(tokens_dict)


class _ChannelIds(__ConfigSection):

    __slots__ = (
        "telegram",
        "discord"
    )

    def __init__(self, channel_ids_dict: dict):
        super().__init__(channel_ids_dict)


class _Credentials(__ConfigSection):

    __slots__ = (
        "telegram",
        "discord"
    )

    def __init__(self, credentials_dict: dict):
        super().__init__(credentials_dict)


class Config:

    def __init__(self, config_path: str = "config.toml"):
        self.config_path = config_path
        self.credentials: _Credentials = Missing
        self.channel_ids: _ChannelIds = Missing
        self.bot_settings: _BotSettings = Missing
        self.preferences: _Preferences = Missing
        self.load()

    def load(self):
        config = toml.load(self.config_path)
        self.credentials = _Credentials(config["credentials"])
        self.channel_ids = _ChannelIds(config["channel_ids"])
        self.bot_settings = _BotSettings(config["bot_settings"])
        self.preferences = _Preferences(config["preferences"])

    def as_dict(self) -> dict:
        return dict(channel_ids=self.channel_ids.as_dict(),
                 bot_settings=self.bot_settings.as_dict(),
                 preferences=self.preferences.as_dict())

    def __repr__(self):
        return str(self.as_dict())

    def __str__(self):
        return toml.dumps(self.as_dict())

    @staticmethod
    def generate_new(output_file: str) -> dict:

        config = {
            "credentials": {
                "tokens": {
                    "telegram": "TOKEN",
                    "discord": "TOKEN"
                },
                "channel_ids": {
                    "telegram": -10012345,
                    "discord": [1234, 5678, 9012]
                }
            },
            "preferences": {
                "prefer_telegram_usernames": True,
                "message_cleanup_threshold": 30
            }
        }

        with open(output_file, "w") as output_file:
            toml.dump(config, output_file)

        return config
