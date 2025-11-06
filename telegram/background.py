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

    __slots__ = (
        "type"
    )

    def __init__(self, payload: BackgroundFillPayload):
        self.type = payload["type"]


class BackgroundFillSolid(BackgroundFill):

    __slots__ = (
        "color"
    )

    def __init__(self, payload: BackgroundFillSolidPayload):
        super().__init__(payload)
        self.color = payload["color"]


class BackgroundFillGradient(BackgroundFill):

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

    __slots__ = (
        "colors"
    )

    def __init__(self, payload: BackgroundFillFreeformGradientPayload):
        super().__init__(payload)
        self.colors = payload["colors"]


class BackgroundType:

    __slots__ = (
        "type"
    )

    def __init__(self, payload: BackgroundTypePayload):
        self.type = payload["type"]


class BackgroundTypeFill(BackgroundType):

    __slots__ = (
        "fill",
        "dark_theme_dimming"
    )

    def __init__(self, payload: BackgroundTypeFillPayload):
        super().__init__(payload)
        self.fill = BackgroundFill(payload["fill"])
        self.dark_theme_dimming = payload["dark_theme_dimming"]


class BackgroundTypeWallpaper(BackgroundType):

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


class BackgroundTypePatterns(BackgroundType):

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

    __slots__ = (
        "theme_name"
    )

    def __init__(self, payload: BackgroundTypeChatThemePayload):
        super().__init__(payload)
        self.theme_name = payload["theme_name"]
