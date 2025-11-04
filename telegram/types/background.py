from typing import List

from typing_extensions import TypedDict, NotRequired

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