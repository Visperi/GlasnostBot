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


from typing import TypedDict, NotRequired, List

from .media import Document


class BackgroundFill(TypedDict):
    type: str


class BackgroundFillSolid(BackgroundFill):
    color: int


class BackgroundFillGradient(BackgroundFill):
    top_color: int
    bottom_color: int
    rotation_angle: int


class BackgroundFillFreeformGradient(BackgroundFill):
    colors: List[int]


class BackgroundType(TypedDict):
    type: str


class BackgroundTypeFill(BackgroundType):
    fill: BackgroundFill
    dark_theme_dimming: int


class BackgroundTypeWallpaper(BackgroundType):
    document: Document
    dark_theme_dimming: int
    is_blurred: NotRequired[bool]
    is_moving: NotRequired[bool]


class BackgroundTypePattern(BackgroundType):
    document: Document
    fill: BackgroundFill
    intensity: int
    is_inverted: NotRequired[bool]
    is_moving: NotRequired[bool]


class BackgroundTypeChatTheme(BackgroundType):
    theme_name: str
