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
from typing import List


_logger = logging.getLogger(__name__)


class MessageCache:

    def __init__(self, database: str, pragma_foreign_keys: bool = False) -> None:
        self.connection = self.connect(database, pragma_foreign_keys)
        self.cursor = self.connection.cursor()
        self.ensure_table_exists()

    def ensure_table_exists(self) -> None:
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS discord_messages (
                message_id INTEGER PRIMARY KEY,
                channel_id INTEGER NOT NULL,
                guild_id NOT NULL,
                tg_message_id INTEGER NOT NULL
            );
            """
        )

    def connect(self, database: str, pragma_foreign_keys: bool = False) -> sqlite3.Connection:
        connection = sqlite3.connect(database)
        if pragma_foreign_keys:
            connection.execute("PRAGMA foreign_keys = ON")

        self.connection = connection
        self.cursor = connection.cursor()
        _logger.info(f"Connected to database '{database}'")

        return connection

    def close(self):
        _logger.debug("Closing database connection")
        self.connection.close()
        self.connection = None
        self.cursor = None

    def add(self, tg_message_id: int, discord_message: discord.Message) -> None:
        with self.connection:
            self.cursor.execute(
                """
                INSERT INTO discord_messages (message_id, channel_id, guild_id, tg_message_id) 
                VALUES
                    (?, ?, ?, ?) 
                """, (discord_message.id, discord_message.channel.id, discord_message.guild.id, tg_message_id)
            )

    def delete(self, tg_message_id: int) -> None:
        with self.connection:
            self.cursor.execute(
                """
                DELETE FROM discord_messages WHERE tg_message_id = ?
                """, (tg_message_id, )
            )

    def get(self, tg_message_id: int) -> List[int]:
        with self.connection:
            ids = self.cursor.execute(
                """
                SELECT message_id, channel_id FROM discord_messages WHERE tg_message_id = ?
                """, (tg_message_id, )
            ).fetchall()

        return ids
