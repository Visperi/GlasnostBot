from .types.location import (
    Location as LocationPayload,
    Venue as VenuePayload
)


class Location:

    __slots__ = (
        "longitude",
        "latitude",
        "horizontal_accuracy",
        "live_period",
        "heading",
        "proximity_alert_radius"
    )

    def __init__(self, payload: LocationPayload):
        self.__update(payload)

    def __update(self, payload: LocationPayload):
        self.longitude = payload["longitude"]
        self.latitude = payload["latitude"]
        self.horizontal_accuracy = payload.get("horizontal_accuracy", -1)
        self.live_period = payload.get("live_period", -1)
        self.heading = payload.get("heading", -1)
        self.proximity_alert_radius = payload.get("proximity_alert_radius", -1)


class Venue:

    __slots__ = (
        "location",
        "title",
        "address",
        "foursquare_id",
        "foursquare_type",
        "google_place_id",
        "google_place_type"
    )

    def __init__(self, payload: VenuePayload):
        self.__update(payload)

    def __update(self, payload: VenuePayload):
        self.location = Location(payload["location"])
        self.title = payload["title"]
        self.address = payload["address"]
        self.foursquare_id = payload.get("foursquare_id")
        self.foursquare_type = payload.get("foursquare_type")
        self.google_place_id = payload.get("google_place_id")
        self.google_place_type = payload.get("google_place_type")
