"""
MIT License

Copyright (c) 2022 Niko Mätäsaho

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


import logging
import sqlite3
import discord
import datetime
from typing import List, Union, Tuple


_logger = logging.getLogger(__name__)


class DatabaseHandler:

    def __init__(self, database_path: str, pragma_foreign_keys: bool = False) -> None:
        self.database_path = None
        self.connection = self.connect(database_path, pragma_foreign_keys)
        self.cursor = self.connection.cursor()
        self._ensure_table_exists()

    def _ensure_table_exists(self) -> None:
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS discord_messages (
                message_id INTEGER PRIMARY KEY,
                channel_id INTEGER NOT NULL,
                guild_id NOT NULL,
                tg_message_id INTEGER NOT NULL,
                ts INTEGER NOT NULL
            );
            """
        )

    def connect(self, database_path: str, pragma_foreign_keys: bool = False) -> sqlite3.Connection:
        connection = sqlite3.connect(database_path)
        if pragma_foreign_keys:
            connection.execute("PRAGMA foreign_keys = ON")

        self.connection = connection
        self.cursor = connection.cursor()
        self.database_path = database_path
        on_off = "ON" if pragma_foreign_keys else "OFF"
        _logger.info(f"Connected to database '{database_path}' with PRAGMA foreign_keys {on_off}")

        return connection

    def disconnect(self) -> None:
        _logger.info("Closing database connection")
        self.connection.close()
        self.connection = None
        self.cursor = None
        _logger.debug("Connection closed")

    def add(self, tg_message_id: int, discord_message: discord.Message, ts: Union[int, datetime.datetime]) -> None:
        """
        Add a new Discord message reference to the database for possible later references.

        :param tg_message_id: Telegram message ID. Needed for finding all Discord messages based on the original message
        :param discord_message: The Discord message sent to Discord. Data needed for deserialization is saved to
        the database.
        :param ts: Leap second aware UTC timestamp when the Discord message was sent.
        """
        if isinstance(ts, datetime.datetime):
            ts = int(ts.timestamp())

        with self.connection:
            self.cursor.execute(
                """
                INSERT INTO discord_messages (message_id, channel_id, guild_id, tg_message_id, ts) 
                VALUES
                    (?, ?, ?, ?, ?) 
                """, (discord_message.id, discord_message.channel.id, discord_message.guild.id, tg_message_id, ts)
            )

        _logger.debug(f"Successfully added reference to database with values {tg_message_id}, "
                      f"{discord_message.to_message_reference_dict()}, {ts}")

    def update_ts(self, tg_message_id: int, new_ts: int) -> int:
        """
        Update a timestamp for a message reference to preserve it longer in the database for possible new references.

        :param tg_message_id: ID of the Telegram message
        :param new_ts: Leap second aware UTC Timestamp of the last reference time
        :return: Amount of modified rows
        """
        _logger.debug(
            f"Updating timestamp to {new_ts} for Discord message references with Telegram message ID {tg_message_id}.")

        with self.connection:
            self.cursor.execute(
                """
                UPDATE discord_messages 
                SET ts = ?
                WHERE tg_message_id = ?
                """, (new_ts, tg_message_id)
            )

        modified = self.cursor.rowcount
        _logger.debug(f"Successfully updated timestamp for total of {modified} references.")
        return modified

    def delete_by_id(self, tg_message_id: int) -> int:
        _logger.debug(
            f"Deleting Discord message references with Telegram message ID {tg_message_id} from the database.")

        with self.connection:
            self.cursor.execute(
                """
                DELETE FROM discord_messages WHERE tg_message_id = ?
                """, (tg_message_id, )
            )

        deleted = self.cursor.rowcount
        _logger.debug(f"Successfully deleted {deleted} references.")
        return deleted

    def delete_by_age(self, upper_age_limit: Union[int, datetime.datetime]) -> int:
        """
        Delete message references from the database based on their timestamps. All messages failing to be inside given
        time restrictions are deleted.

        :param upper_age_limit: Inclusive leap second aware UTC timestamp or datetime object determining
        the most recent reference to delete. Messages with this or smaller timestamps will be deleted!
        :return: Amount of deleted messages
        """
        if isinstance(upper_age_limit, datetime.datetime):
            upper_age_limit = int(upper_age_limit.timestamp())

        _logger.debug(f"Deleting Discord message references with upper limit of {upper_age_limit} from the database.")

        with self.connection:
            self.cursor.execute(
                """
                DELETE FROM discord_messages WHERE ts <= ?
                """, (upper_age_limit,)
            )

        deleted = self.cursor.rowcount
        _logger.debug(f"Successfully deleted {deleted} references.")
        return deleted

    def get(self, tg_message_id: int) -> List[Tuple[int, int]]:
        """
        Get Discord message references corresponding to given Telegram message ID.

        :param tg_message_id: The Telegram message ID.
        :return: List containing tuples of Discord message IDs and Discord channel IDs, which can be used to find
        references to actual Discord message objects.
        """
        _logger.debug(f"Fetching all Discord message references with Telegram message ID {tg_message_id}")

        with self.connection:
            ids = self.cursor.execute(
                """
                SELECT message_id, channel_id FROM discord_messages WHERE tg_message_id = ?
                """, (tg_message_id, )
            ).fetchall()

        return ids
