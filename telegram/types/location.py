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


from typing_extensions import TypedDict, NotRequired
from .user import User


class Location(TypedDict):
    longitude: float
    latitude: float
    horizontal_accuracy: NotRequired[float]
    live_period: NotRequired[int]
    heading: NotRequired[int]
    proximity_alert_radius: NotRequired[int]


class ChatLocation(TypedDict):
    location: Location
    address: str


class Venue(TypedDict):
    location: Location
    title: str
    address: str
    foursquare_id: NotRequired[str]
    foursquare_type: NotRequired[str]
    google_place_id: NotRequired[str]
    google_place_type: NotRequired[str]


class ProximityAlertTriggered(TypedDict):
    traveler: User
    watcher: User
    distance: int
