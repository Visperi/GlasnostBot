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


from .types.background import (
    BackgroundFill as BackgroundFillPayload,
    BackgroundFillSolid as BackgroundFillSolidPayload,
    BackgroundFillGradient as BackgroundFillGradientPayload,
    BackgroundFillFreeformGradient as BackgroundFillFreeformGradientPayload,
    BackgroundType as BackgroundTypePayload,
    BackgroundTypeFill as BackgroundTypeFillPayload,
    BackgroundTypeWallpaper as BackgroundTypeWallpaperPayload,
    BackgroundTypePattern as BackgroundTypePatternPayload,
    BackgroundTypeChatTheme as BackgroundTypeChatThemePayload
)
from .media import Document


class BackgroundFill:
    """
    A base class for fill type hat backgrounds.

    Args:
        payload: A dictionary received from Telegram API

    Attributes:
        type: Type of the background fill. Can be "solid", "gradient" or "freeform_gradient".
    """

    __slots__ = (
        "type"
    )

    def __init__(self, payload: BackgroundFillPayload):
        self.type = payload["type"]


class BackgroundFillSolid(BackgroundFill):
    """
    A background that is filled with a solid color.

    Attributes:
        type: Type of the fill. Always "solid".
        color: The background fill color in RGB24 format.
    """

    __slots__ = (
        "color"
    )

    def __init__(self, payload: BackgroundFillSolidPayload):
        super().__init__(payload)
        self.color = payload["color"]


class BackgroundFillGradient(BackgroundFill):
    """
    A background that is filled with a gradient color.

    Attributes:
        type: Type of the fill. Always "gradient".
        top_color: The gradient top color in RGB24 format.
        bottom_color: The gradient bottom color in RGB24 color.
        rotation_angle: The gradient rotation in clockwise degrees. Can be in range 0-359.
    """

    __slots__ = (
        "top_color",
        "bottom_color",
        "rotation_angle"
    )

    def __init__(self, payload: BackgroundFillGradientPayload):
        super().__init__(payload)
        self.top_color = payload["top_color"]
        self.bottom_color = payload["bottom_color"]
        self.rotation_angle = payload["rotation_angle"]


class BackgroundFillFreeformGradient(BackgroundFill):
    """
    A background that is filled with gradient color and rotates after messages in a chat.

    Attributes:
        type: Type of the fill. Always "freeform_gradient".
        colors: List of the 3 or 4 base colors that are used to generate the freeform gradient in the RGB24 format.
    """

    __slots__ = (
        "colors"
    )

    def __init__(self, payload: BackgroundFillFreeformGradientPayload):
        super().__init__(payload)
        self.colors = payload["colors"]


class BackgroundType:
    """
    Base class for background types.

    Attributes:
        type: Type of the background. Can be "fill", "wallpaper", "pattern" or "chat_theme".
    """

    __slots__ = (
        "type"
    )

    def __init__(self, payload: BackgroundTypePayload):
        self.type = payload["type"]


class BackgroundTypeFill(BackgroundType):
    """
    A background that is automatically filled based on selected colors.

    Attributes:
        type: Type of the background. Always "fill".
        dark_theme_dimming: Dimming of the background in dark themes as a percentage in range 0-100.
    """

    __slots__ = (
        "fill",
        "dark_theme_dimming"
    )

    def __init__(self, payload: BackgroundTypeFillPayload):
        super().__init__(payload)
        self.fill = BackgroundFill(payload["fill"])
        self.dark_theme_dimming = payload["dark_theme_dimming"]


class BackgroundTypeWallpaper(BackgroundType):
    """
    A background that is a wallpaper in JPEG format.

    Attributes:
        type: Type of the background. Always "wallpaper".
        document: ``telegram.Document`` with the wallpaper.
        dark_theme_dimming: Dimming of the background in dark themes as a percentage in range 0-100.
        is_blurred: True, if the wallpaper is downscaled to fit in a 450x450 square and then box-blurred with radius 12.
        is_moving: True, if the background moves slightly when the device is tilted.
    """

    __slots__ = (
        "document",
        "dark_theme_dimming",
        "is_blurred",
        "is_moving"
    )

    def __init__(self, payload: BackgroundTypeWallpaperPayload):
        super().__init__(payload)
        self.document = Document(payload["document"])
        self.dark_theme_dimming = payload["dark_theme_dimming"]
        self.is_blurred = payload.get("is_blurred", False)
        self.is_moving = payload.get("is_moving", False)


class BackgroundTypePattern(BackgroundType):
    """
    A background that is a PNG or TGV format pattern to be combined with a background fill chosen by user.

    Attributes:
        type: Type of the background. Always "pattern".
        document: ``telegram.Document`` with the pattern.
        fill: ``telegram.BackgroundFill`` that is combined with the pattern.
        intensity: Intensity of the pattern in percentage 0-100 when it is shown above the filled background.
        is_inverted: True, if the background fill must be applied only to the pattern itself. All other pixels are
                     black in this case. For dark themes only.
        is_moving: True if the background moves slightly when the device is tilted.
    """

    __slots__ = (
        "document",
        "fill",
        "intensity",
        "is_inverted",
        "is_moving"
    )

    def __init__(self, payload: BackgroundTypePatternPayload):
        super().__init__(payload)
        self.document = Document(payload["document"])
        self.fill = BackgroundFill(payload["fill"])
        self.intensity = payload["intensity"]
        self.is_inverted = payload.get("is_inverted", False)
        self.is_moving = payload.get("is_moving", False)


class BackgroundTypeChatTheme(BackgroundType):
    """
    A background that is taken from a built-in chat theme.

    Attributes:
        type: Type of the background. Always "chat_theme".
        theme_name: Nme of the chat theme. Usually an emoji.
    """

    __slots__ = (
        "theme_name"
    )

    def __init__(self, payload: BackgroundTypeChatThemePayload):
        super().__init__(payload)
        self.theme_name = payload["theme_name"]
