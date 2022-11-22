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
        self._update(payload)

    def _update(self, payload: LocationPayload):
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
        self._update(payload)

    def _update(self, payload: VenuePayload):
        self.location = Location(payload["location"])
        self.title = payload["title"]
        self.address = payload["address"]
        self.foursquare_id = payload.get("foursquare_id")
        self.foursquare_type = payload.get("foursquare_type")
        self.google_place_id = payload.get("google_place_id")
        self.google_place_type = payload.get("google_place_type")
