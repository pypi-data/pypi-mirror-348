import logging
import typing
from collections.abc import Generator
from datetime import datetime, timedelta

from dateutil.parser import isoparse

from mousetools.channels import CouchbaseChannel
from mousetools.channels.enums import CouchbaseChannels, DestinationTimezones
from mousetools.enums import DestinationShort, EntityType
from mousetools.mixins.couchbase import CouchbaseMixin

logger = logging.getLogger(__name__)


class FacilityStatusChildChannel(CouchbaseMixin):
    _subclasses: typing.ClassVar[dict[str, type["FacilityStatusChildChannel"]]] = {}

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
        self._cb_data: typing.Optional[dict] = None
        self._cb_data_pull_time: typing.Optional[datetime] = datetime.now(tz=self._tz.value)

        if not lazy_load:
            self.refresh()

    def refresh(self) -> None:
        """Pulls initial data if none exists or if it is older than the refresh interval"""
        if self._cb_data is None or datetime.now(tz=self._tz.value) - self.last_update > self._refresh_interval:
            self._cb_data = self.get_channel_data(self.channel_id)
            self._cb_data_pull_time = datetime.now(tz=self._tz.value)

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
            dt = isoparse(self._cb_data["lastUpdate"])
            dt = dt.replace(tzinfo=self._tz.value)
            return dt
        except KeyError:
            logger.debug("No last updated found for %s", self.channel_id)
            return self._cb_data_pull_time

    @property
    def fast_pass_available(self) -> typing.Optional[bool]:
        self.refresh()
        try:
            return self._cb_data["fastPassAvailable"]
        except KeyError:
            logger.debug("No fast pass available found for %s", self.channel_id)
            return None

    def get_fast_pass_end_time(self) -> typing.Optional[datetime]:
        self.refresh()

        try:
            dt = isoparse(self._cb_data["fastPassEndTime"])
            dt = dt.replace(tzinfo=self._tz.value)
            return dt
        except (KeyError, ValueError):
            logger.debug("No fast pass end time found for %s", self.channel_id)
            return None

    def get_fast_pass_start_time(self) -> typing.Optional[datetime]:
        self.refresh()

        try:
            dt = isoparse(self._cb_data["fastPassStartTime"])
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
        self.refresh()
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

    @classmethod
    def get_subclass(cls, type_name: str) -> type["FacilityStatusChildChannel"]:
        if type_name not in cls._subclasses:
            cls._subclasses[type_name] = type(type_name, (cls,), {"__doc__": f"Class for {type_name} Entities."})
        return cls._subclasses[type_name]


AttractionFacilityStatusChild = FacilityStatusChildChannel.get_subclass("AttractionFacilityStatusChild")
EntertainmentFacilityStatusChild = FacilityStatusChildChannel.get_subclass("EntertainmentFacilityStatusChild")
EntertainmentVenueFacilityStatusChild = FacilityStatusChildChannel.get_subclass("EntertainmentVenueFacilityStatusChild")
LandFacilityStatusChild = FacilityStatusChildChannel.get_subclass("LandFacilityStatusChild")
RestaurantFacilityStatusChild = FacilityStatusChildChannel.get_subclass("RestaurantFacilityStatusChild")
ThemeParkFacilityStatusChild = FacilityStatusChildChannel.get_subclass("ThemeParkFacilityStatusChild")
WaterParkFacilityStatusChild = FacilityStatusChildChannel.get_subclass("WaterParkFacilityStatusChild")


class FacilityStatusChannel(CouchbaseChannel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_children_channels(self) -> Generator[FacilityStatusChildChannel, None, None]:
        """Gets a list of children channels for the channel.

        Yields:
            typing.Generator[FacilityStatusChildChannel, None, None]: A generator of FacilityStatusChildChannels
        """
        self.refresh()
        for i in self._cb_data["results"]:
            if CouchbaseChannels.FACILITY_STATUS in i["id"]:
                yield FacilityStatusChildChannel(i["id"])

    def get_children_attractions(self) -> Generator[AttractionFacilityStatusChild, None, None]:  # type: ignore
        """Get AttractionFacilityStatusChild Children of a Facility

        Yields:
            Generator[AttractionFacilityStatusChild, None, None]: A generator of AttractionFacilityStatusChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.ATTRACTION.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield AttractionFacilityStatusChild(i["id"])

    def get_children_entertainment(self) -> Generator[EntertainmentFacilityStatusChild, None, None]:  # type: ignore
        """Get EntertainmentFacilityStatusChild Children of a Facility

        Yields:
            Generator[EntertainmentFacilityStatusChild, None, None]: A generator of EntertainmentFacilityStatusChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.ENTERTAINMENT.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield EntertainmentFacilityStatusChild(i["id"])

    def get_children_entertainment_venues(self) -> Generator[EntertainmentVenueFacilityStatusChild, None, None]:  # type: ignore
        """Get EntertainmentVenueFacilityStatusChild Children of a Facility

        Yields:
            Generator[EntertainmentVenueFacilityStatusChild, None, None]: A generator of EntertainmentVenueFacilityStatusChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.ENTERTAINMENT_VENUE.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield EntertainmentVenueFacilityStatusChild(i["id"])

    def get_children_lands(self) -> Generator[LandFacilityStatusChild, None, None]:  # type: ignore
        """Get LandFacilityStatusChild Children of a Facility

        Yields:
            Generator[LandFacilityStatusChild, None, None]: A generator of LandFacilityStatusChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.LAND.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield LandFacilityStatusChild(i["id"])

    def get_children_restaurants(self) -> Generator[RestaurantFacilityStatusChild, None, None]:  # type: ignore
        """Get RestaurantFacilityStatusChild Children of a Facility

        Yields:
            Generator[RestaurantFacilityStatusChild, None, None]: A generator of RestaurantFacilityStatusChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.RESTAURANT.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield RestaurantFacilityStatusChild(i["id"])

    def get_children_theme_parks(self) -> Generator[ThemeParkFacilityStatusChild, None, None]:  # type: ignore
        """Get ThemeParkFacilityStatusChild Children of a Facility

        Yields:
            Generator[ThemeParkFacilityStatusChild, None, None]: A generator of ThemeParkFacilityStatusChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.THEME_PARK.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield ThemeParkFacilityStatusChild(i["id"])

    def get_children_water_parks(self) -> Generator[WaterParkFacilityStatusChild, None, None]:  # type: ignore
        """Get WaterParkFacilityStatusChild Children of a Facility

        Yields:
            Generator[WaterParkFacilityStatusChild, None, None]: A generator of WaterParkFacilityStatusChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.WATER_PARK.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield WaterParkFacilityStatusChild(i["id"])
