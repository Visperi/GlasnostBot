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


from .types.user import User as UserPayload


class User:

    __slots__ = (
        "id",
        "is_bot",
        "first_name",
        "last_name",
        "username",
        "language_code",
        "is_premium",
        "added_to_attachment_menu",
        "can_join_groups",
        "can_read_all_group_messages",
        "supports_inline_queries"
    )

    def __init__(self, payload: UserPayload) -> None:
        self.__update(payload)

    def __update(self, payload: UserPayload) -> None:
        self.id = payload["id"]
        self.is_bot = payload["is_bot"]
        self.first_name = payload["first_name"]
        self.last_name = payload.get("last_name")
        self.username = payload.get("username")
        self.language_code = payload.get("language_code")
        self.is_premium = payload.get("is_premium", False)
        self.added_to_attachment_menu = payload.get("added_to_attachment_menu", False)
        self.can_join_groups = payload.get("can_join_groups", False)
        self.can_read_all_group_messages = payload.get("can_read_all_group_messages", False)
        self.supports_inline_queries = payload.get("supports_inline_queries", False)
