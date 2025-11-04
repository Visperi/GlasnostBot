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


from typing import List

from typing_extensions import TypedDict, NotRequired

from telegram import PhotoSize


class User(TypedDict):
    id: int
    is_bot: bool
    first_name: str
    last_name: NotRequired[str]
    username: NotRequired[str]
    language_code: NotRequired[str]
    is_premium: NotRequired[bool]
    added_to_attachment_menu: NotRequired[bool]
    can_join_groups: NotRequired[bool]
    can_read_all_group_messages: NotRequired[bool]
    supports_inline_queries: NotRequired[bool]


class SharedUser(TypedDict):
    user_id: int
    first_name: NotRequired[str]
    last_name: NotRequired[str]
    username: NotRequired[str]
    photo: NotRequired[List[PhotoSize]]


class UsersShared(TypedDict):
    request_id: int
    users: List[SharedUser]
