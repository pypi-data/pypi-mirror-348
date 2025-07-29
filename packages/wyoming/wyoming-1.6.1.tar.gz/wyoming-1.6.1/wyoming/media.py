"""Media playback."""

import logging
from dataclasses import dataclass

from .event import Event, Eventable

_LOGGER = logging.getLogger(__name__)

_MEDIA_PLAY_TYPE = "media-play"
_MEDIA_PAUSE_TYPE = "media-pause"
_MEDIA_UNPAUSE_TYPE = "media-unpause"
_MEDIA_STOP_TYPE = "media-stop"


@dataclass
class MediaPlay(Eventable):
    """Play a media URL."""

    url: str
    is_announcement: bool = False

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _MEDIA_PLAY_TYPE

    def event(self) -> Event:
        return Event(
            type=_MEDIA_PLAY_TYPE,
            data={"url": self.url, "is_announcement": self.is_announcement},
        )

    @staticmethod
    def from_event(event: Event) -> "MediaPlay":
        return MediaPlay(
            url=event.data["url"],
            is_announcement=event.data.get("is_announcement", False),
        )


@dataclass
class MediaPause(Eventable):
    """Pause media."""

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _MEDIA_PAUSE_TYPE

    def event(self) -> Event:
        return Event(type=_MEDIA_PAUSE_TYPE)

    @staticmethod
    def from_event(event: Event) -> "MediaPause":
        return MediaPause()


@dataclass
class MediaUnpause(Eventable):
    """Unpause media."""

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _MEDIA_UNPAUSE_TYPE

    def event(self) -> Event:
        return Event(type=_MEDIA_UNPAUSE_TYPE)

    @staticmethod
    def from_event(event: Event) -> "MediaUnpause":
        return MediaUnpause()


@dataclass
class MediaStop(Eventable):
    """Stop media."""

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _MEDIA_STOP_TYPE

    def event(self) -> Event:
        return Event(type=_MEDIA_STOP_TYPE)

    @staticmethod
    def from_event(event: Event) -> "MediaStop":
        return MediaStop()
