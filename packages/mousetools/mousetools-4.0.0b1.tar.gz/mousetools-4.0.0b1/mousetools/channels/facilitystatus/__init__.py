import logging
import typing
from datetime import datetime, timedelta

from mousetools.channels import CouchbaseChannel
from mousetools.channels.enums import DestinationShort, DestinationTimezones
from mousetools.mixins.couchbase import CouchbaseMixin

logger = logging.getLogger(__name__)


class FacilityStatusChildChannel(CouchbaseMixin):
    def __init__(self, channel_id: str, lazy_load: bool = True):
        """
        Args:
            channel_id (typing.Union[WDWCouchbaseChannels, DLRCouchbaseChannels]): Channel ID from the enum
            lazy_load (bool, optional): If True, will not pull data until a method or property is called. Defaults to True.
        """
        self.channel_id = channel_id

        self._destination_short: DestinationShort = channel_id.split(".")[0]
        self._tz: DestinationTimezones = (
            DestinationTimezones.WALT_DISNEY_WORLD
            if self._destination_short == DestinationShort.WALT_DISNEY_WORLD
            else DestinationTimezones.DISNEYLAND_RESORT
        )
        self._refresh_interval: timedelta = timedelta(minutes=10)

        if lazy_load:
            self._cb_data: typing.Optional[dict] = None
        else:
            self._cb_data = self.get_channel_data(self.channel_id)

    def refresh(self) -> None:
        """Pulls initial data if none exists or if it is older than the refresh interval"""
        if self._cb_data is None or datetime.now(tz=self._tz.value) - self.last_update > self._refresh_interval:
            self._cb_data = self.get_channel_data(self.channel_id)

    def get_status(self) -> typing.Optional[str]:
        """Get the operating status of the facility

        Returns:
            (typing.Optional[str]): Operating status. Typically "Operating" or "Closed".
        """
        self.refresh()

        try:
            return self._cb_data["status"]
        except KeyError:
            logger.debug("No status found for %s", self.channel_id)
            return None

    def get_wait_time(self) -> typing.Optional[int]:
        """Get the wait time in minutes

        Returns:
            (typing.Optional[int]): Wait time in minutes
        """
        self.refresh()

        try:
            return self._cb_data["waitMinutes"]
        except KeyError:
            logger.debug("No wait time found for %s", self.channel_id)
            return None

    @property
    def last_update(self) -> typing.Optional[datetime]:
        """The last time the data was updated.

        Returns:
            (typing.Optional[datetime]): The last time the entity's data was updated, or None if no such data exists.
        """
        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)

        try:
            dt = datetime.fromisoformat(self._cb_data["lastUpdate"])
            dt = dt.replace(tzinfo=self._tz.value)
            return dt
        except KeyError:
            logger.debug("No last updated found for %s", self.channel_id)
            return None

    @property
    def fast_pass_available(self) -> typing.Optional[bool]:
        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)
        try:
            return self._cb_data["fastPassAvailable"]
        except KeyError:
            logger.debug("No fast pass available found for %s", self.channel_id)
            return None

    def get_fast_pass_end_time(self) -> typing.Optional[datetime]:
        self.refresh()

        try:
            dt = datetime.fromisoformat(self._cb_data["fastPassEndTime"])
            dt = dt.replace(tzinfo=self._tz.value)
            return dt
        except (KeyError, ValueError):
            logger.debug("No fast pass end time found for %s", self.channel_id)
            return None

    def get_fast_pass_start_time(self) -> typing.Optional[datetime]:
        self.refresh()

        try:
            dt = datetime.fromisoformat(self._cb_data["fastPassStartTime"])
            dt = dt.replace(tzinfo=self._tz.value)
            return dt
        except (KeyError, ValueError):
            logger.debug("No fast pass start time found for %s", self.channel_id)
            return None

    @property
    def single_rider(self) -> typing.Optional[bool]:
        """Whether the facility allows single riders

        Returns:
            (typing.Optional[bool]): Whether the facility allows single riders
        """
        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)
        try:
            return self._cb_data["singleRider"]
        except KeyError:
            logger.debug("No single rider found for %s", self.channel_id)
            return None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(channel_id='{self.channel_id}')"

    def __eq__(self, other) -> bool:
        if isinstance(other, FacilityStatusChildChannel):
            return self.channel_id == other.channel_id
        return False


class FacilityStatusChannel(CouchbaseChannel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_children_channels(self) -> typing.Generator[FacilityStatusChildChannel, None, None]:
        """Gets a list of children channels for the channel.

        Yields:
            typing.Generator[FacilityStatusChildChannel, None, None]: A generator of FacilityStatusChildChannels
        """
        self.refresh()
        for i in self._cb_data["results"]:
            yield FacilityStatusChildChannel(i["id"])
