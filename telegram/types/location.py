from typing_extensions import TypedDict, NotRequired


class Location(TypedDict):
    longitude: float
    latitude: float
    horizontal_accuracy: NotRequired[float]
    live_period: NotRequired[int]
    heading: NotRequired[int]
    proximity_alert_radius: NotRequired[int]


class Venue(TypedDict):
    location: Location
    title: str
    address: str
    foursquare_id: NotRequired[str]
    foursquare_type: NotRequired[str]
    google_place_id: NotRequired[str]
    google_place_type: NotRequired[str]
