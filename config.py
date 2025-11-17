"""
MIT License

Copyright (c) 2025 Niko Mätäsaho

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import Optional

import toml

from utils import Missing


class __ConfigSection:

    __slots__ = ()

    def __init__(self, section_dict: dict):
        """
        A base class for all sections in a TOML file.

        :param section_dict: Config section as a dictionary.
        """
        for key, value in section_dict.items():
            setattr(self, key, value)

    def as_dict(self) -> dict:
        """
        Get a configuration section as a dictionary.

        :return: A config section as a dictionary. This is the same format as loading a config TOML would give.
        """
        d = {}
        for attr_name in self.__slots__:
            attr_value = getattr(self, attr_name)
            d[attr_name] = attr_value

        return d

    def __str__(self):
        return str(self.as_dict())

    @classmethod
    def generate_default(cls):
        """
        Generate a config section object with default values.

        :raises NotImplementedError: If ``generate_default`` method is not implemented in the section class.
        """
        raise NotImplementedError(f"generate_default method not implemented in {cls.__name__}")

class _Preferences(__ConfigSection):

    __slots__ = (
        "prefer_telegram_usernames",
        "send_orphans_as_new_message",
        "message_cleanup_threshold",
        "update_age_threshold"
    )

    def __init__(self, preferences_dict: dict):
        """
        An object representing preferences section in a TOML file.

        :param preferences_dict: A preferences section as a dictionary.
        """
        super().__init__(preferences_dict)

    @classmethod
    def generate_default(cls):
        return cls(dict(prefer_telegram_usernames=True,
                        send_orphans_as_new_message=True,
                        message_cleanup_threshold=30,
                        update_age_threshold=600))


class _BotSettings(__ConfigSection):

    __slots__ = (
        "command_prefix",
        "activity_status",
        "dm_only_commands"
    )

    def __init__(self, settings_dict: dict):
        """
        An object representing bot_settings section in a TOML file.

        :param settings_dict: A bot_settings section as a dictionary.
        """
        super().__init__(settings_dict)

    @classmethod
    def generate_default(cls):
        return cls(dict(command_prefix="!",
                        activity_status="Missä mennään ja minne",
                        dm_only_commands=True))


class _ChannelIds(__ConfigSection):

    __slots__ = (
        "telegram",
        "discord"
    )

    def __init__(self, channel_ids_dict: dict):
        """
        An object representing channel_ids section in a TOML file.

        :param channel_ids_dict: A channel_ids section as a dictionary.
        """
        super().__init__(channel_ids_dict)

    @classmethod
    def generate_default(cls):
        return cls(dict(telegram=-10012345,
                        discord=[1234, 5678, 9012]))


class _Users(__ConfigSection):

    __slots__ = (
        "ignored_users",
        "listened_users"
    )

    def __init__(self, users_dict: dict):
        super().__init__(users_dict)

    @classmethod
    def generate_default(cls):
        return cls(dict(ignored_users=[],
                        listened_users=[]))


class _Credentials(__ConfigSection):

    __slots__ = (
        "telegram",
        "discord"
    )

    def __init__(self, credentials_dict: dict):
        """
        An object representing credentials section in a TOML file.

        :param credentials_dict: A credentials section as a dictionary.
        """
        super().__init__(credentials_dict)

    @classmethod
    def generate_default(cls):
        return cls(dict(telegram="TOKEN",
                        discord="TOKEN"))


class _General(__ConfigSection):

    __slots__ = (
        "logging_level",
        "database_path"
    )

    def __init__(self, general_dict: dict):
        """
        An object representing general section in a TOML file.

        :param general_dict: A general section as a dictionary.
        """
        super().__init__(general_dict)

    @classmethod
    def generate_default(cls):
        return cls(dict(logging_level="INFO",
                        database_path="glasnost.db"))


class Config:

    def __init__(self, config_path: Optional[str] = None):
        """
        An object representing a TOML configuration file.

        :param config_path: Path to an existing TOML configuration file. If given, the configuration is automatically
                            loaded from the file during initialization. Otherwise, load a configuration file later
                            with method ``load`` or assign the sections.
        """
        self.config_path = config_path
        """
        Path to the current configuration file.
        """
        self.general: _General = Missing
        """
        General section of the current configuration file.
        """
        self.credentials: _Credentials = Missing
        """
        Credentials section of the current configuration file.
        """
        self.channel_ids: _ChannelIds = Missing
        """
        Channel IDs section of the current configuration file.
        """
        self.users: _Users = Missing
        """
        Users section of the current configuration file.
        """
        self.bot_settings: _BotSettings = Missing
        """
        Bot settings section of the current configuration file.
        """
        self.preferences: _Preferences = Missing
        """
        Preferences section of the current configuration file.
        """

        if config_path:
            self.load()

    @classmethod
    def with_default_values(cls):
        """
        Initialize a ``Config`` object with default values.

        :return: ``Config`` object with default configuration.
        """
        obj = cls()
        obj.general = _General.generate_default()
        obj.credentials = _Credentials.generate_default()
        obj.channel_ids = _ChannelIds.generate_default()
        obj.users = _Users.generate_default()
        obj.bot_settings = _BotSettings.generate_default()
        obj.preferences = _Preferences.generate_default()

        return obj

    def __repr__(self):
        return str(self.as_dict())

    def __str__(self):
        return toml.dumps(self.as_dict())

    def load(self, config_file: Optional[str] = None):
        """
        Load configuration from an existing TOML file.

        :param config_file: Path to the TOML file. If omitted, the current configuration file is used.
        """
        if config_file:
            config = toml.load(config_file)
            self.config_path = config_file
        else:
            config = toml.load(self.config_path)

        self.general = _General(config["general"])
        self.credentials = _Credentials(config["credentials"])
        self.channel_ids = _ChannelIds(config["channel_ids"])
        self.users = _Users(config["users"])
        self.bot_settings = _BotSettings(config["bot_settings"])
        self.preferences = _Preferences(config["preferences"])

    def save(self, output_file: str):
        """
        Save the configuration to a file.

        :param output_file: Path to the file.
        """
        with open(output_file, "w", encoding="utf-8") as out_file:
            toml.dump(self.as_dict(), out_file)

    def as_dict(self) -> dict:
        """
        Get the configuration as a dictionary.

        :return: A dictionary of current values. This is the same format as loading a config TOML would give.
        """
        d = {}

        sections = self.__dict__.copy()
        sections.pop("config_path")
        for section_name, section_value in sections.items():
            try:
                d[section_name] = section_value.as_dict()
            except AttributeError:
                d[section_name] = section_value

        return d


if __name__ == "__main__":
    from pathlib import Path

    valid_inputs = {"yes": True, "y": True, "": True, "no": False, "n": False}
    default_file_path = "config.toml"
    print(f"Creating default configuration file to: {default_file_path}")
    if Path(default_file_path).is_file():
        print(f"File already exists.")
        while True:
            answer = input("Overwrite the existing file [Y/n]? ")
            try:
                overwrite = valid_inputs[answer]
                break
            except KeyError:
                print("Please answer yes or no.")
        if not overwrite:
            print("Will not overwrite the file. Exiting.")
            exit()

    Config.with_default_values().save(default_file_path)
    print(f"Default configuration created.")
